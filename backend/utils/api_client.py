"""
Little Nona - OpenAI API Client
Handles all API communication with error handling
"""

import time
from typing import Optional
from config.settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIClient:
    """
    Wrapper for OpenAI API with error handling and retries.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.model = OPENAI_MODEL
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Setup OpenAI client (supports both old and new API versions)."""
        try:
            # Try new API (openai >= 1.0.0)
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            self.use_new_api = True
        except ImportError:
            # Fall back to old API
            import openai
            openai.api_key = self.api_key
            self.use_new_api = False
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        max_retries: int = 3
    ) -> str:
        """
        Generate text from OpenAI with retry logic.
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
            max_retries: Number of retry attempts
        
        Returns:
            Generated text response
        
        Raises:
            Exception: If all retries fail
        """
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                if self.use_new_api:
                    # New API
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    return response.choices[0].message.content
                else:
                    # Old API
                    import openai
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    return response.choices[0].message["content"]
            
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check if we should retry
                if attempt < max_retries - 1:
                    # Retry on rate limits, timeouts, server errors
                    if any(x in error_msg for x in ["rate_limit", "timeout", "server_error", "503", "429"]):
                        print(f"⚠️  API call failed (attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay}s...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                
                # Final attempt failed or non-retryable error
                if "rate_limit" in error_msg:
                    raise Exception("❌ Rate limit exceeded. Please wait a moment and try again.")
                elif "api_key" in error_msg or "authentication" in error_msg:
                    raise Exception("❌ Invalid API key. Please check your OpenAI API key.")
                elif "quota" in error_msg:
                    raise Exception("❌ API quota exceeded. Please check your OpenAI account.")
                else:
                    raise Exception(f"❌ API error: {str(e)}")
        
        raise Exception("Failed to call OpenAI API after all retries")
    
    def test_connection(self) -> bool:
        """Test if API connection works."""
        try:
            response = self.generate("Say hello!", max_tokens=10, temperature=0.1)
            return bool(response)
        except:
            return False


# Global client instance (will be initialized with API key)
_client: Optional[OpenAIClient] = None


def get_client(api_key: Optional[str] = None) -> OpenAIClient:
    """Get or create the OpenAI client instance."""
    global _client
    if _client is None or api_key:
        _client = OpenAIClient(api_key)
    return _client


def call_model(
    prompt: str,
    max_tokens: int = 1000,
    temperature: float = 0.7
) -> str:
    """
    Convenience function to call the model.
    Uses the global client instance.
    """
    client = get_client()
    return client.generate(prompt, max_tokens, temperature)
