import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import pandas as pd
import time
from urllib.parse import urlparse, parse_qs

def download_file(url, output_path, max_retries=5, backoff_factor=1, timeout=30):
    # Configure retry strategy with longer delays
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

    # Create session with custom headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/pdf'
    })
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        # Extract filename from URL parameters
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        filename = params.get('passcofonumber', ['unknown.pdf'])[0]

        response = session.get(url, stream=True, timeout=timeout)
        response.raise_for_status()

        # Verify content type
        if 'application/pdf' not in response.headers.get('content-type', '').lower():
            print(f"Warning: Response for {filename} is not a PDF")
            return False

        # Save the file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Successfully downloaded: {filename}")
        return True

    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def main():
    # Create output directory
    output_dir = 'downloaded_pdfs'
    os.makedirs(output_dir, exist_ok=True)

    # Read URLs from CSV
    try:
        df = pd.read_csv('links.csv')
        urls = df['coa_file_link'].tolist()
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return

    # Download files with delay between requests
    for i, url in enumerate(urls, 1):
        try:
            # Extract filename from URL parameters
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            filename = str(i)+"ADD:"+params.get('passcofonumber', ['unknown.pdf'])[0]

            output_path = os.path.join(output_dir, filename)

            print(i,f" Processing {i}/{len(urls)}: {filename}")

            if os.path.exists(output_path):
                print(f"File already exists: {filename}")
                continue

            success = download_file(url, output_path)

            # Add delay between requests
            time.sleep(2)  # 2 second delay

        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            continue

if __name__ == "__main__":
    main()
