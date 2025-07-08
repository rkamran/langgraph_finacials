from langchain_core.prompts import ChatPromptTemplate

company_research_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """Use the tool available to get company information using the ticker symbol below. Do not add additional information""",
        ),
        ("human", "Get the company information for stock symbol {input}"),
    ]
)


news_research_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """Your job is to find the most relevant latest news (3 at most) using the search tool provided for the stock ticker below""",
        ),
        ("human", "stock ticker: {input}"),
    ]
)


sentiment_analysis_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You're an expert in analyzing sentiments using the latest news. 
            Below is a list of latest news related to a company and you need to analyze the general sentiments""",
        ),
        ("human", "Latest News Headlines: {input}"),
    ]
)


financial_analysis_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You're an expert financial analyst who can analyze company's performance using the data provided. 
            Please use the tools provided  to pull the earning call transcript for the ticker below and create a report. Use the latest quarter""",
        ),
        ("human", "stock ticker: {input}"),
    ]
)


report_writer_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """You're an expert financial analyst who can analyze company's performance using the data provided. 
            Please use the financial data of a company and write a report solely based on the data provided and format is as per user's instructions.

            """,
        ),
        ("human", """We the following information available for {company}. Please write an executive summary 
         of the data and also format it like a financial health assessment of the company
        
         Latest News: {related_news}
         Sentiments: {sentiments}
         company Info: {company_info}
         financial Data: {financial_data}

        """),
    ]
)
