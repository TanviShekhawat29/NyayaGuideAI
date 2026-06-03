# ⚖️ NyayaGuide AI

An AI-powered legal document assistant that helps users understand complex legal documents through OCR, Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs).

NyayaGuide AI extracts text from legal PDFs and images, identifies important legal information, assesses potential risk levels, and provides simplified legal guidance in an easy-to-understand format.

---

## 🌐 Live Demo

**Application URL:**
https://nyayaguide-321717617708.asia-south1.run.app

---

## 📌 Problem Statement

Legal documents often contain complex terminology and lengthy content that can be difficult for non-legal users to understand.

NyayaGuide AI aims to bridge this gap by:

* Extracting text from legal documents
* Identifying key legal entities and information
* Assessing legal risk indicators
* Providing simplified explanations using AI
* Generating actionable guidance for users

---

## 🚀 Features

### 📄 OCR-Based Document Processing

* Supports PDF and image uploads
* Extracts text using Tesseract OCR
* Handles scanned legal documents

### 🧠 AI-Powered Legal Assistance

* Uses LLaMA 3.3 70B via Groq API
* Generates contextual legal explanations
* Simplifies complex legal language

### 🔍 Information Extraction

* Detects:

  * Legal Sections
  * Important Dates
  * Person Names

### ⚠ Risk Assessment

Automatically classifies documents into:

* 🔴 High Risk
* 🟡 Medium Risk
* 🟢 Low Risk

based on detected legal indicators.

### 📋 Actionable Recommendations

Provides practical next steps such as:

* Reviewing legal sections
* Attending legal proceedings
* Consulting legal professionals
* Preparing supporting documents

### 🔐 Privacy-Oriented Design

* Documents are processed temporarily
* Uploaded files are deleted after processing
* No permanent storage of user documents

---

## 🏗 System Architecture

User Upload
↓
OCR Processing (Tesseract + OpenCV)
↓
Text Cleaning & Preprocessing
↓
Document Chunking
↓
RAG Processing
↓
LLM (Groq - LLaMA 3.3 70B)
↓
Legal Insights & Recommendations

---

## 🛠 Technology Stack

### Backend

* FastAPI
* Python 3.10

### OCR & Image Processing

* Tesseract OCR
* OpenCV
* PDF2Image
* NumPy
* Pillow

### AI & NLP

* Retrieval-Augmented Generation (RAG)
* LLaMA 3.3 70B
* Groq API

### Deployment

* Docker
* Google Cloud Run

---

## 📂 Project Structure

```text
NyayaGuide-AI/
│
├── main.py
├── ocr.py
├── rag_engine.py
├── llm_engine.py
├── chunking.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## ⚙️ Installation

### Clone Repository

```bash
git clone 
cd nyayaguide-ai
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## 🐳 Docker Deployment

Build Image:

```bash
docker build -t nyayaguide-ai .
```

Run Container:

```bash
docker run -p 8080:8080 nyayaguide-ai
```

---

## 📊 Workflow

### Step 1

User uploads a legal document.

### Step 2

OCR extracts text from the uploaded document.

### Step 3

Text is cleaned and divided into chunks.

### Step 4

RAG engine processes the extracted content.

### Step 5

The LLM generates a context-aware response.

### Step 6

The system presents:

* Legal explanation
* Key legal entities
* Risk level
* Recommended actions

---

## 👥 Team Contributions

### Hansika

* RAG Engine Development
* Entity Extraction
* Risk Detection System
* Action Recommendation Logic
* Response Generation Pipeline

### Tanvi

* OCR Pipeline Development
* Image Preprocessing
* PDF Processing Workflow
* LLM Integration using Groq API
* Text Extraction Optimization

### Tanishka

* Project Research
* Documentation
* Testing & Validation
* System Analysis
* Deployment Support

---

## 🔮 Future Enhancements

* Legal-BERT integration
* Semantic vector search
* FAISS-based retrieval
* Multi-language legal support
* Case law recommendation engine
* Local LLM deployment for enhanced privacy
* Advanced Named Entity Recognition (NER)

---

## ⚠ Disclaimer

NyayaGuide AI is an educational and research project developed for academic purposes.

The system does not replace professional legal advice. Users should consult qualified legal professionals before making legal decisions.

---

## 📜 License

This project is developed for educational and academic use.
