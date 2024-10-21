import os
from crewai import Agent
from langchain.llms import OpenAI
from langchain.schema import HumanMessage
from tools.search_summarise_tools import SearchSummarizeTool
from tools.google_snippet_optimize_tool import GoogleSnippetOptimizeTool

from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from os.path import join, dirname
env_path = "/home/appscrip/Desktop/Neetha/Crewai-Marketing-Article-Generation/.env"
load_dotenv(dotenv_path=env_path)
# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

class ArticleAgents():
  

  def content_selection_agent(self, keyword):
    search_tool = SearchSummarizeTool() 
    return Agent(
        role='Content Selection Expert',
        goal=f"""
                Develop a detailed content outline that not only covers all aspects of the target 
                keyword but also provides comprehensive explanations, examples, and in-depth insights 
                for each section, exceeding competitor content in depth and value.Additionally, create a
                “What is {keyword}?” section that provides a clear, concise, and informative explanation of the 
                keyword, using an NLP-friendly format without bullet points and with 2-4 sentences per paragraph.
            """,
        backstory=f"""
                    You are an SEO content strategist tasked with analyzing competitor content from the 
                    top 3 search results. Your job is to create a highly detailed, valuable, and in-depth 
                    content outline by identifying gaps, expanding on subtopics, providing unique insights, 
                    and offering thorough explanations for each section.Make sure to include a section titled
                    
                  """,
        tools=[search_tool],
        verbose=True
    )
    
  
    
  def meta_description_selector_agent(self):

    return Agent(
        role='Meta Description Selection Expert',
        goal='To create an SEO-friendly meta description for a blog post or article.',
        backstory="""
            The agent is trained to optimize and generate meta descriptions for blog posts and articles 
            based on the title and a target keyword. Its output must be between 148 and 158 characters, 
            contain the keyword, and encourage users to click through.
        """,
        tools=[],
        verbose=True
    )

  def pros_and_cons_agent(self):
    return Agent(
        role='Pros and Cons Expert',
        goal='To create a list of pros and cons for a given topic.',
        backstory="""
            The agent is trained to analyze a given topic and create a list of pros and cons.
        """,
        tools=[],
        verbose=True
    )

  def faq_agent(self):
    return Agent(
        role='FAQ Expert',
        goal='To create a list of FAQs for a given topic.',
        backstory="""
            The agent is trained to analyze a given topic and create a list of FAQs.
        """,
        tools=[],
        verbose=True
    )
  
  def myth_busting_agent(self):
    return Agent(
        role='Myth Busting Expert',
        goal='Identify and debunk common myths related to the given keyword',
        backstory="""
            You are an expert at identifying and debunking common myths 
            and misconceptions in various fields. Your role is to provide accurate 
            information to counter widespread misinformation.
        """,
        tools=[],
        verbose=True
    )

  def pdf_statistic_agent(self, keyword):
    
    return Agent(
        role='Statistics Expert',
        goal='Extract top 10 interesting statistics about the keyword.',
        backstory="""
                   Your job is to extract the most relevant 10 statistics about the keyword.
        """,
        tools=[],
        verbose=True
    )

  def title_agent(self):
    return Agent(
        role='SEO Title Generation Expert',
        goal='Generate compelling and SEO-optimized titles for articles',
        backstory="""
            You are a seasoned SEO copywriter specializing in crafting attention-grabbing, 
            click-worthy titles that also rank well in search engines. Your expertise lies 
            in balancing user appeal with search engine requirements.
        """,
        tools=[],
        verbose=True,
        allow_delegation=False,
        
    )
  
   
  def google_snippet_optimization_agent(self, keyword, sections_to_optimize):
    optimize_tool = GoogleSnippetOptimizeTool() 
    return Agent(
        role='Google Snippet Optimization Expert',
        goal="""
                Your task is to read the guidelines about Google featured snippets from the article provided, 
                analyze the competitor's copy that is currently ranking for the featured snippet, and optimize 
                our copy to increase its chances of ranking as the featured snippet. Make necessary changes to 
                improve clarity, conciseness, and structure to meet Google’s criteria for featured snippets.
            """,
        backstory="""
                    You are an SEO expert specializing in optimizing content for featured snippets. Your expertise 
                    lies in crafting concise, clear, and structured responses that Google recognizes as the best 
                    answers for specific queries. After reading the provided guidelines, you will optimize our 
                    content to meet these standards.
                  """,
        tools=[optimize_tool],
        verbose=True
    )


