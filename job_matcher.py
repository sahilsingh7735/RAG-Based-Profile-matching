
import os
import re
import json
from pathlib import Path

import cohere
import chromadb
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError(
        "COHERE_API_KEY not found in .env"
    )

COHERE_MODEL = "embed-v4.0"
EMBEDDING_DIMENSION = 1024

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "resume_collection"

TOP_K = 10

SEARCH_K = 100


# ============================================================
# INITIALIZE COHERE
# ============================================================

co = cohere.ClientV2(
    api_key=COHERE_API_KEY
)


# ============================================================
# INITIALIZE CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = chroma_client.get_collection(
    COLLECTION_NAME
)


# ============================================================
# EMBEDDING
# ============================================================

def generate_query_embedding(job_description):

    response = co.embed(
        model=COHERE_MODEL,
        texts=[job_description],
        input_type="search_query",
        output_dimension=EMBEDDING_DIMENSION,
        embedding_types=["float"]
    )

    return response.embeddings.float[0]


# ============================================================
# EXTRACT KEYWORDS
# ============================================================

def normalize_text(text):
    """
    Normalize text for reliable skill matching.
    """

    text = text.lower()

    # Normalize common variations
    text = text.replace("node.js", "nodejs")
    text = text.replace("express.js", "expressjs")
    text = text.replace("rest apis", "restapi")
    text = text.replace("rest api", "restapi")
    text = text.replace("scikit-learn", "scikitlearn")
    text = text.replace("github actions", "githubactions")
    text = text.replace("spring boot", "springboot")

    # Remove punctuation
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_keywords(job_description):

    skills = [
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "react native",
        "nodejs",
        "expressjs",
        "mongodb",
        "postgresql",
        "mysql",
        "sql",
        "django",
        "fastapi",
        "flask",
        "springboot",
        "c#",
        ".net",
        "aws",
        "azure",
        "docker",
        "kubernetes",
        "terraform",
        "jenkins",
        "git",
        "githubactions",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikitlearn",
        "pandas",
        "numpy",
        "spark",
        "kafka",
        "airflow",
        "mlflow",
        "html",
        "css",
        "tailwind",
        "redux",
        "selenium",
        "playwright",
        "cypress",
        "figma",
        "power bi",
        "tableau",
        "linux",
        "restapi",
        "microservices"
    ]

    normalized_job = normalize_text(
        job_description
    )

    found = []

    for skill in skills:

        normalized_skill = normalize_text(
            skill
        )

        # Exact token/phrase matching
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_skill)
            + r"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            normalized_job
        ):

            found.append(skill)

    return found


def extract_must_have_skills(job_description):
    """
    Extract must-have requirements from the MUST HAVE section.

    Returns:
        A list of individual skills.
    """

    text = job_description.lower()

    if "must have" not in text:
        return []

    section = text.split(
        "must have",
        1
    )[1]

    if "nice to have" in section:

        section = section.split(
            "nice to have",
            1
        )[0]

    return extract_keywords(section)

    text = job_description.lower()

    must_have_section = ""

    if "must have" in text:

        must_have_section = text.split(
            "must have",
            1
        )[1]

        # Stop at NICE TO HAVE if present
        if "nice to have" in must_have_section:

            must_have_section = (
                must_have_section.split(
                    "nice to have",
                    1
                )[0]
            )

    return extract_keywords(
        must_have_section
    )
    
def extract_must_have_requirements(job_description):
    """
    Extract must-have requirements while supporting
    alternatives such as:

        JavaScript or TypeScript

    Returns:
        A list of requirement groups.

    Example:

        [
            ["javascript", "typescript"],
            ["react"],
            ["nodejs"],
            ["mongodb"],
            ["restapi"]
        ]
    """

    text = job_description.lower()

    if "must have" not in text:
        return []

    section = text.split(
        "must have",
        1
    )[1]

    if "nice to have" in section:

        section = section.split(
            "nice to have",
            1
        )[0]

    requirements = []

    # Process each bullet/line
    lines = section.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove bullet characters
        line = re.sub(
            r"^[\-\*\•\d\.\)\s]+",
            "",
            line
        ).strip()

        if not line:
            continue

        # ----------------------------------------------------
        # Handle OR requirements
        # ----------------------------------------------------

        if re.search(
            r"\bor\b",
            line,
            re.IGNORECASE
        ):

            alternatives = re.split(
                r"\bor\b",
                line,
                flags=re.IGNORECASE
            )

            group = []

            for alternative in alternatives:

                skills = extract_keywords(
                    alternative
                )

                group.extend(skills)

            if group:
                requirements.append(
                    list(set(group))
                )

        else:

            skills = extract_keywords(
                line
            )

            for skill in skills:

                requirements.append(
                    [skill]
                )

    return requirements

