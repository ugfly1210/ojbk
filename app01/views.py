import json,os
from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.db import transaction
from django.db.models import F
from app01 import forms
from django.db.models import Count, Sum
from django.http import JsonResponse
from blog import settings

def reg(request):
    if request.method == 'GET':
        form = forms.RegForm()
        return render(request,'reg.html',{'form':form})
    else :
        form = forms.RegForm(request.POST)
        regResponse = {'user':None,'errors':None}
        if not form.is_valid():
            regResponse['errors'] = form.errors
        else :
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            nickname = form.cleaned_data['inputnickname']
            avatar_img = request.FILES['avatar_img']
            if avatar_img:  #如果有头像,就创建用户选定的
                models.Userinfo.objects.create(nickname=nickname,email=email,avatar=avatar_img)
                obj = models.User.objects.create(username=username,password=password)
            else:  #如果没有,就使用默认.
                models.Userinfo.objects.create(nickname=nickname, email=email)
                obj = models.User.objects.create(username=username, password=password)
#   你创建的ava_img就保存在upload_to指定的media下面的这个路径里面,它在数据库里面保存的是路径
            regResponse['user']=obj.username

        import json
        return HttpResponse(json.dumps(regResponse))

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST' :
        username = request.POST.get('name')
        pwd = request.POST.get('pwd')
        validCode = request.POST.get('validCode')
#因为前端是ajax,返回页面没用,所以要给他返回一个状态,
# 而json能适配的 就是一个字典.所以写成这种格式.
        login_response = {'flag':False,'error_massage':None}
        if validCode.upper() == request.session.get('validCode').upper():
            user_obj = models.User.objects.filter(username=username,password=pwd).first()
            print('user_obj===',user_obj)
            # userinfo_obj = models.Userinfo.objects.filter(user__username=user,user__password=pwd).first()
            if not  user_obj:
                login_response['error_massage'] = 'username or password is error!'
            else :
                login_response['flag'] = True
                #这步特别关键,要把登录状态保存在session中.   一定一定!!!
                request.session['user'] = user_obj.username
                request.session['user_id'] = user_obj.userinfo.id
                request.session['nickname'] = user_obj.userinfo.nickname
                # request.session['user_obj'] = user_obj


                '''作者和出版社 多对一'''
                '''通过出版社拿作者'''

        else :
            login_response['error_massage'] = 'validCode is error!'
        import json
        print('------------',login_response,type(login_response))
        return HttpResponse(json.dumps(login_response))
    return render(request,'login.html')

