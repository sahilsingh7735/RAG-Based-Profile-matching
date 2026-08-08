import os
from pathlib import Path
from datetime import datetime

from PyPDF2 import PdfReader
from docx import Document

def list_files(directory: str, extension: str = None):
    """
    List all files in a directory.
    Optionally filter by file extension.
    """

    files = []

    if not os.path.exists(directory):
        return {"status": "error", "message": "Directory not found"}

    for file in Path(directory).iterdir():

        if file.is_file():

            if extension is None or file.suffix.lower() == extension.lower():

                files.append({
                    "name": file.name,
                    "size": file.stat().st_size,
                    "modified_date": datetime.fromtimestamp(
                        file.stat().st_mtime
                    ).strftime("%Y-%m-%d %H:%M:%S")
                })

    return files

def read_file(filepath: str):
    """
    Read TXT, PDF and DOCX files.
    Returns file content and metadata.
    """

    if not os.path.exists(filepath):
        return {
            "status": "error",
            "message": "File not found"
        }

    extension = Path(filepath).suffix.lower()

    try:

        # TXT File
        if extension == ".txt":

            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

        # PDF File
        elif extension == ".pdf":

            reader = PdfReader(filepath)

            content = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    content += page_text + "\n"

        # DOCX File
        elif extension == ".docx":

            doc = Document(filepath)

            content = ""

            for para in doc.paragraphs:
                content += para.text + "\n"

        else:

            return {
                "status": "error",
                "message": "Unsupported file format"
            }

        return {
            "status": "success",
            "filename": Path(filepath).name,
            "extension": extension,
            "content": content
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
        
def write_file(filepath: str, content: str):
    """
    Write content to a file.
    Creates directories if they don't exist.
    """

    try:
        # Create parent directory if needed
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        return {
            "status": "success",
            "message": f"File '{filepath}' written successfully."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
def search_in_file(filepath: str, keyword: str):
    """
    Search for a keyword inside a file.
    Case-insensitive search.
    """

    file_data = read_file(filepath)

    if file_data["status"] == "error":
        return file_data

    content = file_data["content"]

    lines = content.splitlines()

    matches = []

    for index, line in enumerate(lines):

        if keyword.lower() in line.lower():

            start = max(0, index - 1)
            end = min(len(lines), index + 2)

            context = "\n".join(lines[start:end])

            matches.append({
                "line": index + 1,
                "context": context
            })

    return {
        "status": "success",
        "keyword": keyword,
        "matches": matches,
        "total_matches": len(matches)
    }