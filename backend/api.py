"""
Backend API module for Hugging Face integration
Handles model communication, error handling, and response processing
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for model parameters"""
    max_length: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    do_sample: bool = True
    return_full_text: bool = False

class HuggingFaceAPI:
    """Enhanced Hugging Face API client with error handling and caching"""
    
    def __init__(self, api_key: str, base_url: str = "https://api-inference.huggingface.co/models"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Cache for model info
        self._model_cache = {}
        
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get detailed information about a model"""
        if model_name in self._model_cache:
            return self._model_cache[model_name]
            
        try:
            response = self.session.get(f"https://huggingface.co/api/models/{model_name}")
            if response.status_code == 200:
                model_info = response.json()
                self._model_cache[model_name] = model_info
                return model_info
            else:
                logger.warning(f"Failed to get model info for {model_name}: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Error getting model info for {model_name}: {str(e)}")
            return {}
    
    def query_model(self, model_name: str, inputs: str, config: ModelConfig = None) -> Dict[str, Any]:
        """
        Query a model with enhanced error handling and retry logic
        
        Args:
            model_name: Hugging Face model identifier
            inputs: Input text for the model
            config: Model configuration parameters
            
        Returns:
            Dictionary containing success status and response data
        """
        if config is None:
            config = ModelConfig()
            
        # Prepare request payload
        payload = {
            "inputs": inputs,
            "parameters": {
                "max_length": config.max_length,
                "temperature": config.temperature,
                "top_p": config.top_p,
                "top_k": config.top_k,
                "do_sample": config.do_sample,
                "return_full_text": config.return_full_text
            }
        }
        
        # Retry logic
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Querying model {model_name}, attempt {attempt + 1}")
                
                response = self.session.post(
                    f"{self.base_url}/{model_name}",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return self._process_success_response(response.json(), inputs)
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    logger.warning(f"Model {model_name} is loading, waiting...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    return self._process_error_response(response, model_name)
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1} for model {model_name}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                return {"success": False, "error": "Request timeout after multiple retries"}
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error for model {model_name}: {str(e)}")
                return {"success": False, "error": f"Request error: {str(e)}"}
        
        return {"success": False, "error": "Max retries exceeded"}
    
    def _process_success_response(self, response_data: Any, original_input: str) -> Dict[str, Any]:
        """Process successful API response"""
        try:
            if isinstance(response_data, list) and len(response_data) > 0:
                generated_text = response_data[0].get("generated_text", "")
                
                # Clean up the response
                if generated_text.startswith(original_input):
                    clean_response = generated_text[len(original_input):].strip()
                else:
                    clean_response = generated_text.strip()
                
                return {
                    "success": True,
                    "response": clean_response,
                    "full_response": generated_text,
                    "model_info": response_data[0] if response_data else {}
                }
            else:
                return {
                    "success": False,
                    "error": "Unexpected response format"
                }
                
        except Exception as e:
            logger.error(f"Error processing success response: {str(e)}")
            return {"success": False, "error": f"Response processing error: {str(e)}"}
    
    def _process_error_response(self, response: requests.Response, model_name: str) -> Dict[str, Any]:
        """Process error response from API"""
        try:
            error_data = response.json()
            error_message = error_data.get("error", "Unknown error")
        except:
            error_message = response.text or "Unknown error"
        
        return {
            "success": False,
            "error": f"API Error ({response.status_code}): {error_message}",
            "status_code": response.status_code,
            "model": model_name
        }
    
    def get_available_models(self) -> Dict[str, str]:
        """Get curated list of available models with descriptions"""
        return {
            "DeepSeek-R1": {
                "id": "deepseek-ai/DeepSeek-R1",
                "description": "Advanced reasoning model with strong problem-solving capabilities",
                "type": "reasoning",
                "context_length": 128000
            },
            "DialoGPT Medium": {
                "id": "microsoft/DialoGPT-medium",
                "description": "Conversational AI model optimized for dialogue",
                "type": "conversational",
                "context_length": 1024
            },
            "GPT-2": {
                "id": "gpt2",
                "description": "Classic language model, good for text generation",
                "type": "general",
                "context_length": 1024
            },
            "BLOOM": {
                "id": "bigscience/bloom",
                "description": "Large multilingual language model",
                "type": "general",
                "context_length": 2048
            },
            "LLaMA 2 7B Chat": {
                "id": "meta-llama/Llama-2-7b-chat-hf",
                "description": "Meta's chat-optimized LLaMA 2 model",
                "type": "conversational",
                "context_length": 4096
            }
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API connection with a simple model"""
        try:
            result = self.query_model("gpt2", "Hello", ModelConfig(max_length=10))
            return result
        except Exception as e:
            return {"success": False, "error": f"Connection test failed: {str(e)}"}

class ModelManager:
    """Manages multiple model instances and provides unified interface"""
    
    def __init__(self, api_key: str):
        self.api = HuggingFaceAPI(api_key)
        self.active_model = None
        self.model_configs = {}
    
    def set_active_model(self, model_name: str, config: ModelConfig = None):
        """Set the active model for queries"""
        self.active_model = model_name
        if config:
            self.model_configs[model_name] = config
    
    def query(self, text: str, model_name: str = None, config: ModelConfig = None) -> Dict[str, Any]:
        """Query the specified model or active model"""
        target_model = model_name or self.active_model
        if not target_model:
            return {"success": False, "error": "No model specified"}
        
        target_config = config or self.model_configs.get(target_model) or ModelConfig()
        return self.api.query_model(target_model, text, target_config)
    
    def get_model_status(self, model_name: str) -> Dict[str, Any]:
        """Check if a model is available and responsive"""
        try:
            # Quick test with minimal parameters
            test_config = ModelConfig(max_length=5)
            result = self.api.query_model(model_name, "Test", test_config)
            return {
                "available": result["success"],
                "status": "online" if result["success"] else "offline",
                "last_check": time.time()
            }
        except Exception as e:
            return {
                "available": False,
                "status": "error",
                "error": str(e),
                "last_check": time.time()
            }
