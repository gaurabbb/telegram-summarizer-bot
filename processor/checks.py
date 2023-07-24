from processor.preprocess import preprocess
from bot import send, config
import string
from textblob import TextBlob
import nltk
import re
from nltk.corpus import words



nltk.download('words')
english_words = set(words.words())

profanity_file = config['profanity_file'] 
with open(profanity_file, 'r') as file:
        profanity_set = {word.strip().lower() for word in file}
    

async def checks(user_input,  update):

    try:
        await SCcount(user_input)
        await profanity(user_input)
        await length(user_input)
        await is_comprehensible(user_input)
        await preprocess(user_input, update)

    except Exception as e:
        message = str(e)
        await send(message, update)



async def length(user_input):

    l = len(user_input)
    if l>1000:
        message = " ⚠️ Your input is too long. I have a limit of 1000 characters. Please provupdatee a shorter input."
        raise Exception(message)
    elif l<25:
        message = "⚠️ Your input is too short. Please provide a longer response."
        raise Exception(message)
    

async def is_comprehensible(user_input):

    """
    This function takes a user_input string and checks if it contains a sufficient number of valid English words.

    It first removes any special characters and emojis from the input, then splits it into a list of words.
   
    For each word, the function checks if it is a plural noun or if it is in the set of English words.
   
    If the total number of valid words is less than 20, the function raises an exception indicating that the input is not suitable for summarization.
    
    :param user_input: The input string to be checked.
    :return: None
    """
    
    pattern = r"[^\w\s\d\U0001F300-\U0001F6FF]"
    clean = re.sub(pattern, '', user_input)
    clean = clean.split()
    pluralwords = 0
    validwords = 0
    for word in clean:
        text = TextBlob(word)
        if text.tags[0][1] == 'NNS' or text.tags[0][1] == 'NNPS':  
            pluralwords += 1
            
        if word.lower() in english_words:
            validwords += 1
            
                
    totalvalidwords = validwords + pluralwords

    if totalvalidwords < 20:
        message = "⚠️ Your input is not suitable for summarization. Please provide a valid english input."
        raise Exception(message)



async def SCcount(user_input):
      
    """
    This function calculates the percentage of special characters in a given input string.
    If the percentage of special characters exceeds a predefined threshold, an exception is raised.
    :param user_input: The input string to be checked.
    :return: None
    """

    threshold = 10
    total_characters = len(user_input)
    special_characters_count = sum(1 for char in user_input if char in string.punctuation)
    percentage_special_characters = (special_characters_count / total_characters) * 100
    if percentage_special_characters > threshold:
        message = "⚠️ Invalid input. Please provide a valid input."
        raise Exception(message)    


async def profanity(user_input):
    
    words = user_input.lower().split()
    if any(word in profanity_set for word in words):
        message = "🚨 Your input contains profane language. Please provide a respectful response."
        raise Exception(message)