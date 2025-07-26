import os
import shutil
import csv
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import PyPDF2
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer  # ✅ for skill extraction

app = Flask(__name__, template_folder='template')
UPLOAD_FOLDER = 'resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_keywords(text, top_n=20):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
    X = vectorizer.fit_transform([text])
    return set(vectorizer.get_feature_names_out())

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    job_description = ""
    skill_analysis = {}

    if request.method == 'POST':
        shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        job_description = request.form.get('job_description', '').strip()
        resumes = request.files.getlist('resumes')

        if not job_description or not resumes:
            return render_template('index.html', results=None, jd=job_description, error="Please provide both Job Description and Resumes.")

        resume_texts = []
        filenames = []

        for resume in resumes:
            if resume.filename.endswith('.pdf'):
                filename = secure_filename(resume.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                resume.save(filepath)

                text = extract_text_from_pdf(filepath)
                resume_texts.append(text)
                filenames.append(filename)

        # SBERT Encoding
        jd_embedding = model.encode(job_description, convert_to_tensor=True)
        resume_embeddings = model.encode(resume_texts, convert_to_tensor=True)

        cosine_scores = util.cos_sim(jd_embedding, resume_embeddings)[0]

        results = []
        for i, score in enumerate(cosine_scores):
            match_percentage = round(score.item() * 100, 2)
            results.append((filenames[i], match_percentage))

        # Sort by match percentage
        results.sort(key=lambda x: x[1], reverse=True)

        # Save CSV
        with open('ranked_results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Rank', 'Filename', 'Match %'])
            for i, (filename, score) in enumerate(results, start=1):
                writer.writerow([i, filename, score])

        # Skill comparison logic
        jd_keywords = extract_keywords(job_description, top_n=15)

        for i, text in enumerate(resume_texts):
            resume_keywords = extract_keywords(text, top_n=50)
            matched = sorted(jd_keywords & resume_keywords)
            missing = sorted(jd_keywords - resume_keywords)
            skill_analysis[filenames[i]] = {
                'matched': matched,
                'missing': missing
            }

    return render_template(
        'index.html',
        results=results,
        jd=job_description,
        skill_analysis=skill_analysis
    )

@app.route('/download')
def download_results():
    csv_path = 'ranked_results.csv'
    if not os.path.exists(csv_path):
        return "No results available to download."
    return send_file(csv_path, as_attachment=True)


if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)