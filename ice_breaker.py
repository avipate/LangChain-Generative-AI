# Importing required libraries
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv
from third_parties.linkedin import scrape_linkedin_profile

load_dotenv(find_dotenv())


class LangChainLLM:
    def __init__(self):
        self.summary_template = """
            given the Linkedin information {information} about a person from I want you tp create:
            1. short description
            2. two interesting facts about them
        """
        self.chain, self.llm, self.summary_prompt_template = None, None, None

    def prompts(self):
        self.summary_prompt_template = PromptTemplate(
            input_variables=["information"], template=self.summary_template
        )

    def llm_model(self):
        self.prompts()
        # Initialize the ChatOpenAI model
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

        # Build a chain to link the llm model and prompts
        chain = LLMChain(llm=self.llm, prompt=self.summary_prompt_template)

        # get the linkedin data
        linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/avi-patel-93503520b/")

        print(chain.run(information=linkedin_data))


if __name__ == "__main__":
    print("Hello LangChain!")

    IceBreaker = LangChainLLM()
    IceBreaker.llm_model()
