from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from blogapp.models import *
from django.core.paginator import Paginator

# 定义一个检查cookie和session的装饰器
def LoginVaild(func):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get('username')
        session_name = request.session.get('username')
        if username and session_name and username==session_name:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

#  md5加密
import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def ceshi(request):
    return HttpResponse('hello')

@LoginVaild
def about(request):
    return render(request,'about.html')

def index(request):
    # username = request.COOKIES.get('name')
    # if username:
    article = Article.objects.order_by('-data')[:6]
    recommend_article = Article.objects.filter(recommend=1).all()[:7]
    click_article = Article.objects.order_by('-click')[:12]
    return render(request,'index.html',locals())
    # else:
    #     return HttpResponseRedirect('/login/')

@LoginVaild
def listpic(request):
    return render(request,'listpic.html')

@LoginVaild
def newslistpic(request,page=1):
    acticle = Article.objects.order_by('-data')
    paginator = Paginator(acticle,6)
    page_obj = paginator.page(page)
    current_page = page_obj.number
    start = current_page - 3
    if start < 1:
        start = 0
    end = current_page + 2
    if end > paginator.num_pages:
        end = paginator.num_pages
    if start == 0:
        end = 5
    page_range = paginator.page_range[start:end]

    return render(request,'newslistpic.html',locals())

def base(request):
    return render(request,'base.html')

def neirong(request,id):
    id = int(id)
    article = Article.objects.get(id=id)
    return render(request,'neirong.html',locals())

def addarticle(request):
    for x in range(100):
        article = Article()
        article.title = 'title_%s'% x
        article.content = 'content_%s'% x
        article.description = 'description_%s'% x
        article.author = Author.objects.get(id=1)
        article.save()
        article.type.add(Type.objects.get(id=1))
        article.save()
    return HttpResponse('增加数据')

def fytest(request):
    article = Article.objects.all().order_by('-data')
    paginator = Paginator(article,5)
    # print(paginator)
    # print(paginator.count)
    # print(paginator.page_range)
    # print(paginator.num_pages)

    page_obj = paginator.page(2)
    # print(page_obj)
    for i in page_obj:
        print(i.content)
    # print(page_obj.number)
    # print(page_obj.has_next())
    # print(page_obj.has_previous())
    # print(page_obj.has_other_pages())
    # print(page_obj.next_page_number())
    print(page_obj.previous_page_number())
    return HttpResponse('分页功能测试')

def reqtest(request):
    # print(request)
    # print(dir(request))
    # print(request.COOKIES)
    # print(request.FILES)
    # print(request.path)
    # print(request.GET)
    # print(request.scheme)
    # print(request.method)
    # print(request.body)
    # print(request.META)
    # print(request.META.get('HTTP_HOST'))
    # print(request.POST)
    data = request.POST

    return HttpResponse('姓名%s,年龄%s'%(data.get('name'),data.get('age')))

def formtest(request):
    # data = request.GET
    # serach = data.get('serach')
    # article = Article.objects.filter(title__contains=serach).all()

    data = request.POST
    print(data.get('username'))
    print(data.get('password'))

    return render(request,'formtest.html',locals())

def csrfdemo(request):

    return render(request,'csrfdemo.html',locals())



def ajaxget(request):
    return render(request,'ajaxget.html')

def ajaxget_data(request):
    result = {}
    data = request.GET
    username = data.get('username')
    password = data.get('password')
    if len(username)==0 or len(password)==0:
        result = {'code':10001,'content':'请求参数为空'}
    else:
        user = User.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            result['code']=10000
            result['content']='登录成功'
        else:
            result['code']=10002
            result['content']='用户名或者密码不正确'
    return JsonResponse(result)

def ajaxget_blur(request):
    result = {}
    username = request.GET.get('username')
    user = User.objects.filter(name=username).first()
    if user:
        result = {'code':10000,'content':'用户名正确'}
    else:
        result = {'code':10001,'content':'用户名不存在'}
    return JsonResponse(result)

def ajaxpost(request):
    return render(request,'ajaxpost.html')

def ajaxpost_data(request):
    result = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    if len(username)==0 or len(password)==0:
        result['code']=10001
        result['content']='用户名或密码不能为空'
    else:
        user = User()
        user.name=username
        user.password=setPassword(password)
        try:
            user.save()
            result['code']=10000
            result['content']='添加成功'
        except:
            result['code']=10002
            result['content']='添加失败'
    return JsonResponse(result)

