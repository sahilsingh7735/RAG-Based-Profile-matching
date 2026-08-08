import os
import re
from pathlib import Path

import cohere
import chromadb
from dotenv import load_dotenv

from resume_chunker import chunk_resume, load_resume


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError(
        "COHERE_API_KEY not found in .env file"
    )

RESUMES_DIR = Path("resumes")
CHROMA_DIR = "chroma_db"

COLLECTION_NAME = "resume_collection"

COHERE_MODEL = "embed-v4.0"
EMBEDDING_DIMENSION = 1024


# ============================================================
# 2. INITIALIZE COHERE
# ============================================================

co = cohere.ClientV2(
    api_key=COHERE_API_KEY
)


# ============================================================
# 3. INITIALIZE CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

# Get existing collection or create it
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)

# ============================================================
# 4. METADATA EXTRACTION
# ============================================================

def extract_name(text):
    """
    Try to extract the candidate's name.
    """

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return "Unknown"

    # Usually the name is near the top of the resume
    for line in lines[:5]:

        lower_line = line.lower()

        # Ignore common headings
        ignored = [
            "resume",
            "curriculum vitae",
            "cv",
            "profile",
            "summary",
            "objective"
        ]

        if lower_line not in ignored:
            return line

    return "Unknown"


def extract_skills(text):
    """
    Extract skills from common resume skill sections.
    """

    skill_headers = [
        "skills",
        "technical skills",
        "key skills",
        "core skills",
        "core competencies",
        "technical competencies",
        "technologies",
        "tools and technologies"
    ]

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    collecting = False
    skill_lines = []

    for line in lines:

        cleaned = line.strip()
        lower = cleaned.lower().rstrip(":")

        # ----------------------------------------------------
        # Start collecting when we find a skills heading
        # ----------------------------------------------------

        if lower in skill_headers:

            collecting = True
            continue

        # ----------------------------------------------------
        # Stop when another major section starts
        # ----------------------------------------------------

        if collecting:

            possible_header = re.sub(
                r"[:\-]",
                "",
                lower
            ).strip()

            major_sections = [
                "summary",
                "objective",
                "profile",
                "experience",
                "work experience",
                "professional experience",
                "education",
                "projects",
                "certifications",
                "achievements",
                "languages"
            ]

            if possible_header in major_sections:

                break

            skill_lines.append(cleaned)

    if not skill_lines:

        return "Not specified"

    # Join skill lines
    skills_text = ", ".join(skill_lines)

    # Clean duplicate separators
    skills_text = re.sub(
        r",\s*,+",
        ", ",
        skills_text
    )

    return skills_text[:1000]
    """
    Extract skills from the Skills section.
    """

    pattern = re.compile(
        r"(?:skills|technical skills|key skills)\s*:?\s*(.*?)(?=\n[A-Z][A-Za-z ]{2,30}\s*:?\s*\n|\Z)",
        re.IGNORECASE | re.DOTALL
    )

    match = pattern.search(text)

    if match:
        skills_text = match.group(1).strip()

        # Convert common separators into commas
        skills_text = skills_text.replace(
            "\n",
            ", "
        )

        return skills_text[:1000]

    return "Not specified"


def extract_experience_years(text):
    """
    Try to find total experience years.
    """

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+(?:of\s+)?experience",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s*years?"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    return 0


def extract_education(text):
    """
    Try to find education information.
    """

    education_keywords = [
        "B.Tech",
        "B.E.",
        "Bachelor",
        "M.Tech",
        "M.E.",
        "Master",
        "MBA",
        "BCA",
        "MCA",
        "PhD",
        "B.Sc",
        "M.Sc"
    ]

    found = []

    for line in text.split("\n"):

        line = line.strip()

        for keyword in education_keywords:

            if keyword.lower() in line.lower():

                if line not in found:
                    found.append(line)

                break

    if found:
        return " | ".join(found[:5])

    return "Not specified"


def extract_metadata(text, resume_path):

    return {
        "name": extract_name(text),
        "skills": extract_skills(text),
        "experience_years": extract_experience_years(text),
        "education": extract_education(text),
        "resume_path": str(resume_path)
    }


# ============================================================
# 5. COHERE EMBEDDINGS
# ============================================================

def generate_embeddings(texts):

    if not texts:
        return []

    response = co.embed(
        model=COHERE_MODEL,
        texts=texts,
        input_type="search_document",
        output_dimension=EMBEDDING_DIMENSION,
        embedding_types=["float"]
    )

    return response.embeddings.float


# ============================================================
# 6. PROCESS RESUMES
# ============================================================

def process_resumes():

    # Find TXT and PDF files
    resume_files = list(
        RESUMES_DIR.glob("*.txt")
    )

    print("=" * 70)
    print("RAG RESUME PROCESSING PIPELINE")
    print("=" * 70)

    print(
        f"\nFound {len(resume_files)} resume(s)\n"
    )

    if not resume_files:

        print(
            "No .txt resumes found inside the resumes folder."
        )

        return

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    # --------------------------------------------------------
    # Process every resume
    # --------------------------------------------------------

    for index, resume_file in enumerate(
        resume_files,
        start=1
    ):

        print(
            f"[{index}/{len(resume_files)}] "
            f"Processing {resume_file.name}"
        )

        # ----------------------------------------------------
        # Read resume
        # ----------------------------------------------------

        resume_text = load_resume(
            resume_file
        )

        # ----------------------------------------------------
        # Extract metadata
        # ----------------------------------------------------

        metadata = extract_metadata(
            resume_text,
            resume_file
        )

        print(
            f"    Candidate: {metadata['name']}"
        )

        print(
            f"    Experience: "
            f"{metadata['experience_years']} years"
        )

        # ----------------------------------------------------
        # Chunk resume
        # ----------------------------------------------------

        chunks = chunk_resume(
            resume_text
        )

        print(
            f"    Chunks: {len(chunks)}"
        )

        # ----------------------------------------------------
        # Prepare text for embedding
        # ----------------------------------------------------

        chunk_texts = []

        for chunk in chunks:

            text = (
                f"Candidate: {metadata['name']}\n"
                f"Section: {chunk['section']}\n\n"
                f"{chunk['text']}"
            )

            chunk_texts.append(text)

        # ----------------------------------------------------
        # Generate Cohere embeddings
        # ----------------------------------------------------

        chunk_embeddings = generate_embeddings(
            chunk_texts
        )

        # ----------------------------------------------------
        # Store chunks
        # ----------------------------------------------------

        for chunk_index, (
            chunk,
            text,
            embedding
        ) in enumerate(
            zip(
                chunks,
                chunk_texts,
                chunk_embeddings
            )
        ):

            chunk_id = (
                f"{resume_file.stem}_"
                f"{chunk_index}"
            )

            chunk_metadata = {
                **metadata,
                "section": chunk["section"]
            }

            ids.append(chunk_id)

            documents.append(text)

            embeddings.append(
                embedding
            )

            metadatas.append(
                chunk_metadata
            )

    # ========================================================
    # STORE IN CHROMADB
    # ========================================================

    print("\nStoring embeddings in ChromaDB...")

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("RAG PIPELINE COMPLETED")
    print("=" * 70)

    print(
        f"Resumes processed : {len(resume_files)}"
    )

    print(
        f"Chunks created    : {len(documents)}"
    )

    print(
        f"Embeddings        : {len(embeddings)}"
    )

    print(
        f"ChromaDB records  : {collection.count()}"
    )

    print(
        f"Database location : {CHROMA_DIR}"
    )

    print("=" * 70)


# ============================================================
# 7. MAIN
# ============================================================

if __name__ == "__main__":

    process_resumes()