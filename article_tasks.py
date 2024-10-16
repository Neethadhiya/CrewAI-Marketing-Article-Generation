from crewai import Task
from textwrap import dedent
from datetime import date
from article_agents import ArticleAgents
import json
from langchain_openai import ChatOpenAI
import os
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import sys
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.utilities import DuckDuckGoSearchAPIWrapper

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = os.getenv('OPENAI_MODEL_NAME')

from os.path import join, dirname
env_path = "/home/appscrip/Desktop/Neetha/Marketing Article/.env "
load_dotenv(dotenv_path=env_path)
class ArticleTasks:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
  

    def content_selection_task(self, agent, keyword):
      
        return Task(
            description=f"""
                            Analyze the top competitor content for the keyword: {keyword}, 
                            identify gaps, and generate a more comprehensive content outline 
                            that exceeds competitor coverage.
                            Your final result should be a well-structured article with informative 
                            sub-sections, where each sub-section helps readers understand the topic 
                            with concise explanations.Also, include a “What is {keyword}?” section 
                            with a clear and concise explanation of the keyword in an NLP-friendly format 
                            using paragraphs of 2-4 sentences.
                            {self.__tip_section()}
                        """,
            agent=agent,
            expected_output=f"""
            A content outline that's more comprehensive than these competitors and add each topic and subtopic detailed 
            definition and description about the topic.Don't give as introduction and definition as heading in the first
            section.Instead, start with a compelling story or 
            a real-life example related to the topic.Don't add additional resources or links.Give a bit more elaborate 
            information about the topic in the first section.Also, include a “What is {keyword}?” section with a 
            clear and concise explanation of the keyword in an NLP-friendly format using paragraphs of 2-4 sentences.
            """,
            inputs={
                "query": keyword  
            },
            async_execution=False
        )
    
 
        
    def meta_description_task(self, agent, keyword):
        return Task(
                    description=dedent(
                                    f"""
                                    You are a Meta Description Selection Expert. Your task is to 
                                    create an SEO-friendly meta description for an article 
                                    based on the provided keyword '{keyword}'
                                    The meta description must be between 148 and 158 characters, include 
                                    the keyword, and encourage users to click through to the article.
                                    {self.__tip_section()}
                                    keyword: {keyword}
                                    
                                    """),
                    agent=agent,
                    expected_output="A concise meta description between 148 and 158 characters.",
                    async_execution=False
                 )

    def pros_and_cons_task(self, agent, keyword):
        return Task(
            description=dedent(
                f"""
                You are a Pros and Cons Expert. Your task is to develop a comprehensive table outlining the pros and cons of {keyword}.
                - The table should include two columns: 'Pros of {keyword}' and 'Cons of {keyword}'.
                - Provide brief, clear, and informative explanations for each point in the table to help readers understand 
                the advantages and disadvantages associated with {keyword}.
                - Ensure that the explanations are comprehensive and easy to understand.
                {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"A pros and cons table for {keyword} with detailed explanations.",
            async_execution=False
        )

    def faq_task(self, agent, keyword):
        return Task(
            description=dedent(
                f"""
                You are a FAQ Expert. Your task is to develop a comprehensive FAQ section for the topic: {keyword}.
                - Create at least 5 commonly asked questions related to {keyword}.
                - Provide detailed and informative answers to each question, addressing potential concerns and
                providing valuable insights.
                - Ensure that the questions do not repeat any information already answered within the main article.
                - Answers should be written in a clear, concise, and NLP-friendly format.
                {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output=f"An FAQ section with 5 or more questions and answers for {keyword}.",
            async_execution=False
        )
    
    def myth_busting_task(self, agent, keyword):
        return Task(
            description=f"Create a 'Common Myths About {keyword} Debunked' section",
            agent = agent,
            expected_output=dedent(f"""List and debunk 5-10 myths related to {keyword}. 
            Format the output as a markdown list, with each myth as a subheading and 
            its debunking as the content.Do not number as Myth 1, Myth 2, etc. Just list them as a bulleted list."""),
            inputs={
                "query": keyword
            },
            async_execution=False
        )
    
    def pdf_statistic_task(self, agent, keyword):
        return Task(
            description=f"""
            Analyze data sources for '{keyword}'. Extract the top 10 interesting 
            statistics about {keyword} from the analyzed data sources.
            {self.__tip_section()}""",
            agent=agent,
            expected_output=dedent(f"""
                A list of the top 10 interesting statistics about {keyword} 
                extracted from the analyzed data sources.
            """),
            async_execution=False
        )
        
    def title_task(self, agent, keyword):
        return Task(
            description=f"""
            Generate a best SEO title for an SEO article targeting the keyword {keyword}. Limit it to 50-60 characters maximum.
        Use whichever of the following elements you see fit:
        - year
        - numbers
        - desired results
        - beginner's guide
        - by topic experts
        
        {self.__tip_section()}
        
        The final title should be a dictionary with the format:
        {{
            "title": "<SEO Title 1>",
           
        }}
            """,
            agent=agent,
            expected_output=dedent(f"""
                The best SEO title for an SEO article targeting the keyword {keyword} in dictionary format.
                It should always return a title.
            """),
            async_execution=False
        )

    def google_snippet_optimization_task(
                                            self, 
                                            agent, 
                                            keyword,
                                            content_result,
                                            pros_and_cons_result,
                                            faq_result,
                                            myth_busting_result,
                                            pdf_statistic_result,
                                            
                                            ):
        sections_to_optimize = {
        "Content": content_result,
        "Pros and Cons": pros_and_cons_result,
        "FAQ": faq_result,
        "Myth Busting": myth_busting_result,
        "PDF Statistics": pdf_statistic_result,
    }   
        

        return Task(
            description=f"""
                Step 1: Please read the guidelines about how Google featured snippets work at the following link: 
            [https://searchengineland.com/google-featured-snippets-optimization-guidelines-389951]. Please focus on improving 
            the clarity, structure, and presentation to align with the guidelines used for featured snippets.
            Step 2: Optimize the content for Google snippets using the results from prior tasks provided below:
            1. **Content Section:** {content_result}
            2. **Pros and Cons Section:** {pros_and_cons_result}
            3. **FAQ Section:** {faq_result}
            4. **Myth Busting Section:** {myth_busting_result}
            5. **PDF Statistics Section:** {pdf_statistic_result}
            Step 3: Simplify the blog post content to a 6th-grade English reading level to ensure that the 
            information is easy to understand for a wider audience.
            """,
            agent=agent,
            expected_output="""Revised sections for Google Snippets and aligned with a 
                            6th-grade reading level.""",
            inputs={
                "keyword": keyword,
                "sections_to_optimize": sections_to_optimize # Provide the results as input to the agent
            },
            async_execution=False
        )



    def __tip_section(self):
        return "If you provide well-researched, high-quality work, I'll tip you $100 for your efforts!"
