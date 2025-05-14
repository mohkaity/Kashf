from docx import Document
import openai
from prompts import get_prompt
import re

def extract_paragraphs(uploaded_file):
    doc = Document(uploaded_file)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return paragraphs

def process_paragraphs_with_gpt(paragraphs, model="gpt-4"):
    results = []
    for i, para in enumerate(paragraphs):
        prompt = get_prompt(para)
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي ومتمكن في فهم وتحليل النصوص الشرعية بدقة."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            reply = response['choices'][0]['message']['content'].strip()

            match = re.match(r"<(/?\d+/.*)>", reply)
            if match:
                title_tag = match.group(0)
                results.append({
                    "الفقرة رقم": i + 1,
                    "الكشاف": title_tag,
                    "النص": para
                })

        except Exception as e:
            results.append({
                "الفقرة رقم": i + 1,
                "الكشاف": "خطأ: " + str(e),
                "النص": para
            })

    return results

def insert_titles_to_docx(paragraphs, results):
    doc = Document()
    result_dict = {res["النص"]: res["الكشاف"] for res in results if "الكشاف" in res}

    for para in paragraphs:
        if para in result_dict:
            doc.add_paragraph(result_dict[para], style='Normal').bold = True
        doc.add_paragraph(para)

    return doc
