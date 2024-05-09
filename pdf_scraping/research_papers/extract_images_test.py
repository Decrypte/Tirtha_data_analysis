import fitz
import requests
import os
from PIL import Image


# Create output directory if it does not exist
def ensure_output_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Function to download a PDF file from a URL
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


# Extract figures from the PDF and save them
def extract_figures(filepath, output_directory):
    doc = fitz.open(filepath)
    ensure_output_directory(output_directory)
    figure_count = 0

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images()  # Get all images on the page

        for i, img in enumerate(image_list):
            xref = img[0]  # Image XREF number
            pix = fitz.Pixmap(doc, xref)

            # Only extract if a reasonably sized image
            if pix.width >= 50 and pix.height >= 50:
                # Create an image using the Pillow library
                figure_img = Image.frombytes(
                    "RGB", (pix.width, pix.height), pix.samples
                )

                # Save the image to the output directory
                image_path = os.path.join(
                    output_directory,
                    f"page_{page_num + 1}_figure_{i + 1}.png",
                )
                figure_img.save(image_path)
                figure_count += 1

    print(f"Extracted {figure_count} figures.")
    doc.close()


# Example usage
download_directory = r"D:\\#Data\\PDFs"
output_directory = os.path.join(download_directory, "extracted_figures")
pdf_url = "https://arxiv.org/pdf/2301.02560"

pdf_file_path = download_pdf(pdf_url, download_directory)
if pdf_file_path:
    extract_figures(pdf_file_path, output_directory)
