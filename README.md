# RAG-Based Profile Matching System

A Retrieval-Augmented Generation (RAG) based resume matching system that uses Cohere embeddings and ChromaDB to retrieve and rank candidates against job descriptions.

## 1. Project Overview

This project implements a semantic resume search and profile matching pipeline.

The system:

1. Loads resume documents.
2. Extracts candidate metadata.
3. Splits resumes into meaningful sections.
4. Generates Cohere embeddings.
5. Stores embeddings in ChromaDB.
6. Converts job descriptions into query embeddings.
7. Retrieves semantically relevant resume chunks.
8. Groups results by candidate.
9. Performs keyword matching.
10. Checks must-have requirements.
11. Checks experience requirements.
12. Calculates a 0–100 match score.
13. Generates match reasoning.
14. Returns the top 10 candidates as JSON.

---

## 2. Technology Stack

- Python
- Cohere
- ChromaDB
- python-dotenv
- RAG
- Vector Search
- Semantic Search
- Keyword Matching

### Embedding Model

Cohere `embed-v4.0`

### Embedding Dimension

1024

### Vector Database

ChromaDB

---

## 3. Dataset

The project contains:

- 31 resumes
- 155 resume chunks
- 155 stored embeddings
- 5 primary evaluation job descriptions

Each resume is divided into multiple sections such as:

- General
- Summary
- Skills
- Experience
- Education

---

## 4. Project Structure

```text
Project 2 - RAG Profile Matching/
│
├── resumes/
│   ├── resume_01_full_stack.txt
│   ├── resume_02_backend.txt
│   └── ...
│
├── job_descriptions/
│   ├── jd_01_full_stack.txt
│   ├── jd_02_data_scientist.txt
│   └── ...
│
├── chroma_db/
│
├── outputs/
│   ├── match_results.json
│   └── evaluation_results.json
│
├── resume_chunker.py
├── resume_rag.py
├── job_matcher.py
├── evaluation.py
├── generate_dataset.py
├── test_cohere.py
├── test_metadata.py
├── check_database.py
├── evaluation_ground_truth.json
├── requirements.txt
├── .env
└── README.md  