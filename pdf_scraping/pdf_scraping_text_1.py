import fitz  # PyMuPDF
import requests
import os


def download_pdf(url, download_path):
    response = requests.get(url)
    pdf_file_path = os.path.join(download_path, "temp1.pdf")
    with open(pdf_file_path, "wb") as f:
        f.write(response.content)
    return pdf_file_path


def extract_section_from_pdf(filepath, topic):
    doc = fitz.open(filepath)
    section_started = False
    section_text = ""
    possible_endings = [
        "Abstract",
        "Introduction",
        "Related Work",
        "Methodology",
        "Conclusion",
        "References",
        "Acknowledgements",
    ]

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:  # Check if the block contains lines
                for line in block["lines"]:
                    text_line = "".join([span["text"] for span in line["spans"]])
                    if topic in text_line:
                        print(f"Found topic: {topic}")
                        for span in line["spans"]:
                            print(f"Font: {span['font']}, Size: {span['size']}")
                        section_started = True
                        section_text = text_line + " "  # Start capturing from the title
                    elif section_started:
                        if any(
                            keyword in text_line
                            for keyword in possible_endings
                            if keyword != topic
                        ):
                            # This checks if we encounter another section heading, but it's not the current one
                            return section_text.strip()
                        section_text += text_line + " "

    doc.close()
    return section_text.strip()


download_directory = r"D:\\#Data\\PDFs"
pdf_url = "https://arxiv.org/pdf/2301.02560"
pdf_file_path = download_pdf(pdf_url, download_directory)

# Specifying the topic here
topic = "Introduction"
section_text = extract_section_from_pdf(pdf_file_path, topic)
print(f"{topic} Section Text:", section_text)
