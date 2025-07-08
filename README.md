
### Problem 1: Multi-Agent Financial Research Assistant

This problem requires you to design and build a multi-agent system that acts as a financial research assistant. The system will take a high-level user query about a public company, break it down, gather information from various sources, analyze it, and synthesize a comprehensive report.

The core of this problem lies in orchestrating a team of specialized agents, managing state across a complex workflow, and integrating external services for data retrieval and persistence.

---

### **Problem Description**

You are tasked with creating a "Financial Research Assistant." This AI system will receive a ticker symbol for a publicly traded company (e.g., "AAPL," "TSLA," "GOOGL") and generate a detailed research report.

The final report should be a structured document containing the following sections:

1.  **Company Profile:** A brief overview of the company, its business, and its industry.
2.  **Recent Financials:** A summary of the most recent quarterly or annual financial performance (e.g., revenue, net income, EPS).
3.  **Latest News Summary:** A compilation of the top 5-7 most relevant news articles from the past month, with a concise summary for each.
4.  **Market Sentiment Analysis:** An analysis of the overall market sentiment towards the stock based on recent news and headlines. This should be a qualitative assessment (e.g., "Bullish," "Bearish," "Neutral") with a brief justification.
5.  **Final Recommendation:** A concluding paragraph that synthesizes all the gathered information into a high-level recommendation (e.g., "The stock shows strong fundamentals and positive sentiment, suggesting a potential 'buy' for long-term investors.").

### **Workflow & Agent Design**

The system must break down the research task into sub-tasks, each handled by a specialized agent. You need to design the workflow and the interactions between these agents. A possible agent team could be:

* **Research Manager Agent:** The primary orchestrator. It receives the initial user query (the ticker symbol), defines the research plan, and delegates tasks to other agents. It is also responsible for reviewing the final report before it's presented.
* **Company Info Agent:** Tasked with finding and summarizing the company's profile.
* **Financials Agent:** Responsible for fetching and summarizing the latest financial data.
* **News Search Agent:** Scours the web or specific news APIs for recent articles about the company.
* **Sentiment Analyst Agent:** Analyzes the headlines and content of the news articles to determine market sentiment.
* **Report Writer Agent:** Gathers the structured outputs from all other agents and compiles them into the final, polished report.

A crucial part of the design is handling dependencies. For example, the `Sentiment Analyst Agent` can only run after the `News Search Agent` has completed its task. The `Report Writer Agent` must wait for all data-gathering agents to finish.

### **Technical Stack and Constraints**

You **must** adhere to the following technology constraints:

* **Orchestration:** **Langgraph**. You must model the agent interactions and the overall workflow as a graph. This includes defining the state, the nodes (agents), and the conditional edges that control the flow of execution.
* **Database:** **PostgreSQL**. The final generated report and the key findings from each agent must be saved to a PostgreSQL database. You'll need to design a simple schema to store this structured data. This simulates a real-world scenario where research is archived for future reference.
* **Caching:** **Redis**. API calls for financial data and news can be expensive and slow. You must implement a Redis cache to store the results of these external API calls. For a given ticker, if a request is made within a 24-hour window, the cached data for news and financials should be used instead of making a new API call.
* **External APIs:**
    * **Financial Data:** Use a free-tier API like **Alpha Vantage** or **Financial Modeling Prep** to get company profiles and financial statements.
    * **News Data:** Use a free-tier API like **NewsAPI.org** to fetch recent news articles.

### **Your Task**

1.  **Design the Graph:** Whiteboard the Langgraph state graph. What information needs to be carried in the state object? Which nodes represent your agents? What are the conditional edges? For example, an edge might check if the news search was successful before proceeding to sentiment analysis.
2.  **Implement the Agents:** Write the Python functions for each agent. Each function will take the current state as input, perform its task (e.g., call an API, process data), and return a dictionary to update the state.
3.  **Integrate with Redis and PostgreSQL:** Write the necessary code to:
    * Check Redis for cached data before making an API call.
    * Store the results of new API calls in Redis with an expiration time (e.g., 24 hours).
    * Save the final, structured report to a PostgreSQL table.
4.  **Build the Application:** Create a main executable script that ties everything together. It should take a stock ticker as a command-line argument, run it through your Langgraph-powered agent team, print the final report to the console, and confirm that the data has been saved to the database.

Once you have a solution, I will be ready to analyze your code. Good luck! 🚀
