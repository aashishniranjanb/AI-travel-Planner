import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Travel Planner AI", page_icon="✈️")
st.title("AI Travel Planner 🧳")

llm = ChatGoogleGenerativeAI(model="gemini-pro")

source = st.text_input("Enter starting location:")
destination = st.text_input("Enter destination:")
submit = st.button("Plan My Trip")

prompt_template = PromptTemplate.from_template(
    "Suggest travel options between {source} and {destination}. "
    "Include cabs, trains, buses, and flights with estimated costs. "
    "Format as bullet points with emojis. "
    "Mention approximate travel time and distance for each option."
)

if submit and source and destination:
    formatted_prompt = prompt_template.format(
        source=source, 
        destination=destination
    )
    
    #AI response
    try:
        response = llm.invoke(formatted_prompt)
        st.subheader("Travel Options:")
        st.markdown(response.content)
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")