from django.shortcuts import render,redirect
from django.http import HttpResponse
import datetime
from .models import *
from django.contrib.staticfiles import finders
from django.db.models import Avg,Sum,Count
import time
# from gtts import gTTS
import speech_recognition
from pygame import mixer
import tempfile
from pypinyin import pinyin
from wit import Wit
# from numba import jit
from . import label_image, voicework
import os
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache
from django.db import connections, transaction

# Create your views here.

def create(request):
    if request.method == 'POST':
        account = request.POST["useraccount"]
        password = request.POST["password"]
        useremail = request.POST["useremail"]
        gender = request.POST["usergender"]        
        userbirth = request.POST["userbirth"]
        career = request.POST["userCareer"]
        resident = request.POST["userResident"]

        Member.objects.create(account=account,password=password,useremail=useremail,gender=gender,userbirth=userbirth,career=career,resident=resident)
        
        return redirect("/")
        
    return render(request,'home/create.html',locals())

def update(request):
    if request.method == 'POST':            
        useremail = request.POST["useremail"]
        gender = request.POST["usergender"]  
        userbirth = request.POST["userbirth"]
        career = request.POST["userCareer"]
        resident = request.POST["userResident"]

        member = Member.objects.get(id=request.COOKIES["id"])
        member.useremail = useremail
        member.gender = gender
        member.userbirth = userbirth
        member.career = career
        member.resident = resident

        member.save()

        return redirect('/update')


    member = Member.objects.get(id=request.COOKIES["id"])

    return render(request,'home/update.html',locals())

def login(request):   
    if request.method == "POST":
        account = request.POST['account']
        password = request.POST['password']
        member = Member.objects.filter(account=account,password=password).values('id')
        if member:
            themember = member[0]         
            response = HttpResponse("<script>alert('登入成功');location.href='/road_direction'</script>")
            if 'rememberme' in request.POST.keys() and request.POST['rememberme']:
                expiresdate = datetime.datetime.now() + datetime.timedelta(days=1)
                response.set_cookie("id",themember['id'],expires=expiresdate)                 
            else:
                response.set_cookie("id",themember['id'])
            return response
        else:
            return HttpResponse("<script>alert('登入失敗，密碼錯誤');location.href='/'</script>")
    return render(request,'home/login.html',locals())

def logout(request):
    response = HttpResponse("<script>alert('登出');location.href='/'</script>")
    response.delete_cookie('id')
    return response

def storymap(request):
    # voicework.audiofile('Hello, I\'m TripRobot. Just upload your picture, and I\'ll tell you where is your picture in Taipei.',5)
    return render(request,'home/storymap.html',locals())

def checkname(request,name):
    result = Member.objects.filter(account=name)
    if result :
        message = "帳號已註冊"
    else:
        message = "帳號可使用"
        
    return HttpResponse(message)

def survey(request):
    member = Member.objects.get(id=request.COOKIES["id"])
    account = member.account

    if request.method == 'POST':
        Question1 = request.POST["Q1"]
        Question2 = request.POST["Q2"]
        Question3 = request.POST["Q3"]
        Question4 = request.POST["Q4"]        
        Question5 = request.POST["Q5"]
        Question6 = request.POST["Q6"]
        Question7 = request.POST["Q7"]

        Survey_Outcome.objects.create(id=member.id,account=account,Question1=Question1,Question2=Question2,Question3=Question3,Question4=Question4,Question5=Question5,Question6=Question6,Question7=Question7)
        
        return redirect("/road_direction")
     
    return render(request,'home/survey.html',locals())

