from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def index(request):
    return render(request, "HTML/Login.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)  # 认证用户名、密码
       # if username == 'admin' and password == 'admin12345':
        if user is not None:
           auth.login(request, user)  # 登录
           request.session['user'] = username  # 将session信息记录到浏览器
           response = HttpResponseRedirect("/event_manage/")
           #response.set_cookie('user', username, 3600)   # 添加浏览器cookie
           return response
        else:
            return render(request, "HTML/Login.html", {'error': 'username or password error!'})
    else:
        return render(request, "HTML/Login.html", {'error': 'username or password error!'})

@login_required          #必须登录才能访问该页面
def event_manage(request):
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '')
    return render(request, "HTML/event_manage.html", {'user': username})
