from django.shortcuts import render,redirect
from django import template
from django.contrib.sessions.models import Session
import string
from datetime import date
import datetime
from datetime import datetime


import datetime
from datetime import date


from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum, Count

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .forms import ImageFileUploadForm

from kneearth.models import *
from django.shortcuts import render,redirect
from django.http import HttpResponse

from tkinter import *
import tkinter.messagebox
import cv2

import cv2
import numpy as np
import pytesseract
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

import os
from math import hypot
import numpy as np
from keras.models import model_from_json
import operator
import cv2
import sys, os
from tkinter import *

import numpy as np
import pandas as pd
import re
import os
import tensorflow as tf
from numpy import array
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import load_model





def home(request):
    return render(request,'home.html',{})


def about(request):
    return render(request,"about.html",{})


def Admin_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if Admin_Details.objects.filter(Username=Username, Password=password).exists():
                user = Admin_Details.objects.get(Username=Username, Password=password)
                request.session['type_id'] = 'Admin'
                request.session['username'] = Username
                request.session['login'] = 'Yes'
                return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/Admin_login/')
    else:
        return render(request, 'Admin_login.html', {})


def Stylish_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if Stylish_details.objects.filter(Username=Username, Password=password,Status='Confirmed').exists():
            Sty = Stylish_details.objects.get(Username=Username, Password=password)
            request.session['Stylish_id'] = str(Sty.id)
            request.session['type_id'] = 'Stylish'
            request.session['username'] = Username
            request.session['login'] = 'Yes'
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/Stylish_login/')
    else:
        return render(request, 'Stylish_login.html', {})



def User_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if User_details.objects.filter(Username=Username, Password=password).exists():
            ans = ""
            users = User_details.objects.all().filter(Username=Username)

            ExpiryDate = users[0].ExpiryDate
            print("ExpiryDate",ExpiryDate)

            Curr_date = datetime.datetime.now()
            Cyear = Curr_date.strftime('%Y')
            Cmon = Curr_date.strftime('%m')
            Cday = Curr_date.strftime('%d')
            print("Curr_date",Curr_date)

            Eyear = ExpiryDate.strftime('%Y')
            Emon = ExpiryDate.strftime('%m')
            Eday = ExpiryDate.strftime('%d')


            ex_date = date(int(Eyear), int(Emon), int(Eday))
            curr_date = date(int(Cyear), int(Cmon), int(Cday))
            delta = ex_date -  curr_date

            if ex_date > curr_date:
                print("Greater")
            else:
                print("Lesser")

            diff = delta.days

            if int(diff) > 0:
                ans = "Yes"
            else:
                ans = "No"

            if ans == "Yes":
                user = User_details.objects.all().filter(Username=Username, Password=password)
                request.session['User_id'] = str(user[0].id)
                request.session['type_id'] = 'User'
                request.session['username'] = Username
                request.session['login'] = 'Yes'

                User_details.objects.filter(id=str(user[0].id)).update(ChatStatus='Online')
                return redirect('/')
            else:
                messages.info(request,'You Subscriptions is over')
                return redirect('/User_login/')           
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/User_login/')
    else:
        return render(request, 'User_login.html', {})

    



def Register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        Username = request.POST['Username']
        Email = request.POST['Email']        
        Mobile = request.POST['Mobile']
        Password = request.POST['Password']
        Address =  request.POST['Address']
        State =  request.POST['State']
        City =  request.POST['City']
        CreditCard =  request.POST['CreditCard']
        MM =  request.POST['MM']
        YYYY =  request.POST['YYYY']

        CCExpiry = MM+"/"+YYYY
        Cvv =  request.POST['Cvv']


        Expiry_date = datetime.datetime.now() + datetime.timedelta(30)
        Expiry_date = Expiry_date.strftime('%Y-%m-%d')
        print(Expiry_date)

        if User_details.objects.filter(Username=Username).exists():
            messages.info(request,'Username taken')
            return redirect('/AddOfficer/')

        elif User_details.objects.filter(Email=Email).exists():
            messages.info(request,'Email Id taken')
            return redirect('/AddOfficer/')

        else:
            register1 = User_details( FirstName = first_name,LastName = last_name,Username =Username,Email = Email,Password = Password,mobile = Mobile,Address = Address,City = City,State = State,ExpiryDate=Expiry_date,CreditCard = CreditCard,Expiry = CCExpiry,Cvv = Cvv,ChatStatus='Offline')
            register1.save()

            messages.info(request,'Registration Done Successful')
            return redirect('/Register/')
    else:
        return render(request, 'register.html', {})




