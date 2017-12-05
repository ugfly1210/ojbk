"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from django.conf.urls.static import static
from django.views.static import serve
from blog import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^$', views.index),  # index(requset)
    url(r'^cate/(?P<site_article_category>.*)/$', views.index),  # index(requset,site_atricle_category=python)
    url(r'^reg/', views.reg),
    url(r'^base/', views.base),
    url(r'^logout/', views.log_out),

    url(r'^uploadFile/$', views.uploadFile),

                  #个人站点首页
    url(r'^blog/', include('app01.urls')),

    #获取验证码
    url(r'^get_validCode_img/', views.get_validCode_img),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


#配置media
url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
