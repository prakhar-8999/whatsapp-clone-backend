from ast import Continue
from pickle import FALSE
from django.dispatch import receiver
from django.shortcuts import render
from django.contrib.auth.models import User 
from django.http import JsonResponse
from .models import phone_num, messages
from django.db.models import Q
import json
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def register(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        user= User.objects.create_user(data['user'], data['mail'], data['pass1'])
        phonenum = phone_num(auth=user,phone=data['phone'])
        phonenum.save()

        res={'msg':'Account created'}
        
        return JsonResponse(res,status=200)
    else:
        return JsonResponse({'msg':"can't Create"},status=400)


def login_view(request):
    lo = json.loads(request.body)
    auth_id = phone_num.objects.filter(phone=lo['phone']).values()[0]['auth_id']
    username = User.objects.filter(id=auth_id).values()[0]['username']
    user = authenticate(request, username=username, password=lo['pass1'])
    if user is not None:
        login(request, user)
        msg={'msg':'Success'}
        return JsonResponse(msg,status=200)
    else:
        return JsonResponse({'msg':'Invalid credentials !!!!'},status=401)



def dashboard_view(request):
    if request.user.is_authenticated:
        data = User.objects.values_list('username','email').get(username=request.user)
        return JsonResponse(data,status=200,safe=False)
    else:
        return JsonResponse({'msg':'Please Login'},status=401)



def contact(request):
    if request.user.is_authenticated:
        data = list(phone_num.objects.exclude(auth=request.user.id).values('phone','profile_pic'))
        return JsonResponse(data,status=200,safe=False)
    else:
        return JsonResponse({'msg':'Please Login'},status=401)


def profile_upload(request):
    if(request.method=='POST'):
        file = request.FILES['profile']
        ins = phone_num.objects.get(auth=request.user.id)
        ins.profile_pic = file
        ins.save()
        return JsonResponse({'msg':'Successfully Uploaded'},status=200)
    else:
        return JsonResponse({'msg':'Please Login'},status=401)


def user_profile_photo(request):
    if request.user.is_authenticated:
        if(request.method=='GET'):
            profile_photo = phone_num.objects.filter(auth = request.user.id).values('profile_pic')
            return JsonResponse(profile_photo[0],status=200,safe=False)
    else:
        return JsonResponse({'msg':'Please Login'},status=401)


def perticular_contact_details(request):
    if request.user.is_authenticated:
        if(request.method=='POST'):
            data=json.loads(request.body)
            phone=data['phone']
            udata = phone_num.objects.filter(phone=phone).values()[0]
            userdata = User.objects.filter(id=udata['auth_id']).values()[0]
            id = phone_num.objects.filter(phone=phone).values()[0]['auth_id']
            finaldata={
                'phone':phone,
                'username':userdata['username'],
                'email':userdata['email'],
                'profile_pic':udata['profile_pic'],
                'id':id
            }
            return JsonResponse(finaldata,status=200)
    else:
        return JsonResponse({'msg':'Please Login'},status=401)


def message_send(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        messages.objects.create(message=data['message'],sender=request.user.id,receiver=data['reciever'])
        return JsonResponse({'msg':'Success'},status=200)



def recieve_message(request):
    if(request.method == 'POST'):
        data = json.loads(request.body)
        datatosend  = list(messages.objects.filter(Q(sender=request.user.id) | Q(sender = data['reciever']), Q(receiver=request.user.id) | Q(receiver = data['reciever'])).values())
        return JsonResponse(datatosend,status=200,safe=False)


def left_side(request):
    if request.user.is_authenticated:
        ids = []
        userdata = []
        data = list(messages.objects.filter(sender=request.user.id).values('receiver'))
        for i in data:
            if i['receiver'] in ids:
                continue
            else:
                ids.append(i['receiver'])
            # ids.add(i['receiver'])
        # asd = list(ids)
        for x in ids:
            listdata = list(phone_num.objects.filter(auth=x).values('phone','profile_pic','nick_name'))
            userdata.append(listdata[0])
        return JsonResponse(userdata,status=200,safe=False)

def save_name(request):
    if request.user.is_authenticated:
        comedata = json.loads(request.body)
        ins = phone_num.objects.get(auth = comedata['id'])
        ins.nick_name = comedata['name']
        ins.save()
        return JsonResponse({'msg':'success'},status=200)
    else:
        return JsonResponse({'msg':'Please Login !!!!'},status=401)

def logout_view(request):
    logout(request)
    return JsonResponse({'msg':'Logout'},status=200)