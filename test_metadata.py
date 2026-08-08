from pathlib import Path

from resume_chunker import load_resume
from resume_rag import extract_metadata


resume_file = Path("resumes/john_doe.txt")

resume_text = load_resume(resume_file)

metadata = extract_metadata(
    resume_text,
    resume_file
)

print("=" * 60)
print("METADATA EXTRACTION TEST")
print("=" * 60)

print(f"Name             : {metadata['name']}")
print(f"Skills           : {metadata['skills']}")
print(f"Experience Years : {metadata['experience_years']}")
print(f"Education        : {metadata['education']}")
print(f"Resume Path      : {metadata['resume_path']}")

print("=" * 60)