def check_must_have_requirements(
    requirements,
    candidate_skills
):
    """
    Check whether a candidate satisfies all
    must-have requirement groups.

    For example:

        [javascript, typescript]

    means:

        JavaScript OR TypeScript

    while:

        [react]

    means React is required.
    """

    matched_requirements = []

    normalized_candidate = normalize_text(
        candidate_skills
    )

    for requirement_group in requirements:

        matched_option = None

        for skill in requirement_group:

            normalized_skill = normalize_text(
                skill
            )

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalized_skill)
                + r"(?![a-z0-9])"
            )

            if re.search(
                pattern,
                normalized_candidate
            ):

                matched_option = skill
                break

        if matched_option:

            matched_requirements.append(
                matched_option
            )

        else:

            return False, matched_requirements

    return True, matched_requirements
# ============================================================
# EXTRACT EXPERIENCE REQUIREMENT
# ============================================================

def extract_required_experience(job_description):

    patterns = [
        r"(\d+)\+?\s*years?",
        r"minimum\s+of\s+(\d+)\s*years?",
        r"at least\s+(\d+)\s*years?"
    ]

    text = job_description.lower()

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return float(match.group(1))

    return 0


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(
    job_description,
    top_k=SEARCH_K
):

    query_embedding = generate_query_embedding(
        job_description
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    return results

# ============================================================
# KEYWORD MATCHING
# ============================================================
def calculate_keyword_score(
    required_skills,
    candidate_skills
):

    if not required_skills:
        return 0, []

    normalized_candidate = normalize_text(
        candidate_skills
    )

    matched = []

    for skill in required_skills:

        normalized_skill = normalize_text(
            skill
        )

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_skill)
            + r"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            normalized_candidate
        ):

            matched.append(skill)

    score = (
        len(matched)
        / len(required_skills)
    ) * 100

    return score, matched
# ============================================================
# EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(
    required_years,
    candidate_years
):

    if required_years <= 0:
        return 100

    if candidate_years >= required_years:
        return 100

    # Partial score
    score = (
        candidate_years
        / required_years
    ) * 100

    return min(score, 100)


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(
    semantic_score,
    keyword_score,
    experience_score
):

    score = (
        semantic_score * 0.60
        + keyword_score * 0.25
        + experience_score * 0.15
    )

    return round(
        min(score, 100),
        2
    )


# ============================================================
# REASONING
# ============================================================

def generate_reasoning(
    candidate_name,
    matched_skills,
    required_skills,
    candidate_experience,
    required_experience,
    final_score,
    must_have_passed,
    matched_must_have
):

    reasons = []

    # --------------------------------------------------------
    # Must-have requirements
    # --------------------------------------------------------

    if must_have_passed:

        reasons.append(
            "The candidate satisfies the "
            "must-have requirements."
        )

    else:

        reasons.append(
            "The candidate does not satisfy "
            "all must-have requirements."
        )

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    if matched_skills:

        reasons.append(
            "Matched skills include "
            + ", ".join(
                sorted(matched_skills)
            )
            + "."
        )

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    if required_experience > 0:

        if candidate_experience >= required_experience:

            reasons.append(
                f"The candidate has "
                f"{candidate_experience:g} years of "
                f"experience, meeting the "
                f"{required_experience:g}+ year requirement."
            )

        else:

            reasons.append(
                f"The candidate has "
                f"{candidate_experience:g} years of "
                f"experience, below the "
                f"{required_experience:g}+ year requirement."
            )

    # --------------------------------------------------------
    # Overall assessment
    # --------------------------------------------------------

    if final_score >= 85:

        reasons.append(
            "Overall this is a very strong match."
        )

    elif final_score >= 70:

        reasons.append(
            "Overall this is a strong match."
        )

    elif final_score >= 55:

        reasons.append(
            "Overall this is a moderate match."
        )

    else:

        reasons.append(
            "Overall this is a relatively weak match."
        )

    return " ".join(reasons)

# ============================================================
# BUILD MATCH RESULTS
# ============================================================

