import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

google_api_key = "AIzaSyBVOM4Pct30jaUcFUiXpbMy4hVOv2f3kKk"  

st.markdown(
    """
    <style>
    body {
        background-image: url("https://www.hospitalitynewsmag.com/wp-content/uploads/2023/05/travel.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    .reportview-container {
        background: rgba(255, 255, 255, 0.8);  /* Optional: Add a white background with transparency for better readability */
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

chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", "You act as a helpful AI Assistant for a travel agency. You help find flight, railway, or bus bookings based on user queries. Provide a list of all available plans for travel in the form of a table, mentioning all required details about the trip cost and facilities."),
        ("human", "I want to travel from {source} to {destination} on {date} for {passengers} passengers.")
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

# Streamlit UI
st.title("AI Based Travel Planner :airplane:")


travel_query = st.text_input(label="✈️ Enter your travel request (e.g., 'Book a flight from New York to Los Angeles on June 15 for 2 passengers')", placeholder="Type your travel request here...")


btn_click = st.button("Find Travel Options")


if btn_click:
    if not travel_query:
        st.error("Please enter your travel request.")
    else:
        raw_input = {
            "query": travel_query
        }

        try:
            result = chain.invoke(raw_input)
            st.subheader("Available Travel Options:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred while fetching travel options: {str(e)}")