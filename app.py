import PyPDF2
import spacy
import streamlit as st

#Extract Text from Resume PDF
def etract_text_from_pdf(file):
    reader=PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text +=page.extract_text()
    return text

nlp = spacy.load("en_core_web_sm")
#Extract Skills from Resume Text
def extract_keywords(text):
    doc = nlp(text)
    keywords = set()
    for token in doc:
        if token.pos_ in ["NOUN","PROPN","VERB"] and not token.is_stop:
            keywords.add(token.text.lower())
    return list(keywords)

#Compare Resume and Job Description
def compare_keywords(resume_keywords, job_description):
    job_keywords = extract_keywords(job_description)
    resume_set = set(resume_keywords)
    job_set = set(job_keywords)

    matched = resume_set.intersection(job_set)
    unmatched_resume = resume_set - job_set
    matched_percentage = (len(matched) / len(job_set)) * 100 if job_set else 0
    return matched_percentage,list(matched), list(unmatched_resume)

st.title("📄 Resume Parser + Job Matcher")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    resume_text = etract_text_from_pdf(uploaded_file)
    resume_keywords = extract_keywords(resume_text)

    st.success(" Resume uploaded and parsed.")

    job_description = st.text_area("Paste the job description here")

    if job_description:
        match_pct, matched, unmatched = compare_keywords(resume_keywords, job_description)

        st.subheader(f"🔍 Match: {match_pct}%")
        st.markdown(" **Keywords you matched:**")
        st.write(", ".join(matched))

        st.markdown(" **Missing keywords you should consider adding:**")
        st.write(", ".join(unmatched))