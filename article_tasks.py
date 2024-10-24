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
from googlesearch import search
from langchain_core.prompts import PromptTemplate


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
                            using paragraphs of 2-4 sentences.Don't include conclusion.
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
                                            "point": "[Insert Pro Here]",
                                            "description": "[Insert Detailed Description Here]"
                                        }},
                                        {{
                                            "point": "[Insert Pro Here]",
                                            "description": "[Insert Detailed Description Here]"
                                        }}
                                        // Add more pro points as necessary
                                    ],
                                    "cons": [
                                        {{
                                            "point": "[Insert Con Here]",
                                            "description": "[Insert Detailed Description Here]"
                                        }},
                                        {{
                                            "point": "[Insert Con Here]",
                                            "description": "[Insert Detailed Description Here]"
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
            - Make sure not include questions that are already answered within the article
            - Ensure answers are NLP-friendly.
            - Do not include links in the FAQ answers.
            """,
            agent=agent,
              expected_output=f"""
                    ### FAQ

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

    def simplify_content_task(
                                self, 
                                agent, 
                                keyword,
                                title_result,
                                content_result,
                                pros_and_cons_result,
                                myth_busting_result,
                                pdf_statistic_result,
                                country_code
                            ):
        content = {
            "Title":title_result,
            "Content": content_result,
            "Pros_and_Cons": pros_and_cons_result,
            "Myth_Busting": myth_busting_result,
            "PDF_Statistics": pdf_statistic_result,
        }   
        return Task(
                    description=f"""
                    Your task is to simplify the following marketing article based on the keyword '{keyword}'.
                    The entire article must be rewritten to be understandable for a 6th-grade reading level, 
                    keeping all the key points but making them more accessible. Write this in the form of an article.

                    ## {title_result}
                    Use the title provided as the main heading of the article.
                    Rewrite the content below, breaking down complex ideas into simple, clear language:
                    {content_result}

                    ### Pros and Cons
                    Simplify the advantages and disadvantages section. Use simple language, relatable examples, and concise sentences. 
                    Make it easy to follow, and present this section as a part of the article.
                    Current Pros and Cons: {pros_and_cons_result}

                    ### Myth Busting
                    Clarify the myths and their corrections using short, straightforward explanations. 
                    Avoid unnecessary technical terms or complicated phrasing, and write this as part of the article.
                    Current Myth Busting: {myth_busting_result}

                    ### Latest Statistics on {keyword}
                    Present the statistics in an easy-to-understand format. Use everyday comparisons to help illustrate the data 
                    and make it relatable for younger audiences. Incorporate this into the article's body as well.
                    Current PDF Statistics: {pdf_statistic_result}
                    
                    ### Conclusion
                    Add a detailed conclusion that summarizes the key points discussed in the article. 
                    Provide a detailed conclusion that summarizes the main points of the article. Ensure that it encapsulates the essence 
                    of the article and reinforces the importance of the topic for the reader. The conclusion should be clear, concise, and 
                    accessible for a 6th-grade reading level.
                    
                    Ensure the final output is structured, easy to follow, and accessible for a 6th-grade level.
                    The output must be an article format.
                    {self.__tip_section()}
                    """,
                    agent=agent,
                    expected_output="Full marketing article simplified to a 6th-grade English level in article format",
                    async_execution=False
                )


    def google_snippet_optimization_task(
                                            self, 
                                            agent, 
                                            keyword,
                                            simplify_content_result,
                                            country_code
                                        ):
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        search_query = f"{keyword} site:.{country_code}" 
        results = search(search_query, num_results=7)
        links = [result for result in results]
        summary_content = ""
        
        if len(links) > 0:
            competitors_copy = links[0]
            # print(f"Top Competitor's Snippet: {competitors_copy}")
            prompt = f"""
                You are a Google Snippet Optimizer. Analyze the competitor's snippet for the keyword "{keyword}":
                - Competitor's Snippet: {competitors_copy}

                Your task is to:
                1. Analyze the competitor's content{competitors_copy} and change {simplify_content_result}as you see it fit for it to 
                ranked on featurd snippet.Add more details in each section in the newly generated content.
                    
                2. Ensure that each section generated should be more structured, clear, and aligned with Google featured 
                snippets guidelines. The final output should be concise, understandable, and ready to be used as a Google 
                featured snippet.
                3.Add a conclusion at the end
                    """

            # Update the prompt template input variables to include all required variables
            prompt_template = PromptTemplate(
                template=prompt,
                input_variables=["keyword", "competitors_copy", "simplify_content_result"]
            )
            
            summary_chain = prompt_template | llm
            summary = summary_chain.invoke({
                "keyword": keyword,
                "competitors_copy": competitors_copy,
                "simplify_content_result": simplify_content_result,
            
            })

            optimized_content = summary.content if hasattr(summary, 'content') else str(summary)
            # print(f"Optimized Snippet:\n{optimized_content}")
        return Task(
            description=f"""
                Step 1: Please read the article to understand how Google featured snippets work at the following link: 
                [https://searchengineland.com/google-featured-snippets-optimization-guidelines-389951]. 
                
                Aknowledge that you have read it
                Step 2: Search the google for the {keyword} and find the is top ranking article ,that is the competitor's copy.
                
                Step 3: Compare {simplify_content_result} with {competitors_copy}.I want you to change it as you see fit for it to ranked on featured snippet.
                Step 4: Create pros and cons as a table
                Step 5: Add conclusion at the end. 
            """,
            agent=agent,
            expected_output="Full marketing article including all optimized sections and a conclusion at the end.",
            inputs={
                "keyword": keyword ,
                "our_copy":simplify_content_result ,
                "country_code": country_code 
            },
            async_execution=False,
            result=optimized_content 
        )


    def __tip_section(self):
        return "If you provide well-researched, high-quality work, I'll tip you $100 for your efforts!"
