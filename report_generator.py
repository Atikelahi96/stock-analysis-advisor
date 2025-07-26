import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def generate_report(stock_data, sentiment, advice, ticker):
    logging.info("Generating detailed report...")

    # Initializing the report with the stock's overview
    report = f"**Stock Analysis Report for {ticker}**\n\n"
    report += f"**Latest Close Price**: ${stock_data['Close'].iloc[-1]:.2f}\n"
    report += f"**Sentiment**: {sentiment}\n"
    report += f"**Investment Advice**: {advice}\n"

    # Add a detailed Stock Data Overview (Last 10 entries for better context)
    report += f"\n**Stock Data Overview (Last 10 Entries)**:\n"
    report += f"{stock_data.tail(10)[['Close', 'Volume']].to_string()}\n"
    
    # Detailed Sentiment Analysis
    report += f"\n**Sentiment Analysis Explanation**:\n"
    report += f"The sentiment was classified as **{sentiment}** based on recent price movements and market conditions. "
    if sentiment == "Positive":
        report += "The stock is showing an upward trend, indicating strong investor confidence or positive market sentiment."
    elif sentiment == "Negative":
        report += "The stock is showing a downward trend, which may indicate concerns among investors or market pessimism."
    else:
        report += "The stock's performance is stable, showing little change in recent price movements."

    # Calculate and describe the latest price movement
    latest_price = stock_data['Close'].iloc[-1]
    previous_price = stock_data['Close'].iloc[-2]  # 1 hour ago
    price_change = latest_price - previous_price
    percentage_change = (price_change / previous_price) * 100

    # Actionable Insights based on price movement
    report += f"\n**Recent Price Movement**:\n"
    report += f"Latest Price: ${latest_price:.2f}\n"
    report += f"Price Change: {price_change:.2f} (${percentage_change:.2f}%)\n"

    if percentage_change > 2:
        action = "Buy: The stock is experiencing significant upward momentum."
    elif percentage_change < -2:
        action = "Sell: The stock is on a downward trend and could continue falling."
    else:
        action = "Hold: The stock's price trend is stable, but further monitoring is needed."

    report += f"\n**Actionable Insight**: {action}"

    # Adding Volatility Insights: Calculate rolling standard deviation of the last N hours
    volatility = stock_data['Close'].pct_change().rolling(window=5).std().iloc[-1] * 100  # 5-hour volatility

    report += f"\n\n**Volatility Insight**:\n"
    report += f"Recent Volatility (5-hour window): {volatility:.2f}%\n"
    if volatility > 2:
        report += "The stock is showing high volatility, suggesting higher risk in the short term."
    else:
        report += "The stock is showing moderate to low volatility, indicating relatively stable performance."

    # Identify Risks based on recent price movements
    report += f"\n\n**Risk Assessment**:\n"
    if percentage_change < -5:
        report += "The stock has experienced significant losses recently, indicating potential risk. Consider reevaluating your position."
    elif percentage_change > 5:
        report += "The stock has experienced significant gains recently. This could indicate a bubble or overvaluation, so cautious monitoring is recommended."
    else:
        report += "The stock is moving within a reasonable range, but continue monitoring any external market conditions that might impact its future performance."

    # Final remarks
    report += "\n\n**Conclusion**:\n"
    report += f"The stock is currently showing **{sentiment}** sentiment with the latest price movement suggesting a **{action.split(':')[0]}** recommendation. "
    report += "Always consider broader market conditions, and ensure your decisions align with your risk tolerance and investment goals."

    logging.info("Report generated successfully")
    return report
