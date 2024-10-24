from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from serpapi import GoogleSearch

# Load environment variables
env_path = "/home/appscrip/Desktop/Neetha/Crewai-Marketing-Article-Generation/.env"
load_dotenv(dotenv_path=env_path)

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
SERP_API_KEY = os.getenv('SERP_API_KEY')

# Initialize the LLM
llm = OpenAI(temperature=0.0)

# Initialize the Google Serper tool
search = GoogleSerperAPIWrapper()

# Define the function to get FAQs from Serper API
def get_faq(keyword: str):
    # Construct the API request URL
    params = {
    "engine": "google",
    "next_page_token": "eyJvbnMiOiIxMDA0MSIsImZjIjoiRW9vQkNreEJTa2M1U210T1JsQjZhMjAyTVRCMVVsRmhlV05HVnpSdUxTMTRWemhVUm5OVk4yaGxjRXRCWlRKR1RUbHlRWGswU2sxWWVXSTVYemhIWkhWTFNscExNRUpPV25WNWFtcFFUa3d3RWhaT1RIWmFXbk54WDBSTVV6RjNUalJRYnpkcVdFOUJHaUpCUmxoeVJXTnZZMHBFWmxacU5GQnljR3h0Um5KV1lsOVdOVmh1WkcxWFZGRjMiLCJmY3YiOiIzIiwiZWkiOiJOTHZaWnNxX0RMUzF3TjRQbzdqWE9BIiwicWMiOiJDZ1pqYjJabVpXVVFBSDA1VEQ4XyIsInF1ZXN0aW9uIjoiSXMgY29mZmVlIGdvb2Qgb3IgYmFkIGZvciBoZWFsdGg/IiwibGsiOiJHaUJwY3lCamIyWm1aV1VnWjI5dlpDQnZjaUJpWVdRZ1ptOXlJR2hsWVd4MGFBIiwiYnMiOiJjLVB5NGxMMExGWkl6azlMUzAxVlNNX1BUMUhJTDFKSVNreFJTQVBTR2FtSk9TVVo5aEtiZUl5VXBCUXlDYWpqY3VHU0M4LW9SRkpYbkE5UkNsSlRtVjlxTDdGWnpraGVTclljbnlJdVZ5NzU4SXpFRW9YRW9sUUZRd09GcE5TODFMVE1rbUtGX0RTb0Ruc0pFeU1GS2JseXZJcTQ0cmgwd01hazVLY0NoZk5TRlpKTEN4RFNRR0dGa255UWZVQmY1S2RVMmtzc3JqWFNsdElzaDJzeHhLOUJnQkVBIiwiaWQiOiJmY19OTHZaWnNxX0RMUzF3TjRQbzdqWE9BXzQifQ==",
    "q": keyword,  # Add the keyword here
    "api_key": SERP_API_KEY 
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        # Check if the results contain related questions
        if "related_questions" in results:
            related_questions = results["related_questions"]
            # print(f"--------------------{results}---------------------")

            return related_questions
        else:
            print("No related questions found.")
            return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Define the tool that uses the Serper API
def FAQTool():
    return Tool(
        name="FAQ Search",
        func=lambda keyword: get_faq(keyword),  # Passing keyword as an argument
        description="Search Google for 'People Also Ask' questions for a given topic using Google Serp API."
    )
    
# outsourcing vs insourcing 
# https://cdn.worktechacademy.com/uploads/2017/09/Industry-Insights-Insourcing-vs-Outsourcing.pdf
