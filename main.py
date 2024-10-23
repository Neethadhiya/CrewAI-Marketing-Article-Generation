from crewai import Crew
from textwrap import dedent
from article_agents import ArticleAgents
from article_tasks import ArticleTasks
from langchain_community.tools import DuckDuckGoSearchResults
import json  
import os
from dotenv import load_dotenv
from os.path import join, dirname
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from langchain_openai import ChatOpenAI

env_path = "/home/appscrip/Desktop/Neetha/Crewai-Marketing-Article-Generation/.env"
load_dotenv(dotenv_path=env_path)
import random

tracer_provider = None

def initialize_tracer_provider():
    global tracer_provider
    if tracer_provider is None:
        print("Initializing TracerProvider...")
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)
    else:
        print("TracerProvider is already initialized.")

# Call the function to initialize the TracerProvider
initialize_tracer_provider()


class ArticleCrew:

    def __init__(self, keyword, country_code, pdf_path):
        self.keyword = keyword
        self.country_code = country_code
        self.pdf_path = pdf_path

    def run(self):
        agents = ArticleAgents()
        tasks = ArticleTasks()

        # Initialize agents for each task
        content_selector_agent = agents.content_selection_agent(keyword=self.keyword, country_code=self.country_code)
        meta_description_selector_agent = agents.meta_description_selector_agent()
        pros_and_cons_agent = agents.pros_and_cons_agent()
        faq_agent = agents.faq_agent(keyword=self.keyword)
        myth_busting_agent = agents.myth_busting_agent()
        pdf_statistic_agent = agents.pdf_statistic_agent(keyword=self.keyword, pdf_path=self.pdf_path)
        title_agent = agents.title_agent()
        # Step 1: Content Selection Task
        content_selection_task = tasks.content_selection_task(
            content_selector_agent,
            self.keyword,
            self.country_code
        )
        crew = Crew(
            agents=[content_selector_agent],
            tasks=[content_selection_task],
            verbose=True
        )
        content_result = crew.kickoff()
        

        # Step 2: Meta Description Task
        meta_description_task = tasks.meta_description_task(
            meta_description_selector_agent,
            self.keyword,
        )
        crew = Crew(
            agents=[meta_description_selector_agent],
            tasks=[meta_description_task],
            verbose=True
        )
        meta_description_result = crew.kickoff()
        
        # # Step 3: Pros and Cons Task
        pros_and_cons_task = tasks.pros_and_cons_task(
            pros_and_cons_agent,
            self.keyword,
        )

        crew = Crew(
            agents=[
                pros_and_cons_agent,],
            tasks=[pros_and_cons_task],
            verbose=True
        )
        pros_and_cons_result = crew.kickoff()
        

        # Step 4: FAQ Task
        faq_task = tasks.faq_task(
            faq_agent,
            self.keyword,
        )
        crew = Crew(
            agents=[faq_agent],
            tasks=[faq_task],
            verbose=True
        )
        faq_result = crew.kickoff()

        # Step 5: Myth Busting Task
        myth_busting_task = tasks.myth_busting_task(
            myth_busting_agent,
            self.keyword,
        )
        crew = Crew(
            agents=[myth_busting_agent],
            tasks=[myth_busting_task],
            verbose=True
        )
        myth_busting_result = crew.kickoff()

        # Step 6: PDF Statistics Task
        pdf_statistic_task = tasks.pdf_statistic_task(
            pdf_statistic_agent,
            self.keyword,
            self.pdf_path
        )
        crew = Crew(
            agents=[pdf_statistic_agent],
            tasks=[pdf_statistic_task],
            verbose=True
        )
        pdf_statistic_result = crew.kickoff()
        
        title_task = tasks.title_task(
            title_agent,
            self.keyword,
        )
        crew = Crew(
            agents=[title_agent],
            tasks=[title_task],
            verbose=True
        )
        title_result = crew.kickoff()
        sections_to_optimize = {
                "Content": content_result,
                "Pros and Cons": pros_and_cons_result,
                "Myth Busting": myth_busting_result,
                "PDF Statistics": pdf_statistic_result,
            }
        google_snippet_optimization = agents.google_snippet_optimization_agent(
                                                                                keyword=self.keyword,
                                                                                sections_to_optimize=sections_to_optimize,
                                                                                country_code=self.country_code)          
        google_snippet_optimization_task = tasks.google_snippet_optimization_task(
            google_snippet_optimization,
            self.keyword,
            content_result,  # Now this is a dict
            pros_and_cons_result,  # Now this is a dict
            myth_busting_result,  # Now this is a dict
            pdf_statistic_result,  # Now
            self.country_code
        )
        crew = Crew(
            agents=[google_snippet_optimization],
            tasks=[google_snippet_optimization_task],
            verbose=True
        )
        google_snippet_optimization_result = crew.kickoff()
        final_result = {         
            "meta_description_result": meta_description_result,          
            "title_result": title_result,
            "google_snippet_optimization_result": google_snippet_optimization_result,
            "faq_result": faq_result,

        }

        return final_result

if __name__ == "__main__":
    from textwrap import dedent
    def validate_code_with_llm(country_code: str) -> bool:
        """Validate the country code using the LLM."""
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        prompt = (
            f"Please do google search and check '{country_code}' is a valid country code. "
            "If it is valid, respond with 'yes'. If it is invalid, respond with 'no'."
        )

        response = llm.invoke(prompt)  # Use .invoke() instead of direct call
        
        # Extract the content from the response
        response_content = response.content if hasattr(response, 'content') else str(response)

        # Normalize the response and check for validity
        normalized_response = response_content.strip().lower().rstrip('.')
        return normalized_response == 'yes'


    print("## Welcome to Marketing Article Generation Crew")
    
    print('-------------------------------')
    keyword = input(
        dedent("""\
            Please enter the keyword around which you would like to generate the marketing article:
        """))
    country_code = input(
        dedent("""\
            Please enter the country code for Google search-based keyword research (e.g., "US", "UK", "IN"):
        """))
    if not validate_code_with_llm(country_code):
        print(f"The country code '{country_code}' is invalid. Exiting the program.")
        exit()
    
    # Input for PDF file path
    pdf_path = input(
        dedent("""\
            Please enter the path to the PDF file that the PDF statistics agent will analyze:
        """))


    article_crew = ArticleCrew(keyword, country_code, pdf_path)
    result = article_crew.run()

    # Define the output file
    output_file = 'marketing_article_output.txt'
    title_result_str = result['title_result'].raw
    data = json.loads(title_result_str)
    title = data.get("title")
    final_output = (
    # "########################\n\n"
    # f"{title}\n\n"  # Corrected this line
    # "########################\n\n"
    f"{result['google_snippet_optimization_result']}\n"
    f"{result['faq_result']}\n"
)


    # Open the file in write mode and write the final output
    with open(output_file, 'w') as file:
        file.write(final_output)

    print(f"Results have been written to {output_file}")

    


    
    