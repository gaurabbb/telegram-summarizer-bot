from gingerit.gingerit import GingerIt
import re
from processor.summarizer import summarize
from bot import send

async def preprocess(user_input, update):
    try:
       text = await clean_para(user_input)
       text = await fix(text)
       para = text
       await summarize(para, update)
    except Exception as e:
        message = "Internal server error. Please try again later."
        await send(message, update)

async def clean_para(user_input):
    # Remove repetitive special characters and emoji symbols
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251" 
                               "]+", flags=re.UNICODE)
    
    # Remove emojis using the pattern
    rmv_emoji = emoji_pattern.sub(r'', user_input)
    
    pattern = r'([^\w\s])\1+'
    text = re.sub(pattern, r'\1', rmv_emoji)
    return text

async def fix(text):
    parser = GingerIt()
    result = parser.parse(text)
    return result['result']