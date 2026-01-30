from paddleocr import PaddleOCR
import re

ocr = PaddleOCR(use_angle_cls=True, lang="en")

def normalize(text: str):
    text = text.replace("(", " ").replace(")", " ")
    return re.sub(r"\s+", " ", text)

def extract_fields(text: str):
    text = normalize(text)

    def find(pattern):
        m = re.search(pattern, text, re.I)
        return m.group(1).strip() if m else None

    subjects_raw = re.findall(
        r"([A-Z][A-Z &]+)\s+\d+\s+\d+\s+([A-Z+]+)",
        text
    )

    subject_grades = (
        [{"subject": s.strip(), "grade": g} for s, g in subjects_raw]
        if subjects_raw else None
    )

    result_status = None
    if subject_grades:
        result_status = "PASS"
        for s in subject_grades:
            if s["grade"] in ["RA", "FAIL"]:
                result_status = "FAIL"
                break

    gpa = find(r"GPA[^0-9]*([\d]+\.\d+)")
    cgpa = find(r"CGPA[^0-9]*([\d]+\.\d+)")

    return {
        "student_name": find(r"Name\s+of\s+the\s+Candidate\s+([A-Z ]+)"),
        "register_number": find(r"Register\s*No\s*([A-Z0-9]+)"),
        "programme_or_branch": find(r"Programme\s*/\s*Branch\s+([A-Z .]+)"),
        "semester": find(r"(FIRST|SECOND|THIRD|FOURTH)\s+SEMESTER"),
        "gpa": float(gpa) if gpa else None,
        "cgpa": float(cgpa) if cgpa else None,
        "result_status": result_status,
        "subject_grades": subject_grades
    }

def run_ocr(path: str):
    print(">>> OCR FUNCTION ENTERED <<<", path)

    result = ocr.ocr(path)
    print("RAW OCR RESULT:", result)

    text = "\n".join([line[1][0] for page in result for line in page])

    print("==== OCR RAW TEXT START ====")
    print(text)
    print("==== OCR RAW TEXT END ====")

    return extract_fields(text)
