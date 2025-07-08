from typing import Any, TypedDict, List, Literal

from pydantic import BaseModel


class NewsArticles(BaseModel):
    items: List[str]

class CompanyInfo(BaseModel):
    company_name: str
    exchange: str    
    sector: str

class Sentiments(BaseModel):
    sentiments: Literal['negative', 'positive', 'neutral']

class FinancialReportState(TypedDict):
    ticker: str
    company_info: CompanyInfo
    financial_data: Any
    related_news: List[str]
    sentiments: Literal['negative', 'positive', 'neutral']
    final_report: str
