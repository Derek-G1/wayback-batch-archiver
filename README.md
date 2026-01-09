# Wayback Machine Batch Archiver

A professional Python utility designed to automate the process of submitting multiple URLs to the Internet Archive's Wayback Machine. This script utilizes the official S3 API to trigger high-fidelity captures and monitors their progress in real-time.

## ✨ Features

- **Batch Processing**: Archive an unlimited list of URLs in a single execution.
- **Real-Time Status Polling**: The script waits for the Internet Archive to process the request and returns the final permanent URL.
- **Automated CSV Logging**: Records every attempt, timestamp, and result in a local `archive_history.csv` file.
- **Security First**: Uses `.env` files for credential management and a strict `.gitignore` to prevent data leaks.
- **Visual Feedback**: Provides a live progress bar (dots) while waiting for the archive job to complete.

## 🛠️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Derek-G1/Wayback_Machine_Script.git
cd Wayback_Machine_Script
```

### 2. Install Dependencies

This script requires Python 3 and two external libraries:

```bash
pip install requests python-dotenv
```

### 3. Configure API Keys

1. Log in to your Archive.org account.
2. Navigate to your S3 API Keys.
3. Create a file named `.env` in the project root.
4. Add your keys to the `.env` file exactly like this:

```text
WAYBACK_ACCESS_KEY=your_access_key_here
WAYBACK_SECRET_KEY=your_secret_key_here
```

## 🚀 How to Use

### Adding Sites to Archive

Open `archive.py` and navigate to the `sites_to_archive` list at the bottom of the file. Add your URLs inside the brackets:

```python
sites_to_archive = [
    "https://www.example.com",
    "https://www.your-cool-app.io",
]
```

### Running the Script

Execute the script via your terminal:

```bash
python archive.py
```

## 📂 Project Structure

- `archive.py`: The main Python logic.
- `.env`: Stores your private API credentials (hidden from Git).
- `.env.example`: A template to show others how to set up their environment.
- `.gitignore`: Critical file that prevents secrets and logs from being uploaded.
- `archive_history.csv`: A local-only log of your archival activity.

## 🛡️ Security Protocols

This project is built with security in mind to prevent accidental exposure of API keys:

- **Environment Variables**: Credentials are never hardcoded in the script.
- **Git Shielding**: The `.gitignore` file is configured to block all `.env` files and all `*.csv` files, ensuring your keys and your browsing history stay on your local machine only.

## 🔬 Technical Reference (IAS3 API)

This script interacts with the Internet Archive S3-like API (IAS3).

### Documentation Links for archive.org

- [Internet Archive Developer Portal](https://archive.org/developers/index.html)
- [IAS3 (S3-like API) Documentation](https://archive.org/developers/ias3.html)

### Key API Details

- **Authorization**: Uses the **LOW** simple authorization scheme: `Authorization: LOW $accesskey:$secret`. See the IAS3 API documentation above for full technical details.
- **Items vs Buckets**: In the IAS3 system, Archive items map to **S3 Buckets**, and files map to **S3 Keys**.
- **Job Tracking**: The script utilizes the `POST` support to initiate captures and polls the `/save/status/` JSON endpoint.
- **Skip Derive**: The script manages the Archive’s content management system ingestion, ensuring high-priority processing for interactive archival tasks.

## ⚖️ License

```text
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```