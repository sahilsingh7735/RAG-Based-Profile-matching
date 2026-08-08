import json
import time
from pathlib import Path

from job_matcher import match_job


# ============================================================
# CONFIGURATION
# ============================================================

JD_DIR = Path("job_descriptions")

TOP_K = 10


# ============================================================
# EXPECTED RELEVANT CANDIDATES
# ============================================================

EXPECTED_MATCHES = {

    "jd_01_full_stack.txt": [
        "Rahul Sharma",
        "John Doe",
        "Varun Singh",
        "Vikas Mehta",
        "Ayesha Khan",
        "Priya Singh"
    ],

    "jd_02_data_scientist.txt": [
        "Sneha Kapoor",
        "Saurabh Mishra",
        "Meera Nair",
        "Anjali Rao"
    ],

    "jd_03_backend_developer.txt": [
        "Amit Verma",
        "Neha Gupta",
        "Vikas Mehta",
        "Varun Singh"
    ],

    "jd_04_ml_engineer.txt": [
        "Saurabh Mishra",
        "Meera Nair",
        "Harsh Vardhan",
        "Sneha Kapoor"
    ],

    "jd_05_frontend_developer.txt": [
        "Priya Singh",
        "Rahul Sharma",
        "John Doe",
        "Ayesha Khan",
        "Varun Singh"
    ]
}


# ============================================================
# PRECISION@K
# ============================================================

def precision_at_k(
    predicted,
    relevant,
    k=TOP_K
):

    predicted = predicted[:k]

    if not predicted:
        return 0.0

    relevant_set = set(
        relevant
    )

    hits = sum(
        1
        for candidate in predicted
        if candidate in relevant_set
    )

    return hits / len(predicted)


# ============================================================
# RECALL@K
# ============================================================

def recall_at_k(
    predicted,
    relevant,
    k=TOP_K
):

    predicted = predicted[:k]

    if not relevant:
        return 0.0

    relevant_set = set(
        relevant
    )

    hits = sum(
        1
        for candidate in predicted
        if candidate in relevant_set
    )

    return hits / len(relevant_set)


# ============================================================
# MRR
# ============================================================

def mean_reciprocal_rank(
    predicted,
    relevant
):

    relevant_set = set(
        relevant
    )

    for index, candidate in enumerate(
        predicted,
        start=1
    ):

        if candidate in relevant_set:

            return 1 / index

    return 0.0


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    print("=" * 70)
    print("RAG PROFILE MATCHING EVALUATION")
    print("=" * 70)

    results = []

    for jd_filename, relevant_candidates in (
        EXPECTED_MATCHES.items()
    ):

        jd_path = JD_DIR / jd_filename

        if not jd_path.exists():

            print(
                f"\nSkipping missing JD: "
                f"{jd_filename}"
            )

            continue

        job_description = jd_path.read_text(
            encoding="utf-8"
        )

        print(
            f"\nEvaluating: "
            f"{jd_filename}"
        )

        # ----------------------------------------------------
        # Measure latency
        # ----------------------------------------------------

        start_time = time.perf_counter()

        matches = match_job(
            job_description
        )

        end_time = time.perf_counter()

        latency_ms = (
            end_time - start_time
        ) * 1000

        predicted = [
            candidate[
                "candidate_name"
            ]
            for candidate in matches[:TOP_K]
        ]

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        precision = precision_at_k(
            predicted,
            relevant_candidates
        )

        recall = recall_at_k(
            predicted,
            relevant_candidates
        )

        mrr = mean_reciprocal_rank(
            predicted,
            relevant_candidates
        )

        result = {
            "job_description": jd_filename,
            "predicted_candidates": predicted,
            "expected_candidates": relevant_candidates,
            "precision_at_10": round(
                precision,
                4
            ),
            "recall_at_10": round(
                recall,
                4
            ),
            "mrr": round(
                mrr,
                4
            ),
            "latency_ms": round(
                latency_ms,
                2
            )
        }

        results.append(result)

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        print(
            f"Precision@10 : "
            f"{precision:.2%}"
        )

        print(
            f"Recall@10    : "
            f"{recall:.2%}"
        )

        print(
            f"MRR          : "
            f"{mrr:.4f}"
        )

        print(
            f"Latency      : "
            f"{latency_ms:.2f} ms"
        )

    # ========================================================
    # AVERAGES
    # ========================================================

    if results:

        avg_precision = sum(
            r["precision_at_10"]
            for r in results
        ) / len(results)

        avg_recall = sum(
            r["recall_at_10"]
            for r in results
        ) / len(results)

        avg_mrr = sum(
            r["mrr"]
            for r in results
        ) / len(results)

        avg_latency = sum(
            r["latency_ms"]
            for r in results
        ) / len(results)

    else:

        avg_precision = 0
        avg_recall = 0
        avg_mrr = 0
        avg_latency = 0

    # ========================================================
    # SUMMARY
    # ========================================================

    summary = {
        "average_precision_at_10": round(
            avg_precision,
            4
        ),
        "average_recall_at_10": round(
            avg_recall,
            4
        ),
        "average_mrr": round(
            avg_mrr,
            4
        ),
        "average_latency_ms": round(
            avg_latency,
            2
        ),
        "number_of_job_descriptions": len(
            results
        ),
        "details": results
    }

    # ========================================================
    # SAVE
    # ========================================================

    output_dir = Path("outputs")

    output_dir.mkdir(
        exist_ok=True
    )

    output_path = (
        output_dir
        / "evaluation_results.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=2
        )

    # ========================================================
    # FINAL DISPLAY
    # ========================================================

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Average Precision@10 : "
        f"{avg_precision:.2%}"
    )

    print(
        f"Average Recall@10    : "
        f"{avg_recall:.2%}"
    )

    print(
        f"Average MRR          : "
        f"{avg_mrr:.4f}"
    )

    print(
        f"Average Latency      : "
        f"{avg_latency:.2f} ms"
    )

    print(
        f"\nResults saved to:"
        f"\n{output_path}"
    )


if __name__ == "__main__":

    main()