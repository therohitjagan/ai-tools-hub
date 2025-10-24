from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class TextSummarizer:
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        try:
            logger.info("Loading summarization model...")
            self.model = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # CPU, use 0 for GPU
            )
            logger.info("Summarization model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading summarization model: {e}")
            raise
    
    def summarize(self, text, max_length=150, min_length=50):
        """
        Summarize the input text
        
        Args:
            text (str): Input text to summarize
            max_length (int): Maximum length of summary
            min_length (int): Minimum length of summary
            
        Returns:
            str: Summarized text
        """
        try:
            if len(text.split()) < 50:
                return "Text is too short to summarize. Please provide longer text."
            
            summary = self.model(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            return summary[0]['summary_text']
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            raise Exception(f"Summarization failed: {str(e)}")

# Global instance
summarizer = TextSummarizer()