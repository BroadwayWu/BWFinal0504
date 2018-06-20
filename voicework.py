import speech_recognition
from gtts import gTTS
from pygame import mixer
import tempfile
from pypinyin import pinyin
from wit import Wit
import time
from django.http import HttpResponse
from .models import *
from numba import jit
import pyttsx3


@jit
def voicebegin():
    messagestart = "Hello, this is Taipei and the trip! If you want to use this navigation. Please answer some question, thank you!"
    audiofile(messagestart,3)    
    reply = ""
    while reply =="" or reply== 'UnknownValueError' or reply == 'RequestError' or reply == 'Error':
        if reply =="":
            message0 = "The first question, where is your start"
            reply = voicego(message0,1)
        elif reply== 'UnknownValueError' or reply == 'RequestError' or reply == 'Error':
            message1 = "Sorry, I could not understand this audio, please say again!"
            reply = voicego(message1,6)
    else:
        return reply


def voicefinal():
    reply2 = ""
    while reply2 =="" or reply2 == 'UnknownValueError' or reply2 == 'RequestError' or reply2 == 'Error':
        if reply2 =="":
            message2 = "Where is your end?"
            reply2 = voicego(message2,1)
        elif reply2 == 'UnknownValueError' or reply2 == 'RequestError' or reply2 == 'Error':
            message2 = "Sorry, I could not understand this audio, please say again!"
            reply2 = voicego(message2,6)
    else:
        return reply2

def drivemode():
    reply3 = ""
    while reply3 =="" or reply3 == 'UnknownValueError' or reply3 == 'RequestError' or reply3 == 'Error':
        if reply3 =="":
            message3 = "One more question, Driving or Transit?"
            reply3 = voicego(message3,1)
        elif reply3 == 'UnknownValueError' or reply3 == 'RequestError' or reply3 == 'Error':
            message3 = "Sorry, I could not understand this audio, please say again!"
            reply3 = voicego(message3,6)
    else:
        return reply3

def voiceoutcome():
    message4 = "Here is the outcome you want, thanks for your help and enjoy your trip!"
    reply4 = audiofile(message4,1)
    return reply4    
    
def voicefind():
    reply5 = ""
    while reply5 =="" or reply5 == 'UnknownValueError' or reply5 == 'RequestError' or reply5 == 'Error':
        if reply5 =="":
            message5 = "Where do you want to know?"
            reply5 = voicego(message5,1)
        elif reply5 == 'UnknownValueError' or reply5 == 'RequestError' or reply5 == 'Error':
            message5 = "Sorry, I could not understand this audio, please say again!"
            reply5 = voicego(message5,8)
    else:
        return reply5



def voicego(abc,t):
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        audiofile(abc,t)      
        r.adjust_for_ambient_noise(source, duration=2)        
        audio=r.listen(source)
        try :
            r.recognize_google(audio,language='zh-TW')
            input_search = r.recognize_google(audio,language='zh-TW')
            print(input_search)
            re = wit_recognize(input_search) 
            if re != KeyError:
                print(re)
                input_go = transfer_language(re)
                input_word = "Your anwser is "+input_go
                audiofile(input_word,1)
                return re
            else :
                re = 'Error'
                print(re)
                return 'Error'
            
        except speech_recognition.UnknownValueError :
            re = 'UnknownValueError'
            print(re)
            return re
            
        except speech_recognition.RequestError:
            re = 'RequestError'
            print(re)
            return re


def wit_recognize(input_search):
    client = Wit('CSE5MFWK5CN3LKHZWH7DJMTY2FMCB2XP')
    resp = client.message(input_search)
    try:
        resp_val = resp['entities']['location'][0]['value']
        return resp_val
    except KeyError:
        try:
            resp_mode = resp['entities']['intent'][0]['value']
            return resp_mode
        except KeyError:
            return KeyError

# def ORMstore():
    # member = Member.objects.get(id=request.COOKIES["id"])                    
    # account = member.account
    # Search_Record = re
    # UserRecord.objects.create(account=account,Search_Record=Search_Record)                     


def transfer_language(re):
    input_trans = pinyin(re)
    input_go = "" 
    for num in range(len(input_trans)):
        input_go = input_go+str(input_trans[num][0])                    
        # print(input_go)
    return input_go                    

     
# def audiofile(abc,t):    
#     with tempfile.NamedTemporaryFile(delete=False) as fp: 
#         tts=gTTS(text=abc, lang="en", slow =False)
#         tts.save('{}.mp3'.format(fp.name))        
#         mixer.music.load('{}.mp3'.format(fp.name))
#         mixer.music.play(1)
#         time.sleep(t)

def audiofile(abc,t):    
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-60)
    engine.say(abc)
    engine.runAndWait()
    time.sleep(t)
 