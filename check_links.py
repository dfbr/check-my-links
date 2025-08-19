import subprocess
import concurrent.futures
import os

URLS_FILE = "urls.txt"
OUTPUT_DIR = "linkchecker_results"

def run_linkchecker(url, idx):
    output_file = os.path.join(OUTPUT_DIR, f"result_{idx}.html")
    cmd = [
        "linkchecker",
        url,
        "--output=html",
        f"--file-output=html/{output_file}"
    ]
    try:
        subprocess.run(cmd, check=False)
        print(f"Checked {url}, results in {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking {url}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(URLS_FILE) as f:
        urls = [line.strip() for line in f if line.strip()]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for idx, url in enumerate(urls):
            executor.submit(run_linkchecker, url, idx)

if __name__ == "__main__":
    main()