#获得验证码
def get_validCode_img(request):


    # 方式1：
    # import os
    # path= os.path.join(settings.BASE_DIR,"blog","static","img","egon.jpg")
    #
    # with open(path,"rb") as f:
    #     data=f.read()

    # 方式2：
    # from  PIL import Image
    #
    # img=Image.new(mode="RGB",size=(120,40),color="green")
    #
    # f=open("validCode.png","wb")
    # img.save(f,"png")
    #
    # with open("validCode.png","rb") as f:
    #     data=f.read()

    # 方式3：
    # from io import BytesIO
    #
    # from PIL import Image
    # img = Image.new(mode="RGB", size=(120, 40), color="blue")
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()
    # return HttpResponse(data)

    # 方式4 ：
    import random
    from io import BytesIO
    from PIL import Image,ImageDraw,ImageFont
    img = Image.new(mode='RGB',size=(120,40),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    draw = ImageDraw.Draw(img,'RGB')
    font = ImageFont.truetype('app01/static/blog/font/kumo.ttf',25)

    valid_list = []
    for i in range(5):
        random_num = str(random.randint(0,9))
        random_lower_alpha = chr(random.randint(65,90))
        random_upper_alpha = chr(random.randint(97,122))

        random_char = random.choice([random_num,random_lower_alpha,random_upper_alpha])
        draw.text([5+i*25,10],random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        valid_list.append(random_char)

    #将img保存在BytesIO中
    #这里如果报错,是需要创建一个BytesIO的对象的
    obj = BytesIO()
    img.save(obj,'png')
    data=obj.getvalue()   #获取写入的字节内容g
    valid_str = ''.join(valid_list)
    print('valid_str===',valid_str)
    #把valid_str放进session中,一会可以拿出来,在他登录的时候,和用户输入的进行对比.
    request.session['validCode'] = valid_str
    return HttpResponse(data)

def base(req):
    return render(req,'home_site.html')

def index(request,*args,**kwargs):
    if kwargs:
        #如果kwargs有值,说明用户访问的是网站里面大类里面的小类.例如 : 编程语言-->python,然后就把分类为python的显示粗来就好
        article_list = models.Article.objects.filter(site_article_category__name=kwargs.get('site_article_category'))
    else:
        # 渲染文章要用到文章列表
        article_list = models.Article.objects.all()
        # 渲染分类,所以我们要拿到分类列表
        # 网站分类 分为两层,大类和小类
    cate_list = models.SiteCategory.objects.all()
    return render(request, 'index.html', {'article_list': article_list, 'cate_list': cate_list})

def log_out(req):
    req.session.flush()
    return redirect('/login/')

def homesite(request,**kwargs):
    # print(request.session.get('username'))
    if not request.session.get('user'):
        return redirect('/login/')
    else :
        current_user = models.Userinfo.objects.filter(nickname=kwargs["username"]).first()
        #博客和用户是一对一关系,  现在有用户,如何拿到它的博客
        current_blog = models.Blog.objects.filter(user=current_user).first()
        # current_blog1 = models.Blog.objects.filter(user=current_user).first()

        if not current_user:
            return render(request,'gg.html')

        #拿到当前用户所有的文章
        article_list = models.Article.objects.filter(user=current_user).all()
        print('article_lis===',article_list)
        #拿到当前用户所有的文章分类     要拿到分类名称以及 该分类下的文章数
        category_list = models.Category.objects.filter(blog=current_blog).annotate(c=Count('article__id')).values_list('c','title')
        print('category_list===',category_list)
        #拿到当前用户所有的标签
        tag_list = models.Tag.objects.filter(blog=current_blog).annotate(c=Count('article__id')).values_list('c','title')
        print('tag_list===',tag_list)
        #拿到当前用户所有的日期
        #extra是在   django提供的查询语法不够用时,使用django提供的一种结果修改器,尽量少用
        #select的作用是:  声明一个额外的sql表字段.键值对
        #键就是额外生成的表字段,值就是字段对应的表记录值
        date_list = models.Article.objects.filter(user=current_user).\
            extra(select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).\
            values_list("filter_create_date").annotate(Count("id"))
        print('date_list===',date_list)


        if kwargs:
            if kwargs.get('condition') == 'category':
                #这里的 user=current_user 比较的是dom对象,     filter里面要比较两个值,一个是当前登录的用户,还有一个是url里面传过来的'para'
                article_list = models.Article.objects.filter(user=current_user,category__title=kwargs.get('para'))
            elif kwargs.get('conditon') == 'tag':
                article_list = models.Article.objects.filter(user=current_user,tags__title=kwargs.get('para'))
            elif kwargs.get('condition') == 'date':
                #如果选的是日期,  通过取kwargs中的para,可以打印看一下. 按/切分,拿到年和月两个参数.
                #取表中create_time中的年和月,直接__year,__month
                year,month = kwargs.get('para').split('/')
                article_list = models.Article.objects.filter(user=current_user,create_time__year=year,create_time__month=month)
        return render(request,'home_site.html',locals())

def article_detail(request,**kwargs):
    if not request.session.get('user'):
        return redirect('/login/')
    else:
        current_user = models.Userinfo.objects.filter(nickname=kwargs["username"]).first()
        # 博客和用户是一对一关系,  现在有用户,如何拿到它的博客
        current_blog = models.Blog.objects.filter(user=current_user).first()
        # current_blog1 = models.Blog.objects.filter(user=current_user).first()
        # print('current_blog===',current_blog)
        # print('current_blog1======',current_blog1)
        if not current_user:
            return render(request, 'gg.html')
        # 拿到当前用户所有的文章
        article_list = models.Article.objects.filter(user=current_user).all()
        # 拿到当前用户所有的文章分类     要拿到分类名称以及 该分类下的文章数
        category_list = models.Category.objects.filter(blog=current_blog).annotate(c=Count('article__id')).values_list('c', 'title')
        # 拿到当前用户所有的标签
        tag_list = models.Tag.objects.filter(blog=current_blog).annotate(c=Count('article__id')).values_list('c','title')
        #拿到当前文章所有的评论
        comment_list = models.Comment.objects.filter(article_id=kwargs.get('article_id')).all()
        # 拿到当前用户所有的日期
        # extra是在   django提供的查询语法不够用时,使用django提供的一种结果修改器,尽量少用
        # select的作用是:  声明一个额外的sql表字段.键值对
        # 键就是额外生成的表字段,值就是字段对应的表记录值
        date_list = models.Article.objects.filter(user=current_user). \
            extra(select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}). \
            values_list("filter_create_date").annotate(Count("id"))


        obj = models.Article.objects.filter(id=kwargs.get('article_id')).first()
        print('obj===',obj)
        # return render(request,'article_detail.html',{'obj':obj,})
        return render(request,'article_detail.html',locals())

def poll(request):
    #我们写点赞,要知道是哪个用户给哪篇文章点了赞,而且要看该用户是否是第一次给当前文章点赞,所以有必要拿到用户
    if not request.session.get('user'):
        return redirect('/login/')
    else:
        '''
        待会要从文章点赞表中拿数据
        文章点赞表和userinfo表有关联.
        我在session中存的一个username在user表      nickname在userinfo表中.
        所以从session中拿nickname'''
        nickname = request.session.get('nickname')
        print('nickname===',nickname)
        uid = models.Userinfo.objects.filter(nickname=nickname).first().id
        print('nickname,uid===',nickname,uid)
        aid = request.POST.get('article_id')
        print('aid===',aid)

        obj = models.ArticleUp.objects.filter(article_id=aid,user_id=uid).first()
        poll_response = {'state':False,'repeat':False}
        if obj :
            poll_response['repeat'] = True
        else:
            #如果没有,就创建该用户和文章的关系
            #点赞了之后数据库创建了赞记录,相对应的文章表里面的poll_count字段也要+1,
            #所以把它俩限定为同一事务
            #这两条任意谁出错就会回滚
            with transaction.atomic():
                art_up = models.ArticleUp.objects.create(article_id=aid,user_id=uid)
                # print('art_up===',art_up)
                #然后让文章点赞数加1
                models.Article.objects.filter(id=aid).update(poll_count=F('poll_count')+1)
                poll_response['state']=True
                print('poll_response===',poll_response)

        return HttpResponse(json.dumps(poll_response))

def comment(request):
    print("++++++++++++++++++++++++++++++++++++++",request.session["nickname"])
    print("request.session[]", request.session.get("user_id"))

    user_obj = models.Userinfo.objects.filter(id=request.session['user_id']).first()
    avator_user = user_obj.avatar.url

    print("avatar_____🎃🎃🎃🎃🎃🎃🎃_user",avator_user)


    aid = request.POST.get('article_id')
    comment_content = request.POST.get('content')
    Pid = request.POST.get('Pid')
    '''如果是对文章评论的话,需要传三个值 : 文章id,用户id(我们可以从session中拿),评论内容
    如果是对评论评论的话,要传的值就多一个 : 要传一个parent_id.
    这俩可以走一个视图函数, 判断一下parent_id是否有值,就可以知道是文章评论还是评论评论'''
    CommentResponse = {}
    if request.POST.get('Pid'):  #有Pid说明,是回复别人的评论,  它属于子评论
        with transaction.atomic():
            print("equest.session.get('user_id')equest.session.get('user_id')",request.session.get('user_id'))
            comment_obj = models.Comment.objects.create(article_id=aid,parent_comment_id=Pid,user_id=request.session.get('user_id'),content=comment_content)
            models.Article.objects.filter(id=aid).update(comment_count=F('comment_count')+1)
            CommentResponse['parent_comment_nickname'] = comment_obj.parent_comment.user.nickname
            CommentResponse['parent_comment_content'] = comment_obj.parent_comment.content
    else:  #文章评论
        #创建事务
        with transaction.atomic():
            #评论表创建数据
            comment_obj = models.Comment.objects.create(user_id=request.session.get("user_id"), article_id=aid,content=comment_content)
            #文章表中,comment_count+1
            models.Article.objects.filter(id=aid).update(comment_count=F('comment_count')+1)
        #在表中创建完成后,就可以去前端页面操作了

        #返回的内容一定要有用,咱们先返回它的创建时间,用户和article前端有可以拿到,我们还需要时间,所以就先传时间过去
            #拿到上面创建的评论的时间拿过来就可以
    # print(comment_obj.create_time)
    CommentResponse['create_time'] = str(comment_obj.create_time)
    CommentResponse['comment_id'] = comment_obj.id
    CommentResponse["ava"] = avator_user
    # return HttpResponse(json.dumps(CommentResponse))
    # return HttpResponse('🎃🎃🎃')
    return JsonResponse(CommentResponse,safe=False)

def commentTree(request,article_id):
    # print('11111111111111')
    '''拿到当前文章所有的评论,然后给它搞成一定格式,像权限管理那样'''
    comment_dict = {}
    comment_list = models.Comment.objects.filter(article_id=article_id).values('id','content','parent_comment_id')
    # print('comment_list===',comment_list)
    # comment_list == = < QuerySet[{'id': 30, 'content': '说爱我...asdf', 'parent_comment_id': None}, {'id': 31,'content': '说爱我...12321','parent_comment_id': None}, {'id': 32, 'content': '说爱我...12321', 'parent_comment_id': None}, {'id': 33,'content': '说爱我...12321','parent_comment_id': None}, {'id': 34, 'content': '说爱我...sdfdsf', 'parent_comment_id': None}] >

    for comment in comment_list:
        # print(comment)   {'id': 35, 'content': '说爱我...123123123123123', 'parent_comment_id': None}
        comment['children_comment_list'] = []
        comment_dict[comment['id']]=comment

    commentTree=[]
    for comment in comment_list:
        #有pid,就说明是子评论
        if comment.get('parent_comment_id'):
            #多个子评论可能属于一个父评论,所以用append
            comment_dict[comment['parent_comment_id']]['children_comment_list'].append(comment)
            '''{35: {'id': 35, 'content': '说爱我...123123123123123', 'parent_comment_id': None, 'children_comment_list': []}, 36: {'id': 36, 'content': '说爱我...123123213213', 'parent_comment_id': None, 'children_comment_list': [{'id': 37, 'content': '123123', 'parent_comment_id': 36, 'children_comment_list': [{'id': 38, 'content': '1231232132132132', 'parent_comment_id': 37, 'children_comment_list': []}]}]}, 37: {'id': 37, 'content': '123123', 'parent_comment_id': 36, 'children_comment_list': [{'id': 38, 'content': '1231232132132132', 'parent_comment_id': 37, 'children_comment_list': []}]}, 38: {'id': 38, 'content': '1231232132132132', 'parent_comment_id': 37, 'children_comment_list': []}, 39: {'id': 39, 'content': '说爱我...123213123213213', 'parent_comment_id': None, 'children_comment_list': [{'id': 40, 'content': 'dsfdsfds', 'parent_comment_id': 39, 'children_comment_list': []}]}, 40: {'id': 40, 'content': 'dsfdsfds', 'parent_comment_id': 39, 'children_comment_list': []}}'''
            # print(comment_dict)
        else:
            commentTree.append(comment)


    print(type(commentTree),'commentTree-----',commentTree)
    # < class 'list'> commentTree-----[{'id': 35, 'content': '说爱我...123123123123123'
    # , 'parent_comment_id': None, 'children_comment_list': []}, {'id': 36, 'content': '说爱我...123123213213',
    #                                                             'parent_comment_id': None, 'children_comment_list': [
    #         {'id': 37, 'content': '123123', 'parent_comment_id': 36, 'children_comment_list': [
    #             {'id': 38, 'content': '1231232132132132', 'parent_comment_id': 37, 'children_comment_list': []}]}]}, {
    #                                                                'id': 39, 'content': '说爱我...123213123213213',
    #                                                                'parent_comment_id': None, 'children_comment_list': [
    #         {'id': 40, 'content': 'dsfdsfds', 'parent_comment_id': 39, 'children_comment_list': []}]}]

    print(json.dumps(commentTree),type(json.dumps(commentTree)))
    # [{"id": 35, "content": "\u8bf4\u7231\u6211...123123123123123", "parent_comment_id": null,
    #   "children_comment_list": []},
    #  {"id": 36, "content": "\u8bf4\u7231\u6211...123123213213", "parent_comment_id": null, "children_comment_list": [
    #      {"id": 37, "content": "123123", "parent_comment_id": 36, "children_comment_list": [
    #          {"id": 38, "content": "1231232132132132", "parent_comment_id": 37, "children_comment_list": []}]}]},
    #  {"id": 39, "content": "\u8bf4\u7231\u6211...123213123213213", "parent_comment_id": null, "children_comment_list": [
    #      {"id": 40, "content": "dsfdsfds", "parent_comment_id": 39, "children_comment_list": []}]}] <
    #
    # class 'str'>

    return HttpResponse(json.dumps(commentTree))

#后台管理页面,用户在homesite页面点击管理,跳转到当前路径
def backend(request):
    article_list = models.Article.objects.filter(user__nickname=request.session['nickname']).all()
    return render(request,'backend_index.html',{'article_list':article_list})

def add_article(request):
    if not request.session.get('nickname'):
        return redirect('/login/')
    if request.method == 'GET':
        add_art = forms.Add_article()
        return render(request, 'add_art.html', {'add_art': add_art})

    else:
        user_obj = models.Userinfo.objects.filter(nickname=request.session.get('nickname')).first()
        add_art = forms.Add_article(request.POST)
        if add_art.is_valid():
            title = add_art.cleaned_data.get('title')
            content = add_art.cleaned_data.get('content')
            art_obj = models.Article.objects.create(title=title,summary=content[:30],user=user_obj)
            models.ArticleDetail.objects.create(content=content,article=art_obj)
            return redirect('/blog/backend/')

def edit_article(request,article_id):
    if not request.session.get('nickname'):
        return redirect('/login/')
    if request.method == 'GET':
        art_obj = models.Article.objects.filter(id=article_id).first()
        form = forms.Add_article(initial={'title':art_obj.title,'content':art_obj.articledetail.content})
        return render(request,'edit_art.html',{'form':form})
    else:
        user_obj = models.Userinfo.objects.filter(nickname=request.session.get('nickname')).first()
        form = forms.Add_article(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            art_obj = models.Article.objects.create(title=title, summary=content[:30], user=user_obj)
            models.ArticleDetail.objects.filter(article=art_obj).update(content=content)
            return redirect('/blog/backend/')

def del_article(request,article_id):
    flag = False
    obj = models.Article.objects.filter(id=article_id).delete()
    if obj :
        flag=True
    # models.ArticleDetail.objects.filter(article_id=article_id).delete()
    # print('--------------')
    return HttpResponse(flag)

def uploadFile(request):
    print("POST",request.POST)
    print("FILES",request.FILES)
    file_obj=request.FILES.get("imgFile")
    file_name=file_obj.name


    path=os.path.join(settings.MEDIA_ROOT,"article_uploads",file_name)
    with open(path,"wb") as f:
        for i in file_obj.chunks():
            f.write(i)

    response={
        "error":0,
        "url":"/media/article_uploads/"+file_name+"/"

    }

    import json
    return HttpResponse(json.dumps(response))