def userpattern(request):
    dictMale = Member.objects.filter(gender="男性").aggregate(Count("gender"))
    numMale = dictMale["gender__count"]    
    dictFemale = Member.objects.filter(gender="女性").aggregate(Count("gender"))
    numFemale = dictFemale["gender__count"]
    
    dictC0 = Member.objects.filter(career="金融業").aggregate(Count("career"))
    numC0 = dictC0["career__count"]    
    dictC1 = Member.objects.filter(career="製造業").aggregate(Count("career"))
    numC1 = dictC1["career__count"]
    dictC2 = Member.objects.filter(career="軍公教").aggregate(Count("career"))
    numC2 = dictC2["career__count"]
    dictC3 = Member.objects.filter(career="電子科技業").aggregate(Count("career"))
    numC3 = dictC3["career__count"]    
    dictC4 = Member.objects.filter(career="傳統產業").aggregate(Count("career"))
    numC4 = dictC4["career__count"]
    dictC5 = Member.objects.filter(career="服務業").aggregate(Count("career"))
    numC5 = dictC5["career__count"]
    dictC6 = Member.objects.filter(career="媒體行銷公關").aggregate(Count("career"))
    numC6 = dictC6["career__count"]    
    dictC7 = Member.objects.filter(career="法律顧問").aggregate(Count("career"))
    numC7 = dictC7["career__count"]
    dictC8 = Member.objects.filter(career="自營商").aggregate(Count("career"))
    numC8 = dictC8["career__count"]
    dictC9 = Member.objects.filter(career="自由業(SOHO)").aggregate(Count("career"))
    numC9 = dictC9["career__count"]    
    dictC10 = Member.objects.filter(career="學生").aggregate(Count("career"))
    numC10 = dictC10["career__count"]
    dictC11 = Member.objects.filter(career="其他").aggregate(Count("career"))
    numC11 = dictC11["career__count"]


    dictCTotal = Member.objects.all().aggregate(Count("career"))
    numCTotal = dictCTotal["career__count"]  
    perC0 =  format(int(numC0)/int(numCTotal),  '.0%')
    perC1 =  format(int(numC1)/int(numCTotal),  '.0%')  
    perC2 =  format(int(numC2)/int(numCTotal),  '.0%')
    perC3 =  format(int(numC3)/int(numCTotal),  '.0%')  
    perC4 =  format(int(numC4)/int(numCTotal), '.0%')  
    perC5 =  format(int(numC5)/int(numCTotal), '.0%')  
    perC6 =  format(int(numC6)/int(numCTotal), '.0%')  
    perC7 =  format(int(numC7)/int(numCTotal), '.0%')  
    perC8 =  format(int(numC8)/int(numCTotal), '.0%')   
    perC9 =  format(int(numC9)/int(numCTotal), '.0%')   
    perC10 =  format(int(numC10)/int(numCTotal), '.0%')   
    perC11 =  format(int(numC11)/int(numCTotal), '.0%')   


    dictR0 = Member.objects.filter(resident="台北市").aggregate(Count("resident"))
    numR0 = dictR0["resident__count"]   
    dictR1 = Member.objects.filter(resident="新北市").aggregate(Count("resident"))
    numR1 = dictR1["resident__count"]  
    dictR2 = Member.objects.filter(resident="基隆市").aggregate(Count("resident"))
    numR2 = dictR2["resident__count"] 
    dictR3 = Member.objects.filter(resident="宜蘭縣").aggregate(Count("resident"))
    numR3 = dictR3["resident__count"]
    dictR4 = Member.objects.filter(resident="桃園市").aggregate(Count("resident"))
    numR4 = dictR4["resident__count"]   
    dictR5 = Member.objects.filter(resident="新竹縣").aggregate(Count("resident"))
    numR5 = dictR5["resident__count"]  
    dictR6 = Member.objects.filter(resident="新竹市").aggregate(Count("resident"))
    numR6 = dictR6["resident__count"] 
    dictR7 = Member.objects.filter(resident="苗栗縣").aggregate(Count("resident"))
    numR7 = dictR7["resident__count"] 
    dictR8 = Member.objects.filter(resident="台中市").aggregate(Count("resident"))
    numR8 = dictR8["resident__count"]   
    dictR9 = Member.objects.filter(resident="彰化縣").aggregate(Count("resident"))
    numR9 = dictR9["resident__count"]  
    dictR10 = Member.objects.filter(resident="南投縣").aggregate(Count("resident"))
    numR10 = dictR10["resident__count"] 
    dictR11 = Member.objects.filter(resident="雲林縣").aggregate(Count("resident"))
    numR11 = dictR11["resident__count"]
    dictR12 = Member.objects.filter(resident="嘉義縣").aggregate(Count("resident"))
    numR12 = dictR12["resident__count"]   
    dictR13 = Member.objects.filter(resident="嘉義市").aggregate(Count("resident"))
    numR13 = dictR13["resident__count"]  
    dictR14 = Member.objects.filter(resident="台南市").aggregate(Count("resident"))
    numR14 = dictR14["resident__count"] 
    dictR15 = Member.objects.filter(resident="高雄市").aggregate(Count("resident"))
    numR15 = dictR15["resident__count"]  
    dictR16 = Member.objects.filter(resident="屏東縣").aggregate(Count("resident"))
    numR16 = dictR16["resident__count"]   
    dictR17 = Member.objects.filter(resident="花蓮縣").aggregate(Count("resident"))
    numR17 = dictR17["resident__count"]  
    dictR18 = Member.objects.filter(resident="台東縣").aggregate(Count("resident"))
    numR18 = dictR18["resident__count"] 
    dictR19 = Member.objects.filter(resident="澎湖縣").aggregate(Count("resident"))
    numR19 = dictR19["resident__count"] 
    dictR20 = Member.objects.filter(resident="金門縣").aggregate(Count("resident"))
    numR20 = dictR20["resident__count"] 
    dictR21 = Member.objects.filter(resident="連江縣").aggregate(Count("resident"))
    numR21 = dictR21["resident__count"]   
   


    dictRTotal = Member.objects.all().aggregate(Count("resident"))
    numRTotal = dictRTotal["resident__count"]  
    perR0 =  format(int(numR0)/int(numRTotal),  '.0%')
    perR1 =  format(int(numR1)/int(numRTotal),  '.0%')  
    perR2 =  format(int(numR2)/int(numRTotal),  '.0%')
    perR3 =  format(int(numR3)/int(numRTotal),  '.0%')  
    perR4 =  format(int(numR4)/int(numRTotal), '.0%')  
    perR5 =  format(int(numR5)/int(numRTotal), '.0%')  
    perR6 =  format(int(numR6)/int(numRTotal), '.0%')  
    perR7 =  format(int(numR7)/int(numRTotal), '.0%')  
    perR8 =  format(int(numR8)/int(numRTotal), '.0%')   
    perR9 =  format(int(numR9)/int(numRTotal), '.0%')   
    perR10 =  format(int(numR10)/int(numRTotal), '.0%')   
    perR11 =  format(int(numR11)/int(numRTotal), '.0%')
    perR12 =  format(int(numR12)/int(numRTotal),  '.0%')
    perR13 =  format(int(numR13)/int(numRTotal),  '.0%')  
    perR14 =  format(int(numR14)/int(numRTotal),  '.0%')
    perR15 =  format(int(numR15)/int(numRTotal),  '.0%')  
    perR16 =  format(int(numR16)/int(numRTotal), '.0%')  
    perR17 =  format(int(numR17)/int(numRTotal), '.0%')  
    perR18 =  format(int(numR18)/int(numRTotal), '.0%')  
    perR19 =  format(int(numR19)/int(numRTotal), '.0%')  
    perR20 =  format(int(numR20)/int(numRTotal), '.0%')   
    perR21 =  format(int(numR21)/int(numRTotal), '.0%')   

    return render(request,'home/userpattern.html',locals())
