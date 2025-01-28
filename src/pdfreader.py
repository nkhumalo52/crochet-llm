from pypdf import PdfReader
import os

BAD = []
def extract_section(full_text, start_marker, end_marker=None):
    """Extract text between start_marker and end_marker from full_text."""
    start_index = full_text.find(start_marker)
    if start_index == -1:
        #print(f"Start marker '{start_marker}' not found in the text.")
        return None
    
    if end_marker:
        end_index = full_text.find(end_marker, start_index)
        if end_index == -1:
            #print(f"End marker '{end_marker}' not found after the start marker.")
            return None
        section_text = full_text[start_index:end_index].strip()
    else:
        section_text = full_text[start_index:].strip()
    
    return section_text

def get_text(file_path):
    try:
        reader = PdfReader(file_path)
        full_text = ""
        
        # Extract text from each page
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        # Printing number of pages in the PDF file
        print(f"Number of pages in {file_path}: {len(reader.pages)}")
        
        # Extract specific sections
        start_marker = "INSTRUCTIONS"
        end_marker = "MATERIALS"
        section_text = extract_section(full_text, start_marker, end_marker)
        
        if section_text:
            print(f"Extracted text from {file_path}:")
            #print(section_text)
        else:
            BAD.append(file_path)
            #print(f"Could not extract section from {file_path}.")
        
    except Exception as e:
        print(f"Failed to extract text from {file_path}. Error: {e}")

def find_pdfs(directory="/Users/nkhumalo/VSCode/webscrape/downloaded_patterns"):
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist")
        return

    try:
        for root, dirs, files in os.walk(directory, topdown=True):
            for entry in files:
                if entry.endswith(".pdf"):
                    full_path = os.path.join(root, entry)
                    #print(f"Found PDF: {full_path}")
                    get_text(full_path)
                    #print("Extraction complete!")
    except PermissionError:
        print(f"Permission denied to access the directory {directory}")
    except OSError as e:
        print(f"An OS error occurred: {e}")

find_pdfs()
print(BAD)
