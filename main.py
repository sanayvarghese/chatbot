import re
import datetime
import random
import wikipedia
import googlesearch
from wikipediaapi import Wikipedia
import time
import socket
import time
print('''\033[92m\033[4mA Simple Chat Bot made with Python\033[0m
By: \033[91mSanay George Varghese\033[0m
Website: \033[34mhttps://sanayvarghese.tk\033[0m''')
print("\033[93mPress CTRL + C to exit or type exit(or q or quit) to exit out of the bot \033[0m \n")

# Function for check the probability of the occurence of the recognized words in the user input
def messageProbability(user_message, recognised_words, single_response=False, required_word=[]):
    message_certainity = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainity += 1

    percentage = float(message_certainity) / float(len(recognised_words))

    for word in required_word:
        if word not in user_message:
            has_required_words = False
        else:
            has_required_words= True
   
    if has_required_words  or single_response:
        return int(percentage*100)
    else:
        return 0


def check_messages(message):
    now = datetime.datetime.now()
    hour = now.hour
    highest_prop_list = {}

    # Function to add a response to the highest_prop_list dictionary by calculating the probability
    def response(bot_response, list_of_words, single_response=False, required_word=[]):
        nonlocal highest_prop_list
        highest_prop_list[bot_response] = messageProbability(
            message, list_of_words, single_response=single_response, required_word=required_word)

    # Response ++++++++++++++++++++++++++++++++++++++++++
    
    hello_responses = ["Hello! How can I help you?","Hey! How can I help you?", "What\'s up! how can I Help you?"]
    response(hello_responses[random.randint(0,len(hello_responses)-1)], ["hello", "hi", "sup","hey", "heyo"], single_response=True)

    response(("Good morning!" if hour < 12 else "Good afternoon!" if hour <
             18 else "Good evening!")+" How are you doing?", ["good evening", "good afternoon", "good morning","morning","evening","afternoon","good"], single_response=True)

    response("I\'am doing fine and you?", [
             "how", "doing", "have", "are", "you"], single_response=True, required_word=["doing"])

    response("I\'am doing nothing. I am here to help you with your questions :)",["what","are","you","doing","up","to"],single_response=True)

    response("I\'am a ChatBot made with Python Programming Language. Made By Sanay George Varghese",["who","are","you","made","creator"],single_response=True,required_word=["who"])

    response("I\'am glad to hear that!",["i","am","doing","great","good","well","fine","happy","ok"],single_response=True,required_word=["doing","fine","am","i"])

    response("Current date and time is "+ now.strftime("%I:%M %p %d/%m/%Y "), ["what","is","the","current","time","tell","me","which","this","date","month","year","weak"],single_response=True,required_word=["time","year","month","date","which","what","is","the","now"])

    response("You\'re welcome! I\'m glad I could help. Let me know if there's anything else I can do for you.",["you","thank","thanks","alot","thenks","great","its","helpfull","worked","help","fine","nice","answer","thankyou"],single_response=True,required_word=["thankyou","thanks","helpfull","thank","you","thankyou"])
    
    
    response("Bye! See u later :>",["bye","good","see","you","u","later","exit","quit","q","bie"],single_response=True,required_word=["bye","good","exit","q","quit"],)

    # Code for search in google and wikipedia
    if ("who" in message or "what" in message or "about"  in message or "tell" in message or  "on"  in message or "which"  in message or "is" in message ):
        socket.setdefaulttimeout(10)
        try:
            googleSearchUrls = list(googlesearch.search(" ".join(message),num_results=1))
            for url in googleSearchUrls:
                if "wikipedia" in url:
                        # print(url)
                        data = Wikipedia(language='en').page(re.split("/", url)[-1]).summary[0:400].capitalize()+ f"........... \n\n  Continue Reading: \033[34m{url}\033[0m"
                        response(data,["who","what","is","about","tell","which","on"],single_response=True, required_word=["who","what","is","about","on","tell","tankyou"])
                        break
            else:
                try:
                    wikiSearch = wikipedia.search(" ".join(message))
                    summary = re.sub("[,;?!.-]", "",wikiSearch[0])
                    response(wikipedia.summary(summary.lower()[:-1],1),["who","what","is","about","tell","which","on"],single_response=True,required_word=["who","what","is","about","on","tell"])
                except:
                        response("Oops! Something wrong with the prompt.",["who","what","is","about","tell","which","on"],single_response=True,required_word=["who","what","is","about","on","tell"])
        except socket.timeout:
                response("Oops! Something wrong with the prompt.",["who","what","is","about","tell","which","on"],single_response=True,required_word=["who","what","is","about","on","tell"])


    # End of Responses --------------------------------------------------------------

    # Find the item which has maximum probability in the dictionary 
    best_match_tuple =  max(zip(highest_prop_list.values(),
                     highest_prop_list.keys()))

    # Gets the Best Match for the user input
    best_match = best_match_tuple[1]

    # If the response probability is less than 5 shows an error message
    if(best_match_tuple[0] > 5):
        return best_match
    else:
        return "Sorry! Unknown prompt. Try different"
    


def getResponse(user_input: str):
    # Split Message using regex
    # regex split text between space, and other opeators like ,;?!.-
    splited = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_messages(splited)
    return response

# Printing Effect like typing 
def print_with_typing_effect(text, delay=[0.01,0.01,0.001]):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay[2])
    print()

# Loop to run continues
loop_varible = True
while loop_varible:
    try :
        user_input = input("\033[95mYou:\033[0m ")
        response =getResponse(user_input)
        print_with_typing_effect("\033[92mBot:\033[0m " + response)
        if("Bye" in response or "exit" in response):
            loop_varible = False
    except:
        print()
        print_with_typing_effect("\033[91mSomething Went Wrong! Quitting.....\033[0m \n\033[92mBot:\033[0m Bye See U late!")
        exit()
else:
    print("\033[91mQuitting...\033[0m")
    exit()