def StylishRegister(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        emailid = request.POST['emailid']
        Username = request.POST['Username']
        Password = request.POST['Password']
        Address = request.POST['Address']
        Image1 = request.FILES['Image1']
        Image2 = request.FILES['Image2']
        Image3 = request.FILES['Image3']
        Image4 = request.FILES['Image4']
        Image5 = request.FILES['Image5']
        Speciality =  request.POST['Speciality']


        if Stylish_details.objects.filter(Username=Username).exists():
            messages.info(request,'Username taken')
            return redirect('/StylishRegister/')

        elif Stylish_details.objects.filter(Email=emailid).exists():
            messages.info(request,'Email Id taken')
            return redirect('/StylishRegister/')

        else:
            register1 = Stylish_details( Name  = "Name",Contact = "Age",Address = "Symptoms",Email = "Detection",Username = "Username ",Password = "Password",Image1 = Image1,Image2= Image2,Image3 = Image3,Image4 = Image4,Image5 = Image5,Status = "Pending",Speciality="Solution")
            register1.save()
            print("abc")
            print(Image1)
            books_image = str(Image1)
            books_image = books_image
            books_image = books_image
            
            
            
            
            
            print(name)
            img_name = "F:/knee_arthiritis/knee_arthiritis/knee_arthiritis/media/img/images/" + books_image
            img_name=img_name
            img_name=img_name
            print(img_name)
            
            json_file = open("F:/knee_arthiritis/knee_arthiritis/knee_arthiritis/kneearth/model-bw.json", "r")
            model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(model_json)
            # load weights into new model
            loaded_model.load_weights("F:/knee_arthiritis/knee_arthiritis/knee_arthiritis/knee_arthiritis/kneearth/model-bw.h5")
            print("Loaded model from disk")

            a = cv2.imread(img_name)
            a = cv2.flip(a, 1)
            roi = cv2.resize(a, (64, 64))
            
            roi = cv2.cvtColor(roi, cv2.COLOR_BGRA2GRAY)
            
            
            
            _, test_image = cv2.threshold(roi, 100, 255, cv2.THRESH_BINARY)
            
            result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))
            print(result)
            vector = np.array([test_image.flatten()])
            print(vector)
            
            
            prediction = {'INITIAL STAGE': result[0][0], 
                            'LOW': result[0][1],
                            'MEDIUM': result[0][2],
                            'HIGH': result[0][3],
                            'CRITICAL': result[0][4]
                            }
            # Sorting based on top prediction
            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            print(prediction)
            
            a = prediction
            a = (a[0])
            a = a[-2]
            print(a)
            a = a
            a = a
            if a== "INITIAL STAGE":
                Address = "The joint may become stiff and swollen, making it difficult to bend and straighten the knee.Pain and swelling may be worse in the morning, or after sitting or resting."
                Speciality = "Weight loss and Exercise"

                print(Address)
               
            elif a== "LOW":
                Address = "Patients develop very minor wear & tear and bone spur growths at the end of the knee joints."
                Speciality = "Accessories,Braces and wraps can help stabilize your knee"
                print(Address)
                

            elif a== "MEDIUM":
                Address = "knee joints will show more bone spur growth, and though the space between the bones appear normal, people will begin experiencing symptoms of joint pain"
                Speciality = "knee wraps. acetaminophen. nonsteroidal anti-inflammatory drugs (NSAIDs) nonsteroidal gels"
                print(Address)
               
            elif a== "HIGH":
                Address = "With the progression of osteoarthritis of the knee, there is obvious joint inflammation which causes frequent pain when walking, running, squatting, extending or kneeling"
                Speciality = "you should continue with nonpharmacological therapies such as exercise and weight loss. People with stage 3 OA will also continue to receive NSAIDs or acetaminophen." 
                print(Address)
               
            elif a== "CRITICAL":
                Address = "the joint space between the bones are considerably reduced, causing the cartilage to wear off, leaving the joint stiff. The breakdown of cartilage leads to a chronic inflammatory response, with decreased synovial fluid that causes friction, greater pain and discomfort when walking or moving the joint"
                Speciality = "Soft tissue destruction may be noted around the knees in this stage.Treatment options include osteotomy or bone realignment surgery"
                print(Address)
             
            
            




            books_image = "F:/knee_arthiritis/knee_arthiritis/knee_arthiritis/media/img/images/" + books_image
            
            
            
            
            
            
            

            


            
            print("abc")
            
            
            abc = "abc"
            print(abc)
            print(Address)
            Address = Address
            register1 = Stylish_details( Name  = name,Contact = contact,Address = Address,Email = Username + " has been detected with " + a + " condition ",Username = Username,Password = Password,Image1 = Image1,Image2= Image2,Image3 = Image3,Image4 = Image4,Image5 = Image5,Status = "Pending",Speciality=Speciality)
            register1.save()
        

            messages.info(request,'Details filled! See your results in the admin page!')
            return redirect('/StylishRegister/')
    else:
        return render(request, 'StylishRegister.html', {})




