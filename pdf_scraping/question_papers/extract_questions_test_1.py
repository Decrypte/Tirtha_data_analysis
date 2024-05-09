import re
from pdfminer.high_level import extract_text


# Function to download a PDF file
def download_pdf(url, directory):
    import requests
    import os

    response = requests.get(url)
    pdf_file_path = os.path.join(directory, "question_paper.pdf")
    with open(pdf_file_path, "wb") as f:
        f.write(response.content)
    return pdf_file_path


# Function to extract and clean the text from the PDF
def extract_and_clean_text(pdf_path):
    text = extract_text(pdf_path)
    # Clean up common OCR misreads here if necessary
    return text


# Function to parse questions from the extracted text
def parse_questions(text):
    questions = {}
    # Enhanced regex to capture questions and multiple choice options accurately
    pattern = re.compile(r"(\d+)\.\s+([^(]+)(\((?:[A-D])\)[^\(]+)+", re.DOTALL)
    matches = pattern.finditer(text)
    for match in matches:
        question_num = int(match.group(1))
        content = match.group(2).strip()
        options = dict(
            re.findall(r"\(([A-D])\)\s*(.*?)\s*(?=\([A-D]\)|$)", match.group(0))
        )
        questions[question_num] = {"question": content, "options": options}
    return questions


# Example usage
def main():
    download_directory = "D:\\#Data\\PDFs"
    url = "https://ncert.nic.in/pdf/publication/modelquestionpaper/classXII/Math.pdf"
    pdf_file_path = download_pdf(url, download_directory)

    text = extract_and_clean_text(pdf_file_path)
    questions = parse_questions(text)

    for q_num, details in questions.items():
        print(f"Question {q_num}: {details['question']}")
        for opt_key, opt_value in details["options"].items():
            print(f"  ({opt_key}) {opt_value}")


if __name__ == "__main__":
    main()
