# Misinfo Verifier AI - Project Plan

## **1. Project Overview**
### **1.1 Objective**
Misinfo Verifier AI is an open-source project designed to search for, analyze, and verify the credibility of online sources. The AI uses web search APIs, NLP (Natural Language Processing), and machine learning to assess the reliability of online content.

### **1.2 Current State**
The project is now in a **finished state** for the time being. It includes:
- A **web-based interface** built with Flask for interacting with the system.
- A **data collection module** that fetches articles using NewsAPI.
- An **NLP-based credibility analysis** module that predicts the credibility of articles using a trained machine learning model.
- A **PostgreSQL database** to store search results and credibility scores.

While the project is functional, there are opportunities for future improvements and expansions (see **Section 6**).

---

## **2. Technology Stack**
### **2.1 Programming Languages**
- **Python** (primary language for NLP, machine learning, and backend development)

### **2.2 Libraries & Frameworks**
- **Web Scraping**: `requests`, `BeautifulSoup`
- **NLP**: `scikit-learn`, `TfidfVectorizer`
- **Machine Learning**: `scikit-learn` (for text classification)
- **Database**: `PostgreSQL`, `psycopg2` (for database connectivity)
- **Web Framework**: `Flask` (for the web interface)
- **Version Control**: `Git/GitHub`

### **2.3 External APIs**
- **NewsAPI** (for fetching news articles)

---

## **3. System Architecture**
### **3.1 High-Level Flow**
1. **User Input** → The user provides a search term (e.g., "covid").
2. **Data Collection** → The system retrieves search results from NewsAPI.
3. **Text Processing & NLP Analysis** → Extracts article content and predicts credibility using a trained machine learning model.
4. **Credibility Scoring** → Assigns a credibility score ("Real" or "Fake") based on the model's prediction.
5. **Output Results** → Presents analyzed data in a structured format via a web interface.

### **3.2 Component Breakdown**
- **Data Collection Module**: Fetches articles using NewsAPI.
- **NLP Analysis Module**: Predicts credibility using a trained machine learning model.
- **Database Module**: Stores search results and credibility scores in PostgreSQL.
- **User Interface**: A Flask-based web interface for interacting with the system.

---

## **4. Development Roadmap**
### **Phase 1: Setup & Research (Completed)**
- [x] Created a GitHub repository.
- [x] Researched available APIs and datasets.
- [x] Set up the development environment (Python, libraries, database).

### **Phase 2: Data Collection (Completed)**
- [x] Implemented web search using NewsAPI.
- [x] Developed a basic web scraper for extracting article content.
- [x] Stored collected data in a PostgreSQL database.

### **Phase 3: NLP Processing (Completed)**
- [x] Trained a machine learning model for text classification (true vs. false information).
- [x] Integrated the model into the system for credibility prediction.

### **Phase 4: Credibility Scoring (Completed)**
- [x] Developed a credibility scoring system based on the model's predictions.
- [x] Stored credibility scores in the database.

### **Phase 5: UI & Deployment (Completed)**
- [x] Built a Flask-based web interface for interacting with the system.
- [x] Deployed the application locally for testing.

---

## **5. Challenges & Considerations**
### **5.1 Ethical & Legal Considerations**
- Ensured compliance with **NewsAPI's terms of service**.
- Avoided reinforcing bias in the AI model by using a diverse dataset for training.
- Clearly defined the limitations of the system to prevent misuse.

### **5.2 Technical Challenges**
- Handled connection issues with external APIs.
- Managed large-scale text data efficiently.
- Balanced real-time speed with deep analysis.

---

## **6. Future Improvements**
While the project is functional, there are several areas for future improvement:
1. **Expand Data Sources**:
    - Integrate additional APIs (e.g., Bing News Search, The Guardian) for broader coverage.
    - Implement web scraping for sources not covered by APIs.

2. **Enhance NLP Analysis**:
    - Use advanced NLP techniques (e.g., entity extraction, sentiment analysis) to improve credibility predictions.
    - Integrate fact-checking APIs (e.g., Google Fact Check, Snopes) for cross-referencing claims.

3. **Improve User Interface**:
    - Add pagination and filtering options for search results.
    - Use a modern frontend framework (e.g., React) for a more interactive experience.

4. **Add Multilingual Support**:
    - Extend the system to analyze articles in multiple languages.

5. **Deploy the Application**:
    - Deploy the application to a cloud platform (e.g., Heroku, AWS) for public access.

6. **Add Testing**:
    - Write unit and integration tests to ensure the system's reliability.

---

## **7. How to Use**
### **7.1 Prerequisites**
- Python 3.9 or higher
- PostgreSQL
- NewsAPI key (register at [NewsAPI](https://newsapi.org/))

### **7.2 Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/EnesByakuya/misinfo-verifier-ai.git
   cd misinfo-verifier-ai
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. Set up the database:
    - Create a PostgreSQL database and update the `.env` file with your database credentials:
      ```env
      DB_NAME=your_database_name
      DB_USER=your_username
      DB_PASS=your_password
      DB_HOST=localhost
      DB_PORT=5432
      
4. Run the application:
   ```bash
   python app.py
   
5. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to use the web interface.

---

### **8. Contributing**
Contributions are welcome! If you'd like to contribute, please:
- Fork the repository.
- Create a new branch for your feature or bugfix.
- Submit a pull request with a detailed description of your changes.

---

### **9. License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### **10. Acknowledgments**
- Thanks to NewsAPI for providing the news data.
- Thanks to the open-source community for the libraries and tools used in this project.