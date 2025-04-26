import argparse
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


parser = argparse.ArgumentParser()
parser.add_argument('--repo_path')
parser.add_argument('--use_stat')
parser.add_argument('--ai_summary')
parser.add_argument('--test_mode')
parser.add_argument('--api_key')
args = parser.parse_args()

print(f"Analyzing {args.repo_path} with use_stat={args.use_stat}, ai_summary={args.ai_summary}, test_mode={args.test_mode}", flush=True)
for step in ['Fetching commits', 'Parsing diffs', 'Generating summaries', 'Saving output']:
    print(f"🔸 {step}...", flush=True)
    time.sleep(1)
print("✅ Analysis complete!", flush=True)

# print("ok")