# Importing required libraries
from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv
from third_parties.linkedin import scrape_linkedin_profile
from output_parser import *

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

load_dotenv(find_dotenv())


# Function to integrate LangChain with OpenAI gpt model and get data from LinkedIn
def ice_break(name: str) -> Tuple[PersonalIntel, str]:
    # LinkedIn URL
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    # get the linkedin data
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    summary_template = """
                given the Linkedin information {information} about a person from I want you to create:
                1. short description
                2. two interesting facts about them
                3. A topic that may interest them
                4. 2 creative Ice Breaker to open a conversation with them
                \n{format_instructions} 
            """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )
    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    # Build a chain to link the llm model and prompts
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(information=linkedin_data)

    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Hello LangChain!")
    ice_break(name="Avi Patel")
