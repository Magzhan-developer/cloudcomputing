import PyPDF2
import os
import sys

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            total_pages = len(pdf_reader.pages)
            
            print(f"\n{'='*80}")
            print(f"File: {os.path.basename(pdf_path)}")
            print(f"Total Pages: {total_pages}")
            print(f"{'='*80}\n")
            
            # Extract text from all pages
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            return text
    except Exception as e:
        return f"Error reading {pdf_path}: {str(e)}"

def main():
    sources_dir = r"d:\KBTU-directories\semester6\cloud computing for big data\tsis 1\sources"
    
    pdf_files = [
        "2023_ESG_Report__.pdf",
        "3Q_2025_Financial_Statements (1).pdf",
        "3Q_2025_Presentation.pdf",
        "3Q_2025_Results_.pdf"
    ]
    
    all_text = ""
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(sources_dir, pdf_file)
        if os.path.exists(pdf_path):
            text = extract_text_from_pdf(pdf_path)
            all_text += text
        else:
            print(f"File not found: {pdf_path}")
    
    # Save all extracted text to a file
    output_file = r"d:\KBTU-directories\semester6\cloud computing for big data\tsis 1\extracted_content.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"\n\nAll content extracted to: {output_file}")
    print(f"Total length: {len(all_text)} characters")

if __name__ == "__main__":
    main()
