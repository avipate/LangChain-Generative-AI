# Importing required libraries
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


# Base model from Pydantic
class PersonalIntel(BaseModel):
    summary: str = Field(description="Summary of the person")
    facts: List[str] = Field(description="Interesting facts about the person")
    topics_of_interest: List[str] = Field(
        description="Topics that may interest the person"
    )
    ice_breaker: List[str] = Field(
        description="Create ice breaker to open a conversation with the person"
    )

    # Function to serialize the code
    def to_dict(self):
        return {
            "summary": self.summary,
            "facts": self.facts,
            "topics_of_interest": self.topics_of_interest,
            "ice_breaker": self.ice_breaker,
        }


person_intel_parser: PydanticOutputParser = PydanticOutputParser(
    pydantic_object=PersonalIntel
)
