
import openai
import os
import streamlit as st

# Load environment variables

  # This is optional if you're setting the API key through platform secrets
openai.api_key = os.getenv("OPENAI_API_KEY")  # Access API key from environment

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
        /* Footer styling */
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #555;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar with navigation buttons
st.sidebar.title("Quick Links")
if st.sidebar.button("Bentley Health Portal"):
    st.sidebar.markdown(
        '<a href="https://bentley.medicatconnect.com/home.aspx" target="_blank">Go to Bentley Health Portal</a>',
        unsafe_allow_html=True
    )
if st.sidebar.button("Make an Appointment with Health Center"):
    st.sidebar.markdown(
        '<a href= "https://bentley.medicatconnect.com/appointment.aspx" target="_blank">Schedule Health Center Appointment</a>',
        unsafe_allow_html=True
    )
if st.sidebar.button("Visit Wellness Center"):
    st.sidebar.markdown(
        '<a href="https://www.bentley.edu/university-life/student-health/counseling-center" target="_blank">Go to Counseling Center</a>',
        unsafe_allow_html=True
    )

# Center the image using st.image with custom CSS
st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
st.image("logo3.jpg", width=200, caption="Medical Diagnosis Logo")
st.markdown('</div>', unsafe_allow_html=True)

# App Title and Instructions
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="header">FalconCheck</div>', unsafe_allow_html=True)
st.write("Enter your symptoms or health concerns and press Enter for a preliminary diagnosis.")

# Input for symptoms or health concerns
symptoms_input = st.text_input("Please describe your symptoms or concerns:")


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
                    "Bentley University’s campus is organized into distinct zones with academic, administrative, residential, and recreational buildings, all connected by main roads and pathways. The Main Entrance on Forest Street is the primary entry point, leading visitors directly to several key buildings, including LaCava Center (1), an administrative hub, and Bentley Library (2). Close by, Morison Hall (4) and Lindsay Hall (5) are important academic buildings located near the entrance. Continuing into the campus, the core academic area includes Adamian Academic Center (6), Smith Academic Technology Center (7), and Jennison Hall (8), which are centrally located and close to one another, providing convenient access to educational resources. Adjacent to this academic cluster are Rauch Administration Center (9) and Falcone Complex (10), which provide additional administrative support."
                    "The Student Center and Residential Center (19) is a hub for student life, located near Rhodes Hall (18), which serves as Health Services, and is accessible from both Forest Street and Falcon Way. Surrounding residential buildings, such as Orchard North Apartments (20), Orchard South Apartments (21), The Trees (10), and Boylston Apartments (13), are positioned to facilitate easy access to student services and social areas. Collins Hall (15), near Falcon Way, houses the Bentley Bookstore, making it a central location for student supplies. Miller Hall (16), Slade Hall (11), and Forest Hall (17) are also among the residential buildings distributed around the campus, providing convenient accommodations for students."
                    "For dining and social interactions, The Castle (22) and The Cape (23) are notable gathering places near residential areas, fostering a community atmosphere. The campus wellness and safety facilities include University Police and Counseling Center (12), ensuring student safety, and the Wellness Center near the Bentley Police Station. At the eastern end of the campus, the Dana Athletic Center (29) and nearby athletic fields serve as the main facilities for sports and recreation. Additional buildings, like Lewis Hall (30), Fenway (26), and Dovecote (27), contribute to campus life. Parking areas are conveniently placed around the campus perimeter, while North Campus Apartments (34), located separately across Forest Street, offer additional residential options."
                    ""

                )
            },
            {"role": "user", "content": symptoms}
        ]
    )
    return response['choices'][0]['message']['content'].strip()


# Function to check if diagnosis indicates a campus location
def contains_location_reference(text):
    campus_locations = [
    "Wellness Center",                # Near Bentley Police Station
    "Health Center",                  # Located in Rhodes Hall (Building 18)
    "Rhodes Hall",                    # Building 18
    "Collins Hall",                   # Building 15
    "Falcon Market",                  # Inside Collins Hall
    "Bentley Police Station",         # Near Rhodes Hall
    "Student Center",                 # Building 19
    "LaCava Center",                  # Building 1
    "Bentley Library",                # Building 2
    "Morison Hall",                   # Building 4
    "Lindsay Hall",                   # Building 5
    "Adamian Academic Center",        # Building 6
    "Smith Academic Technology Center", # Building 7
    "Jennison Hall",                  # Building 8
    "Rauch Administration Center",    # Building 9
    "Falcone Complex",                # Building 10
    "The Trees",                      # Building 10
    "Boylston Apartments",            # Building 13
    "Miller Hall",                    # Building 16
    "Slade Hall",                     # Building 11
    "Forest Hall",                    # Building 17
    "Orchard North Apartments",       # Building 20
    "Orchard South Apartments",       # Building 21
    "Kresge Hall",                    # Building 14
    "The Castle",                     # Building 22
    "The Cape",                       # Building 23
    "Dana Athletic Center",           # Building 29
    "North Campus Apartments",        # Building 34
    "Fenway",                         # Building 26
    "Dovecote",                       # Building 27
    "Lewis Hall",                     # Building 30
    "Baseball Fields",                # East of Dana Athletic Center
    "Softball Fields",                # Near Baseball Fields
    "North Campus Residence Halls",  # General area near Building 34
    "Parking Lot A",                  # Near Main Entrance
    "Parking Lot B",                  # Near Jennison Hall
    "Parking Lot C",                  # Near Dana Athletic Center
    "Parking Lot D",                  # Near North Campus Apartments
    "Parking Lot E"                   # Behind Orchard Apartments
]


    return any(location in text for location in campus_locations)


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

                # Check if the diagnosis contains any campus location references
                if contains_location_reference(diagnosis):
                    st.write(
                        "Since this recommendation includes a specific campus location, here’s a map for your reference:")
                    st.image("bentleyMap.jpg", caption="Bentley University Campus Map")

                # Display a link to the Wellness Center if mental health support is suggested
                if "Wellness Center" in diagnosis:
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

# Footer with professional disclaimer
st.markdown(
    """
    <div class="footer">
        
        <p>**Disclaimer:** This application provides general information based on AI-generated responses and is not a substitute for professional medical advice. Please consult a healthcare provider for personal medical guidance.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Close the main container div
st.markdown('</div>', unsafe_allow_html=True)



