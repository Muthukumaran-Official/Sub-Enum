# Sub-Enum 

## 📌 Overview

**Sub-Enum** is a **Python-based** tool designed to enumerate subdomains of a given domain efficiently. It uses **multithreading** to speed up the scanning process and **categorizes the discovered subdomains based on their HTTP response status.**

---

 Remember guys!!! this is a **Subdomain Enumerator Tool** ✅ and not a **Hidden-Directories Enumerator** ❌

---

## 🎯 Difference Between Subdomain Enumeration & Hidden-Directory Enumeration

| Feature          | Subdomain Enumeration                         | Hidden-Directory Enumeration (e.g., dirsearch/dirbuster tool)                                      |
| ---------------- | --------------------------------------------- | ----------------------------------------------------------------------- |
| Purpose          | Finds subdomains (e.g., `api.example.com`)    | Finds directories and files within a domain (e.g., `example.com/admin`) |
| Method Used      | Resolves subdomains from DNS & HTTP responses | Sends requests for common directory names                               |
| Tools Used       | Sublist3r, Amass, This Subdomain Scanner      | Dirsearch, Gobuster, Dirb                                               |
| Target Discovery | Identifies separate subdomains                | Identifies hidden directories & files                                   |
| Use Case         | Finding additional assets of a target domain  | Locating admin panels, sensitive directories                            |

---

## 🛠️ Installation Guide

### **Step 1: Install Python**

Ensure Python 3.x is installed on your system. Download and install it from: 🔗 [Python Official Website](https://www.python.org/downloads/)

Verify the installation:

```sh
python --version
```

or

```sh
python3 --version
```

### **Step 2: Install Required Libraries**

Run the following command to install the required dependencies:

```sh
pip install requests colorama
```

Alternatively, you can also install the required dependencies via `requirements.txt` file by running the following command:

```sh
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the tool with the following command:

```sh
python SubEnum.py
```

You will be prompted to **enter a domain**, and the scanner will enumerate subdomains.

#### ⚠️NOTE : 
**Make sure every files cloned, are in the same directory/folder for better performance and usabilty.\
(or)\
If you wanna change the locations of the files...mention the filepaths in the appropriate places in the code.** 

---

## 📝 Features

✔️ Multi-threaded scanning for faster enumeration\
✔️ Supports both HTTP & HTTPS checks\
✔️ Categorizes results (Valid, Redirects, Forbidden, Errors)\
✔️ Saves results to a file with timestamps

---

## 📝 Output Format

If results are saved, they are stored in a file in the following format:

```plaintext
=================================================
Domain Name: example.com
Scan time and date: YYYY-MM-DD HH:MM:SS

===[scan results]===

[VALIDS : 1]
[REDIRECTS : 0]
[FORBIDS : 0]
[OTHERS : 0]
[ERRORS : 0]


[+]-----[ VALID ]--------------------------------

[+] https://www.example.com

[~]-----[ REDIR ]--------------------------------


[~]-----[ FORBID ]-------------------------------


[~]-----[ OTHER ]--------------------------------


[-]-----[ ERRORS ]------------------------------

===============end of results===============
```

---

## 📌 Contribution & License

😎Feel free to contribute to the project! Fork, enhance, and submit PRs.\

📄Licensed under MIT License.📄

---

## 🤝 Credits

Developed by **Muthukumaran** 🚀

Stay Tuned For Lot More Funs.....📈⚡\
HAPPY CODING GUYS!!!👋🏻👋🏻
