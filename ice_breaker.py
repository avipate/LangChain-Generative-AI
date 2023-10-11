# Importing required libraries
from typing import Tuple, Any

from pydantic import BaseModel
from pydantic.v1 import BaseModel

from chains.custom_chains import (
    get_summary_chain,
    get_ice_breaker_chain,
)
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv, find_dotenv
from third_parties.linkedin import scrape_linkedin_profile
from output_parser import (
    summary_parser,
    ice_breaker_parser,
    Summary,
    IceBreaker,
    TopicOfInterest,
)

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

load_dotenv(find_dotenv())


# Function to integrate LangChain with OpenAI gpt model and get data from LinkedIn
def ice_break(name: str) -> tuple[Any, Any, Any]:
    # LinkedIn URL
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    # get the linkedin data
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    summary_chain = get_summary_chain()
    summary_and_facts = summary_chain.run(information=linkedin_data)

    summary_and_facts = summary_parser.parse(summary_and_facts)

    ice_breaker_chain = get_ice_breaker_chain()
    ice_breakers = ice_breaker_chain.run(information=linkedin_data)

    ice_breakers = ice_breaker_parser.parse(ice_breakers)

    return (summary_and_facts, ice_breakers, linkedin_data.get("profile_pic_url"))


if __name__ == "__main__":
    print("Hello LangChain!")
    ice_break(name="Rahul Pandey")
