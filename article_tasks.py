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
env_path = "/home/appscrip/Desktop/Neetha/Crewai-Marketing-Article-Generation/.env"
load_dotenv(dotenv_path=env_path)
class ArticleTasks:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
  

    def content_selection_task(self, agent, keyword, country_code):
      
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
            Please return the response in the following JSON format:
            {{
                "content_outline": [
                    {{
                        "title": "Section Title",
                        "description": "Detailed description of the section."
                    }},
                    {{
                        "title": "What is {keyword}?",
                        "description": "Clear and concise explanation of the keyword in an NLP-friendly format."
                    }}
                    // You can include additional sections here.
                ]
            }}
            """,
            inputs={
                "query": keyword ,
                "country_code": country_code 
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
                    expected_output="""
                                        {
                                            "meta_description": "A concise meta description between 148 and 158 characters that includes the keyword."
                                        }
                                        """,
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
            expected_output=f"""
                                {{
                                    "pros": [
                                        {{
                                            "point": "<Pro point 1 for {keyword}>",
                                            "explanation": "<Brief explanation of Pro point 1.>"
                                        }},
                                        {{
                                            "point": "<Pro point 2 for {keyword}>",
                                            "explanation": "<Brief explanation of Pro point 2.>"
                                        }}
                                        // Add more pro points as necessary
                                    ],
                                    "cons": [
                                        {{
                                            "point": "<Con point 1 for {keyword}>",
                                            "explanation": "<Brief explanation of Con point 1.>"
                                        }},
                                        {{
                                            "point": "<Con point 2 for {keyword}>",
                                            "explanation": "<Brief explanation of Con point 2.>"
                                        }}
                                        // Add more con points as necessary
                                    ]
                                }}
                                """,

            async_execution=False
        )

    def faq_task(self, agent, keyword):
        return Task(
            description=f"""
            You are a FAQ Expert. Your task is to develop a comprehensive FAQ section for the topic: '{keyword}'.
            - Use the Google Serp API to fetch at least 5 commonly asked 'People Also Ask' questions related to {keyword}.
            - Use the 'question' field from the tool's results for the FAQ question.
            - Use the 'snippet' field from the tool's results for the answer to each FAQ.
            - Ensure answers are NLP-friendly and do not repeat any information already answered within the main article.
            """,
            agent=agent,
              expected_output=f"""
                    ### FAQ: {keyword}

                    1. [Insert Question Here]
                    - [Insert Answer Here]

                    2.[Insert Question Here]
                    - [Insert Answer Here]
                    ......
                    add more
                    """ 
        )


    
    def myth_busting_task(self, agent, keyword):
        return Task(
            description=f"Create a 'Common Myths About {keyword} Debunked' section",
            agent = agent,
            expected_output=dedent(f"""{{
                                        "myths": [
                                            {{
                                                "myth": "<Myth 1 related to {keyword}>",
                                                "debunking": "<Explanation debunking Myth 1>"
                                            }},
                                            {{
                                                "myth": "<Myth 2 related to {keyword}>",
                                                "debunking": "<Explanation debunking Myth 2>"
                                            }},
                                            {{
                                                "myth": "<Myth 3 related to {keyword}>",
                                                "debunking": "<Explanation debunking Myth 3>"
                                            }}
                                            // Add more myths and their debunkings as necessary
                                        ]
                                    }}
                                    """),

            inputs={
                "query": keyword
            },
            async_execution=False
        )
    
    def pdf_statistic_task(self, agent, keyword,pdf_path):
        return Task(
            description=f"""
            Analyze the provided PDF {pdf_path} file for '{keyword}'. Extract the top 10 most 
            interesting and relevant statistics about {keyword} from the analyzed PDF data.
            {self.__tip_section()}""",
            agent=agent,
            expected_output=dedent(f"""
                {{
                    "statistics": [
                        {{
                            "title": "<title_1>",
                            "statistic": "<statistic_1>"
                        }},
                        {{
                            "title": "<title_2>",
                            "statistic": "<statistic_2>"
                        }},
                    add more
                    ]
                }}
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
                                            myth_busting_result,
                                            pdf_statistic_result,
                                            country_code
                                        ):
        sections_to_optimize = {
            "Content": content_result,
            "Pros and Cons": pros_and_cons_result,
            "Myth Busting": myth_busting_result,
            "PDF Statistics": pdf_statistic_result,
        }   

        return Task(
            description=f"""
                Step 1: Please read the guidelines about how Google featured snippets work at the following link: 
                [https://searchengineland.com/google-featured-snippets-optimization-guidelines-389951]. 
                Focus on improving clarity, structure, and presentation to align with the guidelines used for featured snippets.
                
                Step 2: Optimize the content for Google snippets using the results from prior tasks provided below:
                1. **Content Section:** {content_result}
                2. **Pros and Cons Section:** {pros_and_cons_result}
                3. **Myth Busting Section:** {myth_busting_result}
                4. **PDF Statistics Section:** {pdf_statistic_result}
                
                Step 3: Generate a complete marketing article blog post that ranks at the top of search results. Ensure that the content is optimized for readability and 
                comprehension at a 6th-grade level, making it accessible to a wider audience.
            """,
            agent=agent,
            expected_output="Full marketing article including all optimized sections and a conclusion.",
            inputs={
                "keyword": keyword,
                "sections_to_optimize": sections_to_optimize,
                "country_code":country_code
            },
            async_execution=False
        )



    def __tip_section(self):
        return "If you provide well-researched, high-quality work, I'll tip you $100 for your efforts!"