# @jit
# def voice(request):
#     client = Wit('CSE5MFWK5CN3LKHZWH7DJMTY2FMCB2XP')
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         with tempfile.NamedTemporaryFile(delete=True) as fp:
#             tts=gTTS(text="Hello Where do you want to know", lang="en", slow =False)
#             tts.save('{}.mp3'.format(fp.name))
#             mixer.init()
#             mixer.music.load('{}.mp3'.format(fp.name))
#             mixer.music.play(1)
#             time.sleep(1)
#             r.adjust_for_ambient_noise(source, duration=2)        
#             audio=r.listen(source)        
#             try: 
#                 input_search = r.recognize_google(audio,language='zh-TW')
#                 print(input_search)
#                 resp = client.message(input_search)
#                 try: 
#                     resp_val = resp['entities']['location'][0]['value']
#                     print(resp_val)
#                     member = Member.objects.get(id=request.COOKIES["id"])
#                     account = member.account
#                     Search_Record = resp_val
#                     UserRecord.objects.create(account=account,Search_Record=Search_Record)            
#                     input_trans = pinyin(resp_val)
#                     input_go = "" 
#                     for num in range(len(input_trans)):
#                         input_go = input_go+str(input_trans[num][0])    
#                     print(input_go)
#                     with tempfile.NamedTemporaryFile(delete=True) as fp: 
#                         tts=gTTS(text="You want to know "+input_go+"It is as follow", lang="en", slow =False)
#                         tts.save('{}.mp3'.format(fp.name))
#                         mixer.init()
#                         mixer.music.load('{}.mp3'.format(fp.name))
#                         mixer.music.play(1)
#                         time.sleep(4)
#                     return HttpResponse(resp_val)
#                 except KeyError:
#                     print('go')
#                     return HttpResponse("/voiceUnknown")             
#             except speech_recognition.UnknownValueError:
#                 return redirect("/voiceUnknown")    
#             except speech_recognition.RequestError as e:
#                 return redirect("/voiceError")        

