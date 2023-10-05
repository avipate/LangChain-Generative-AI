# Importing required libraries
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import get_profile_url


def lookup(name: str) -> str:
    # Load the ChatOpenai model
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """given the full name {name_of_person} I want you to get a link to their linkedin
                profile page. Your answer should contain only URL."""

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you " "need get the Linked " "Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    linked_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))

    return linked_profile_url
