from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv
from output_parser import summary_parser, ice_breaker_parser, topics_of_interest_parser


load_dotenv(find_dotenv())

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=2000)
llm_creative = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo",  max_tokens=2000)


def get_summary_chain() -> LLMChain:
    summary_template = """
         given the information about a person from linkedin {information} I want you to create:
         1. a short summary
     """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )

    return LLMChain(llm=llm, prompt=summary_prompt_template)


def get_ice_breaker_chain() -> LLMChain:
    ice_breaker_template = """
         given the information about a person from linkedin {information} I want you to create:
         2 creative Ice breakers with them that are derived from their activity on Linkedin.
     """

    ice_breaker_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=ice_breaker_template,
    )

    return LLMChain(llm=llm_creative, prompt=ice_breaker_prompt_template)
