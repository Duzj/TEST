from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from firstapp.models import Event, Guest
#引用Django中的pageinator实现嘉宾分页功能
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


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

# @login_required          #必须登录才能访问该页面
def event_manage(request):
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    event_list = Event.objects.all()      # 查询发布会数据
    username = request.session.get('user', '')
    return render(request, "HTML/event_manage.html", {'user': username, 'events': event_list})

#嘉宾页面处理
# @login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guests = Guest.objects.all()
    paginator = Paginator(guests, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of results
        contacts = Paginator.page(paginator.num_pages)
    return render(request, "HTML/guest_manage.html", {'user': username, 'guests': contacts})

#发布会搜索表单处理
def search_name(request):
    search_name = request.GET.get("name", '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "HTML/event_manage.html", {'events': event_list})


#嘉宾搜索表单处理
def guest_name(request):
    search_realname = request.GET.get("real_name", '')
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of results
        contacts = Paginator.page(paginator.num_pages)
    return render(request, "HTML/guest_manage.html", {'guests': contacts})

#发布会签到处理
# @login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'HTML/sign_incex.html', {'event', event})
