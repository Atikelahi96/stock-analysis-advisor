
# **Stock Analysis and Investment Advisor**

This project is an AI-powered stock analysis and investment advisory system that utilizes **financial data analysis**, **sentiment analysis**, and **investment recommendations** based on real-time stock data. It uses a **hybrid sentiment analysis model** to evaluate stock trends, perform sentiment analysis, and provide investment advice.

## **Features**

- **Stock Data Fetching**: Retrieves real-time stock data for analysis using **Yahoo Finance API**.
- **Sentiment Analysis**: Utilizes **FinBERT** (a pre-trained BERT model for financial sentiment analysis) to assess the market sentiment for stocks.
- **Investment Advice**: Provides **Buy**, **Sell**, or **Hold** advice based on **Simple Moving Averages (SMA)** and **sentiment analysis**.
- **Report Generation**: Generates a detailed stock analysis report, including sentiment, price movement, volatility insights, and actionable advice.
- **AI-driven Refinement**: Uses **Groq API** to refine and enhance the generated reports, making them more insightful and actionable for users.

## **Project Overview**

### **Key Components**:

- **financial_data_fetcher.py**: Fetches stock data from Yahoo Finance using the `yfinance` library. It retrieves stock history for the past 7 days at hourly intervals.

- **investment_advisor.py**: Calculates the **investment advice** based on the stock's **Simple Moving Average (SMA)** and compares it to the latest price.

- **sentiment_analysis.py**: 
    - **analyze_sentiment**: Uses the **FinBERT model** to analyze the sentiment of a given stock description (positive, negative, or neutral).
    - **aggregate_sentiment**: Combines both price-based sentiment and FinBERT sentiment analysis to provide a hybrid sentiment score based on recent stock price movements.

- **report_generator.py**: 
    - Generates a detailed report for the given stock, including sentiment analysis, price movement, actionable insights, and volatility assessment.

- **main.py**: 
    - The main API endpoint built with **FastAPI**, which combines all the modules to fetch stock data, analyze sentiment, provide investment advice, generate reports, and refine them using **Groq**.

- **requirements.txt**: Contains all the required Python libraries and dependencies to run the project, such as `yfinance`, `torch`, `transformers`, `FastAPI`, and others.

## **Project Setup**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/stock-analysis-advisor.git
   cd stock-analysis-advisor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root directory with your **Groq API Key**:
   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Run the FastAPI app**:
   ```bash
   uvicorn main:app --reload
   ```

   The FastAPI app will run on [http://127.0.0.1:8000](http://127.0.0.1:8000).

## **Endpoints**

### **`/analyze/{ticker}`**

**Method**: `GET`  
**Description**: Fetches the stock data, performs sentiment analysis, provides investment advice, generates a report, and refines the report using Groq AI.

**Example**:
```bash
GET http://127.0.0.1:8000/analyze/AAPL
```

## **Files Explanation**

1. **financial_data_fetcher.py**: 
   - Fetches the stock data for the last 7 days at hourly intervals from Yahoo Finance.
   - Returns the stock data in a DataFrame format.

2. **investment_advisor.py**: 
   - **provide_advice**: Calculates **investment advice** based on the **Simple Moving Average (SMA)** of the stock's closing price.

3. **sentiment_analysis.py**: 
   - **analyze_sentiment**: Analyzes the sentiment of the provided stock price description using **FinBERT**.
   - **aggregate_sentiment**: Aggregates sentiment from the price movement and FinBERT, and returns the combined sentiment score.

4. **report_generator.py**:
   - **generate_report**: Generates a detailed stock analysis report with sentiment, price change, volatility insights, actionable recommendations, and risk assessment.

5. **main.py**:
   - The core FastAPI app that integrates all modules, provides the `/analyze/{ticker}` endpoint, and uses Groq for report refinement.

6. **requirements.txt**:
   - Contains all the dependencies required for the project to work.

## **Libraries and Technologies Used**

- **FastAPI**: Web framework to build the API endpoints.
- **Groq API**: For advanced report refinement and analysis.
- **yfinance**: To fetch stock data from Yahoo Finance.
- **FinBERT (from Hugging Face Transformers)**: Used for **sentiment analysis** on stock data descriptions.
- **Pandas**: For data manipulation and analysis.
- **Torch**: For running the FinBERT model.
- **dotenv**: To load environment variables (like API keys).

## **Contributing**

1. Fork the repository.
2. Clone your fork.
3. Create a new branch (`git checkout -b feature-name`).
4. Commit your changes (`git commit -am 'Add feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request.

## **License**

This project is licensed under the MIT License.
