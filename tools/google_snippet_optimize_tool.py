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


def search_summarize(keyword: str, sections_to_optimize: dict) -> str:
    """Perform a web search, summarize the result, and optimize using other agent results."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    results = search(keyword, num_results=7)
    links = []
    for i, result in enumerate(results, 1):
        links.append(result)
    summary_content = ""
    
    if len(links) > 0:
        top_link = links[0]
        
        print(f"Top Competitor's Snippet: {top_link}")
        
        # Combine agent results into a summary
        combined_agent_results = "\n".join([f"{key}: {value}" for key, value in sections_to_optimize.items()])
        
        prompt = f"""
            You are a Google Snippet Optimizer. Analyze the competitor's snippet for the keyword "{keyword}":
            - Competitor's Snippet: {top_link}

            Based on this analysis and the following results from our content agents:
            {combined_agent_results}

            Your task is to:
            1. Analyze the competitor's content and identify specific improvements that can be added to our content.
            2. Directly rewrite our content to incorporate these improvements, making it more structured, clear, and 
                aligned with Google featured snippets guidelines.
            3. Ensure that the new content is concise and ready to be used as a Google featured snippet.
        """

        prompt_template = PromptTemplate(
            template=prompt,
            input_variables=["keyword", "top_link", "combined_agent_results"]
        )
        
        summary_chain = prompt_template | llm
        summary = summary_chain.invoke({
            "keyword": keyword,
            "top_link": top_link,
            "combined_agent_results": combined_agent_results
        })
        
        summary_content = summary.content if hasattr(summary, 'content') else str(summary)
        print(f"Optimized Snippet:\n{summary_content}")
        
    return summary_content


def GoogleSnippetOptimizeTool():
    return Tool(
        name="search_summarize",
        func=lambda keyword, sections_to_optimize: search_summarize(keyword,sections_to_optimize),  # Accept both keyword and all agent results
        
        description="""
                        Search the web, summarize the top 1 result for the provided keyword, and optimize 
                        based on the content from other agents.
                    """
    )
