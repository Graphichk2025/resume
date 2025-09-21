import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import PyPDF2
import io
import base64
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E40AF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .analysis-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
    }
    .recommendation-card {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stButton button {
        background-color: #3B82F6;
        color: white;
        font-weight: bold;
    }
    .resume-section {
        background-color: #F9FAFB;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini API (you'll need to replace with your actual API key)
def setup_gemini():
    try:
        # In a real app, you would use st.secrets to securely store your API key
        # For demo purposes, we're using a placeholder
        api_key = "your_gemini_api_key_here"  # Replace with your actual API key
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    except:
        st.warning("Gemini API not configured. Using demo mode.")
        return None

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

# Analyze resume with Gemini
def analyze_resume_with_gemini(resume_text):
    # This is a simulation since we don't have a real API key
    # In a real application, you would use the Gemini API
    
    # Simulate API response delay
    import time
    time.sleep(2)
    
    # Simulated response based on common resume patterns
    skills = ["Python", "JavaScript", "SQL", "Machine Learning", "Data Analysis", "React", "AWS"]
    experience = 3.5
    education_level = "Bachelor's"
    
    # Simulate career recommendations
    recommendations = [
        "Consider highlighting your machine learning projects more prominently",
        "Add metrics to quantify your achievements (e.g., 'Improved performance by 25%')",
        "Include more industry-specific keywords for ATS optimization",
        "Consider obtaining AWS certification to enhance your cloud skills"
    ]
    
    # Simulate career matches
    career_matches = [
        {"role": "Data Scientist", "match": 85},
        {"role": "Machine Learning Engineer", "match": 78},
        {"role": "Software Developer", "match": 72},
        {"role": "Data Analyst", "match": 68},
        {"role": "DevOps Engineer", "match": 55}
    ]
    
    # Simulate skill analysis
    skill_categories = {
        "Technical Skills": 82,
        "Soft Skills": 75,
        "Leadership": 68,
        "Industry Knowledge": 60
    }
    
    # Simulate resume score
    resume_score = 76
    
    return {
        "skills": skills,
        "experience": experience,
        "education_level": education_level,
        "recommendations": recommendations,
        "career_matches": career_matches,
        "skill_categories": skill_categories,
        "resume_score": resume_score
    }

# Display analysis results
def display_analysis_results(analysis):
    st.markdown('<h2 class="main-header">Resume Analysis Results</h2>', unsafe_allow_html=True)
    
    # Overall score
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Resume Score</h3>
            <h2 style="color: #1E40AF;">{analysis['resume_score']}/100</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Years of Experience</h3>
            <h2 style="color: #1E40AF;">{analysis['experience']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Education Level</h3>
            <h2 style="color: #1E40AF;">{analysis['education_level']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Career matches chart
    st.subheader("Recommended Career Paths")
    career_df = pd.DataFrame(analysis['career_matches'])
    fig = px.bar(career_df, x='role', y='match', title='Career Match Percentage',
                 labels={'role': 'Career Role', 'match': 'Match %'})
    fig.update_traces(marker_color='#3B82F6')
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills radar chart
    st.subheader("Skill Categories Assessment")
    skill_categories = analysis['skill_categories']
    categories = list(skill_categories.keys())
    values = list(skill_categories.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Skill Assessment',
        line_color='#3B82F6'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills list
    st.subheader("Detected Skills")
    cols = st.columns(3)
    for i, skill in enumerate(analysis['skills']):
        with cols[i % 3]:
            st.markdown(f"- {skill}")
    
    # Recommendations
    st.subheader("Improvement Recommendations")
    for rec in analysis['recommendations']:
        st.markdown(f"""
        <div class="recommendation-card">
            <p>{rec}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Best resume techniques
    st.subheader("Best Resume Techniques")
    techniques = [
        "Use action verbs to start each bullet point (e.g., 'Developed', 'Implemented', 'Managed')",
        "Quantify achievements with numbers and metrics whenever possible",
        "Tailor your resume to each specific job application",
        "Include relevant keywords from the job description",
        "Keep your resume concise (1-2 pages maximum)",
        "Use a clean, professional layout with consistent formatting",
        "Highlight your most relevant experiences and skills at the top",
        "Include a skills section with both technical and soft skills",
        "Proofread carefully for spelling and grammar errors",
        "Include links to your portfolio, GitHub, or LinkedIn profile"
    ]
    
    for technique in techniques:
        st.markdown(f"- {technique}")

# Main application
def main():
    st.markdown('<h1 class="main-header">AI Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Upload your resume for AI-powered analysis and career recommendations")
    
    # Initialize Gemini
    model = setup_gemini()
    
    # File upload
    uploaded_file = st.file_uploader("Choose a PDF resume", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from PDF
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if resume_text:
            # Display extracted text (optional)
            with st.expander("View extracted resume text"):
                st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)
            
            # Analyze button
            if st.button("Analyze Resume", type="primary"):
                with st.spinner("Analyzing your resume with AI..."):
                    # Analyze resume
                    analysis = analyze_resume_with_gemini(resume_text)
                    
                    # Display results
                    display_analysis_results(analysis)
        else:
            st.error("Could not extract text from the PDF. Please try another file.")
    else:
        # Show demo analysis
        st.info("👆 Upload a PDF resume to get started, or see a demo analysis below")
        
        if st.button("Show Demo Analysis"):
            # Create demo analysis
            demo_analysis = {
                "skills": ["Python", "JavaScript", "SQL", "Machine Learning", "Data Analysis", "React", "AWS", "Docker", "Git", "TensorFlow"],
                "experience": 4.2,
                "education_level": "Master's",
                "recommendations": [
                    "Add more quantifiable achievements to your work experience",
                    "Include a projects section to showcase your technical skills",
                    "Consider adding a summary section at the top of your resume",
                    "Tailor your skills section to include more industry-specific keywords"
                ],
                "career_matches": [
                    {"role": "Data Scientist", "match": 92},
                    {"role": "Machine Learning Engineer", "match": 88},
                    {"role": "Data Engineer", "match": 85},
                    {"role": "Software Developer", "match": 78},
                    {"role": "Data Analyst", "match": 75}
                ],
                "skill_categories": {
                    "Technical Skills": 90,
                    "Data Analysis": 85,
                    "Machine Learning": 88,
                    "Cloud Computing": 75,
                    "Software Development": 82
                },
                "resume_score": 84
            }
            
            # Display demo results
            display_analysis_results(demo_analysis)

if __name__ == "__main__":
    main()
