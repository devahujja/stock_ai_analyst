import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from tavily import TavilyClient

from pathlib import Path
load_dotenv(Path(__file__).parent / ".env")

def get_latest_news(company_name):
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        return "News unavailable: TAVILY_API_KEY is not set."

    try:
        client = TavilyClient(api_key=tavily_key)
        results = client.search(
            query=f"{company_name} stock news latest",
            max_results=5
        )
        news_text = ""
        for i, result in enumerate(results.get('results', [])):
            news_text += f"\nNews {i+1}: {result.get('title', 'No title')}\n"
            news_text += f"{result.get('content', 'No content available')}\n"

        if not news_text.strip():
            return "News unavailable: no results found from Tavily."

        return news_text
    except Exception as exc:
        return f"News unavailable: Tavily request failed ({exc})."

def analyse_stock(stock_data, news):
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return (
            "### AI analysis unavailable\n"
            "`GROQ_API_KEY` is not set. Add it to your `.env` file and restart the app.\n\n"
            "### Quick Snapshot\n"
            f"- Company: {stock_data['company_name']}\n"
            f"- Current Price: {stock_data['current_price']}\n"
            f"- 30 Day Change: {stock_data['change_30d_percent']}%\n"
            f"- 52 Week High: {stock_data['52_week_high']}\n"
            f"- 52 Week Low: {stock_data['52_week_low']}\n"
            f"- PE Ratio: {stock_data['pe_ratio']}\n"
            f"- Market Cap: {stock_data['market_cap']}\n"
        )

    llm = ChatGroq(
        api_key=groq_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )
    system = SystemMessage(content="""
    You are an expert stock market analyst.
    Give a clear structured report with these sections:
    1. Stock Overview
    2. Price Performance Analysis  
    3. News Sentiment (positive/negative/neutral)
    4. Key Risks
    5. Final Verdict (Buy / Hold / Sell) with reason
    Be specific and use the numbers provided.
    """)
    user = HumanMessage(content=f"""
    Analyse this stock:
    Company: {stock_data['company_name']}
    Current Price: {stock_data['current_price']}
    30 Day Change: {stock_data['change_30d_percent']}%
    52 Week High: {stock_data['52_week_high']}
    52 Week Low: {stock_data['52_week_low']}
    PE Ratio: {stock_data['pe_ratio']}
    Market Cap: {stock_data['market_cap']}
    Latest News:
    {news}
    Give a full analyst report.
    """)
    try:
        response = llm.invoke([system, user])
        return response.content
    except Exception as exc:
        return f"AI analysis failed: {exc}"
