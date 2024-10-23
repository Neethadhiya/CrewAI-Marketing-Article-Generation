import os
from functools import lru_cache
from typing import List, Tuple, Optional
import nltk
from dotenv import load_dotenv
import time
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from googlesearch import search


def search_summarize(keyword: str, country_code: str) -> str:
    """Perform a web search and summarize the results."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    search_query = f"{keyword} site:.{country_code}" 
    results = search(search_query, num_results=7)
    links = []
    for i, result in enumerate(results, 1):
        links.append(result)
    summary_content = ""
    if len(links) > 0:
        links_1 = links[0]
        links_2 = links[1]
        links_3 = links[2]
        print("=======",keyword,links_1, links_2, links_3,"============")
        prompt = f"""
            You are an SEO content writer. Analyse these 3 top-ranking articles for {keyword}:
            - {links_1}
            - {links_2}
            - {links_3}
            Create a content outline that's more comprehensive than these competitors and add each topic detailed 
            definition and description about the topic. 
        """
        prompt = PromptTemplate(
            template = """You are an SEO content writer. Analyse these 3 top-ranking articles for {keyword}
            ::\n-{links_1}\n-{links_2}\n-{links_3}\nCreate a content outline that's more comprehensive 
            than these competitors and add each topic detailed definition and description about the topic.Don't 
            give as introduction and definition in the first section.Instead, start with a compelling story or 
            a real-life example related to the topic.Don't add additional resources or links.Give a bit more elaborate 
            information about the topic in the first section.
            """,
            input_variables=["keyword","links_1", "links_2", "links_3"],
        )
        summary_chain = prompt | llm
        summary = summary_chain.invoke(
            {
                "keyword": keyword,
                "links_1": links_1,
                "links_2": links_2,
                "links_3": links_3,
                
                
            }
        )
        
        summary_content = summary.content if hasattr(summary, 'content') else str(summary)
    return summary_content
    

def SearchSummarizeTool(country_code: str):

    return Tool(
        name="search_summarize",
        func=lambda keyword: search_summarize(keyword, country_code),  # Pass keyword as an argument
        description="Search the web for the specified keyword and summarize the top 3 results relevant to that keyword from the given country."
    )