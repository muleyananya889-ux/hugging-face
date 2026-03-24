"""
Model definitions and utilities for the Hugging Face application
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import json
import time

class ModelType(Enum):
    """Enumeration of different model types"""
    REASONING = "reasoning"
    CONVERSATIONAL = "conversational"
    GENERAL = "general"
    EMBEDDING = "embedding"
    CODE = "code"

@dataclass
class ModelMetadata:
    """Metadata for AI models"""
    name: str
    model_id: str
    description: str
    model_type: ModelType
    context_length: int
    parameters: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "model_id": self.model_id,
            "description": self.description,
            "model_type": self.model_type.value,
            "context_length": self.context_length,
            "parameters": self.parameters,
            "tags": self.tags,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelMetadata':
        """Create from dictionary"""
        return cls(
            name=data["name"],
            model_id=data["model_id"],
            description=data["description"],
            model_type=ModelType(data["model_type"]),
            context_length=data["context_length"],
            parameters=data.get("parameters", {}),
            tags=data.get("tags", []),
            created_at=data.get("created_at", time.time())
        )

class ModelRegistry:
    """Registry for managing available models"""
    
    def __init__(self):
        self._models: Dict[str, ModelMetadata] = {}
        self._load_default_models()
    
    def _load_default_models(self):
        """Load default models into registry"""
        default_models = [
            ModelMetadata(
                name="DeepSeek-R1",
                model_id="deepseek-ai/DeepSeek-R1",
                description="Advanced reasoning model with strong problem-solving capabilities",
                model_type=ModelType.REASONING,
                context_length=128000,
                tags=["reasoning", "advanced", "problem-solving"],
                parameters={
                    "max_length": 2048,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            ),
            ModelMetadata(
                name="DialoGPT Medium",
                model_id="microsoft/DialoGPT-medium",
                description="Conversational AI model optimized for dialogue",
                model_type=ModelType.CONVERSATIONAL,
                context_length=1024,
                tags=["conversation", "dialogue", "chat"],
                parameters={
                    "max_length": 1024,
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "do_sample": True
                }
            ),
            ModelMetadata(
                name="GPT-2",
                model_id="gpt2",
                description="Classic language model, good for text generation",
                model_type=ModelType.GENERAL,
                context_length=1024,
                tags=["text-generation", "classic", "general"],
                parameters={
                    "max_length": 1024,
                    "temperature": 0.8,
                    "top_p": 0.92,
                    "do_sample": True
                }
            ),
            ModelMetadata(
                name="BLOOM",
                model_id="bigscience/bloom",
                description="Large multilingual language model",
                model_type=ModelType.GENERAL,
                context_length=2048,
                tags=["multilingual", "large", "general"],
                parameters={
                    "max_length": 2048,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            ),
            ModelMetadata(
                name="LLaMA 2 7B Chat",
                model_id="meta-llama/Llama-2-7b-chat-hf",
                description="Meta's chat-optimized LLaMA 2 model",
                model_type=ModelType.CONVERSATIONAL,
                context_length=4096,
                tags=["chat", "meta", "llama"],
                parameters={
                    "max_length": 2048,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            ),
            ModelMetadata(
                name="Code Llama",
                model_id="codellama/CodeLlama-7b-hf",
                description="Code generation model optimized for programming tasks",
                model_type=ModelType.CODE,
                context_length=16384,
                tags=["code", "programming", "development"],
                parameters={
                    "max_length": 2048,
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "do_sample": True
                }
            )
        ]
        
        for model in default_models:
            self._models[model.name] = model
    
    def register_model(self, model: ModelMetadata):
        """Register a new model"""
        self._models[model.name] = model
    
    def get_model(self, name: str) -> Optional[ModelMetadata]:
        """Get model by name"""
        return self._models.get(name)
    
    def get_model_by_id(self, model_id: str) -> Optional[ModelMetadata]:
        """Get model by model ID"""
        for model in self._models.values():
            if model.model_id == model_id:
                return model
        return None
    
    def list_models(self, model_type: ModelType = None) -> List[ModelMetadata]:
        """List all models, optionally filtered by type"""
        models = list(self._models.values())
        if model_type:
            models = [m for m in models if m.model_type == model_type]
        return models
    
    def get_models_by_tag(self, tag: str) -> List[ModelMetadata]:
        """Get models by tag"""
        return [m for m in self._models.values() if tag in m.tags]
    
    def search_models(self, query: str) -> List[ModelMetadata]:
        """Search models by name, description, or tags"""
        query = query.lower()
        results = []
        
        for model in self._models.values():
            if (query in model.name.lower() or 
                query in model.description.lower() or 
                any(query in tag.lower() for tag in model.tags)):
                results.append(model)
        
        return results
    
    def remove_model(self, name: str) -> bool:
        """Remove a model from registry"""
        if name in self._models:
            del self._models[name]
            return True
        return False
    
    def export_registry(self) -> str:
        """Export registry to JSON string"""
        models_data = [model.to_dict() for model in self._models.values()]
        return json.dumps(models_data, indent=2)
    
    def import_registry(self, json_data: str):
        """Import registry from JSON string"""
        try:
            models_data = json.loads(json_data)
            for model_dict in models_data:
                model = ModelMetadata.from_dict(model_dict)
                self._models[model.name] = model
            return True
        except Exception as e:
            raise ValueError(f"Failed to import registry: {str(e)}")

class ConversationHistory:
    """Manages conversation history with persistence"""
    
    def __init__(self, max_length: int = 100):
        self.messages: List[Dict[str, Any]] = []
        self.max_length = max_length
    
    def add_message(self, role: str, content: str, model: str = None, metadata: Dict[str, Any] = None):
        """Add a message to the conversation"""
        message = {
            "role": role,
            "content": content,
            "model": model,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        self.messages.append(message)
        
        # Trim if exceeding max length
        if len(self.messages) > self.max_length:
            self.messages = self.messages[-self.max_length:]
    
    def get_messages(self, role: str = None) -> List[Dict[str, Any]]:
        """Get messages, optionally filtered by role"""
        if role:
            return [m for m in self.messages if m["role"] == role]
        return self.messages.copy()
    
    def get_context(self, max_tokens: int = 2048) -> str:
        """Get conversation context as formatted string"""
        context_parts = []
        current_tokens = 0
        
        # Simple token estimation (rough approximation)
        for message in reversed(self.messages):
            message_text = f"{message['role']}: {message['content']}\n"
            estimated_tokens = len(message_text.split()) * 1.3  # Rough estimate
            
            if current_tokens + estimated_tokens > max_tokens:
                break
            
            context_parts.insert(0, message_text)
            current_tokens += estimated_tokens
        
        return "".join(context_parts)
    
    def clear(self):
        """Clear all messages"""
        self.messages.clear()
    
    def export_history(self) -> str:
        """Export conversation history to JSON"""
        return json.dumps(self.messages, indent=2)
    
    def import_history(self, json_data: str):
        """Import conversation history from JSON"""
        try:
            self.messages = json.loads(json_data)
            return True
        except Exception as e:
            raise ValueError(f"Failed to import history: {str(e)}")

@dataclass
class UserPreferences:
    """User preferences and settings"""
    default_model: str = "DeepSeek-R1"
    theme: str = "light"
    auto_save: bool = True
    max_history_length: int = 100
    default_parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "default_model": self.default_model,
            "theme": self.theme,
            "auto_save": self.auto_save,
            "max_history_length": self.max_history_length,
            "default_parameters": self.default_parameters
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create from dictionary"""
        return cls(
            default_model=data.get("default_model", "DeepSeek-R1"),
            theme=data.get("theme", "light"),
            auto_save=data.get("auto_save", True),
            max_history_length=data.get("max_history_length", 100),
            default_parameters=data.get("default_parameters", {})
        )