def logout(request):
    if request.session['type_id'] == 'User':
        uid = request.session['User_id']
        User_details.objects.filter(id=uid).update(ChatStatus='Offline')
    elif request.session['type_id'] == 'Stylish':
        uid = request.session['Stylish_id']
        User_details.objects.filter(id=uid).update(ChatStatus='Offline')
    
    Session.objects.all().delete()
    return redirect('/')


def ViewUsers(request):
    if request.method == 'POST':
        return redirect('/ViewUsers/')
    else:
        users = User_details.objects.all()
        print(users)
        return render(request, 'ViewUsers.html', {'users':users})


def Stylish_Chat(request):
    if request.method == 'POST':
        return redirect('/Stylish_Chat/')
    else:
        Sid = request.session['Stylish_id']
        
        ids = Chat_details.objects.filter(Sid=Sid).values_list('Uid', flat=True)
        print('ids',ids)
        users = User_details.objects.all().filter(ChatStatus='Online').filter(id__in=ids)
        print(users)
        return render(request, 'Stylish_Chat.html', {'users':users})



def User_Chat(request):
    if request.method == 'POST':
        return redirect('/User_Chat/')
    else:
        sty = Stylish_details.objects.all()
        return render(request, 'User_Chat.html', {'sty':sty})



def MyDetails(request):
    if request.method == 'POST':
        return redirect('/MyDetails/')
    else:
        uid = request.session['User_id']
        users = User_details.objects.all().filter(id=uid)

        ExpiryDate = users[0].ExpiryDate
        print("ExpiryDate",ExpiryDate)

        Curr_date = datetime.datetime.now()
        Cyear = Curr_date.strftime('%Y')
        Cmon = Curr_date.strftime('%m')
        Cday = Curr_date.strftime('%d')
        print("Curr_date",Curr_date)

        Eyear = ExpiryDate.strftime('%Y')
        Emon = ExpiryDate.strftime('%m')
        Eday = ExpiryDate.strftime('%d')


        ex_date = date(int(Eyear), int(Emon), int(Eday))
        curr_date = date(int(Cyear), int(Cmon), int(Cday))
        delta = ex_date -  curr_date

        if ex_date > curr_date:
            print("Greater")
        else:
            print("Lesser")

        diff = delta.days

        ans = "Yes"

        if int(diff) <= 5:
            ans = "Yes"
        else:
            ans = "No"

        return render(request, 'MyDetails.html', {"users":users,"ans":ans})