# def voiceUnknown(request):
#     client = Wit('CSE5MFWK5CN3LKHZWH7DJMTY2FMCB2XP')
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         with tempfile.NamedTemporaryFile(delete=True) as fp:
#             tts=gTTS(text="Sorry, I could not understand this audio! please say again! ", lang="en", slow =False)
#             tts.save('{}.mp3'.format(fp.name))
#             mixer.init()
#             mixer.music.load('{}.mp3'.format(fp.name))
#             mixer.music.play(1)
#             time.sleep(1)
#             r.adjust_for_ambient_noise(source, duration=2)        
#             audio=r.listen(source)
#             try:
#                 input_search = r.recognize_google(audio,language='zh-TW')
#                 print(input_search)                 
#                 resp = client.message(input_search)
#                 try:
#                     resp_val = resp['entities']['location'][0]['value']
#                     print(resp_val) 
#                     member = Member.objects.get(id=request.COOKIES["id"])
#                     account = member.account
#                     Search_Record = resp_val
#                     UserRecord.objects.create(account=account,Search_Record=Search_Record)                
#                     input_trans = pinyin(resp_val)
#                     input_go = "" 
#                     for num in range(len(input_trans)):
#                         input_go = input_go+str(input_trans[num][0])
#                     print(input_go)
#                     with tempfile.NamedTemporaryFile(delete=True) as fp: 
#                         tts=gTTS(text="You want to know "+input_go+"It is as follow", lang="en", slow =False)
#                         tts.save('{}.mp3'.format(fp.name))
#                         mixer.init()
#                         mixer.music.load('{}.mp3'.format(fp.name))
#                         mixer.music.play(1)
#                         time.sleep(4)
#                     return HttpResponse(resp_val)
#                 except KeyError:
#                     print('go')
#                     return HttpResponse("/voiceUnknown")
#             except speech_recognition.UnknownValueError:
#                 return redirect("/voiceUnknown")    
#             except speech_recognition.RequestError as e:
#                 return redirect("/voiceError")

