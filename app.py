import streamlit as st
import openai
import pdfplumber
import docx
import os

# Load OpenAI API key from Hugging Face Secrets
from openai import OpenAI

client = OpenAI()  # Initializes OpenAI client

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to analyze resume
def analyze_resume(resume_text, job_description):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional job application assistant. Analyze resumes for strengths, weaknesses, and keyword optimization."},
            {"role": "user", "content": f"Analyze this resume:\n{resume_text}\n\nFor this job description:\n{job_description}\n\nProvide improvements, missing skills, and keyword suggestions."}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Function to generate a cover letter
def generate_cover_letter(resume_text, job_description):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in writing professional and tailored cover letters."},
            {"role": "user", "content": f"Write a compelling cover letter using this resume:\n{resume_text}\n\nFor the job description:\n{job_description}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Function to analyze LinkedIn profile
def analyze_linkedin_profile(profile_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in LinkedIn profile optimization."},
            {"role": "user", "content": f"Analyze this LinkedIn profile:\n{profile_text}\n\nProvide suggestions for better visibility, keyword optimization, and professionalism."}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("🚀 AI-Powered Job Application Assistant")
st.write("Upload your resume, paste your job description, or enter your LinkedIn profile to get AI-powered insights!")

# File uploader for resume
uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_description = st.text_area("📝 Paste the job description here")

# LinkedIn Profile Analysis
linkedin_profile = st.text_area("🔗 Paste your LinkedIn profile content (optional)")

if uploaded_file is not None and job_description:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("❌ Unsupported file format")
        resume_text = ""

    if resume_text:
        # Resume Analysis
        st.subheader("📊 Resume Analysis & Optimization")
        analysis = analyze_resume(resume_text, job_description)
        st.write(analysis)

        # Cover Letter Generation
        st.subheader("✍️ Generated Cover Letter")
        cover_letter = generate_cover_letter(resume_text, job_description)
        st.write(cover_letter)
    else:
        st.error("⚠️ Could not extract text from the uploaded file.")

if linkedin_profile:
    st.subheader("🔍 LinkedIn Profile Analysis")
    linkedin_analysis = analyze_linkedin_profile(linkedin_profile)
    st.write(linkedin_analysis)
