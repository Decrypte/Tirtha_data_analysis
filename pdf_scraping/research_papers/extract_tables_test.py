import os
import requests
import camelot


# Directory management function
def ensure_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# PDF downloader
def download_pdf(url, filepath):
    response = requests.get(url)
    if response.status_code == 200:
        pdf_file_path = os.path.join(filepath, "temp.pdf")
        with open(pdf_file_path, "wb") as f:
            f.write(response.content)
        return pdf_file_path
    else:
        print("Failed to download PDF")
        return None


# Extract tables using Camelot
def extract_tables(filepath, output_directory, mode="stream"):
    ensure_output_directory(output_directory)

    # Extract tables using Camelot
    tables = camelot.read_pdf(filepath, pages="all", flavor=mode)

    valid_tables = 0
    for i, table in enumerate(tables):
        # Check if the table has valid content and meaningful headers
        df = table.df
        if not any("Unnamed" in col for col in df.iloc[0]) and not df.empty:
            csv_path = os.path.join(output_directory, f"table_{valid_tables + 1}.csv")
            df.to_csv(csv_path, index=False)
            valid_tables += 1

    print(f"Extracted {valid_tables} valid tables.")


# Example usage
download_directory = r"D:\\#Data\\PDFs"
output_directory = os.path.join(download_directory, "extracted_tables")
pdf_url = "https://arxiv.org/pdf/2301.02560"

pdf_file_path = download_pdf(pdf_url, download_directory)
if pdf_file_path:
    extract_tables(pdf_file_path, output_directory)
