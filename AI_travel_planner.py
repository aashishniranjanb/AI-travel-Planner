import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Set the background image using CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("URL_TO_YOUR_IMAGE") no-repeat center center fixed; 
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", "You act as a helpful AI Assistant for a travel agency. You help find flight, railway, or bus bookings from source to destination. Provide a list of all available plans for travel in the form of a table, mentioning all required details about the trip cost and facilities."),
        ("human", "Book a flight from {source} to {destination} on date {date}. Have {passengers} number of passengers. Don't ask for any more information; just give a list of all available flights, railways, and buses.")
    ],
    partial_variables={"source": "ABD", "destination": "HYB", "passengers": 1}
)

# Initialize the ChatGoogleGenerativeAI model
chat_model = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-2.0-flash-exp",
    temperature=1
)

parser = StrOutputParser()

chain = chat_prompt_template | chat_model | parser

# Streamlit UI
st.title(":tophat: AI Based Travel Planner")

# User input fields
source = st.text_input(label=":earth_asia: Source:", placeholder="Enter Your Source...")
destination = st.text_input(label=":earth_asia: Destination:", placeholder="Enter Your Destination...")
date = st.date_input(label=":calendar: Date:", value=None)
passengers = st.number_input(label=":blond-haired-man: No. Of Passengers:", min_value=1, max_value=10, value=1, step=1)

# Button to find trip plan availability
btn_click = st.button("Find A Trip Plan Availability")

# Process user input when button is clicked
if btn_click:
    # Validate inputs
    if not source or not destination or date is None:
        st.error("Please fill in all fields: Source, Destination, and Date.")
    else:
        # Prepare raw input for the chain
       raw_input = {
    "source": source,
    "destination": destination,
    "date": date.strftime("%Y-%m-%d"),  # Ensure the date is formatted correctly
    "passengers": passengers  # Include the number of passengers if applicable
}
