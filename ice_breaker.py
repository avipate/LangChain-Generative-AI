# Importing required libraries
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv
from third_parties.linkedin import scrape_linkedin_profile
from output_parser import *

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

load_dotenv(find_dotenv())


class LangChainLLM:
    def __init__(self):
        self.summary_template = """
            given the Linkedin information {information} about a person from I want you to create:
            1. short description
            2. two interesting facts about them
            3. A topic that may interest them
            4. 2 creative Ice Breaker to open a conversation with them
            \n{format_instructions} 
        """
        self.chain, self.llm, self.summary_prompt_template, self.format_instruction = (
            None,
            None,
            None,
            None,
        )
        name = None

    def prompts(self):
        self.summary_prompt_template = PromptTemplate(
            input_variables=["information"],
            template=self.summary_template,
            partial_variables={
                "format_instructions": person_intel_parser.get_format_instructions()
            },
        )

    def llm_model(self, name) -> PersonalIntel:
        self.prompts()
        # Initialize the ChatOpenAI model
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

        # Build a chain to link the llm model and prompts
        chain = LLMChain(llm=self.llm, prompt=self.summary_prompt_template)

        # LinkedIn URL
        linkedin_profile_url = linkedin_lookup_agent(name=name)
        # get the linkedin data
        linkedin_data = scrape_linkedin_profile(
            linkedin_profile_url=linkedin_profile_url
        )

        result = chain.run(information=linkedin_data)

        return person_intel_parser.parse(result)


if __name__ == "__main__":
    print("Hello LangChain!")

    IceBreaker = LangChainLLM()
    IceBreaker.llm_model(name="Avi Patel")
