from fastapi import FastAPI
import time
from financial_data_fetcher import fetch_stock_data
from sentiment_analysis import aggregate_sentiment
from investment_advisor import provide_advice
from report_generator import generate_report
import os
from dotenv import load_dotenv
from groq import Groq
import logging
from transformers import BertTokenizer, BertForSequenceClassification

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load pre-trained FinBERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/analyze/{ticker}")
def analyze_stock(ticker: str):
    start_time = time.time()

    logger.info(f"Fetching stock data for {ticker}...")
    stock_data = fetch_stock_data(ticker)
    logger.info(f"Time taken for stock data fetch: {time.time() - start_time} seconds")

    # Check if stock_data is empty
    if stock_data.empty:
        logger.error(f"No stock data available for {ticker}.")
        return {"error": f"No stock data available for {ticker}."}

    # Ensure there is enough data to calculate price change
    if len(stock_data) < 2:
        logger.error("Insufficient data to calculate price change.")
        return {"error": "Not enough data to calculate price change."}

    # Use the hybrid sentiment analysis (price-based + FinBERT-based)
    combined_sentiment = aggregate_sentiment(stock_data, model, tokenizer)
    logger.info(f"Combined sentiment analysis: {combined_sentiment}")

    # Provide investment advice
    advice = provide_advice(stock_data)
    logger.info(f"Time taken for providing advice: {time.time() - start_time} seconds")

    # Generate the basic report
    report = generate_report(stock_data, combined_sentiment, advice, ticker)  # Pass ticker here
    logger.info(f"Time taken for report generation: {time.time() - start_time} seconds")

    # Create a prompt that instructs Groq to refine and analyze the report, considering 24-hour sentiment
    prompt = f"""
    You are a professional AI stock advisor model. Your task is to analyze and refine the provided stock analysis report based on the stock's **recent 24-hour performance**. Please perform the following:

    1. **Analyze the Report**: Carefully read and analyze the stock analysis report. Identify areas where the report can be improved in terms of clarity, structure, and depth, specifically focusing on **recent 24-hour stock movements**.

    2. **Refine the Sentiment Analysis**: Provide more detailed reasoning behind the sentiment classification (e.g., why it’s positive, neutral, or negative). Make sure the sentiment analysis aligns with the **stock's recent 24-hour performance**.

    3. **Improve Actionable Insights**: Based on the sentiment, stock movement, and **24-hour price trends**, provide **clear, actionable insights** for the user. Ensure that the report gives specific recommendations such as **Buy**, **Sell**, or **Hold**, with appropriate reasoning.

    4. **Assess Volatility and Risks**: Add insights on **stock volatility** and potential **risks** observed over the last 24 hours. Highlight any **recent volatility spikes**, rapid price changes, or potential **external market risks** that could affect the stock’s immediate future.

    5. **Make the Report More Readable**: Ensure the report is concise, well-organized, and uses clear, professional language. Avoid jargon and ensure that the advice and insights are easy to understand for a broad audience.

    6. **Provide a Clear Conclusion**: Summarize the key findings of the report in a **concise conclusion**. This should reiterate the actionable insights, volatility, risks, and final investment advice, especially focusing on **recent market conditions** (within 24 hours).

    **Input Report:**
    {report}

    Please provide the **final refined version** of the report after your analysis. Ensure it is well-structured, insightful, and professional.
    """

    # Pass the generated report to Groq for final analysis and refinement with the detailed prompt
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    # Get the advanced analysis from Groq
    advanced_analysis = chat_completion.choices[0].message.content
    logger.info(f"Time taken for Groq API call: {time.time() - start_time} seconds")

    # Returning the refined report with Groq's advanced analysis 
    refined_report = f"**Final Stock Analysis Report**\n\n{advanced_analysis}"

    return {"advanced_analysis": refined_report}
