from transformers import pipeline
from textblob import TextBlob
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        try:
            logger.info("Loading sentiment analysis model...")
            self.model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1
            )
            logger.info("Sentiment model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading sentiment model: {e}")
            raise
    
    def analyze(self, text):
        """
        Analyze sentiment of text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment analysis results
        """
        try:
            # Transformer-based analysis
            result = self.model(text[:512])[0]  # Limit to 512 tokens
            
            # TextBlob for additional metrics
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Normalize score to 0-100
            confidence = result['score'] * 100
            
            return {
                'label': result['label'],
                'confidence': round(confidence, 2),
                'polarity': round(polarity, 2),
                'subjectivity': round(subjectivity, 2),
                'interpretation': self._interpret_sentiment(result['label'], polarity)
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            raise Exception(f"Sentiment analysis failed: {str(e)}")
    
    def _interpret_sentiment(self, label, polarity):
        """Generate human-readable interpretation"""
        if label == 'POSITIVE':
            if polarity > 0.5:
                return "Very positive sentiment detected"
            else:
                return "Positive sentiment detected"
        else:
            if polarity < -0.5:
                return "Very negative sentiment detected"
            else:
                return "Negative sentiment detected"

# Global instance
sentiment_analyzer = SentimentAnalyzer()