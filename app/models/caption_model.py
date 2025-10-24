from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ImageCaptioner:
    def __init__(self):
        self.processor = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        try:
            logger.info("Loading image captioning model...")
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            logger.info("Image captioning model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading image captioning model: {e}")
            raise
    
    def generate_caption(self, image_path, max_length=50):
        """
        Generate caption for image
        
        Args:
            image_path (str): Path to image file
            max_length (int): Maximum caption length
            
        Returns:
            str: Generated caption
        """
        try:
            # Open and process image
            image = Image.open(image_path).convert('RGB')
            
            # Process image
            inputs = self.processor(image, return_tensors="pt")
            
            # Generate caption
            output = self.model.generate(**inputs, max_length=max_length)
            
            # Decode caption
            caption = self.processor.decode(output[0], skip_special_tokens=True)
            
            return caption
        except Exception as e:
            logger.error(f"Image captioning error: {e}")
            raise Exception(f"Image captioning failed: {str(e)}")
    
    def generate_detailed_caption(self, image_path):
        """Generate a more detailed caption with conditional generation"""
        try:
            image = Image.open(image_path).convert('RGB')
            
            # Unconditional caption
            inputs = self.processor(image, return_tensors="pt")
            output = self.model.generate(**inputs)
            caption = self.processor.decode(output[0], skip_special_tokens=True)
            
            # Conditional caption with prompt
            prompt = "a detailed description of"
            inputs = self.processor(image, text=prompt, return_tensors="pt")
            output = self.model.generate(**inputs, max_length=100)
            detailed_caption = self.processor.decode(output[0], skip_special_tokens=True)
            
            return {
                'simple': caption,
                'detailed': detailed_caption
            }
        except Exception as e:
            logger.error(f"Detailed captioning error: {e}")
            raise Exception(f"Detailed captioning failed: {str(e)}")

# Global instance
image_captioner = ImageCaptioner()