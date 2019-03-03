from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index_page(request):
    return render(request,"index_bs.html")

def login_anction(request):
    host=request.META.get("HTTP_HOST")
    print(request.method)
    if request.method == 'POST':
        login_username=request.POST.get("username","")
        login_password = request.POST.get("password","")
        print("----------------")
        print(login_username)
        print(login_password)
        print("----------------")
        if login_username=="" or login_password=="":
            return render(request, "index_bs.html",{"error":"username or password null"})
        else:
            user = auth.authenticate(username=login_username, password=login_password)
            print(user)
            if user is not None:
                auth.login(request, user)  # 登录
                response = HttpResponseRedirect('/event_manage/')  # http 302
                request.session['user'] = login_username  # 将 session 信息记录到浏览器
                return response
            else:
                return render(request, "index_bs.html", {"error": "username or password error"})
    else:
        return render(request, "index_bs.html")

#发布会管理
@login_required()
def event_manage(request):
    event_list=Event.objects.all()
    print(event_list)
    # username = request.COOKIES.get('user', '')  # 读取浏览器 cookie
    username = request.session.get('user', '')  # 读取浏览器 session
    return render(request, "event_manage.html",{"login_user":username,"events":event_list})

#搜索
@login_required()
def search_name(request):
    if request.method == 'GET':
        event_name=request.GET.get("event_name","")
        event_list=Event.objects.filter(name__contains=event_name)
        username = request.session.get('user', '')  # 读取浏览器 session
        return render(request, "event_manage.html", {"login_user": username, "events": event_list})


#嘉宾管理
@login_required()
def guest_manage(request):
    guest_list=Guest.objects.all()
    print(guest_list)
    username = request.session.get('user', '')  # 读取浏览器 session

    paginator = Paginator(guest_list, 4)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html",{"login_user":username,"guests":contacts})

# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
    username = request.session.get('username', '')

# 发布会签到页
@login_required
def sign_index(request,event_id):
    events = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)  # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)  # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': events,
                                               'guest': guest_data,
                                               'sign': sign_data})

# 签到动作
@login_required
def sign_index_action(request,event_id):

    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))

    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.get(event_id = event_id,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
            'user': result,
            'guest':guest_data,
            'sign':str(int(sign_data)+1)
            })

# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response