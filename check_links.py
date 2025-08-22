import subprocess
import concurrent.futures
import os
import html2text  # Add this import

URLS_FILE = "urls.txt"
OUTPUT_DIR = "linkchecker_results"
MARKDOWN_DIR = "linkchecker_markdown"

def run_linkchecker(url, idx):
    domain = url.split("//")[-1].split("/")[0]
    output_file = os.path.join(OUTPUT_DIR, f"result_{domain}.html")
    md_file = os.path.join(MARKDOWN_DIR, f"result_{domain}.md")
    cmd = [
        "linkchecker",
        url,
        "--output=html",
        "--threads=8",
        "--timeout=10",
        "--ignore-url=.*\\?.*", # should ignore get requests where parameters are set in the URL
        "--verbose",
        f"--file-output=html/{output_file}"
    ]
    try:
        subprocess.run(cmd, check=False)
        print(f"Checked {url}, results in {output_file}")
        # Convert HTML to Markdown
        with open(output_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        md_content = html2text.html2text(html_content)
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Converted {output_file} to {md_file}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(MARKDOWN_DIR):
        os.makedirs(MARKDOWN_DIR)
    with open(URLS_FILE) as f:
        urls = [line.strip() for line in f if line.strip()]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for idx, url in enumerate(urls):
            executor.submit(run_linkchecker, url, idx)

if __name__ == "__main__":
    main()
