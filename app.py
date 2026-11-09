
from flask import Flask, render_template, request
import os

from resume_parser import extract_resume_text
from skill_extractor import (
    extract_skills,
    find_missing_skills
)
from job_matcher import calculate_match

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["resume"]

        job_description = request.form[
            "job_description"
        ]

        if not file or not file.filename:
            return "Please upload a resume."

        if not file.filename.lower().endswith(
            (".pdf", ".docx")
        ):
            return "Upload only PDF or DOCX files."

        path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(path)

        resume_text = extract_resume_text(path)

        resume_skills = extract_skills(resume_text)

        job_skills = extract_skills(job_description)

        matched, missing = find_missing_skills(
            resume_skills, job_skills
        )

        score = calculate_match(
            resume_text, job_description
        )

        coverage = (
            len(matched) / len(job_skills) * 100
            if job_skills else 0
        )

        os.remove(path)

        return render_template(
            "result.html",
            score=score,
            coverage=round(coverage, 2),
            matched=matched,
            missing=missing
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
