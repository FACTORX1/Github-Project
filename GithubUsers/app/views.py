from django.shortcuts import render, HttpResponse
import requests
import json
import calendar
from app.models import GithubUser
import datetime

# Create your views here.

def index(request):
    return HttpResponse('Hello world')

def test(request):
    return HttpResponse('Test page')

def profile(request):
    parsedData = []
    if request.method == 'POST':
        username = request.POST.get('user')
        #ids = request.POST.get('avatar_url')
        req = requests.get('https://api.github.com/users/' + username)
       # image = requests.get('https://avatars0.githubusercontent.com/u/' + ids + '?v=4')
        jsonList = []
        #imagess = []
        jsonList.append(json.loads(req.content.decode('utf-8')))
        #jsonList.append(json.loads(ids.content.decode('utf-8')))
        #imagess.append(json.loads(ids.content.decode('utf-8')))
        userData = {}
        #images = {} 

        try:

            for data in jsonList:
                    userData['id'] = data['id']
                    userData['name'] = data['name']
                    userData['blog'] = data['blog']
                    userData['email'] = data['email']
                    userData['public_gists'] = data['public_gists']
                    userData['public_repos'] = data['public_repos']
                    userData['followers'] = data['followers']
                    userData['following'] = data['following']
                    userData['location'] = data['location']
                    userData['avatar_url'] = data['avatar_url']
            parsedData.append(userData)
            SaveToDB(parsedData)
        except:
            return HttpResponse("Object Not found")
    return render(request, 'app/profile.html', {'data': parsedData})

def SaveToDB(parsedData):
    for data in parsedData:
        p1 = GithubUser.objects.get_or_create(
            user_id = data['id'],
            username = data['name'],
            blog = data['blog'],
            email = data['email'],
            followers = data['followers'],
            following = data['following'],
            location = data['location'],
            avatar = data['avatar_url'],
        )

    return True
# def filter(request):
#     start = request.POST.get('start')
#     ends = request.POST.get('ends') 
#     Userd = 'SELECT username FROM GithubUser WHERE start>=01/01/1000 AND ends<=31/12/3000'
        
#     return render(request, 'app/filter.html')

def filter(request):
    if request.method == 'GET':
        return render(request, 'app/filter.html')
    if request.method == 'POST':
        userData={}
        a=[]
        start = request.POST.get('start')
        ends = request.POST.get('ends')
        for user in GithubUser.objects.all():
            datetime_start = datetime.datetime.strptime(str(user.date).split(" ")[0], '%Y-%m-%d')
            start1 = datetime.datetime.strptime(start, '%Y-%m-%d')
            ends1 = datetime.datetime.strptime(ends, '%Y-%m-%d')
            if  start1 <= datetime_start <= ends1:
                userData['id'] = user.user_id
                userData['name'] = user.username
                userData['blog'] = user.blog
                userData['email'] = user.email
                userData['followers'] = user.followers
                userData['following'] = user.following
                userData['location'] = user.location
                userData['avatar_url'] = user.avatar
                # print("__________________")
                # print(userData)
                a.append(userData.copy())
                # print(a)
                # print("------------------"
            
    #Userd = GithubUser.objects.filter('start'>1000) & GithubUser.objects.filter('ends'<3000)
        return render(request, 'app/filter.html',{'data':a})

        
    