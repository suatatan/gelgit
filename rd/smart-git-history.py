import os
import subprocess
import pandas as pd
import time
from openai import OpenAI
import openai  # RateLimitError için

# 🔧 Ayarlar
GIT_REPO_PATH = r"D:\suat\gitrepo_vectorsolv\data-science-utility-code"
USE_STAT = True               # True: git show --stat, False: full diff
AI_SUMMARY = False            # GPT ile açıklama alınsın mı
TEST_MODE = False            # True: sadece ilk 3 commit
TOKEN_LIMIT_CHARS = 3000     # diff metni kesilme limiti
WAIT_SECONDS = 15            # Rate limit durumunda bekleme süresi

# 📁 Gerekli bilgiler
GIT_REPO_PATH_NAME = os.path.basename(GIT_REPO_PATH)
os.chdir(GIT_REPO_PATH)

# 🔑 OpenAI API bağlantısı
API_KEY = os.getenv("OPENAI_API_KEY")  # API anahtarını ortam değişkeninden al
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
client = OpenAI(api_key=API_KEY)

# 🚀 Commit hash listesini al
def get_commit_hashes():
    result = subprocess.run(["git", "log", "--pretty=format:%H"], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().splitlines()

# 🔍 Commit içeriğini al
def get_commit_info(commit_hash):
    message = subprocess.run(["git", "log", "-1", "--pretty=format:%s", commit_hash], stdout=subprocess.PIPE, text=True).stdout.strip()
    date = subprocess.run(["git", "log", "-1", "--pretty=format:%ad", "--date=short", commit_hash], stdout=subprocess.PIPE, text=True).stdout.strip()
    diff_cmd = ["git", "show", "--stat" if USE_STAT else "", commit_hash]
    diff_cmd = [d for d in diff_cmd if d]
    diff = subprocess.run(diff_cmd, stdout=subprocess.PIPE, text=True).stdout.strip()

    # diff çok uzunsa kes
    if len(diff) > TOKEN_LIMIT_CHARS:
        diff = diff[:TOKEN_LIMIT_CHARS] + "\n\n[...diff truncated due to token limit...]"

    return message, date, diff

# 🧠 GPT ile commit açıklaması üret
def summarize_diff(diff_text, retries=3):
    prompt = f"""
You are analyzing a Git commit. Below is the `git show {'--stat' if USE_STAT else ''}` output for this commit:
Please generate a concise, one-line **English commit message** that explains what was changed.
Be specific and avoid generic phrases like "updated code" or "fixed bug". Emphasize the innovativeness of the changes if any.

```{diff_text}```
"""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            print(f"⏳ Rate limit reached. Waiting {WAIT_SECONDS} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(WAIT_SECONDS)
        except openai.BadRequestError as e:
            print("❗ Diff too large for GPT-4 context. Skipping.")
            return "[Skipped: Diff too long for model input]"
        except Exception as e:
            raise e
    return "[Error: GPT-4 API failed after retries]"

# 📦 Ana işlem
def main():
    hashes = get_commit_hashes()
    if TEST_MODE:
        hashes = hashes[:3]

    results = []
    for idx, commit_hash in enumerate(hashes):
        print(f"[{idx + 1}/{len(hashes)}] Processing: {commit_hash}")
        try:
            original_msg, date, diff = get_commit_info(commit_hash)
            summary = summarize_diff(diff) if AI_SUMMARY else ""
            result = {
                "commit_hash": commit_hash,
                "date": date,
                "original_message": original_msg,
                "diff_summary": diff
            }
            if AI_SUMMARY:
                result["description_of_work"] = summary
            results.append(result)
        except Exception as e:
            print(f"⚠️ Error ({commit_hash}): {e}")
            continue

    df = pd.DataFrame(results)
    filename = f"{GIT_REPO_PATH_NAME}_commit_diff_summary_with_descriptions_ai.xlsx" if AI_SUMMARY else f"{GIT_REPO_PATH_NAME}_commit_diff_summary.xlsx"
    df.to_excel(filename, index=False)
    print(f"✅ Done! Excel file created: {filename}")

if __name__ == "__main__":
    main()
