import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

google_api_key = "AIzaSyBVOM4Pct30jaUcFUiXpbMy4hVOv2f3kKk"  

chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", "You act as an AI-powered Travel Planner. Your task is to find the best travel options including flights, trains, buses, and cabs between the given source and destination. Provide travel time, cost, and facilities in a structured table."),
        ("human", "Find me the best travel options from {source} to {destination} on {date} for {passengers} passengers.")
    ]
)

chat_model = ChatGoogleGenerativeAI(
    google_api_key=google_api_key,
    model="gemini-2.0-flash-exp",
    temperature=0.7
)

parser = StrOutputParser()
chain = chat_prompt_template | chat_model | parser

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="centered")

st.markdown(
    """
    <style>
    /* Page Background & General Text Color */
    body {
        background-color: #CFB5FF; 
        color: #FFFFFF;             
    }
    
    /* Main App Container */
    .stApp {
        background-color: #DBD3EF;  /* Amethyst purple */
        padding: 20px;
    }
    
    /* Input Fields: Text Input & Text Area */
    .stTextInput, .stTextArea {
        background-color: #7F3FBF !important;  /* Lighter purple for inputs */
        color: #FFFFFF !important;             /* White text inside inputs */
        border-radius: 8px;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #9B59B6 !important;  /* Vibrant purple for buttons */
        color: #FFFFFF !important;             /* White text on buttons */
        border-radius: 8px;
    }
    
    /* Result Container Styling */
    .result-container {
        background-color: #8E44AD;  /* Complementary purple */
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        color: #FFFFFF;             /* White text inside results */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 AI Travel Planner ✈️")
st.subheader("🚀 Find the Best Travel Options in Seconds")

source = st.text_input("📍 Source Location", placeholder="Enter starting city (e.g., New York)")
destination = st.text_input("📍 Destination", placeholder="Enter destination city (e.g., Los Angeles)")
date = st.date_input("📅 Travel Date")
passengers = st.number_input("👥 Number of Passengers", min_value=1, max_value=10, value=1)

if st.button("🔍 Find Travel Options"):
    if not source or not destination or not date:
        st.error("⚠️ Please enter all required details (Source, Destination, and Date).")
    else:
        user_input = {
            "source": source,
            "destination": destination,
            "date": date.strftime("%Y-%m-%d"),
            "passengers": passengers
        }

        try:
            result = chain.invoke(user_input)
            st.markdown("<div class='result-container'>", unsafe_allow_html=True)
            st.subheader("🚀 Available Travel Options:")
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ An error occurred while fetching travel options: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #000000;'>💡 Powered by AI | Developed by Aashish Niranjan B </p>", unsafe_allow_html=True)
