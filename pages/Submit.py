import streamlit as st
#from datetime import datetime
import os
import time

#DATA_FILE = "/mnt/data/doi_entries.txt"   # or any path on your server
current_dir = os.path.dirname(__file__)
uni_path = os.path.join(current_dir, "logo.png")
image_path = os.path.join(current_dir, "logo3.jpeg")
logo_path = os.path.join(current_dir, "logo4.png")
file_path = os.path.join(current_dir, "database3.ttl")

st.set_page_config(
    page_title="Cold Spray Hub",        
    page_icon= logo_path,                  
    layout="centered",                   
    initial_sidebar_state="expanded",
    menu_items = {'About': 'This is a tool desined and provided by ## University of Waterloo ## and ##University of Ottowa##'} 
)

# Optional: Top navigation using st.page_link
left, mid, right = st.columns([9, 1, 1])

with left:
    col1, col2, col3, col4 = st.columns([1.3, 3, 3, 1.5])
    with col1:
        st.page_link("main.py", label= "Database")

    with col2:
        st.page_link("pages/Calculator.py", label="Critical Velocity Calculator")
    
    with col3:
        st.page_link("pages/ParticleVelocity.py", label="Particle Velocity Calculator")

    with col4:
        st.page_link("pages/Submit.py", label="Your Contribution")

st.markdown("""
    <style>
    .title-font {
        font-family: 'Lato', sans-serif;
        font-size: 48px;
        font-weight: 400;
        margin-bottom: 0px;
        color: #2c3e50;
    }
    .subtitle-font {
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        font-weight: 200;
        margin-top: -20px;
        color: #2c3e50;
    }
    </style>
            
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    }

    </style>

""", unsafe_allow_html=True)
st.image(uni_path, width=600, output_format="auto")

DATA_FILE = current_dir + "/doi_entries.txt"

st.divider()
st.markdown("If you find a paper related to cold spray technology that is not included in the database, you can add its DOI in the box below to contribute to the Cold Spray Hub. This paper will be included in the next update.")
st.title("Submit a Paper DOI")

# Initialize session state for the text input
if "doi_input" not in st.session_state:
    st.session_state.doi_input = ""

# Text input linked to session state
doi = st.text_input("Enter DOI", key="doi_input")



def save_doi():

    doi_value = st.session_state.doi_input.strip()

    if not doi_value:
        st.warning("Please enter a DOI before saving.")
        return
    
    # Create directory if needed
    #os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # Append each new DOI to the file
    with open(DATA_FILE, "a") as f:
        #timestamp = datetime.utcnow().isoformat()
        #f.write(f"{doi_text} | {timestamp}\n")
        # If you want ONLY the DOI with no timestamp, use:
        f.write(doi_value + "\n")

    #st.success(f"DOI is saved. Thank you for contributing to the Cold Spray Hub!")
        # Create a placeholder for the success message
    msg = st.empty()
    msg.success(f"DOI is saved. Thank you for contributing to the Cold Spray Hub!")

    # Wait 3 seconds, then clear the message
    time.sleep(3)
    msg.empty()

    # Clear the text box
    st.session_state.doi_input = ""



st.button("Submit DOI", on_click=save_doi)


