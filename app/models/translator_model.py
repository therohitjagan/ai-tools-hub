from transformers import MarianMTModel, MarianTokenizer
import logging

logger = logging.getLogger(__name__)

class Translator:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        
        # Supported language pairs
        self.language_pairs = {
            'en-es': 'Helsinki-NLP/opus-mt-en-es',
            'en-fr': 'Helsinki-NLP/opus-mt-en-fr',
            'en-de': 'Helsinki-NLP/opus-mt-en-de',
            'en-it': 'Helsinki-NLP/opus-mt-en-it',
            'es-en': 'Helsinki-NLP/opus-mt-es-en',
            'fr-en': 'Helsinki-NLP/opus-mt-fr-en',
            'de-en': 'Helsinki-NLP/opus-mt-de-en',
        }
    
    def _load_model(self, lang_pair):
        """Load model and tokenizer for specific language pair"""
        if lang_pair not in self.models:
            try:
                model_name = self.language_pairs[lang_pair]
                logger.info(f"Loading translation model: {model_name}")
                
                self.tokenizers[lang_pair] = MarianTokenizer.from_pretrained(model_name)
                self.models[lang_pair] = MarianMTModel.from_pretrained(model_name)
                
                logger.info(f"Model loaded successfully: {lang_pair}")
            except Exception as e:
                logger.error(f"Error loading translation model {lang_pair}: {e}")
                raise
    
    def translate(self, text, source_lang, target_lang):
        """
        Translate text from source to target language
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language code
            target_lang (str): Target language code
            
        Returns:
            str: Translated text
        """
        lang_pair = f"{source_lang}-{target_lang}"
        
        if lang_pair not in self.language_pairs:
            raise ValueError(f"Translation pair {lang_pair} not supported")
        
        try:
            self._load_model(lang_pair)
            
            # Tokenize
            inputs = self.tokenizers[lang_pair](text, return_tensors="pt", padding=True)
            
            # Translate
            translated = self.models[lang_pair].generate(**inputs)
            
            # Decode
            translation = self.tokenizers[lang_pair].decode(translated[0], skip_special_tokens=True)
            
            return translation
        except Exception as e:
            logger.error(f"Translation error: {e}")
            raise Exception(f"Translation failed: {str(e)}")
    
    def get_supported_languages(self):
        """Return list of supported language pairs"""
        return list(self.language_pairs.keys())

# Global instance
translator = Translator()