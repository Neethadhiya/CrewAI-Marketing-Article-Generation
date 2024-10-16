from crewai import Crew
from textwrap import dedent
from article_agents import ArticleAgents
from article_tasks import ArticleTasks
from langchain_community.tools import DuckDuckGoSearchResults
import json  
import os
from dotenv import load_dotenv
from os.path import join, dirname
env_path = "/home/appscrip/Desktop/Neetha/Marketing Article/.env "
load_dotenv(dotenv_path=env_path)
import random

class ArticleCrew:

    def __init__(self, keyword):
        self.keyword = keyword

    def run(self):
        agents = ArticleAgents()
        tasks = ArticleTasks()

        # Initialize agents for each task
        content_selector_agent = agents.content_selection_agent(keyword=self.keyword)
        meta_description_selector_agent = agents.meta_description_selector_agent()
        pros_and_cons_agent = agents.pros_and_cons_agent()
        faq_agent = agents.faq_agent()
        myth_busting_agent = agents.myth_busting_agent()
        pdf_statistic_agent = agents.pdf_statistic_agent(keyword=self.keyword)
        title_agent = agents.title_agent()
        google_snippet_optimization = agents.google_snippet_optimization_agent(keyword=self.keyword)
        # Step 1: Content Selection Task
        content_selection_task = tasks.content_selection_task(
            content_selector_agent,
            self.keyword
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
        print("11111",content_result,"1111111111")
        print("222222222",pros_and_cons_result,"2222222222")
        print("33333333333",faq_result,"3333333333")
        print("444444444",myth_busting_result,"444444")
        print("55555555",pdf_statistic_result,"555555555555555")
        print("666666666666",title_result,"666666666666")

        content_result_dict = json.loads(content_result) 
        pros_and_cons_result_dict = json.loads(pros_and_cons_result) 
        faq_result_dict = json.loads(faq_result) 
        myth_busting_result_dict = json.loads(myth_busting_result) 
        pdf_statistic_result_dict = json.loads(pdf_statistic_result) 
        print("lllllkkkkkkkkkkksdfsdddddddddddddddddddddd")

        print("11111",content_result_dict,"1111111111")
        print("222222222",pros_and_cons_result_dict,"2222222222")
        print("33333333333",faq_result_dict,"3333333333")
        print("444444444",myth_busting_result_dict,"444444")
        print("55555555",pdf_statistic_result_dict,"555555555555555")
        print("666666666666",title_result,"666666666666")
        google_snippet_optimization_task = tasks.google_snippet_optimization_task(
            google_snippet_optimization,
            self.keyword,
            content_result_dict,  # Now this is a dict
            pros_and_cons_result_dict,  # Now this is a dict
            faq_result_dict,  # Now this is a dict
            myth_busting_result_dict,  # Now this is a dict
            pdf_statistic_result_dict  # Now
        )
        crew = Crew(
            agents=[google_snippet_optimization],
            tasks=[google_snippet_optimization_task],
            verbose=True
        )
        google_snippet_optimization_result = crew.kickoff()
        final_result = {
            "content_result": content_result,
            "meta_description_result": meta_description_result,
            "pros_and_cons_result": pros_and_cons_result,
            "faq_result": faq_result,
            "myth_busting_result": myth_busting_result,
            "pdf_statistic_result": pdf_statistic_result,
            "title_result": title_result,
            "google_snippet_optimization_result": google_snippet_optimization_result
        }

        return final_result

if __name__ == "__main__":
    from textwrap import dedent
    print("## Welcome to Marketing Article Generation Crew")
    print('-------------------------------')
    keyword = input(
        dedent("""\
            Please enter the keyword around which you would like to generate the marketing article:
        """))

    article_crew = ArticleCrew(keyword)
    result = article_crew.run()

    # Define the output file
    output_file = 'marketing_article_output.txt'
    title_result = result.get('title_result')
    print(result['title_result'],"title_result==========")
    # Initialize best_title
    best_title = None           
    best_title = title_result['title']
  
    final_output = (
        "########################\n\n"
        f"{best_title}\n\n"
        "########################\n\n"
        f"{result['content_result']}\n\n"
        "## Pros and Cons\n"
        "########################\n\n"
        f"{result['pros_and_cons_result']}\n\n"
        
        "## Myth Busting\n"
        "########################\n\n"
        f"{result['myth_busting_result']}\n\n"
        f"## Amazing Statistics on {keyword}\n"
        "########################\n\n"
        f"{result['pdf_statistic_result']}\n\n"
       "## FAQ\n"
        "########################\n\n"
        f"{result['faq_result']}\n\n"
        # "## Google Snippet Optimization\n"
        # "########################\n\n"
        # f"{result['google_snippet_optimization_result']}\n"
    )

    # Open the file in write mode and write the final output
    with open(output_file, 'w') as file:
        file.write(final_output)

    print(f"Results have been written to {output_file}")

    


    
    