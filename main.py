import streamlit as st
import openai
import pandas as pd
from docx import Document
from io import BytesIO
from utils import extract_paragraphs, process_paragraphs_with_gpt, insert_titles_to_docx

st.set_page_config(page_title="كشافات شيخ الإسلام")

if 'processed_docx' not in st.session_state:
    st.session_state.processed_docx = None
if 'excel_output' not in st.session_state:
    st.session_state.excel_output = None

st.title("📚 استخراج وتمييز الكشافات العلمية من كتب شيخ الإسلام ابن تيمية")

openai_key = st.text_input("🔐 أدخل مفتاح OpenAI الخاص بك", type="password")
model_choice = st.selectbox("🧠 اختر نموذج OpenAI", ["gpt-4", "gpt-3.5-turbo"])
uploaded_file = st.file_uploader("📄 ارفع ملف وورد يحتوي على النص", type=["docx"])

if st.button("⚙️ تنفيذ التحليل") and uploaded_file and openai_key:
    openai.api_key = openai_key

    # استخراج النصوص
    paragraphs = extract_paragraphs(uploaded_file)

    # معالجة الفقرات
    processed_results = process_paragraphs_with_gpt(paragraphs, model_choice, api_key=openai_key)

 #   processed_results = process_paragraphs_with_gpt(paragraphs, model_choice)

    # إنشاء ملف وورد جديد
    modified_doc = insert_titles_to_docx(paragraphs, processed_results)

    # حفظ ملف وورد في الذاكرة
    word_io = BytesIO()
    modified_doc.save(word_io)
    st.session_state.processed_docx = word_io

    # إنشاء ملف إكسل
    df = pd.DataFrame(processed_results)
    excel_io = BytesIO()
    df.to_excel(excel_io, index=False)
    st.session_state.excel_output = excel_io

    st.success("✅ تم التحليل بنجاح! يمكنك الآن تحميل النتائج.")

# زر تنزيل ملف وورد
if st.session_state.processed_docx:
    st.download_button("📥 تحميل ملف وورد المعدّل", data=st.session_state.processed_docx.getvalue(),
                       file_name="processed.docx")

# زر تنزيل ملف إكسل
if st.session_state.excel_output:
    st.download_button("📥 تحميل ملف الكشافات (Excel)", data=st.session_state.excel_output.getvalue(),
                       file_name="kashafaat.xlsx")
