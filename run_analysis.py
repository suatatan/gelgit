import argparse
import os
import subprocess
import time
import sys
import io

# 🛠 Gerekli paketleri kontrol et ve yükle
required_packages = ['openai', 'pandas']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"[GelGIT] Installing missing package+: {package}", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[GelGIT] {package} installed successfully.", flush=True)


import pandas as pd
from openai import OpenAI



# stdout encoding ayarı (Windows için)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 🛠 Argümanları al
parser = argparse.ArgumentParser()
parser.add_argument('--repo_path')
parser.add_argument('--use_stat')
parser.add_argument('--ai_summary')
parser.add_argument('--test_mode')
parser.add_argument('--api_key')
args = parser.parse_args()

# 🎯 Ayarları işle
GIT_REPO_PATH = args.repo_path
GIT_REPO_PATH_NAME = os.path.basename(GIT_REPO_PATH)
USE_STAT = args.use_stat.lower() == "true"
AI_SUMMARY = args.ai_summary.lower() == "true"
TEST_MODE = args.test_mode.lower() == "true"
API_KEY = args.api_key

os.chdir(GIT_REPO_PATH)

# 🔑 OpenAI istemcisi (AI Summary aktifse)
if AI_SUMMARY:
    client = OpenAI(api_key=API_KEY)

# 📦 Fonksiyonlar
def get_commit_hashes():
    result = subprocess.run(["git", "log", "--pretty=format:%H"], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().splitlines()

def get_commit_info(commit_hash):
    message = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%s", commit_hash],
        stdout=subprocess.PIPE, text=True
    ).stdout.strip()

    date = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%ad", "--date=short", commit_hash],
        stdout=subprocess.PIPE, text=True
    ).stdout.strip()

    author = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%an", commit_hash],
        stdout=subprocess.PIPE, text=True
    ).stdout.strip()

    diff_cmd = ["git", "show", "--stat" if USE_STAT else "", commit_hash]
    diff_cmd = [arg for arg in diff_cmd if arg]
    diff = subprocess.run(diff_cmd, stdout=subprocess.PIPE, text=True).stdout.strip()

    return message, date, author, diff

def summarize_diff(diff_text):
    prompt = f"""
You are analyzing a Git commit. Below is the {'git show --stat' if USE_STAT else 'git show'} output:

Please generate a concise, one-line English commit message that explains what was changed. Avoid generic phrases like "updated code" or "fixed bug".

"""
    retry_count = 0
    while retry_count < 3:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            retry_count += 1
            print(f"[stderr] OpenAI error, retrying ({retry_count}/3): {e}", flush=True)
            time.sleep(2)
    return "Summary generation failed"

# 🚀 Ana işlem
print(f"Analyzing {GIT_REPO_PATH} with use_stat={USE_STAT}, ai_summary={AI_SUMMARY}, test_mode={TEST_MODE}", flush=True)

hashes = get_commit_hashes()
if TEST_MODE:
    hashes = hashes[:5]

results = []

for idx, commit_hash in enumerate(hashes):
    print(f"[{idx+1}/{len(hashes)}] Processing commit {commit_hash}", flush=True)
    try:
        original_msg, date, author, diff = get_commit_info(commit_hash)
        summary = ""
        if AI_SUMMARY:
            summary = summarize_diff(diff)
        results.append({
            "commit_hash": commit_hash,
            "date": date,
            "original_message": original_msg,
            "suggested_summary": summary,
            "author": author
        })
    except Exception as e:
        print(f"[stderr] Error processing {commit_hash}: {e}", flush=True)
        continue

# 📦 Excel çıktısı
print(f"Saving {len(results)} commits into Excel...", flush=True)

df = pd.DataFrame(results)
filename = f"{GIT_REPO_PATH_NAME}_commit_summary.xlsx"
df.to_excel(filename, index=False)

print(f"✅ Analysis completed! File saved as {filename}", flush=True)
