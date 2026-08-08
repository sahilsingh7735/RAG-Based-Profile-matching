import re
from pathlib import Path


# Resume sections that we want to preserve
SECTION_HEADERS = [
    "summary",
    "objective",
    "profile",
    "skills",
    "technical skills",
    "experience",
    "work experience",
    "professional experience",
    "education",
    "projects",
    "certifications",
    "achievements",
    "languages",
]


def normalize_text(text):
    """
    Clean unnecessary spaces and blank lines.
    """

    # Convert Windows line endings
    text = text.replace("\r\n", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def is_section_header(line):
    """
    Check whether a line looks like a resume section heading.
    """

    cleaned = line.strip().lower()

    # Remove common punctuation
    cleaned = cleaned.rstrip(":").strip()

    return cleaned in SECTION_HEADERS


def chunk_resume(text):
    """
    Split a resume into meaningful sections.

    Returns:
        list of dictionaries containing section name and text.
    """

    text = normalize_text(text)

    lines = text.split("\n")

    chunks = []

    current_section = "General"
    current_content = []

    for line in lines:

        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        if is_section_header(line):

            # Save previous section
            if current_content:

                section_text = "\n".join(current_content).strip()

                if section_text:
                    chunks.append({
                        "section": current_section,
                        "text": section_text
                    })

            # Start new section
            current_section = line.strip().rstrip(":").title()

            current_content = []

        else:
            current_content.append(line)

    # Save final section
    if current_content:

        section_text = "\n".join(current_content).strip()

        if section_text:
            chunks.append({
                "section": current_section,
                "text": section_text
            })

    return chunks


def load_resume(file_path):
    """
    Load a text resume from disk.
    """

    path = Path(file_path)

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":

    resume_path = Path("resumes")

    resume_files = list(resume_path.glob("*.txt"))

    print("=" * 60)
    print("RESUME CHUNKING TEST")
    print("=" * 60)

    print(f"\nFound {len(resume_files)} resume(s)\n")

    if not resume_files:

        print("No .txt resumes found in the resumes folder.")

    else:

        # Test first resume
        first_resume = resume_files[0]

        print(f"Testing: {first_resume}\n")

        resume_text = load_resume(first_resume)

        chunks = chunk_resume(resume_text)

        print(f"Created {len(chunks)} chunks\n")

        for index, chunk in enumerate(chunks, start=1):

            print("-" * 60)

            print(f"Chunk {index}")
            print(f"Section: {chunk['section']}")

            print("\nText:")
            print(chunk["text"][:500])

        print("\n")
        print("=" * 60)