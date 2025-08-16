import webbrowser
import datetime
from pathlib import Path

# Third-party libraries for uploading
import requests

# Local imports
from .core import EXPORTS
from .dependencies import ensure_pkg

class Uploader:
    def __init__(self, proj: Path):
        self.proj = proj
        EXPORTS.mkdir(parents=True, exist_ok=True)

    def gumroad_create_and_upload(self, token: str, product_name: str, price_cents: int, summary: str, file_path: Path) -> dict:
        file_path = Path(file_path)
        if not token:
            raise RuntimeError("Gumroad API token required")
        if not file_path.exists():
            raise FileNotFoundError(file_path)
        headers = {"Authorization": f"Bearer {token}"}
        data = {"name": product_name, "price": price_cents, "description": summary}
        r = requests.post("https://api.gumroad.com/v2/products", headers=headers, data=data, timeout=90)
        r.raise_for_status()
        product_id = (r.json().get("product") or {}).get("id") or r.json().get("id")
        if not product_id:
            raise RuntimeError(f"Product id not found in response: {r.text}")

        with open(file_path, "rb") as fh:
            files = {"file": fh}
            r2 = requests.post(f"https://api.gumroad.com/v2/products/{product_id}/files", headers=headers, files=files, timeout=300)
        r2.raise_for_status()
        return {"product_id": product_id, "result": r2.json()}

    def kofi_open_shop(self):
        webbrowser.open("https://ko-fi.com/manage/shop")

    def google_onix_xml(self, metadata: dict) -> Path:
        today = datetime.date.today().strftime("%Y%m%d")
        def esc(x): return (x or "").replace("&", "&amp;").replace("<", "&lt;")
        onix = f"""
<?xml version="1.0" encoding="UTF-8"?>
<ONIXMessage release="3.0">
  <Header>
    <Sender><SenderName>{esc(metadata.get('publisher',''))}</SenderName></Sender>
    <SentDateTime>{today}</SentDateTime>
  </Header>
  <Product>
    <RecordReference>{esc(metadata.get('isbn','NA'))}</RecordReference>
    <NotificationType>03</NotificationType>
    <ProductIdentifier><ProductIDType>15</ProductIDType><IDValue>{esc(metadata.get('isbn','NA'))}</IDValue></ProductIdentifier>
    <DescriptiveDetail>
      <ProductComposition>00</ProductComposition>
      <ProductForm>ED</ProductForm>
      <TitleDetail><TitleType>01</TitleType><TitleElement>
        <TitleElementLevel>01</TitleElementLevel>
        <TitleText>{esc(metadata.get('title','Untitled'))}</TitleText>
        <Subtitle>{esc(metadata.get('subtitle',''))}</Subtitle>
      </TitleElement></TitleDetail>
      <Contributor><SequenceNumber>1</SequenceNumber><ContributorRole>A01</ContributorRole><PersonName>{esc(metadata.get('author',''))}</PersonName></Contributor>
      <Language><LanguageRole>01</LanguageRole><LanguageCode>eng</LanguageCode></Language>
    </DescriptiveDetail>
  </Product>
</ONIXMessage>
""".strip()
        out = EXPORTS / "onix.xml"
        out.write_text(onix, encoding="utf-8")
        return out

    def google_sftp_upload(self, host: str, port: int, username: str, password: str | None, key_path: str | None, files: list[Path]) -> str:
        paramiko = ensure_pkg("paramiko", "paramiko")
        transport = None
        try:
            transport = paramiko.Transport((host, int(port or 22)))
            if key_path:
                pkey = paramiko.RSAKey.from_private_key_file(key_path)
                transport.connect(username=username, pkey=pkey)
            else:
                transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            remote_dir = "/incoming"
            try:
                sftp.chdir(remote_dir)
            except IOError:
                sftp.mkdir(remote_dir)
                sftp.chdir(remote_dir)
            for fp in files:
                sftp.put(str(fp), Path(fp).name)
            sftp.close()
            return f"SFTP upload complete to {host}:{remote_dir}"
        finally:
            if transport:
                transport.close()
