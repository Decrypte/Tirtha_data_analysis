from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from pdf2image import convert_from_path
import pytesseract
import requests
import re
import os
from PIL import Image


# Function to download a PDF file
def download_pdf(url, directory):
    response = requests.get(url)
    pdf_file_path = os.path.join(directory, "question_paper.pdf")
    with open(pdf_file_path, "wb") as f:
        f.write(response.content)
    return pdf_file_path


# Function to extract text blocks from a PDF page using pdfminer
def extract_text_blocks_from_page(page):
    blocks = []
    for element in page:
        if isinstance(element, LTTextContainer):
            text = element.get_text()
            # Normalize whitespaces and strip unwanted characters
            cleaned_text = " ".join(text.split())
            blocks.append(cleaned_text)
    return blocks


# Function to convert PDF pages to images and perform OCR with Tesseract
def extract_text_with_ocr(pdf_path, dpi=300):
    images = convert_from_path(pdf_path, dpi)
    all_text = []
    for i, image in enumerate(images):
        image_path = f"temp_page_{i}.png"
        image.save(image_path, "PNG")
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        all_text.append(text)
        os.remove(image_path)
    return "\n".join(all_text)


# Function to parse questions using regex
def parse_questions(text):
    question_pattern = re.compile(r"\d+\.\s+(.*?)(?=\n)")
    option_pattern = re.compile(r"\(([A-D])\)\s+(.*)")
    answer_pattern = re.compile(r"Ans\.\s*([A-D])")

    questions = {}
    current_question = None

    for match in question_pattern.finditer(text):
        question_number = int(re.search(r"\d+", match.group(0)).group())
        questions[question_number] = {"question_text": match.group(1), "options": {}}
        current_question = question_number

        options = option_pattern.findall(match.group(0))
        for option in options:
            questions[current_question]["options"][option[0]] = option[1]

    answers = answer_pattern.findall(text)
    for i, answer in enumerate(answers, start=1):
        if i in questions:
            questions[i]["answer"] = answer

    return questions


# Function to extract all questions and answers from a PDF file
def extract_questions_from_pdf(pdf_path):
    # Extract text directly using pdfminer
    all_text_blocks = []
    for page in extract_pages(pdf_path):
        all_text_blocks.extend(extract_text_blocks_from_page(page))
    direct_extracted_text = "\n".join(all_text_blocks)

    # Extract text using OCR as a fallback
    ocr_text = extract_text_with_ocr(pdf_path)

    # Organize and parse questions
    questions = parse_questions(direct_extracted_text + "\n" + ocr_text)

    return questions


download_directory = "D:\\#Data\\PDFs"
url = "https://ncert.nic.in/pdf/publication/modelquestionpaper/classXII/Math.pdf"
pdf_file_path = download_pdf(url, download_directory)

questions = extract_questions_from_pdf(pdf_file_path)

# Output the questions in the desired structure
for question_number, content in questions.items():
    print(f"Question {question_number}: {content['question_text']}")
    for option, text in content["options"].items():
        print(f"  {option}. {text}")
    print(f"Answer: {content.get('answer', 'Not Provided')}\n")
