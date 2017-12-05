from django.forms import Form,fields,widgets,forms
from app01 import models
#判断正则
from django.core.validators import RegexValidator
#捕捉错误
from django.core.exceptions import ValidationError


class RegForm(Form):
    email = fields.EmailField(
        required=True,
        error_messages={'required':'邮箱不能为空!'},
        widget=widgets.EmailInput(
            attrs={'placeholder': 'Email💃💃💃', 'type': "email", 'class': "form-control"})
    )
    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=16,
        error_messages={
            'required' : '用户名不能为空!',
            'min_length' : '稍微长点哦',
            'max_length' : '稍微短点哦'
        },
        widget=widgets.TextInput(attrs={'placeholder':'输!名字!','type':"text",'class':"form-control"})
    )
    password = fields.CharField(
        required=True,
        min_length=6,
        max_length=16,
        error_messages={
            'required' : '密码不能为空',
            'min_length' : '密码短短短',
            'max_length' : '稍微短点兄弟',
            'invalid' : '密码格式有问题'
        },
        widget=widgets.PasswordInput(attrs={'placeholder': '输!密码!', 'type': "password", 'class': "form-control"}),
        validators=[RegexValidator('/d+','密码只能为数字.')]
        # validators=[RegexValidator('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z_]{8,16}$',
        # '可以包含数字、字母、下划线，并且要同时含有数字和字母，且长度要在8-16位之间。')]
    )
    repassword = fields.CharField(
        required=True,
        min_length=6,
        max_length=16,
        error_messages={
            'required': '密码不能为空',
        },
        widget=widgets.PasswordInput(
            attrs={'placeholder': '重复密码', 'type': "password", 'class': "form-control"})
    )

    tel = fields.CharField(
        required=True,
        max_length=15,
        min_length=11,
        error_messages={
            'required' : '电话号码不能为空!',
            'min_length' : '你家电话号码这么短?',
            'max_length' : '你家走哪买的电话卡'
        },
        widget=widgets.NumberInput(
            attrs={'placeholder': 'shu! dianhua !', 'type': "number", 'class': "form-control"})
    )

    nickname = fields.CharField(
        required=True,
        max_length=32,
        min_length=1,
        error_messages={
            'required' : '昵称不阔以为空!',
            'min_length' : '您太短',
            'max_length' : '昵称长度超过最大限制'
        },
        widget=widgets.TextInput(
            attrs={'placeholder': "shu! nicheng!", 'type': "text", 'class': "form-control"})
    )
    #头像不需要验证,所以不用写在form里面.可以拿出来单独写
    # avatar = fields.FileField(
    #     required=False,
    #     widget=widgets.FileInput(attrs={'id':'avatar'})
    # )
    #下面是格式输入通过,  然后可以拿到用户输入的数据,去和数据库的值比对,用到的是源码中的clean_字段名的方法
    def clean_username(self):
        # 因为格式没错,所以我们可以从clean_data中,拿到用户输入的数据
        user = self.cleaned_data.get('username')
        # 去比对,看用户输入的用户名在数据库里是否存在
        is_exist = models.User.objects.filter(username=user).count()
        if is_exist:
            # 如果存在,就捕捉错误.用raise V方法
            raise ValidationError('用户名已存在,请重新输入')
        return user

    def clean_email(self):
        try :
            email = self.cleaned_data.get('email')
            is_exist = models.Userinfo.objects.filter(email=email).count()
            if is_exist:
                raise ValidationError('邮箱已被注册!')
            return email
        except Exception as e:
            print('except: ' + str(e))
            raise ValidationError(u"注册账号需为邮箱格式")


#form本来就是用来验证,所以有关验证的我们尽量都放在form组件里面来做.
    def clean(self):
        if self.cleaned_data.get('password')==self.cleaned_data.get('repassword'):
          return self.cleaned_data
        else:
            raise ValidationError('两次密码输入不一致!')



class Add_article(Form):
    title = fields.CharField(max_length=32,required=True,error_messages={'requeired':'标题不能为空'},
                             widget=widgets.TextInput())
    content = fields.CharField(required=True,error_messages={'requeired':'内容不能为空'},widget=widgets.Textarea())


    def clean_content(self):
        html_str = self.cleaned_data.get('content')
        from app01.plugins import xxs_plugin
        #这里最开始不理解,  为什么可以直接返回调用函数.
        #联想之前, 写的clean_username.最后返回的也是一个通过验证的Httpresponse(username)  就理解了.这里返回的是筛选过后的用户输入的内容.
        return xxs_plugin.filter_tag(html_str)