# def voiceError(request):
#     client = Wit('CSE5MFWK5CN3LKHZWH7DJMTY2FMCB2XP')
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         with tempfile.NamedTemporaryFile(delete=True) as fp:
#             tts=gTTS(text="No response from service, please say again! ", lang="en", slow =False)
#             tts.save('{}.mp3'.format(fp.name))
#             mixer.init()
#             mixer.music.load('{}.mp3'.format(fp.name))
#             mixer.music.play(1)
#             time.sleep(1)
#             r.adjust_for_ambient_noise(source, duration=2)        
#             audio=r.listen(source)
#             try:
#                 input_search = r.recognize_google(audio,language='zh-TW')
#                 print(input_search)
#                 resp = client.message(input_search)
#                 try:
#                     resp_val = resp['entities']['location'][0]['value']
#                     print(resp_val)
#                     member = Member.objects.get(id=request.COOKIES["id"])
#                     account = member.account
#                     Search_Record = resp_val
#                     UserRecord.objects.create(account=account,Search_Record=Search_Record)                                                
#                     input_trans = pinyin(resp_val)
#                     input_go = ""
#                     for num in range(len(input_trans)):
#                         input_go = input_go+str(input_trans[num][0])
#                     print(input_go)
#                     with tempfile.NamedTemporaryFile(delete=True) as fp: 
#                         tts=gTTS(text="You want to know "+input_go, lang="en", slow =False)
#                         tts.save('{}.mp3'.format(fp.name))
#                         mixer.init()
#                         mixer.music.load('{}.mp3'.format(fp.name))
#                         mixer.music.play(1)
#                         time.sleep(4) 
#                     return HttpResponse(resp_val)
#                 except KeyError:
#                     print('go')
#                     return HttpResponse("/voiceUnknown")
#             except speech_recognition.UnknownValueError:
#                 return redirect("/voiceUnknown")    
#             except speech_recognition.RequestError as e:
#                 return redirect("/voiceError")
  
# def voiceContinue(request):
#     client = Wit('CSE5MFWK5CN3LKHZWH7DJMTY2FMCB2XP')
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         with tempfile.NamedTemporaryFile(delete=True) as fp:
#             tts=gTTS(text="anything help", lang="en", slow =False)
#             tts.save('{}.mp3'.format(fp.name))
#             mixer.init()
#             mixer.music.load('{}.mp3'.format(fp.name))
#             mixer.music.play(1)
#             time.sleep(1)
#             r.adjust_for_ambient_noise(source, duration=2)        
#             audio=r.listen(source)
#             try:
#                 input_search = r.recognize_google(audio,language='zh-TW')
#                 print(input_search)
#                 resp = client.message(input_search)
#                 try:
#                     resp_val = resp['entities']['location'][0]['value']
#                     print(resp_val)
#                     member = Member.objects.get(id=request.COOKIES["id"])
#                     account = member.account
#                     Search_Record = resp_val
#                     UserRecord.objects.create(account=account,Search_Record=Search_Record)                                                
#                     input_trans = pinyin(resp_val)
#                     input_go = ""
#                     for num in range(len(input_trans)):
#                         input_go = input_go+str(input_trans[num][0])
#                     print(input_go)
#                     with tempfile.NamedTemporaryFile(delete=True) as fp: 
#                         tts=gTTS(text="You want to know "+input_go+"It is as follow", lang="en", slow =False)
#                         tts.save('{}.mp3'.format(fp.name))
#                         mixer.init()
#                         mixer.music.load('{}.mp3'.format(fp.name))
#                         mixer.music.play(1)
#                         time.sleep(4)
#                     return HttpResponse(resp_val)
#                 except KeyError:     
#                     print('go')
#                     return HttpResponse("/voiceUnknown")
#             except speech_recognition.UnknownValueError:
#                 return redirect("/voiceUnknown")    
#             except speech_recognition.RequestError as e:
#                 return redirect("/voiceError")        


