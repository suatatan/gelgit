# GelGIT

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![Built With](https://img.shields.io/badge/built%20with-Electron.js-brightgreen)
![Python](https://img.shields.io/badge/python-Required-important)
![Status](https://img.shields.io/badge/status-Development-yellow)
![OpenAI Supported](https://img.shields.io/badge/OpenAI-Supported-blueviolet)

> An intelligent Git repository analyzer with AI-supported commit summarization.

**GelGIT** is a lightweight Electron.js and Python-powered desktop application that analyzes Git repositories, extracts commit histories, and optionally generates AI-driven summaries using OpenAI.

---

## ✨ Features

- 📂 Select any local Git repository
- 🔎 Analyze commit history and diffs
- ✍️ (Optional) Summarize commits using GPT-4
- 📊 Export results to Excel (.xlsx)
- 🖥️ Clean and modern user interface
- 🛠️ Easy to build as a standalone executable (.exe)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vectorsolv/gelgit.git
cd gelgit
```

### 2. Install Node.js dependencies

```bash
npm install
```

### 3. Install Python dependencies

Make sure **Python 3.8+** is installed.  
Then install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run locally (development mode)

```bash
npm start
```

✅ This will open the application for local testing.

---

## 🛠 Packaging the Application

### Package a simple `.exe` (without installer)

```bash
npm run package
```
- Output: `/GelGIT-win32-x64/` folder containing `GelGIT.exe`

### Create a full Setup Installer (with installation wizard)

```bash
npm run dist
```
- Output: `/dist/` folder containing `GelGIT Setup 1.0.0.exe`

---

## 📋 Requirements

- **Node.js** (v18+ recommended)
- **Python** (3.8+ or higher)
- Python packages:
  - `openai`
  - `pandas`

You can easily install the Python requirements:

```bash
pip install -r requirements.txt
```

---

## 📸 Screenshots

### Main Dashboard

![Main Dashboard](screenshots/main.png)

### Options

![Main Dashboard](screenshots/main2.png)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and distribute it.

---

## 👨‍💻 Contributors

- Developed by the **Vectorsolv Team** with contributions from **Suat Atan** 💬

Pull requests are welcome!  
For major changes, please open an issue first to discuss your ideas.

---

## 🌐 About

Vectorsolv is a forward-thinking technology company specializing in intelligent software solutions.  
GelGIT is part of our ongoing efforts to simplify developer workflows with smart automation tools.

