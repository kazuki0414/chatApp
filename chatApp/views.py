from django.shortcuts import render,redirect
from django.contrib.auth.models import User,UserManager
from django.contrib.auth import authenticate,login,logout,get_user_model
from chatApp.models import Profile,FriendTable,TalkMessageList
from django.db.models import Q
from django.http import JsonResponse
import json
from datetime import datetime


# Create your views here.

User = get_user_model()

#ログイン
def loginfunc(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #データがあるかどうか検索する
        user = authenticate(request,username=username,password=password)

        if user is not None :
            login(request,user)
            return redirect('main')
        else:
            return redirect('login')

    return render(request,'login.html')

#ログアウト
def logoutfunc(request):

    logout(request)
    return redirect('login')


#サインアップをする
def signupfunc(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        fullname = request.POST["fullname"]

        try:
            user = User.objects.get(username=username)
            return render(request,'signup.html',{'error':"このユーザーは既に登録されています。"})
        except:
            user = User.objects.create_user(username,"",password)
            login(request,user)
            return redirect('createProfile')

    return render(request,"signup.html")

#プロフィール作成画面へ
def createProfilefunc(request):

    if request.method == 'POST':

        #入力されたデータを取得する
        gender = request.POST["gender"]
        birth_date = request.POST["birth_date"]
        location = request.POST["location"]
        favorite_words = request.POST["favorite_words"]
        images = request.POST["images"]

        #Userクラスに紐づくプロフィール情報を取得する
        profile = request.user.profile

        #プロフィールモデルを更新する
        profile.gender = gender
        profile.birth_date = birth_date
        profile.location = location
        profile.favorite_words = favorite_words
        profile.images = images

        profile.save()

        return redirect('main')

    return render(request,"createProfile.html")

#main画面を表示
def mainviewfunc(request):
    return render(request,'main.html')


#フレンド検索
def friendSearchfunc(request):


    if request.method == 'POST':

        #入力されたデータを取得する
        username = request.POST["friendName"]

        #取得したusernameを含むデータを取得
        user = User.objects.filter(username__contains=username)

        context = { 'users':user }

        return render(request,"friendsearch.html",context)

    return render(request,"friendsearch.html")


#フレンド登録
def friendRegifunc(request,pk):

    #選択されたユーザ取得
    selectUser = User.objects.get(pk=pk)
    #FriendTableテーブルにデータを登録する
    FriendTable.objects.create(myId=request.user.pk, friendId=selectUser.pk)

    return redirect('friendSearch')


#フレンドリストを表示
def friendsListViewfunc(request):

    #ログインユーザを取得
    loginUser = request.user

    #ログインユーザとフレンドになっているユーザ情報テーブルを取得
    friendList = FriendTable.objects.filter(myId__iexact=loginUser.pk)

    list = []
    for friend in friendList:

        list.append(friend.friendId)

    #ログインユーザとフレンドになっているユーザデータを取得
    users = User.objects.filter(pk__in=list)

    context = { 'friendList' : users}

    return render(request,"friendslist.html",context)



#フレンドトーク画面表示
def friendTalkingfunc(request,pk):

    #トークするフレンド情報を取得する
    frienduser = User.objects.get(pk=pk)

    context = {
        'friendId' : frienduser.pk
    }

    return render(request,"friendTalking.html",context)
    # return render(request,"friendTalking.html",{'talkmessagelist':talkmessagelist})


#メッセージを取得する
def getMessagefunc(request):

    userId = int(request.GET.get('userId',None))
    friendId = int(request.GET.get('friendId',None))

    #対象のメッセージを取得する
    talkmessagelist = TalkMessageList.objects.filter(Q(fromuser=userId) | Q(fromuser=friendId), Q(touser=userId) | Q(touser=friendId))

    strJson = "{\"talkmessage\" : ["
    for talkmessage in talkmessagelist :

        strJson += "{\"message\":\"" + talkmessage.message +"\",\"touser\":\"" + str(talkmessage.touser) + "\",\"fromuser\":\"" + str(talkmessage.fromuser) + "\"},"

    strJson = strJson[:-1]
    strJson += "]}"

    data = {
        'allmessage':strJson
    }
    return JsonResponse(data)



#メッセージを送信したらAjaxでデータを登録
def messageSubmitfunc(request):

    message = request.GET.get('message', None)
    userId = int(request.GET.get('userId',None))
    friendId = int(request.GET.get('friendId', None))

    TalkMessageList.objects.create(message=message, fromuser=userId, touser=friendId)

    talkmessagelist = TalkMessageList.objects.filter(Q(fromuser=userId) | Q(fromuser=friendId), Q(touser=userId) | Q(touser=friendId))

    strJson = "{\"talkmessage\" : ["
    for talkmessage in talkmessagelist :

        strJson += "{\"message\":\"" + talkmessage.message +"\",\"touser\":\"" + str(talkmessage.touser) + "\",\"fromuser\":\"" + str(talkmessage.fromuser) + "\"},"

    strJson = strJson[:-1]
    strJson += "]}"

    data = {
        'message': message,
        'allmessage':strJson
    }
    return JsonResponse(data)







