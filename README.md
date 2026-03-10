# Image to Text UI
A personal project I built to **digitize my handwritten quotes into editable digital text using OCR**.

I often write down quotes, ideas, and reflections by hand in a notebook. Over time, I wanted a way to **convert these notes into digital text** that I could store, search, and reuse easily. This project provides a lightweight **Image-to-Text interface** that allows images of handwritten notes to be uploaded and processed into readable text.

This project also allowed me to explore **OCR integration, image processing, and building a simple yet functional user interface** for a practical personal workflow.


## Project MotivationS

I keep a notebook where I write:

- Quotes that inspire me
- Personal reflections
- Notes from books or articles

Instead of manually typing everything into a digital format, I decided to build a tool that can:

1. Take an image of handwritten notes  
2. Extract the text using OCR  
3. Convert it into digital text that can be copied, stored, or reused  

This repository contains the UI and logic that powers that workflow.


## Screenshot / Demo

Example of handwritten notes being converted into digital text.



## Features

- Upload images containing handwritten text  
- Auto crop the document by line
- Extract text from images using OCR  
- Display recognized text in a simple, clean interface  
- Able to edit the extracted text for accuracy and future training
- Save to a database
- Lightweight and easy to run locally  


## Tech Stack

This project demonstrates experience with:

**Frontend**
- HTML
- CSS
- JavaScript

**Backend / Processing**
- Python
- Flask
- SQLAlchemy
- TrOCR (Transformers)
- OpenCV

**Tools**
- Git / GitHub



## Installation & Run

Follow these steps to set up and run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/sysharl/image-to-text-ui.git
cd image-to-text-ui
```

### 2. Install dependencies

Make sure you have Python 3.10+ installed, then run:
```
pip install -r requirements.txt
```

### 3. Set environment variables
Using a .env file (recommended)

Fill in the required values:
```
FLASK_APP=app.py
FLASK_ENV=development
DB_USER=your_db_username
DB_PASS=your_db_password
DB_HOST=localhost
DB_NAME=your_database_name
```
### 4. Run the Flask app

Option 1: Using Flask CLI
```
flask run
```
Option 2: Directly with Python
```
python app.py
```

The app will run at:

http://127.0.0.1:5000/

Open this URL in your browser to access the UI, upload handwritten notes, and see the extracted text.



## Project Structure
```
image-to-text-ui
│
├── app.py # Main application logic and server
├── models.py # Model definitions for OCR / text extraction
├── prediction.py # Image processing and prediction functions
├── sample.html # Sample HTML for testing or demo
├── static/ # CSS, JS, and other static assets
├── templates/ # HTML templates for UI
└── to_decode/ # Folder for images to be processed
```

## What I Learned
Through this project, I gained hands-on experience in the **full data lifecycle**:

1. **Data Collection** – I personally gathered my own handwritten notes and quotes as the raw dataset.  
2. **Data Labeling / Preprocessing** – Labeled the text manually to create training examples and preprocessed the images for better OCR accuracy.  
3. **Model/Tool Training** – Experimented with OCR tools to improve recognition of my handwriting.  
4. **Application Integration** – Built a simple interface to upload images and display extracted text.  
5. **Iteration** – Tested the system, refined preprocessing, and improved accuracy over time.  

This project helped me understand **how data flows from collection to actionable output**, and how small-scale personal projects can mimic professional data workflows.


## Possible Improvements

Better line by line cropping of document image page

Batch processing for multiple images

Faster model to extract text

Deploying the application online