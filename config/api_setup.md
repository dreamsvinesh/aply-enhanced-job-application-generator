# API Setup Instructions

## Required API Keys

### Claude API (Primary)
1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

### OpenAI API (Fallback)
1. Go to https://platform.openai.com/api-keys
2. Create an account or sign in
3. Create a new API key
4. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Install Dependencies
```bash
pip install anthropic openai requests
```

## Test Setup
```python
from modules.llm_service import call_llm, get_usage_report

# Test basic functionality
response = call_llm("Hello, this is a test", task_type="simple")
print(f"Success: {response.success}")
print(f"Content: {response.content}")
print(f"Cost: ${response.cost_usd:.4f}")

# Check usage
print(get_usage_report())
```

## Cost Monitoring

The system automatically tracks:
- Total requests and tokens used
- Costs by model
- Usage statistics saved to `cache/usage_stats.json`
- Response caching to reduce costs

## Model Selection

- **Simple tasks**: Claude Haiku (cheapest)
- **Analysis**: Claude Sonnet (balanced)
- **Generation**: Claude Sonnet (best quality)
- **Fallback**: OpenAI GPT models if Claude fails

## Security Notes

- Never commit API keys to git
- Use environment variables
- API keys are stored securely in environment only
- Usage logs do not include sensitive data