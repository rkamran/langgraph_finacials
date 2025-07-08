import sys
from typing import List, Literal, TypedDict, Annotated
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langgraph.graph import START, END

from langgraph.graph import StateGraph
from datatypes import FinancialReportState, CompanyInfo, NewsArticles, Sentiments
from tools import get_financial_data, get_llm, get_logger, get_company_info
from prompts import (
    company_research_prompt, 
    news_research_prompt, 
    sentiment_analysis_prompt, 
    financial_analysis_prompt,
    report_writer_prompt
)

#region Globals
llm = get_llm("llama3.2")
logger = get_logger(__name__)
#endregion

#region  Agents
k_researcher_supervisor_agent = "researcher_supervisor_agent"
def researcher_supervisor_agent(state: FinancialReportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")


# --
k_news_research_agent = "news_research_agent"
def news_research_agent(state: FinancialReportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    assert state.get('ticker') is not None, "We can't do research without ticker"    
    
    search_tool = TavilySearch(max_results=10)

    agent = create_react_agent(
        model=llm.bind_tools([search_tool]), 
        response_format=NewsArticles,
        tools=[search_tool]
    )

    results = agent.invoke(news_research_prompt.invoke({"input": state['ticker']}))

    return {"related_news": results.items}


# --
k_financial_data_analyst_agent = "financial_data_analyst_agent"
def financial_data_analyst_agent(state: FinancialReportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")

    assert state.get('ticker') is not None, "We can't do research without ticker"    
    research_agent = create_react_agent(
        model=llm.bind_tools([get_financial_data]),        
        tools=[get_financial_data]
    )

    result = research_agent.invoke(financial_analysis_prompt.invoke({"input": state['ticker']}))    
    return {"financial_data": result}


# -- 
k_company_info_research_agent = "company_info_research_agent"
def company_info_research_agent(state: FinancialReportState):    
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")

    assert state.get('ticker') is not None, "We can't do research without ticker"    
    research_agent = create_react_agent(
        model=llm.bind_tools([get_company_info]),
        response_format=CompanyInfo,
        tools=[get_company_info]
    )

    result = research_agent.invoke(company_research_prompt.invoke({"input": state['ticker']}))
    
    return {"company_info": result}


k_sentiment_analysis_agent = "sentiment_analysis_agent"
def sentiment_analysis_agent(state: FinancialReportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")
    assert state.get('related_news') is not None, "We can't do research without ticker"  
    assert len(state.get('related_news')) > 0, "At lest one headline news items requried to run sentiment analysis"

    agent = create_react_agent(
        model=llm,
        response_format=Sentiments,
        tools=[]
    )

    response = agent.invoke(sentiment_analysis_prompt.invoke({"input": state.get('related_news')}))
    return {"sentiments": response.sentiments}


# k_report_writer_agent = "report_writer_agent"
# def report_writer_agent(state: FinancialReportState):
#     logger.info(f"Running {sys._getframe(0).f_code.co_name}")
#     pipeline = report_writer_prompt | llm
#     response = pipeline.invoke({
#         "company": state.get("company_info").get("company_name"),
#         "related_news": state.get("related_news"),
#         "sentiments": state.get("sentiments"),
#         "company_info": state.get("company_info"),
#         "financial_data": state.get("financial_data")
#     })
#
#
#     return {"final_report": response.content}


k_report_writer_agent = "report_writer_agent"
def report_writer_agent(state: FinancialReportState):
    logger.info(f"Running {sys._getframe(0).f_code.co_name}")

    # Ensure we have the ticker to name the file
    assert state.get('ticker') is not None, "Ticker is required to create the report file."

    pipeline = report_writer_prompt | llm
    response = pipeline.invoke({
        "company": state.get("company_info").get("company_name"),
        "related_news": state.get("related_news"),
        "sentiments": state.get("sentiments"),
        "company_info": state.get("company_info"),
        "financial_data": state.get("financial_data")
    })

    report_content = response.content
    ticker = state.get("ticker")
    file_name = f"{ticker}_financial_report.md"

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(report_content)
        logger.info(f"Financial report saved to {file_name}")
    except IOError as e:
        logger.error(f"Error writing report to file {file_name}: {e}")

    return {"final_report": report_content}
#endregion 


#region Execution Graph

sentiments_builder = StateGraph(FinancialReportState)

sentiments_builder.add_node(k_news_research_agent, news_research_agent)
sentiments_builder.add_node(k_sentiment_analysis_agent, sentiment_analysis_agent)
sentiments_builder.set_entry_point(k_news_research_agent)

k_sentiment_graph = "sentiment_graph"
sentiments_graph = sentiments_builder.compile()

builder = StateGraph(FinancialReportState)

builder.add_node(k_researcher_supervisor_agent, researcher_supervisor_agent)
builder.add_node(k_financial_data_analyst_agent, financial_data_analyst_agent)
builder.add_node(k_company_info_research_agent, company_info_research_agent)
builder.add_node(k_sentiment_graph, sentiments_graph)
builder.add_node(k_report_writer_agent, report_writer_agent)

builder.add_edge(START, k_researcher_supervisor_agent)

builder.add_edge(k_researcher_supervisor_agent, k_financial_data_analyst_agent)
builder.add_edge(k_researcher_supervisor_agent, k_company_info_research_agent)
builder.add_edge(k_researcher_supervisor_agent, k_sentiment_graph)

builder.add_edge(k_sentiment_graph, k_report_writer_agent)
builder.add_edge(k_financial_data_analyst_agent, k_report_writer_agent)
builder.add_edge(k_company_info_research_agent, k_report_writer_agent)

builder.add_edge(k_report_writer_agent, END)

graph = builder.compile()
#endregion 