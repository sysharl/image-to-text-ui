from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from dotenv import load_dotenv
from models import db, thoughts_archive_test
# from prediction import extract_text
import os
from heic2png import HEIC2PNG
from werkzeug.utils import secure_filename
import json
import uuid
from datetime import datetime
from collections import defaultdict

load_dotenv()  # take environment variables from .env

app = Flask(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_heic(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == 'HEIC'


@app.route("/upload", methods=["GET"])
def uploadImageView():
    return render_template("add_quotes.html")


@app.route("/upload-image", methods=["POST"])
def upload_files():
    print(request)
    if 'files' not in request.files:
        return "No file part", 400

    batch_id = datetime.today().strftime('%Y-%m-%d')+"_"+str(uuid.uuid4())[:8]
    batch_dir = os.path.join(app.config['UPLOAD_FOLDER'], batch_id)
    os.makedirs(batch_dir, exist_ok=True)

    files = request.files.getlist('files')  # get multiple files
    saved_files = []

    for file in files:
        if file.filename != "":
            filename = secure_filename(file.filename)

            if is_heic(filename):
                filename = HEIC2PNG(filename)

            filepath = os.path.join(batch_dir, filename)
            file.save(filepath)

            error_text = ""
            extracted_text = ""
            details = {}
            # try:
            #     details, extracted_text = extract_text(filepath,batch_dir)
            # except Exception as e:
            #     error_text =str(e)
            # finally:
            #     saved_files.append({
            #         "image_url": f"{batch_id}/{filename}",
            #         "filename": filename,
            #         "text": extracted_text,
            #         "details": details,
            #         "error": error_text
            #     })

    meta_path = os.path.join(batch_dir, "results.json")
    with open(meta_path, "w", encoding="utf-8") as fp:
        json.dump({"batch_id": batch_id, "saved_files": saved_files},
                  fp, ensure_ascii=False, indent=2)

    return redirect(url_for("review", batch_id=batch_id))


@app.route("/review/<batch_id>", methods=["GET"])
def review(batch_id):
    batch_dir = os.path.join(app.config['UPLOAD_FOLDER'], batch_id)
    meta_path = os.path.join(batch_dir, "results.json")
    if not os.path.exists(batch_dir):
        return "Batch not found", 404
    if not os.path.exists(batch_dir):
        return "Results Json not found", 404
    review_data = []
    with open(meta_path, "r", encoding="utf-8") as fp:
        review_data = json.load(fp)
    return render_template("review.html", batch_id=batch_id, review_data=review_data["saved_files"])


@app.route("/edit/<string:id>", methods=["PATCH"])
def editText(id):
    data = request.get_json()
    quote = thoughts_archive_test.query.get_or_404(id)
    if "author" in data:
        quote.author = data["author"]
    if "title" in data:
        quote.title = data["title"]
    if "quote" in data:
        quote.quote = data["quote"]
    if "category" in data:
        quote.category = data["category"]
    if "actor" in data:
        quote.actor = data["actor"]
    db.session.commit()
    return jsonify({
        "message": "Quote updated successfully",
        "id": quote.id
    })


@app.route("/", methods=["GET"])
def retrieveQuotes():
    quotes = thoughts_archive_test.query.all()
    return render_template("index.html", quotes=quotes)


@app.route("/save/<batch_id>", methods=["POST"])
def save(batch_id):
    quotes_result = defaultdict(lambda: {"edited_text":"","segmented":[]})
    print(request.form.keys())
    for key in request.form.keys():
        full_text_id = ""
        if ("texts_" in key and not "[]" in key):
            full_text_id = key.replace("texts_", "")
            textarea_edited_text = request.form.get("texts_"+full_text_id)
            
            authors = request.form.getlist("segments_"+full_text_id+"_author[]")
            titles = request.form.getlist("segments_"+full_text_id+"_title[]")
            actors = request.form.getlist("segments_"+full_text_id+"_actor[]")
            categories = request.form.getlist("segments_"+full_text_id+"_category[]")
            quotes = request.form.getlist("segments_"+full_text_id+"_quote[]")

            for author, title, actor,category, quote in zip(authors, titles, actors, categories, quotes):
                new_quote = thoughts_archive_test(
                    author=none_if_empty(author),
                    title=none_if_empty(title),
                    actor=none_if_empty(actor),
                    category = none_if_empty(category),
                    quote=quote,
                    image = none_if_empty(request.form.get("file_"+full_text_id))
                )
                
                quotes_result[key]["segmented"].append(new_quote.to_dict())
                db.session.add(new_quote)
                
            quotes_result[key]["edited_text"] = textarea_edited_text 

    batch_dir = os.path.join(app.config['UPLOAD_FOLDER'], batch_id)
    meta_path = os.path.join(batch_dir, "results_segmented.json")
    with open(meta_path, "w", encoding="utf-8") as fp:
        json.dump(quotes_result, fp, ensure_ascii=False, indent=2)
    db.session.commit()

    return "success"

def none_if_empty(value):
    return value if value.strip() else None

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create tables if not exists
    app.run(debug=True)
