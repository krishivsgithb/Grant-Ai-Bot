import streamlit as st
from google import genai

st.set_page_config(page_title="Startup Grant Finder AI", page_icon="", layout="centered")


st.title("AI Startup Grant Finder")
st.write("Enter your startup idea to get recommendations for  grants, schemes, and incubators.")


api_key = st.secrets["GEMINI_API_KEY"]

# Inputs
idea = st.text_area("Describe your startup idea:", placeholder="e.g., An AI-driven device for automated soil health analysis...")
stage = st.selectbox("Current Stage:", ["Idea / Prototype", "Early Traction", "Scaling"])
location = st.text_input("Target Location / Country:", value="India")
state = st.selectbox("State:", ["Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"])
if st.button("Find Eligible Grants"):
    if not idea:
        st.warning("Please enter your startup idea first.")
    else:
        with st.spinner("Analyzing startup concept..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                You are an expert startup consultant specializing in government grants, schemes, and non-dilutive funding.
                
                Startup Details:
                - Idea/Product: {idea}
                - Stage: {stage}
                - Location: {location}
                - state: {state}
                Task:
                1. Identify 7-9 specific grants, government schemes (e.g., Startup India Seed Fund, NIDHI PRAYAS, BIRAC, state schemes), or incubators relevant to this idea.
                2. For each scheme, details:
                   - **Grant Name & Provider**
                   - **Funding Amount / Range**
                   - **Key Eligibility Requirements**
                   - **Why it fits this startup**
                3. Write in bullet points strictly
                If in the idea section there is some rubbish thing which is not related to any idea,just return "Please give a valid Idea"
                
                Try to go more state specific that saying general grants like MeitY,Birac,Nidhi Prayaas or Bionest.Also don't completely avoid them.
                """
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
                
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")