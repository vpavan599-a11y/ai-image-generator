import re
import hashlib
import json
from datetime import datetime
from typing import Dict, Any

class Helpers:
    @staticmethod
    def validate_prompt(prompt: str) -> bool:
        """
        Validate the user prompt
        
        Args:
            prompt (str): The prompt to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not prompt or not isinstance(prompt, str):
            return False
        
        # Check length
        if len(prompt.strip()) < 3 or len(prompt) > 1000:
            return False
        
        # Check for potentially harmful content (basic check)
        harmful_patterns = [
            r'violence', r'gore', r'nude', r'explicit',
            r'offensive', r'hate speech', r'discrimination'
        ]
        
        prompt_lower = prompt.lower()
        for pattern in harmful_patterns:
            if re.search(pattern, prompt_lower):
                return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        # Remove any path components
        filename = filename.replace('/', '').replace('\\', '')
        # Remove special characters
        filename = re.sub(r'[^\w\-_\. ]', '', filename)
        return filename
    
    @staticmethod
    def generate_image_id(prompt: str, style: str) -> str:
        """Generate a unique ID for an image based on prompt and timestamp"""
        timestamp = datetime.now().isoformat()
        unique_string = f"{prompt}_{style}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:10]
    
    @staticmethod
    def format_prompt_for_display(prompt: str, max_length: int = 50) -> str:
        """Format a prompt for display (truncate if too long)"""
        if len(prompt) <= max_length:
            return prompt
        return prompt[:max_length - 3] + "..."
    
    @staticmethod
    def create_error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
        """Create a standardized error response"""
        return {
            'success': False,
            'error': message,
            'status_code': status_code,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def create_success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        """Create a standardized success response"""
        response = {
            'success': True,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        if data is not None:
            response['data'] = data
        return response
    
    @staticmethod
    def estimate_processing_time(prompt_length: int) -> int:
        """Estimate processing time based on prompt length"""
        base_time = 5  # seconds
        if prompt_length < 50:
            return base_time
        elif prompt_length < 200:
            return base_time + 2
        else:
            return base_time + 5