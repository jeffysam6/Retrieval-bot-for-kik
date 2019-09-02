import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeerInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage,IncomingGroupChatMessage,IncomingStatusResponse, IncomingGroupStatus, OutgoingChatMessage
from kik_unofficial.datatypes.xmpp.login import ConnectionFailedResponse
import logging
import time
import threading
from typing import List, Union
from kik_unofficial.datatypes.xmpp.base_elements import XMPPElement
import datetime
import random
import json

import nltk
import numpy as np
import random
import string


f=open('chatbot.txt','r',errors = 'ignore')
raw=f.read()

raw=raw.lower()

sent_tokens = nltk.sent_tokenize(raw)

word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey","sir")
GREETING_RESPONSES = ["yes sir", "*nods*", "*winks*", "*grabs u*","smacks u"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)



from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


username = {kik_username}
password = {kik password}

with open("quotes.json","r",encoding="utf8") as f:
  quotes_list = json.load(f)


current_time = datetime.datetime.now()



class EchoBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    
 
    def on_group_message_received(self, chat_message:chatting.IncomingGroupChatMessage):
         print("[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid,
                                                          chat_message.body))
         if ("hello" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,f"Aye")

         elif ("lucad" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,"leave me alone")

         elif ("time"== chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,f"{currentTime()}")

         elif ("o" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid,"wisdom")

         elif ("exit" == chat_message.body.lower()):
            self.client.send_chat_message(chat_message.group_jid, exit())


        #CODE FOR RETRIEVAL BOT
         elif("lucad" in chat_message.body.lower().split(" ")):

            user_response = chat_message.body.lower()
            user_response=user_response.lower()
    
            if(greeting(user_response)!=None):
                self.client.send_chat_message(chat_message.group_jid," "+greeting(user_response))
            else:
                self.client.send_chat_message(chat_message.group_jid,response(user_response))
                sent_tokens.remove(user_response)


    def on_message_read(self, response: chatting.IncomingMessageReadEvent):
        print("[+] Human has read the message with ID {}.".format(response.message_id))


def currentTime():
    return(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def main():
    bot = EchoBot()


if __name__ == '__main__':
    main()