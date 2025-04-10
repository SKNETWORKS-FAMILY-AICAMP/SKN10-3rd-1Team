import streamlit as st
from langchain_community.tools import TavilySearchResults


def tavily_search(query: str, num_results: int = 5) -> list:
    """
    Perform a search using Tavily and return the results.
    """
    # Initialize the TavilySearchResults tool
    tavily_search = TavilySearchResults()

    # Perform the search
    results = tavily_search.run(query=query, num_results=num_results)

    # Return the search results
    return results