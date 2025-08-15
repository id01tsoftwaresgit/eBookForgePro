Here’s a clean, professional **README.md** for your GitHub repo **`eBookForgePro`**.

````markdown
# eBookForgePro

**Version:** 1.0.0  
**Author:** Guillaume Lessard  
**Publisher:** iD01t Softwares  
**Website:** [https://www.id01t.ca](https://www.id01t.ca)  
**Support:** itechinfomtl@gmail.com  

---

## 📖 Overview

**eBookForgePro** is a professional, all-in-one Python application for creating, compiling, and managing eBooks with production-ready quality.  
It supports multiple formats, automated table of contents generation, integrated cover design, and direct export to publishing platforms.

Designed for speed, ease of use, and maximum compatibility, eBookForgePro is the go-to tool for authors, publishers, and independent creators.

---

## 🚀 Features

- **Multi-format Export**: PDF, EPUB, MOBI, and DOCX.
- **Auto Table of Contents**: Generates and formats TOC instantly.
- **Integrated Cover Designer**: Create or import high-resolution covers.
- **Batch Processing**: Compile multiple books in one click.
- **Custom Metadata**: Add title, subtitle, author, description, ISBN, and more.
- **Local Processing**: All work is done on your machine, no data is uploaded.
- **One-Click Compilation**: Professional output in seconds.

---

## 📦 Requirements

- **OS**: Windows 10 or 11 (x64)
- **Python**: 3.10+
- **Dependencies**:
  - `fpdf2`
  - `ebooklib`
  - `python-docx`
  - `Pillow`
  - `reportlab`

You can install them all with:
```bash
pip install -r requirements.txt
````

---

## ⚡ Quick Start

1. **Clone the Repository**

```bash
git clone https://github.com/id01tsoftwaresgit/eBookForgePro.git
cd eBookForgePro
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the Application**

```bash
python ebookforgepro.py
```

4. **Select Your Project**

   * Add your manuscript.
   * Configure metadata.
   * Generate cover.
   * Click **Compile eBook**.

---

## 🛠 Building an Executable (.exe)

If you want to create a Windows executable:

```bash
pyinstaller --noconsole --onefile --name "eBookForgePro" --icon "assets/icon.ico" ebookforgepro.py
```

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🌐 Links

* **Website**: [https://www.id01t.ca](https://www.id01t.ca)
* **GitHub**: [https://github.com/id01tsoftwaresgit/eBookForgePro](https://github.com/id01tsoftwaresgit/eBookForgePro)
* **Contact**: [itechinfomtl@gmail.com](mailto:itechinfomtl@gmail.com)

```

