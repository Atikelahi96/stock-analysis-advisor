from transformers import BertTokenizer, BertForSequenceClassification
import torch
import logging

logging.basicConfig(level=logging.INFO)

# Load pre-trained FinBERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')

def analyze_sentiment(text: str):
    """
    Analyze sentiment using FinBERT.
    This function processes a given text and returns the sentiment as 'Positive', 'Neutral', or 'Negative'.
    """
    logging.info(f"Analyzing sentiment for: {text}")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    sentiment = torch.argmax(logits, dim=1).item()
    sentiment_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    sentiment_result = sentiment_map[sentiment]
    logging.info(f"Sentiment analysis result: {sentiment_result}")
    return sentiment_result


def aggregate_sentiment(stock_data, model, tokenizer):
    """
    Aggregate sentiment over the past 24 hours using a hybrid approach.
    This function evaluates sentiment based on price change (price-based sentiment)
    and generates sentiment using FinBERT for each hourly price change.
    """
    sentiment_scores = []  # List to store sentiment scores from price-based approach
    finbert_sentiment_scores = []  # List to store sentiment scores from FinBERT

    # Loop through stock data to generate sentiment for each 1-hour period
    for i in range(len(stock_data) - 1):  # Loop through all data points
        latest_price = stock_data['Close'].iloc[i]
        previous_price = stock_data['Close'].iloc[i + 1]  # Next data point
        price_change = latest_price - previous_price
        percentage_change = (price_change / previous_price) * 100

        # Improved sentence formatting based on price change
        if price_change > 0:
            sentiment_text = f"The stock price has increased by {percentage_change:.2f}% in the last hour."
        elif price_change < 0:
            sentiment_text = f"The stock price has decreased by {abs(percentage_change):.2f}% in the last hour."
        else:
            sentiment_text = "The stock price has remained unchanged over the last hour."

        # Price-based sentiment: Positive (1), Negative (-1), Neutral (0)
        if price_change > 0:
            sentiment_scores.append(1)  # Positive sentiment
        elif price_change < 0:
            sentiment_scores.append(-1)  # Negative sentiment
        else:
            sentiment_scores.append(0)  # Neutral sentiment
        
        # FinBERT sentiment using model-based approach
        sentiment = analyze_sentiment(sentiment_text)
        finbert_sentiment_scores.append(sentiment)  # Store FinBERT's sentiment output

    # Combine both sentiment sources using majority voting or simple aggregation
    combined_sentiment = combine_sentiments(sentiment_scores, finbert_sentiment_scores)

    return combined_sentiment


def combine_sentiments(price_based_scores, finbert_scores):
    """
    Combine the sentiment scores from both approaches with a thresholding strategy.
    - Price-based sentiment is based on price change direction (Positive/Negative/Neutral).
    - FinBERT sentiment is based on sentence analysis.
    """
    # Sum of price-based sentiment scores
    price_based_final = sum(price_based_scores)

    # Sum of FinBERT sentiment scores (convert Positive to 1, Negative to -1, Neutral to 0)
    finbert_final = sum([1 if x == 'Positive' else -1 if x == 'Negative' else 0 for x in finbert_scores])

    # Optionally: Apply a threshold to small price changes and boost price-based sentiment
    if abs(price_based_final) < 2 and finbert_final == 0:
        # Give more weight to price-based sentiment when price changes are small
        final_sentiment = "Neutral"
    elif price_based_final > 0 and finbert_final > 0:
        final_sentiment = "Positive"
    elif price_based_final < 0 and finbert_final < 0:
        final_sentiment = "Negative"
    else:
        # If there's a conflict, choose the stronger sentiment from both
        final_sentiment = "Neutral" if price_based_final == 0 and finbert_final == 0 else \
                          "Positive" if price_based_final > 0 or finbert_final > 0 else "Negative"

    return final_sentiment
