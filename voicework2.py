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
def voicetake():
    take0 = ""
    while take0 =="" or take0== 'UnknownValueError' or take0 == 'RequestError' or take0 == 'Error':
        if take0 =="":
            mess0 = "Hello, Where is the start"
            take0 = voicesearch(mess0,1)
        elif take0 == 'UnknownValueError' or take0 == 'RequestError' or take0 == 'Error':
            mess0 = "Sorry, I could not understand this audio, please say again!"
            take0 = voicesearch(mess0,4)
    else:
        return reply
        message1 = "Sorry, I could not understand your audio, please say again!"
        reply = voicego(message1,5)


# def voicefinal():
#     reply2 = ""
#     while reply2 =="" or reply2 == 'UnknownValueError' or reply2 == 'RequestError' or reply2 == 'Error':
#         if reply2 =="":
#             message2 = "Where is the end?"
#             reply2 = voicego(message2,1)
#         elif reply2 == 'UnknownValueError' or reply2 == 'RequestError' or reply2 == 'Error':
#             message2 = "Sorry, I could not understand this audio, please say again!"
#             reply2 = voicego(message2,4)
#     else:
#         return reply2

# def drivemode():
#     reply3 = ""
#     while reply3 =="" or reply3 == 'UnknownValueError' or reply3 == 'RequestError' or reply3 == 'Error':
#         if reply3 =="":
#             message3 = "Driving or Transit?"
#             reply3 = voicego(message3,1)
#         elif reply3 == 'UnknownValueError' or reply3 == 'RequestError' or reply3 == 'Error':
#             message3 = "Sorry, I could not understand this audio, please say again!"
#             reply3 = voicego(message3,5)
#     else:
#         return reply3

# def voiceoutcome():
#     reply4 = ""
#     while reply4 =="" or reply4 == 'UnknownValueError' or reply4 == 'RequestError' or reply4 == 'Error':
#         if reply4 =="":
#             message4 = "Here is the Naviation, anything help?"
#             reply4 = voicego(message4,1)
#         elif reply4 == 'UnknownValueError' or reply4 == 'RequestError' or reply3 == 'Error':
#             message3 = "Sorry, I could not understand this audio, please say again!"
#             reply3 = voicego(message3,5)
#     else:
#         return reply3    
    


def voicego():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        audiofile('Hello, please tell me the start and the end. Thank you!',4)      
        r.adjust_for_ambient_noise(source, duration=2)        
        audio=r.listen(source)
        try :
            r.recognize_google(audio,language='zh-TW')
            input_search = r.recognize_google(audio,language='zh-TW')
            print(input_search)
            re = wit_recognize(input_search) 
            if re != KeyError:
                input_go0 = transfer_language(re[0])
                input_go1 = transfer_language(re[1])
                input_word = "Your anwser is "+input_go0+"to"+input_go1
                audiofile(input_word,2)
                return (input_go0,input_go1)
            else :
                re = 'Error'
                print(re)
                return
            
        except speech_recognition.UnknownValueError :
            re = 'UnknownValueError'
            print(re)
            return re
            
        except speech_recognition.RequestError:
            re = 'RequestError'
            print(re)
            return re


def wit_recognize(input_search):
    client = Wit('EYTESN3PCWJCRRMVWZ7PBNGFMT2UFE6R')
    resp = client.message(input_search)
    resp_val = list()
    for i in range(0,2,1)
        try:
            xx = resp['entities']['location'][i]['value']
            resp_val.append(xx) 
        except KeyError:
            return KeyError
    return resp_val
    

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
 