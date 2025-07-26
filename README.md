# 🧠 AI Resume Ranker

An intelligent resume ranking system that compares uploaded resumes to a given job description using NLP techniques. This tool uses Sentence-BERT and cosine similarity to rank resumes by how well they match the job posting. Ideal for recruiters or job platforms.

---

## 🚀 Features

- 🔍 Upload multiple PDF resumes
- 📝 Paste any job description
- 📊 Get ranked results based on match percentage
- 🥇 Highlight top-matching resume
- ✅ View matched and ❌ missing skills
- 📥 Download results as a CSV file
- 🎨 Beautiful, responsive, glassmorphic UI

---

## 🛠️ Technologies Used

- **Frontend**: HTML, Bootstrap 5, CSS
- **Backend**: Flask (Python)
- **Model**: Sentence-BERT (`all-MiniLM-L6-v2`)
- **PDF Parsing**: PyPDF2
- **Similarity Scoring**: Cosine similarity (scikit-learn)
- **Skill Matching**: Keyword extraction from JD vs resume

---

## 💻 Getting Started

### 1. Clone the Repository

git clone https://github.com/rakshithdn/ai-resume-ranker.git
cd ai-resume-ranker

### Create Virtual Environment & Activate

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

### Install Requirements

pip install -r requirements.txt

### Run the Flask App

python app.py

Then open http://127.0.0.1:5000 in your browser.
📥 Download CSV
After ranking, click the 📥 Download CSV button to export results including ranks and match percentages.

🎯 Future Enhancements
🔒 Add user authentication (admin/recruiter roles)

💾 Save ranking history in SQLite database

🧠 More advanced skill matching logic

🌐 Ability to scrape job descriptions from LinkedIn

🖼️ UI Preview
![Preview](screenshot.png)

🙋‍♂️ Author
Rakshith D N
Built as a resume project integrating AI, web development, and UI design.
