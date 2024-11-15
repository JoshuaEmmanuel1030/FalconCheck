import os
from dotenv import load_dotenv
import openai
import streamlit as st

# Load environment variables
load_dotenv()  # This is optional if you're setting the API key through platform secrets
openai.api_key = os.getenv('OPENAI_API_KEY')  # Access API key from environment

# Custom CSS for styling, including button transition
st.markdown("""
    <style>
        body {
            background-color: #FFFFFF !important;
            color: #333;
        }
        .main-container {
            max-width: 700px;
            margin: auto;
            padding: 20px;
            border-radius: 8px;
        }
        .header {
            font-size: 2.2em;
            font-weight: bold;
            color: #004aad;
            text-align: center;
            margin-bottom: 20px;
        }
        .stTextInput > div > input {
            border: 2px solid #004aad;
            border-radius: 8px;
            padding: 8px;
            font-size: 1em;
        }
        .result-box {
            background-color: #f1f8ff;
            padding: 20px;
            margin-top: 20px;
            border-radius: 8px;
            border-left: 5px solid #004aad;
            font-size: 1em;
            color: #333;
        }
        .redirect-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 1.1em;
            color: #004aad;
            background-color: white;
            text-align: center;
            text-decoration: none;
            border: 2px solid #004aad;
            border-radius: 8px;
            margin-top: 20px;
            transition: background-color 0.3s ease;
        }
        .redirect-button:hover {
            background-color: #004aad;
            color: white;
            text-decoration: none; /* Removes underline on hover */
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar (you can add more content here later)
st.sidebar.title("Sidebar")
st.sidebar.write("This is the sidebar content placeholder.")

# Center the image using st.image with custom CSS
st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
st.image("logo2.png", width=200, caption="Medical Diagnosis Logo")
st.markdown('</div>', unsafe_allow_html=True)

# App Title and Instructions
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="header">Medical Diagnosis Assistant</div>', unsafe_allow_html=True)
st.write("Enter your symptoms or health concerns and press Enter for a preliminary diagnosis.")

# Input for symptoms or health concerns
symptoms_input = st.text_input("Please describe your symptoms or health concerns:")

# Function to call OpenAI API for diagnosis
def get_diagnosis(symptoms):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medical assistant trained to provide preliminary diagnoses based on symptoms and health concerns provided by the user. "
                    "For each diagnosis, provide possible causes and next steps, including recommendations to consult a healthcare professional if necessary. "
                    "Also include concise bullet points on how the patient should: Recover, what possible medicines to take, and what foods to eat. "
                    "When recommending a healthcare professional, refer them to the health center at Rhodes Hall. If they need to get Tylenol, ibuprofen, or something equivalent, suggest they buy it "
                    "from the Falcon Market under Collins Hall. "
                    "You should also act as a makeshift therapist if the situation requires it. If it seems that the symptoms the user describes are related to mental health issues, suggest they visit "
                    "the wellness center near the Bentley Police Station."
                )
            },
            {"role": "user", "content": symptoms}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to check if diagnosis indicates a need for mental health support
def needs_mental_health_support(diagnosis_text):
    # Keywords that might indicate a need for mental health support
    mental_health_keywords = ["anxiety", "depression", "mental health", "stress", "nervous", "panic", "therapy", "counseling"]
    return any(keyword in diagnosis_text.lower() for keyword in mental_health_keywords)

# Automatically run the diagnosis if symptoms are entered
if symptoms_input:
    with st.spinner("Analyzing symptoms..."):
        try:
            diagnosis = get_diagnosis(symptoms_input)
            if diagnosis:  # Only display result box if there is a diagnosis
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write("## Preliminary Diagnosis")
                st.write(diagnosis)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Check if the diagnosis indicates a need for mental health support
                if needs_mental_health_support(diagnosis):
                    # Directly display a styled button that links to the wellness center
                    st.markdown(
                        """
                        <a href="https://www.bentley.edu/university-life/student-health/health-center" target="_blank" class="redirect-button">
                            Visit the Wellness Center
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Close the main container div
st.markdown('</div>', unsafe_allow_html=True)
