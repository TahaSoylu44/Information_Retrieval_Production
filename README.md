# Information Retrieval Techniques Comparison

This repository contains an Information Retrieval (IR) system designed to implement and compare various retrieval models. The primary goal of this project is to analyze how different algorithms perform in terms of indexing, searching, and ranking documents based on user queries.

## About The Project

Information Retrieval is a fundamental concept in search engines and data mining. This project provides a practical implementation of multiple IR models, allowing for a direct comparison of their efficiency, accuracy, and ranking behaviors when processing identical datasets and queries.

## Techniques Compared

This project evaluates and compares the following Information Retrieval techniques:

*   **Boolean Retrieval Model:** A foundational model based on set theory and boolean algebra, utilizing exact-match retrieval with operators (AND, OR, NOT).
*   **Vector Space Model (VSM):** An algebraic model that represents documents and queries as vectors. It compares ranking performance using Term Frequency-Inverse Document Frequency (TF-IDF) weighting and Cosine Similarity.
*   **Okapi BM25:** A probabilistic retrieval framework that improves upon standard TF-IDF by incorporating document length normalization and term frequency saturation, representing modern search engine standards.
*   **Evaluation Metrics:** The models are systematically compared using standard IR evaluation metrics, including Precision, Recall, F1-Score, and Mean Average Precision (MAP), to objectively determine which technique yields the most relevant results.

## Installation

To run this project and the comparison scripts locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/TahaSoylu44/Information-Retrieval.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Information-Retrieval
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
