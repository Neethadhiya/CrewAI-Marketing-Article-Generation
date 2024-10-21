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
from langchain.tools import StructuredTool
from pydantic import BaseModel

class SearchAndOptimizeInput(BaseModel):
    keyword: str
    sections_to_optimize: dict


def search_and_optimize(keyword: str, sections_to_optimize: dict) -> str:
    """Perform a web search, summarize the result, and optimize using other agent results."""
    print("*****************************")
    print(f"Keyword: {keyword}")
    print(f"Sections to Optimize: {sections_to_optimize}")
    print("*****************************")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    results = search(keyword, num_results=7)
    links = [result for result in results]
    summary_content = ""
    
    if len(links) > 0:
        top_link = links[0]
        print(f"Top Competitor's Snippet: {top_link}")

        # Assuming you have the following variables defined based on previous results
        statistics_result = sections_to_optimize.get('statistics', '')  # Replace with your actual data retrieval logic
        pros_and_cons_result = sections_to_optimize.get('pros', '')
        myth_busting_result = sections_to_optimize.get('myths', '')
        faq_result = sections_to_optimize.get('faqs', '')
        content_outline = sections_to_optimize.get('content_outline', '')

        prompt = f"""
                    You are a Google Snippet Optimizer. Analyze the competitor's snippet for the keyword "{keyword}":
                    - Competitor's Snippet: {top_link}

                    Your task is to:
                    1. Analyze the competitor's content and identify specific improvements that can be added to our content.
                    2. Generate a complete marketing article blog post that ranks at the top of search results. The blog post should include:
                        - An optimized Content section that provides a clear and concise explanation of the topic with informative sub-sections,
                        where each sub-section helps readers understand the topic 
                            with concise explanations.
                         Include a "What is {keyword}?" section that explains the keyword in an NLP-friendly format using paragraphs of 2-4 
                         sentences. (Do not include a main heading for this section): {content_outline}
                        - A captivating heading and an optimized Pros and Cons section with **6 points each**: {pros_and_cons_result}
                        - A captivating heading and an optimized Myth Busting section with **6 myths**: {myth_busting_result}
                        - A captivating heading and an optimized Latest Statistics section: {statistics_result}
                        - A captivating heading and a well-structured Conclusion 
                        - A captivating heading and an optimized FAQ section with **6 commonly asked questions and detailed answers**: {faq_result}
                    Ensure that each section generated should be more structured, clear, and aligned with Google featured 
                    snippets guidelines. The final output should be concise, understandable, and ready to be used as a Google 
                    featured snippet.
                """

        # Update the prompt template input variables to include all required variables
        prompt_template = PromptTemplate(
            template=prompt,
            input_variables=["keyword", "top_link", "statistics", "pros", "myths", "faqs", "content_outline"]
        )
        
        summary_chain = prompt_template | llm
        summary = summary_chain.invoke({
            "keyword": keyword,
            "top_link": top_link,
            "statistics": statistics_result,
            "pros": pros_and_cons_result,
            "myths": myth_busting_result,
            "faqs": faq_result,
            "content_outline": content_outline
        })

        summary_content = summary.content if hasattr(summary, 'content') else str(summary)
        print(f"Optimized Snippet:\n{summary_content}")

    return summary_content


def GoogleSnippetOptimizeTool():
    return StructuredTool(
        name="search_and_optimize",
        func=search_and_optimize,  # Reference to your existing function
        args_schema=SearchAndOptimizeInput,  # Specify the input schema
        description="""
            Search the web for the provided keyword, analyze the top competitor's content, 
            and generate a complete marketing article blog post that includes:
            1. Optimized Content Section
            2. Optimized Pros and Cons Section
            3. Optimized Myth Busting Section
            4. Optimized PDF Statistics Section
            5. Optimized FAQ Section
            6. Conclusion

            Ensure that the final content is structured for readability and comprehension at a 6th-grade level.
        """
    )



def GoogleSnippetOptimizeTool():
    return StructuredTool(
        name="search_and_optimize",
        func=search_and_optimize,  # Reference to your existing function
        args_schema=SearchAndOptimizeInput,  # Specify the input schema
        description="""
            Search the web for the provided keyword, analyze the top competitor's content, 
            and generate a complete marketing article blog post that includes:
            1. Optimized Content Section
            2. Optimized Pros and Cons Section
            3. Optimized Myth Busting Section
            4. Optimized PDF Statistics Section
            5. Optimized FAQ Section
            6. Conclusion

            Ensure that the final content is structured for readability and comprehension at a 6th-grade level.
        """
    )