from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

rag_instance = None


# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>NyayaGuide AI</title>
            <style>
                body {
                    background: linear-gradient(to right, #1e3c72, #2a5298);
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .card {
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                    width: 520px;
                    text-align: center;
                }
                input {
                    width: 90%;
                    padding: 10px;
                    margin-top: 10px;
                    border-radius: 6px;
                    border: 1px solid #ccc;
                }
                button {
                    padding: 10px 20px;
                    margin-top: 15px;
                    border: none;
                    background-color: #2a5298;
                    color: white;
                    border-radius: 6px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #1e3c72;
                }
                h2 {
                    margin-bottom: 10px;
                }
                .section {
                    margin-top: 20px;
                }
                footer {
                    margin-top: 10px;
                    font-size: 12px;
                    color: gray;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>⚖ NyayaGuide AI</h2>

                <div class="section">
                    <h3>Upload Legal Document</h3>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="file" required>
                        <br>
                        <button type="submit">Upload</button>
                    </form>
                </div>

                <div class="section">
                    <h3>Ask a Question</h3>
                    <form action="/ask" method="post">
                        <input type="text" name="question" placeholder="Enter your legal question..." required>
                        <br>
                        <button type="submit">Ask</button>
                    </form>
                </div>

                <footer>AI-powered Legal Assistant with Privacy Protection</footer>
            </div>
        </body>
    </html>
    """


# ---------------- UPLOAD ----------------
@app.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile = File(...)):
    global rag_instance
    try:
        from ocr import extract_text
        from chunking import chunk_text
        from rag_engine import RAGEngine

        content = await file.read()
        path = file.filename

        with open(path, "wb") as f:
            f.write(content)

        text = extract_text(path)

        if "OCR ERROR" in text:
            return f"<h3>{text}</h3><br><a href='/'>Go Back</a>"

        chunks = chunk_text(text)

        rag_instance = RAGEngine()
        rag_instance.add_documents(chunks)

        os.remove(path)

        return """
        <html>
            <body style="font-family: Arial; text-align:center; padding:50px;">
                <h2>✅ Document Processed Successfully</h2>
                <a href="/">Go Back</a>
            </body>
        </html>
        """

    except Exception as e:
        return f"<h3>❌ Upload Error: {str(e)}</h3>"


# ---------------- ASK ----------------
@app.post("/ask", response_class=HTMLResponse)
def ask(question: str = Form(...)):
    global rag_instance
    try:
        if rag_instance is None:
            return "<h3>⚠ Upload a document first</h3>"

        result = rag_instance.search(question)

        actions_html = "".join([f"<li>{a}</li>" for a in result["actions"]])

        return f"""
        <html>
        <body style="font-family: Arial; background:#f5f7fa; padding:40px;">

        <div style="background:white; padding:30px; border-radius:10px; max-width:750px; margin:auto; box-shadow:0 5px 15px rgba(0,0,0,0.1);">

            <h2 style="text-align:center;">⚖ NyayaGuide AI</h2>

            <h3>Question:</h3>
            <p>{result["question"]}</p>

            <h3>Answer:</h3>
            <div style="background:#eef3ff; padding:10px; border-radius:6px;">
                <p>{result["answer"]}</p>
            </div>

            <h3>📌 Key Legal Information:</h3>
            <ul>
                <li>{result["top_3_sections"][0]}</li>
                <li>{result["top_3_sections"][1]}</li>
                <li>{result["top_3_sections"][2]}</li>
            </ul>

            <h3>⚠ Risk Level:</h3>
            <p><b>{result["risk"]}</b></p>

            <h3>📋 What You Should Do:</h3>
            <ul>
                {actions_html}
            </ul>

            <p><i>{result["confidence"]}</i></p>

            <a href="/" style="display:block; text-align:center; margin-top:20px;">Ask another question</a>

        </div>

        </body>
        </html>
        """

    except Exception as e:
        return f"<h3>❌ Ask Error: {str(e)}</h3>"