def match_job(job_description):

    print("\nGenerating job description embedding...")

    required_skills = extract_keywords(
        job_description
    )

    required_experience = extract_required_experience(
        job_description
    )

    must_have_requirements = (
        extract_must_have_requirements(
            job_description
        )
    )

    print(
        f"Must-have requirements: "
        f"{must_have_requirements}"
    )

    print(
        f"Required experience: "
        f"{required_experience:g} years"
    )

    print("\nRunning semantic search...")

    results = semantic_search(
        job_description,
        SEARCH_K
    )
    
    print(
        f"\nRetrieved chunks: "
        f"{len(results['documents'][0])}"
    )

    candidates = {}

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        name = metadata["name"]

        # --------------------------------------------------------
        # Semantic similarity
        # --------------------------------------------------------

        semantic_similarity = 1 - distance

        semantic_score = max(
            0,
            min(
                semantic_similarity * 100,
                100
            )
        )

        # --------------------------------------------------------
        # Keyword matching
        # --------------------------------------------------------

        keyword_score, matched_skills = (
            calculate_keyword_score(
                required_skills,
                metadata.get(
                    "skills",
                    ""
                )
            )
        )

        # --------------------------------------------------------
        # Must-have matching
        # --------------------------------------------------------

        must_have_passed, matched_must_have = (
            check_must_have_requirements(
                must_have_requirements,
                metadata.get(
                    "skills",
                    ""
                )
            )
        )


        # --------------------------------------------------------
        # Experience
        # --------------------------------------------------------

        candidate_experience = float(
            metadata.get(
                "experience_years",
                0
            )
        )

        experience_score = (
            calculate_experience_score(
                required_experience,
                candidate_experience
            )
        )

        experience_passed = (
            candidate_experience >= required_experience
        )

        must_have_passed = (
            must_have_passed
            and experience_passed
        )

        # --------------------------------------------------------
        # Final score
        # --------------------------------------------------------

        final_score = calculate_final_score(
            semantic_score,
            keyword_score,
            experience_score
        )

        # --------------------------------------------------------
        # Candidate-level aggregation
        # --------------------------------------------------------

        if name not in candidates:

            candidates[name] = {
                "candidate_name": name,
                "resume_path": metadata[
                    "resume_path"
                ],
                "match_score": final_score,
                "best_semantic_score": semantic_score,
                "keyword_score": keyword_score,
                "experience_score": experience_score,
                "matched_skills": matched_skills,
                "matched_must_have": matched_must_have,
                "must_have_passed": must_have_passed,
                "candidate_experience": candidate_experience,
                "relevant_excerpts": [
                    document
                ]
            }

        else:

            candidate = candidates[name]

            # ----------------------------------------------------
            # Keep the strongest semantic chunk
            # ----------------------------------------------------

            if semantic_score > candidate[
                "best_semantic_score"
            ]:

                candidate[
                    "best_semantic_score"
                ] = semantic_score

            # ----------------------------------------------------
            # Keep strongest final score
            # ----------------------------------------------------

            if final_score > candidate[
                "match_score"
            ]:

                candidate[
                    "match_score"
                ] = final_score

            # ----------------------------------------------------
            # Merge matched skills
            # ----------------------------------------------------

            candidate[
                "matched_skills"
            ] = list(
                set(
                    candidate[
                        "matched_skills"
                    ]
                    + matched_skills
                )
            )

            candidate[
                "matched_must_have"
            ] = list(
                set(
                    candidate[
                        "matched_must_have"
                    ]
                    + matched_must_have
                )
            )

            # ----------------------------------------------------
            # Must-have should remain true only if all
            # requirements are satisfied
            # ----------------------------------------------------

            candidate[
                "must_have_passed"
            ] = (
                candidate[
                    "must_have_passed"
                ]
                and must_have_passed
            )

            # ----------------------------------------------------
            # Add useful excerpts
            # ----------------------------------------------------

            if document not in candidate[
                "relevant_excerpts"
            ]:

                candidate[
                    "relevant_excerpts"
                ].append(document)

    # ========================================================
    # SORT
    # ========================================================

    ranked_candidates = sorted(
        candidates.values(),
        key=lambda x: (
            x["must_have_passed"],
            x["match_score"]
        ),
        reverse=True
    )

    ranked_candidates = ranked_candidates[:TOP_K]

    # ========================================================
    # ADD REASONING
    # ========================================================

    for candidate in ranked_candidates:

        candidate["reasoning"] = (
            generate_reasoning(
                candidate["candidate_name"],
                candidate["matched_skills"],
                required_skills,
                candidate["candidate_experience"],
                required_experience,
                candidate["match_score"],
                candidate["must_have_passed"],
                candidate["matched_must_have"]
            )
        )

        # Remove internal scoring fields
        candidate.pop(
            "semantic_score",
            None
        )

        candidate.pop(
            "keyword_score",
            None
        )

        candidate.pop(
            "experience_score",
            None
        )

    return ranked_candidates


# ============================================================
# SAVE JSON
# ============================================================

def save_results(
    job_description,
    matches
):

    output = {
        "job_description": job_description,
        "top_matches": matches[:TOP_K]
    }

    output_path = Path(
        "outputs/match_results.json"
    )

    output_path.parent.mkdir(
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    return output_path


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(matches):

    print("\n")
    print("=" * 70)
    print("TOP CANDIDATES")
    print("=" * 70)

    for index, candidate in enumerate(
        matches[:TOP_K],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{candidate['candidate_name']}"
        )

        print(
            f"   Match Score: "
            f"{candidate['match_score']}/100"
        )

        print(
            f"   Skills: "
            f"{', '.join(candidate['matched_skills'])}"
        )

        print(
            f"   Reasoning: "
            f"{candidate['reasoning']}"
        )

    print("\n" + "=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RAG BASED PROFILE MATCHING")
    print("=" * 70)

    print(
        f"\nResumes indexed in ChromaDB: "
        f"{collection.count()}"
    )

    print("\nEnter your job description.")

    print(
        "Type END on a new line when finished."
    )

    lines = []

    while True:

        line = input()

        if line.strip().upper() == "END":

            break

        lines.append(line)

    job_description = "\n".join(
        lines
    ).strip()

    if not job_description:

        print(
            "No job description provided."
        )

        exit()

    matches = match_job(
        job_description
    )

    display_results(
        matches
    )

    output_path = save_results(
        job_description,
        matches
    )

    print(
        f"\nJSON saved to: "
        f"{output_path}"
    )