import fitz
import requests
import os


def download_pdf(url, filepath):
    response = requests.get(url)
    pdf_file_path = os.path.join(filepath, "temp.pdf")
    with open(pdf_file_path, "wb") as f:
        f.write(response.content)
    return pdf_file_path


# Extract headings from a given file
def extract_headings(filepath):
    doc = fitz.open(filepath)
    headings = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        potential_headings = []

        for block in blocks:
            if "lines" in block and block["lines"]:
                text_lines = [
                    line["spans"][0]["text"] for line in block["lines"] if line["spans"]
                ]

                if is_likely_heading(block, text_lines):
                    potential_headings.append((text_lines[0], page_num))

        headings.extend(process_potential_headings(potential_headings))

    doc.close()
    return headings


# Heuristic for detecting if a block is a heading
def is_likely_heading(block, text_lines):
    if not text_lines or len(text_lines[0]) < 3 or len(text_lines[0]) > 100:
        return False

    # Consider block size and font attributes
    font_size = block["lines"][0]["spans"][0]["size"]
    font_flags = block["lines"][0]["spans"][0]["flags"]

    is_sufficient_size = 14 > font_size > 10
    has_font_flags = font_flags & 4

    return is_sufficient_size and has_font_flags


# Ensure unique headings
def process_potential_headings(potential_headings):
    seen = set()
    processed_headings = []

    for text, page_num in potential_headings:
        if text not in seen:
            processed_headings.append((text, page_num))
            seen.add(text)

    return processed_headings


# Extract sections based on identified headings
def extract_sections(filepath, headings):
    doc = fitz.open(filepath)
    sections = {}
    num_pages = len(doc)

    for i, (heading, page_num) in enumerate(headings):
        start_page = page_num - 1
        end_page = headings[i + 1][1] - 1 if i + 1 < len(headings) else num_pages - 1
        section_text = []
        section_started = False

        for page in range(start_page, end_page + 1):
            blocks = doc.load_page(page).get_text("dict")["blocks"]

            for block in blocks:
                if "lines" in block and block["lines"]:
                    text_lines = [
                        " ".join(span["text"] for span in line["spans"])
                        for line in block["lines"]
                        if line["spans"]
                    ]

                    # Check if the current block starts with the heading title
                    if text_lines and text_lines[0].startswith(heading):
                        section_started = True
                        section_text.append(" ".join(text_lines))
                    elif section_started:
                        # Stop if the next heading is encountered
                        if any(
                            text_lines[0].startswith(next_heading[0])
                            for next_heading in headings[i + 1 :]
                        ):
                            break

                        # Otherwise, continue collecting text
                        section_text.extend(text_lines)

            if section_started and page == end_page:
                break

        sections[heading] = " ".join(section_text).strip()[len(heading) + 1 :]

    doc.close()
    return sections


# Example usage
download_directory = r"D:\\#Data\\PDFs"
pdf_url = "https://arxiv.org/pdf/2301.02560"
pdf_file_path = download_pdf(pdf_url, download_directory)

# Extract headings and print them
headings = extract_headings(pdf_file_path)
print("Detected Headings:")
for heading, page_num in headings:
    print(f"Heading: {heading}, Page: {page_num}")

print(f"No. of headings in the doc: {len(headings)}")

# Extract section-wise data and print
sections = extract_sections(pdf_file_path, headings)
print("\nSection-wise Data:")
for heading, text in sections.items():
    print(f"\n{heading}")
    print(f"{text[:300]}...")