def UpdateSubscription(request):
    if request.method == 'POST':
        UserId = request.POST['UserId']
        if User_details.objects.filter(id = UserId).exists():
            Package = request.POST['Package']
            CCNumber = request.POST['CCNumber']
            Month = request.POST['Month']
            Year = request.POST['Year']
            Cvv = request.POST['Cvv']

            CCExpiry = Month+"/"+Year
            count = 0

            if Package == "Half Yearly":
                count= 182
                
            elif Package == "Yearly":
                count= 365

            users = User_details.objects.all().filter(id=UserId)
            ExpiryDate = users[0].ExpiryDate

            Expiry_date = ExpiryDate + datetime.timedelta(int(count))
            Expiry_date = Expiry_date.strftime('%Y-%m-%d')
            print(Expiry_date)

            OriginalCC = users[0].CreditCard
            OriginalExp = users[0].Expiry
            OriginalCvv = users[0].Cvv


            if OriginalCC == CCNumber and OriginalCvv == Cvv and OriginalExp == CCExpiry:
                User_details.objects.filter(id=UserId).update(ExpiryDate=Expiry_date)
                messages.info(request,'Plan updated Successfully')
            else:
                messages.info(request,'Credentials doesnt match')
        else:
            messages.info(request,'Id doesnt match')

        return render(request, 'MyDetails.html', {})
        
    else:
        return redirect('/')





def ViewStylish(request):
    if request.method == 'POST':
        return redirect('/ViewStylish/')
    else:
        sty = Stylish_details.objects.all()
        return render(request, 'ViewStylish.html', {'sty':sty})




def User_CP(request):
    if request.method == 'POST':
        CurrentPassword = request.POST['CurrentPassword']
        NewPassword = request.POST['NewPassword']
        ConfirmPassword = request.POST['ConfirmPassword']

        uid = request.session['Stylish_id']
        CurrUser = Stylish_details.objects.all().filter(id=uid)
        if CurrUser[0].Password == CurrentPassword:
            if NewPassword == ConfirmPassword:
                Stylish_details.objects.filter(id=uid).update(Password=NewPassword)
                messages.info(request,'Passwords Changed Successfully')
                return render(request, 'User_CP.html', {})
            else:
                messages.info(request,'New Passwords doesnt match')
                return render(request, 'User_CP.html', {})
        else:
            messages.info(request,'Current Password doesnt match')
            return render(request, 'User_CP.html', {})
        
    else:
        return render(request, 'User_CP.html', {})



def ChangePassword(request):
    if request.method == 'POST':
        CurrentPassword = request.POST['CurrentPassword']
        NewPassword = request.POST['NewPassword']
        ConfirmPassword = request.POST['ConfirmPassword']

        uid = request.session['Stylish_id']
        CurrUser = Stylish_details.objects.all().filter(id=uid)
        if CurrUser[0].Password == CurrentPassword:
            if NewPassword == ConfirmPassword:
                Stylish_details.objects.filter(id=uid).update(Password=NewPassword)
                messages.info(request,'Passwords Changed Successfully')
                return render(request, 'ChangePassword.html', {})
            else:
                messages.info(request,'New Passwords doesnt match')
                return render(request, 'ChangePassword.html', {})
        else:
            messages.info(request,'Current Password doesnt match')
            return render(request, 'ChangePassword.html', {})
        
    else:
        return render(request, 'ChangePassword.html', {})



def AcceptStylish(request):
    if request.method == 'POST':
        return redirect('/AcceptStylish/')
    else:
        sty = Stylish_details.objects.all().filter(Status= 'Pending')
        return render(request, 'AcceptStylish.html', {'sty':sty})


def ManageSubscription(request):
    if request.method == 'POST':
        return redirect('/ManageSubscription/')
    else:
        sty = Subscriptions.objects.all().filter(id='1')
        half = sty[0].halfyear
        print('half',half)
        year = sty[0].year
        print('year',year)
        return render(request, 'ManageSubscription.html', {'half':half,'year':year})