def checkusername(request):
    result = {}
    username = request.GET.get('username')
    user = User.objects.filter(name=username).first()
    if user:
        result = {'code':10001,'content':'用户名已存在'}
    else:
        result = {'code':10000,'content':'用户名不存在'}
    return JsonResponse(result)

def nameblur(request):
    result = {}
    username = request.GET.get('username')
    user = User.objects.filter(name=username).first()
    if user:
        result = {'code':10000,"content":'用户名正确~'}
    else:
        result = {'code':10001,'content':'用户名不存在!'}
    return JsonResponse(result)

def ajaxget_demo(request):
    return render(request,'ajaxget_demo.html')

def ajaxget_demo_data(request):
    result = {}
    username = request.GET.get('username')
    password = request.GET.get('password')
    if len(username)==0 or len(password)==0:
        result = {'code':10001,'content':'用户名或密码不能为空!'}
    else:
        user = User.objects.filter(name=username).first()
        if user:
            result = {'code':10002,'content':'用户名已存在，换一个吧!'}
        else:
            user = User()
            user.name = username
            user.password = setPassword(password)
            user.save()
            result = {'code':10000,'content':'注册成功!'}
    return JsonResponse(result)

def ajaxpost_demo(request):
    return render(request,'ajaxpost_demo.html')

def ajaxpost_demo_data(request):
    result = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    if len(username)==0 or len(password)==0:
        result = {'code':10001,'content':'用户名或密码不能为空'}
    else:
        user = User.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            # return HttpResponseRedirect('/index/')
            result = {'code':10000,'content':'登陆成功'}
        else:
            result = {'code': 10002, 'content': '用户名或密码不正确'}
    return JsonResponse(result)

def login_demo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if len(username)==0 or len(password)==0:
            content = '用户名或密码不能为空'
        else:
            user = User.objects.filter(name=username,password=setPassword(password)).first()
            if user:
                data = HttpResponseRedirect('/index/')
                data.set_cookie('name',username)
                return data
            else:
                content = '用户名或密码错误'
    return render(request,'login_demo.html',locals())

def logout(request):
    response = HttpResponseRedirect('/login/')
    response.delete_cookie('username')
    response.delete_cookie('userid')
    del request.session['username']
    # request.session.flush()  #  删除所有的session
    return response


# 注册页面
def register(request):
    content = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if email:
            emailname = LoginUser.objects.filter(email=email).first()
            if emailname:
                content = '用户名已存在,换一个吧~'
            else:
                if password==password2:
                    loginuser = LoginUser()
                    loginuser.email = email
                    loginuser.password = setPassword(password)
                    loginuser.username = email
                    loginuser.save()
                    content = '注册成功!'
                else:
                    content = '两次密码不一样!'
        else:
            content = '邮箱不能为空!'
    return render(request,'register.html',locals())

# 登录页面
def login(request):
    content = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            loginuser = LoginUser.objects.filter(email=email).first()
            if loginuser:
                if loginuser.password == setPassword(password):
                    response = HttpResponseRedirect('/index/')
                    response.set_cookie('username',loginuser.username)
                    request.session['username']=loginuser.username
                    response.set_cookie('userid',loginuser.id)
                    return response
                else:
                    content = '密码错误!'
            else:
                content = '邮箱不存在!'
        else:
            content = '邮箱不能为空!'

    return render(request,'login.html',locals())

@LoginVaild
def myblog(request):
    error = ''
    email = request.COOKIES.get('username')
    author = Author.objects.filter(email=email).first()
    if author :
        article = author.article_set.all()
    else:
        error = '您还没有文章呢~'
    return render(request,'myblog.html',locals())

@LoginVaild
def addblog(request):
    data = Type.objects.all().values('name')
    type = []
    for i in data:
        type.append(i['name'])
    if request.method == 'POST':
        data = request.POST
        ar_type = data.get('type')
        type_obj = Type.objects.filter(name=ar_type).first()
        article = Article()
        article.title = data.get('title')
        article.content = data.get('content')
        article.description = data.get('description')
        article.type = type_obj
        article.picture = request.FILES.get('img')
        article.save()
    return render(request,'addblog.html',locals())