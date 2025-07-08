from langchain.tools import tool
from langchain_core.language_models import BaseChatModel
from langchain.chat_models import init_chat_model
import logging
import requests
import os
import sys
from cache import get_cache, set_cache

from dotenv import load_dotenv
load_dotenv()

def get_logger(name: str, level=logging.INFO):    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name) 
    logger.addHandler(stream_handler)
    logger.setLevel(level)    
    
    return logger

logger = get_logger(__name__)

@tool
def get_financial_data(ticker: str, quarter='2025Q1') -> Dict:
    """
    Gets the transcript of the earning call of the company represented by the stock ticker and selected quarter

    args:
        ticker: Stock ticker
        quarter: Fiscal quarter in the format YYYYQX

    """
    logger.info(f"Executing  {get_financial_data}")

    # First check if we have it in cache?
    cache_key = f"{ticker}_{quarter}"
    data = get_cache(cache_key)
    if data:
        logger.info("Cache hit")
        return data
    
    logger.info("Cache miss")
    url = f'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol={ticker}&quarter={quarter}&apikey={os.getenv("ALPHA_VINTAGE_API_KEY")}'
    r = requests.get(url)
    data = r.json()
    
    #cache it for later user
    set_cache(cache_key, data)
    return data


@tool
def get_company_info(ticker: str):
    """Get the company information based on provided ticker symbol"""
    logger.info(f"Executing  {get_company_info}")
    
    # First check if we have it in cache?
    cache_key = f"company_info_{ticker}"
    data = get_cache(cache_key)
    if data:
        logger.info("Cache hit")
        return data
    
    logger.info("Cache miss")

    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={os.getenv("ALPHA_VINTAGE_API_KEY")}'
    r = requests.get(url)
    data = r.json()

    #cache it for later user
    set_cache(cache_key, data)
    
    return data



def get_llm(model_name: str, temperature: float = 0) -> BaseChatModel:
    return init_chat_model(
        model=f"ollama:{model_name}", 
        base_url=f'{os.getenv("OLLAMA_BASE_URL")}', 
        temperature=temperature
    )


        