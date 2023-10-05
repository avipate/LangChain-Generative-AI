# Importing required libraries
from langchain.serpapi import SerpAPIWrapper

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_profile_url(text: str) -> str:
    """Searches for LinkedIn Profile Page"""
    # SerpApi is an api service that wraps around the Google api
    search = SerpAPIWrapper()
    res = search.run(f"{text}")
    return res