# def voiceContinue_con(request):
#     client = Wit('CSE5MFWK5CN3LKHZWH7DJMTY2FMCB2XP')
#     r = speech_recognition.Recognizer()
#     with speech_recognition.Microphone() as source:
#         with tempfile.NamedTemporaryFile(delete=True) as fp:
#             tts=gTTS(text="anything help", lang="en", slow =False)
#             tts.save('{}.mp3'.format(fp.name))
#             mixer.init()
#             mixer.music.load('{}.mp3'.format(fp.name))
#             mixer.music.play(1)
#             time.sleep(1)
#             r.adjust_for_ambient_noise(source, duration=2)        
#             audio=r.listen(source)
#             try:
#                 input_search = r.recognize_google(audio,language='zh-TW')
#                 print(input_search)
#                 resp = client.message(input_search)
#                 try:
#                     resp_val = resp['entities']['location'][0]['value']
#                     print(resp_val)
#                     member = Member.objects.get(id=request.COOKIES["id"])
#                     account = member.account
#                     Search_Record = resp_val
#                     UserRecord.objects.create(account=account,Search_Record=Search_Record)
#                     input_trans = pinyin(resp_val)
#                     input_go = ""
#                     for num in range(len(input_trans)):
#                         input_go = input_go+str(input_trans[num][0])
#                     print(input_go)
#                     with tempfile.NamedTemporaryFile(delete=True) as fp: 
#                         tts=gTTS(text="You want to go to "+input_go+"It is as follow", lang="en", slow =False)
#                         tts.save('{}.mp3'.format(fp.name))
#                         mixer.init()
#                         mixer.music.load('{}.mp3'.format(fp.name))
#                         mixer.music.play(1)
#                         time.sleep(4)
#                     return HttpResponse(resp_val)
#                 except KeyError:     
#                     print('go')
#                     return redirect("/voiceUnknown")
#             except speech_recognition.UnknownValueError:
#                 return redirect("/voiceUnknown")    
#             except speech_recognition.RequestError as e:
#                 return redirect("/voiceError")  
# 
# def voice(request):
#     sr = voicework.voicefind()
#     return HttpResponse(sr)



#def yarn_test(request):
#    return render(request,'127.0.0.1:1234',locals())

# def up_load_gragh(request):
#    return HttpResponse('ok')

def pic_saver(request):
    f1 = request.FILES.get('pic_go')
    f2 = FileSystemStorage()

    r = f2.save('pic/%s'%(f1.name),f1)
    files = 'home/static/images/kayak-2975812.jpg'
    if f2.exists(files):
        f2.delete(files)        
    y = f2.save(files,f1)
    p1 = PicSave()
    p1.pic = r
    p1.save()

    p2 = PicSave()
    p2.pic = y
    p2.save()
    file_obj = open('home/static/note.txt','w',encoding='utf-8')
    file_obj.write(str(f1.name))
    file_obj.close()
    print(str(f1.name))
    cache.delete('/static/images/kayak-2975812.jpg')
    return redirect('/storymap')
 

def graphmodel(request):
    file_obj = open('home/static/note.txt','r',encoding='utf-8')
    linedata = file_obj.readline()
    print(linedata)
    xx = label_image.use_for(linedata)
    member = Member.objects.get(id=request.COOKIES["id"])
    account = member.account
    Search_Record = xx
    UserRecord.objects.create(account=account,Search_Record=Search_Record)    
    voicework.audiofile('I know, This is'+xx,0)
    return HttpResponse(xx)

def road_direction(request):
    return render(request,'home/road_direction.html',locals())

def voicestart(request):
    re = voicework.voicebegin()
    return HttpResponse(re)    

def voiceend(request):
    rf = voicework.voicefinal()
    return HttpResponse(rf)    

def voicemode(request):
    dr = voicework.drivemode()
    out = voicework.voiceoutcome()
    return HttpResponse(dr)