def AcceptRequest(request,id):
    Stylish_details.objects.filter(id=id).update(Status='Confirmed')
    messages.info(request,'Requested Accepted')
    return redirect('/AcceptStylish/')

def UpdateSubs(request):
    if request.method == 'POST': 
        half = request.POST['half']
        year = request.POST['year'] 

        Subscriptions.objects.filter(id='1').update(halfyear=half,year=year)
        messages.info(request,'Pricing Changed')

        return redirect('/ManageSubscription/')
    else:
        return redirect('/ManageSubscription/')



def Chatreply(request): 
    
    MType = request.POST.get('MessageType')
    x = datetime.datetime.now()
    currdate = x.strftime('%Y-%m-%d %H:%M:%S')

    if MType == "Text":
        inputtext = request.POST.get('text')        
        Sid = request.POST.get('Sid')
        chat = Chat_details( Type  = MType,MsgFrom = "User",Context = inputtext,ContextImage = '',Uid = request.session['User_id'],Sid = Sid,Datetime=currdate)
        chat.save()
    else:
        print("enter Image")
        inputtext =request.POST.get('image')
        print("inputt IMage",inputtext)
        Sid = request.POST.get('Sid')
        chat = Chat_details( Type  = MType,MsgFrom = "User",Context = '',ContextImage = inputtext,Uid = request.session['User_id'],Sid = Sid,Datetime=currdate)
        chat.save()



    answer = "Success"
    data = {
        'respond': answer
            }
    return JsonResponse(data)





def StylishChatreply(request):     
    MType = request.POST.get('MessageType')
    x = datetime.datetime.now()
    currdate = x.strftime('%Y-%m-%d %H:%M:%S')

    if MType == "Text":
        inputtext = request.POST.get('text')        
        Uid = request.POST.get('Uid')
        chat = Chat_details( Type  = MType,MsgFrom = "Stylish",Context = inputtext,ContextImage = '',Uid = Uid ,Sid = request.session['Stylish_id'],Datetime=currdate)
        chat.save()
    else:
        print("enter Image")
        inputtext =request.POST.get('image')
        print("inputt IMage",inputtext)
        Uid = request.POST.get('Uid')
        chat = Chat_details( Type  = MType,MsgFrom = "Stylish",Context = '',ContextImage = inputtext,Uid = Uid ,Sid = request.session['Stylish_id'],Datetime=currdate)
        chat.save()



    answer = "Success"
    data = {
        'respond': answer
            }
    return JsonResponse(data)
        


def FillUserChat(request): 
    Sid = request.POST.get('Sid')
    UserId = request.session['User_id']

    answer = ""
    chattype = ""
    chatcontent = ""

    chat = Chat_details.objects.filter(Uid=UserId,Sid=Sid).order_by('Datetime')
    for x in chat:
        chattype =  x.Type
        if chattype == "Text":
            chatcontent = x.Context
        else:
           chatcontent = x.ContextImage 
        chatmessagefrom  = x.MsgFrom
        chatdatetime = x.Datetime

        answer += chattype+"&"+str(chatcontent)+"&"+chatmessagefrom+"&"+str(chatdatetime)+"#"

    #print(answer)

    data = {
        'respond': answer
            }
    return JsonResponse(data)



def FillStylishChat(request): 
    UserId = request.POST.get('Uid')
    Sid = request.session['Stylish_id']

    answer = ""
    chattype = ""
    chatcontent = ""

    chat = Chat_details.objects.filter(Uid=UserId,Sid=Sid).order_by('Datetime')
    for x in chat:
        chattype =  x.Type
        if chattype == "Text":
            chatcontent = x.Context
        else:
           chatcontent = x.ContextImage 
        chatmessagefrom  = x.MsgFrom
        chatdatetime = x.Datetime

        answer += chattype+"&"+str(chatcontent)+"&"+chatmessagefrom+"&"+str(chatdatetime)+"#"

    #print(answer)

    data = {
        'respond': answer
            }
    return JsonResponse(data)




