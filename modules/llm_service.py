#!/usr/bin/env python3
"""
LLM Service Layer
Provides unified interface for Claude and OpenAI APIs with cost tracking and error handling
"""

import json
import os
import time
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path
import hashlib

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic library not installed. Install with: pip install anthropic")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai library not installed. Install with: pip install openai")

@dataclass
class LLMResponse:
    """Standardized response from LLM services"""
    success: bool
    content: str
    model: str
    tokens_used: int
    cost_usd: float
    execution_time: float
    error_message: Optional[str] = None
    raw_response: Optional[Dict] = None

@dataclass
class UsageStats:
    """Track LLM usage and costs"""
    total_requests: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    by_model: Dict[str, Dict] = None
    
    def __post_init__(self):
        if self.by_model is None:
            self.by_model = {}

class LLMService:
    """Unified LLM service supporting Claude and OpenAI with intelligent routing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Initialize clients
        self.claude_client = None
        self.openai_client = None
        self.setup_clients()
        
        # Cost tracking
        self.usage_stats = self.load_usage_stats()
        
        # Model pricing (per 1M tokens) - Updated with latest prices
        self.pricing = {
            'claude-3-haiku': {'input': 0.25, 'output': 1.25},
            'claude-3-sonnet': {'input': 3.0, 'output': 15.0},
            'claude-3-opus': {'input': 15.0, 'output': 75.0},
            'gpt-4o-mini': {'input': 0.15, 'output': 0.60},  # CHEAPEST OPTION!
            'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50},
            'gpt-4': {'input': 30.0, 'output': 60.0},
            'gpt-4-turbo': {'input': 10.0, 'output': 30.0},
            'gpt-4o': {'input': 5.0, 'output': 15.0}
        }
        
        # Response cache for identical requests
        self.cache = {}
        self.cache_file = Path(__file__).parent.parent / "cache" / "llm_cache.json"
        self.load_cache()
        
    def setup_logging(self):
        """Setup logging for LLM service"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def setup_clients(self):
        """Initialize LLM clients with API keys"""
        
        # Load .env file if it exists
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # Claude setup
        if ANTHROPIC_AVAILABLE:
            claude_api_key = os.getenv('ANTHROPIC_API_KEY')
            if claude_api_key:
                try:
                    self.claude_client = anthropic.Anthropic(api_key=claude_api_key)
                    self.logger.info("Claude API client initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize Claude client: {e}")
            else:
                self.logger.warning("ANTHROPIC_API_KEY environment variable not set")
        
        # OpenAI setup
        if OPENAI_AVAILABLE:
            openai_api_key = os.getenv('OPENAI_API_KEY')
            if openai_api_key:
                try:
                    self.openai_client = openai.OpenAI(api_key=openai_api_key)
                    self.logger.info("OpenAI API client initialized successfully")
                except Exception as e:
                    self.logger.error(f"Failed to initialize OpenAI client: {e}")
            else:
                self.logger.warning("OPENAI_API_KEY environment variable not set")
    
    def get_cache_key(self, prompt: str, model: str, max_tokens: int) -> str:
        """Generate cache key for request"""
        content = f"{prompt}_{model}_{max_tokens}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def load_cache(self):
        """Load response cache from file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
                self.logger.info(f"Loaded {len(self.cache)} cached responses")
            except Exception as e:
                self.logger.error(f"Failed to load cache: {e}")
                self.cache = {}
    
    def save_cache(self):
        """Save response cache to file"""
        try:
            self.cache_file.parent.mkdir(exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            self.logger.error(f"Failed to save cache: {e}")
    
    def load_usage_stats(self) -> UsageStats:
        """Load usage statistics from file"""
        stats_file = Path(__file__).parent.parent / "cache" / "usage_stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                return UsageStats(**data)
            except Exception as e:
                self.logger.error(f"Failed to load usage stats: {e}")
        
        return UsageStats()
    
    def save_usage_stats(self):
        """Save usage statistics to file"""
        stats_file = Path(__file__).parent.parent / "cache" / "usage_stats.json"
        try:
            stats_file.parent.mkdir(exist_ok=True)
            with open(stats_file, 'w') as f:
                json.dump({
                    'total_requests': self.usage_stats.total_requests,
                    'total_tokens': self.usage_stats.total_tokens,
                    'total_cost_usd': self.usage_stats.total_cost_usd,
                    'by_model': self.usage_stats.by_model
                }, f)
        except Exception as e:
            self.logger.error(f"Failed to save usage stats: {e}")
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for token usage"""
        if model not in self.pricing:
            self.logger.warning(f"Unknown model for pricing: {model}")
            return 0.0
        
        pricing = self.pricing[model]
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        
        return input_cost + output_cost
    
    def update_usage_stats(self, model: str, tokens: int, cost: float):
        """Update usage statistics"""
        self.usage_stats.total_requests += 1
        self.usage_stats.total_tokens += tokens
        self.usage_stats.total_cost_usd += cost
        
        if model not in self.usage_stats.by_model:
            self.usage_stats.by_model[model] = {
                'requests': 0,
                'tokens': 0,
                'cost': 0.0
            }
        
        self.usage_stats.by_model[model]['requests'] += 1
        self.usage_stats.by_model[model]['tokens'] += tokens
        self.usage_stats.by_model[model]['cost'] += cost
        
        # Save periodically
        if self.usage_stats.total_requests % 10 == 0:
            self.save_usage_stats()
    
    def call_claude(self, prompt: str, model: str = "claude-3-sonnet-20241022", max_tokens: int = 1500, temperature: float = 0.3) -> LLMResponse:
        """Call Claude API"""
        if not self.claude_client:
            return LLMResponse(
                success=False,
                content="",
                model=model,
                tokens_used=0,
                cost_usd=0.0,
                execution_time=0.0,
                error_message="Claude client not initialized"
            )
        
        start_time = time.time()
        
        try:
            response = self.claude_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            execution_time = time.time() - start_time
            content = response.content[0].text if response.content else ""
            
            # Calculate tokens and cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            cost = self.calculate_cost(model, input_tokens, output_tokens)
            
            # Update stats
            self.update_usage_stats(model, total_tokens, cost)
            
            self.logger.info(f"Claude API call successful: {total_tokens} tokens, ${cost:.4f}")
            
            return LLMResponse(
                success=True,
                content=content,
                model=model,
                tokens_used=total_tokens,
                cost_usd=cost,
                execution_time=execution_time,
                raw_response=response.dict() if hasattr(response, 'dict') else None
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Claude API call failed: {e}")
            
            return LLMResponse(
                success=False,
                content="",
                model=model,
                tokens_used=0,
                cost_usd=0.0,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def call_openai(self, prompt: str, model: str = "gpt-4-turbo", max_tokens: int = 1500, temperature: float = 0.3) -> LLMResponse:
        """Call OpenAI API"""
        if not self.openai_client:
            return LLMResponse(
                success=False,
                content="",
                model=model,
                tokens_used=0,
                cost_usd=0.0,
                execution_time=0.0,
                error_message="OpenAI client not initialized"
            )
        
        start_time = time.time()
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            execution_time = time.time() - start_time
            content = response.choices[0].message.content if response.choices else ""
            
            # Calculate tokens and cost (approximate for OpenAI)
            prompt_tokens = response.usage.prompt_tokens if response.usage else len(prompt.split()) * 1.3
            completion_tokens = response.usage.completion_tokens if response.usage else len(content.split()) * 1.3
            total_tokens = int(prompt_tokens + completion_tokens)
            cost = self.calculate_cost(model, int(prompt_tokens), int(completion_tokens))
            
            # Update stats
            self.update_usage_stats(model, total_tokens, cost)
            
            self.logger.info(f"OpenAI API call successful: {total_tokens} tokens, ${cost:.4f}")
            
            return LLMResponse(
                success=True,
                content=content,
                model=model,
                tokens_used=total_tokens,
                cost_usd=cost,
                execution_time=execution_time,
                raw_response=response.dict() if hasattr(response, 'dict') else None
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"OpenAI API call failed: {e}")
            
            return LLMResponse(
                success=False,
                content="",
                model=model,
                tokens_used=0,
                cost_usd=0.0,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def call_llm(self, 
                 prompt: str,
                 task_type: str = "general",
                 use_cache: bool = True,
                 max_tokens: int = 1500,
                 temperature: float = 0.3) -> LLMResponse:
        """
        Intelligent LLM calling with automatic model selection
        
        Args:
            prompt: The prompt to send
            task_type: Type of task for model selection (analysis, generation, simple)
            use_cache: Whether to use cached responses
            max_tokens: Maximum tokens for response
            temperature: Controls randomness (0.0-1.0, default 0.3)
        """
        
        # Model selection optimized for cost - prioritize GPT if available
        if self.openai_client and not self.claude_client:
            # User has GPT API - use cheapest GPT model (0.2¢ per application!)
            primary_model = "gpt-4o-mini"
            fallback_model = "gpt-3.5-turbo"
        elif self.claude_client and not self.openai_client:
            # User has Claude API - use cheapest Claude (0.3¢ per application)
            primary_model = "claude-3-haiku-20240307"
            fallback_model = "claude-3-sonnet-20241022"
        elif self.openai_client and self.claude_client:
            # Both available - use Claude Haiku (cheapest option)
            primary_model = "claude-3-haiku-20240307" 
            fallback_model = "gpt-3.5-turbo"
        else:
            # No API keys - will fail gracefully
            primary_model = "gpt-3.5-turbo"
            fallback_model = "claude-3-haiku-20240307"
        
        # Check cache first
        if use_cache:
            cache_key = self.get_cache_key(prompt, primary_model, max_tokens)
            if cache_key in self.cache:
                self.logger.info("Using cached response")
                cached = self.cache[cache_key]
                return LLMResponse(**cached)
        
        # Try primary model (Claude)
        response = self.call_claude(prompt, primary_model, max_tokens)
        
        # Fallback to OpenAI if Claude fails
        if not response.success and self.openai_client:
            self.logger.warning("Claude failed, falling back to OpenAI")
            response = self.call_openai(prompt, fallback_model, max_tokens)
        
        # Cache successful responses
        if response.success and use_cache:
            cache_key = self.get_cache_key(prompt, response.model, max_tokens)
            self.cache[cache_key] = {
                'success': response.success,
                'content': response.content,
                'model': response.model,
                'tokens_used': response.tokens_used,
                'cost_usd': response.cost_usd,
                'execution_time': response.execution_time
            }
            self.save_cache()
        
        return response
    
    def get_usage_report(self) -> Dict:
        """Get detailed usage report"""
        return {
            'total_requests': self.usage_stats.total_requests,
            'total_tokens': self.usage_stats.total_tokens,
            'total_cost_usd': round(self.usage_stats.total_cost_usd, 4),
            'average_cost_per_request': round(
                self.usage_stats.total_cost_usd / max(self.usage_stats.total_requests, 1), 4
            ),
            'by_model': self.usage_stats.by_model,
            'cached_responses': len(self.cache)
        }
    
    def reset_usage_stats(self):
        """Reset usage statistics (use with caution)"""
        self.usage_stats = UsageStats()
        self.save_usage_stats()
        self.logger.info("Usage statistics reset")

# Global instance
llm_service = LLMService()

# Convenience functions
def call_llm(prompt: str, task_type: str = "general", use_cache: bool = True, max_tokens: int = 1500, temperature: float = 0.3) -> LLMResponse:
    """Convenience function for calling LLM"""
    return llm_service.call_llm(prompt, task_type, use_cache, max_tokens, temperature)

def get_usage_report() -> Dict:
    """Get current usage statistics"""
    return llm_service.get_usage_report()