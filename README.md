# Text Summarizer Telegram Bot

**Welcome to our Telegram bot - Text Summarizer!** 📚🤖

### How to Use:

1. Send any text message to the bot.
2. The bot will process your input and generate a **concise summary** for it.

### Models Used for Summarization:

It uses **Hugging Face Transformer models** to generate accurate and informative summaries for your text.

- [**BART-Large-CNN**](https://api-inference.huggingface.co/models/facebook/bart-large-cnn)
- [**BART-Large-News**](https://api-inference.huggingface.co/models/divg07/facebook-bart-large-news)
- [**BART-Large-XSum**](https://api-inference.huggingface.co/models/facebook/bart-large-xsum)

### How to Run:

To run the bot, ensure you have Python installed along with the required dependencies. Add your Telegram bot token and Hugging Face API key to the `config.json` file. Then, execute the `bot.py` script, and your bot will be up and running to summarize text for you!

Feel free to contribute and improve the bot! **Happy summarizing!** 😄📝
