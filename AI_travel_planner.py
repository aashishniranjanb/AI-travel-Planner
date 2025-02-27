import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

google_api_key = "AIzaSyBVOM4Pct30jaUcFUiXpbMy4hVOv2f3kKk"  
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.hospitalitynewsmag.com/wp-content/uploads/2023/05/travel.jpg") no-repeat center center fixed; 
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", "You act as a helpful AI Assistant for a travel agency. You help find flight, railway, or bus bookings from source to destination. Provide a list of all available plans for travel in the form of a table, mentioning all required details about the trip cost and facilities."),
        ("human", "Book a flight from {source} to {destination} on date {date}. Have {passengers} number of passengers. Don't ask for any more information; just give a list of all available flights, railways, and buses.")
    ],
    partial_variables={"source": "ABD", "destination": "HYB", "passengers": 1}
)


chat_model = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-2.0-flash-exp",
    temperature=1
)

parser = StrOutputParser()

chain = chat_prompt_template | chat_model | parser

st.title(":tophat: AI Based Travel Planner :airplane: :train: :bus:")

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
        # Prepare raw input for the chain without formatting the date
        raw_input = {
            "source": source,
            "destination": destination,
            "date": date,  # Use the date object directly
            "passengers": passengers
        }

        # Invoke the chain and display the result
        try:
            result = chain.invoke(raw_input)
            st.subheader("Available Travel Options:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred while fetching travel options: {str(e)}")