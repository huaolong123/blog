from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from blogapp.models import *
from django.core.paginator import Paginator

def loginValid(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get('username')
        if username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login')
    return inner

def ceshi(request):
    return HttpResponse('hello')

def about(request):
    return render(request,'about.html')

@loginValid
def index(request):
    # username = request.COOKIES.get('name')
    # if username:
    article = Article.objects.order_by('-data')[:6]
    recommend_article = Article.objects.filter(recommend=1).all()[:7]
    click_article = Article.objects.order_by('-click')[:12]
    return render(request,'index.html',locals())
    # else:
    #     return HttpResponseRedirect('/login/')

def listpic(request):
    return render(request,'listpic.html')

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

#  md5加密
import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

from blogapp.forms import Register
def register(request):
    register_form = Register()
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     password2 = request.POST.get('password2')
    #     if password != password2:
    #         print('两次密码不一样')
    #         pass
    #     else:
    #         user = User()
    #         user.name = username
    #         user.password = setPassword(password)
    #         user.save()
    # 前端验证
    # if request.method == 'POST':
    #     username = request.POST.get('name')
    #     password = request.POST.get('password')
    #     content = '参数不全'
    #     if username and password:
    #         user = User()
    #         user.name = username
    #         user.password = setPassword(password)
    #         user.save()
    #         content = '添加成功'

    # 后端验证
    error = ''
    #  !!!固定写法
    if request.method == 'POST':
        data = Register(request.POST)  #将POST传来的请求进行校验
        if data.is_valid():  #判断校验是否为True
            clean_data = data.cleaned_data  #返回一个字典类型
            username = clean_data.get('name')
            password = clean_data.get('password')
            # user = User()
            # user.name = username
            # user.password = setPassword(password)
            # user.save()
            # error = '添加成功'
            user = User.objects.filter(name=username).first()
            if user:
                error = '用户名已存在，换一个吧!'
            else:
                user.name = username
                username = setPassword(password)
                user.save()
                error = '注册成功'
        else:
            error = data.errors
            print(error)

    return render(request,'register.html',locals())

from django.http import HttpResponseRedirect
def login(request):
    error = ''
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        passwordold = data.get('password')
        password = setPassword(passwordold)
        print(username)
        if User.objects.filter(name=username,password=password).first() is None:
            error = '用户名或密码错误'
        else:
            response = HttpResponseRedirect('/index/')
            response.set_cookie('username',username)
            request.session['username']=username
            return response

    return render(request,'login.html',locals())

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
    response = HttpResponseRedirect('/index/')
    response.delete_cookie('username')
    del request.session['username']
    # request.session.flush()  #  删除所有的session
    return response