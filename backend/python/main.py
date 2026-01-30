from fastapi import FastAPI, UploadFile, File
import shutil, uuid
from extractor import run_ocr

app = FastAPI()

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    temp = f"/tmp/{uuid.uuid4()}_{file.filename}"

    with open(temp, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        return run_ocr(temp)
    except:
        return {
            "student_name": None,
            "register_number": None,
            "programme_or_branch": None,
            "semester": None,
            "gpa": None,
            "cgpa": None,
            "result_status": None,
            "subject_grades": None
        }
    finally:
        file.file.close()