# Information Retrieval System - Production

This repository contains the production deployment of the Information Retrieval (IR) comparison project. It transforms the core algorithmic implementations into a fully functional, user-friendly web application using the Django framework.

## About The Project

While the core Information Retrieval repository focuses on the backend implementation and theoretical comparison of search models, this repository provides a web interface for end-users to interact with those systems. It allows users to input queries and instantly see how different retrieval techniques process, retrieve, and rank documents in real-time.

## Key Features

* **Web-Based Interface:** A clean, accessible front-end built with HTML, CSS, and Django templates for executing search queries.
* **Real-Time Comparison:** Enter a single query and view the side-by-side results from multiple IR models (such as Vector Space Model, Boolean, and BM25).
* **Metric Visualization:** Displays performance and evaluation metrics (like retrieval time and relevance scores) directly in the browser.
* **Scalable Architecture:** Built on Django, allowing for easy integration of databases, user authentication, and future scalability.

## Technologies Used

* **Backend Framework:** Django (Python)
* **Core IR Libraries:** NLTK, Scikit-learn, NumPy, Pandas (inherited from the core project)
* **Frontend:** HTML5, CSS3, JavaScript

## Installation and Setup

To run this Django web application on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/TahaSoylu44/Information_Retrieval_Production.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Information_Retrieval_Production
   ```

3. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows use: venv\Scripts\activate
   # On macOS/Linux use: source venv/bin/activate
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application by opening a web browser and navigating to `http://127.0.0.1:8000/`.

## Core Algorithmic Implementation

This project relies on the algorithms developed in the base repository. If you are interested in the raw implementation of the Vector Space Model, Boolean Retrieval, or BM25 without the web overhead, please refer to the core [Information Retrieval repository](https://github.com/TahaSoylu44/Information-Retrieval).

## Contributing

Contributions to improve the web interface, add new visualization features, or optimize the Django views are welcome. Please fork the repository, create a branch for your feature, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
