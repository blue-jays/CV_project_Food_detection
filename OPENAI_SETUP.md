# 🤖 OpenAI Integration Guide

Snap2Recipe now supports **AI-powered recipe generation** using OpenAI's GPT models!

## ✨ Features

When OpenAI is enabled:
- **Dynamic recipe generation** based on detected ingredients
- **Creative and personalized** recipes tailored to your ingredients
- **Detailed instructions** with step-by-step guidance
- **Automatic fallback** to local recipes if OpenAI is unavailable

## 🔑 Setup

### 1. Get an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create new secret key**
5. Copy your API key (starts with `sk-...`)

### 2. Configure the API

Create or edit `api/.env` file:

```bash
# Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional: Choose the model (default: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini
```

**Model Options:**
- `gpt-4o-mini` - Fast and cost-effective (recommended)
- `gpt-4o` - More capable, higher cost
- `gpt-3.5-turbo` - Budget option

### 3. Restart the Backend

```bash
# The backend will auto-reload if running with --reload
# Or restart manually:
cd api
uvicorn main:app --reload
```

## 💰 Cost Considerations

OpenAI API usage is **pay-per-use**:

- **gpt-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Each recipe generation uses approximately 500-1000 tokens
- **Estimated cost**: $0.001-0.002 per recipe generation

### Cost Management Tips

1. **Use gpt-4o-mini** for most use cases (default)
2. **Set usage limits** in your OpenAI account dashboard
3. **Monitor usage** at https://platform.openai.com/usage
4. **Fallback works automatically** if quota is exceeded

## 🔄 How It Works

1. **User uploads image** → Ingredients detected
2. **User clicks "Find Recipes"**
3. **System checks** if OpenAI API key is configured
4. **If available**: OpenAI generates 5 custom recipes
5. **If not available**: Falls back to local BM25 search

## 🧪 Testing

Test the OpenAI integration:

```bash
# With OpenAI configured
curl -X POST http://localhost:8000/suggest \
  -H "Content-Type: application/json" \
  -d '{"ingredients": ["chicken", "garlic", "soy sauce"], "max_results": 3}'
```

You should see AI-generated recipes with:
- Creative titles
- Detailed ingredient lists
- Step-by-step instructions
- Cuisine types and tags

## 🛡️ Security

**Important**: Never commit your API key to version control!

✅ **Good**:
```bash
# In api/.env (gitignored)
OPENAI_API_KEY=sk-your-key-here
```

❌ **Bad**:
```python
# Don't hardcode in code!
api_key = "sk-your-key-here"
```

## 🔧 Troubleshooting

### "OpenAI API key not provided"
- Check that `OPENAI_API_KEY` is set in `api/.env`
- Restart the backend after adding the key

### "Rate limit exceeded"
- You've hit your OpenAI usage limit
- Check your usage at https://platform.openai.com/usage
- The app will automatically fallback to local recipes

### "Invalid API key"
- Verify your API key is correct
- Check that it starts with `sk-`
- Regenerate key if necessary

### Recipes not using OpenAI
- Check backend logs for errors
- Verify API key is loaded: `echo $OPENAI_API_KEY`
- Test API key with curl command above

## 📊 Comparison

| Feature | Local BM25 | OpenAI |
|---------|-----------|---------|
| Speed | ⚡ Instant | 🕐 2-5 seconds |
| Cost | 💰 Free | 💳 ~$0.001/recipe |
| Recipes | 📚 10 static | 🎨 Unlimited custom |
| Creativity | 🔄 Pre-defined | ✨ AI-generated |
| Offline | ✅ Works | ❌ Needs internet |

## 🎯 Best Practices

1. **Start with gpt-4o-mini** - Best balance of quality and cost
2. **Monitor your usage** - Set up billing alerts
3. **Test locally first** - Ensure fallback works
4. **Keep API key secure** - Never share or commit it

## 🚀 Advanced Configuration

### Custom System Prompt

Edit `api/recipes/openai_generator.py` to customize the chef's personality:

```python
"role": "system",
"content": "You are a Michelin-star chef specializing in fusion cuisine..."
```

### Adjust Temperature

Higher temperature = more creative recipes:

```python
temperature=0.8,  # 0.0 = conservative, 1.0 = very creative
```

### Change Max Tokens

For longer/shorter recipes:

```python
max_tokens=2000,  # Increase for more detailed recipes
```

---

**Enjoy AI-powered recipe generation! 🍳✨**
