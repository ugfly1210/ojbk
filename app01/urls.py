from django.conf.urls import url
from app01 import views


#http://127.0.0.1:8000/blog    /ddd/category/1

urlpatterns = [
    url(r'^poll/$', views.poll),
    url(r'^comment/$', views.comment),
    url(r'^comment_tree/(?P<article_id>\d+)/$', views.commentTree),

    url(r'^backend/$', views.backend),
    url(r'^backend/add_article/$', views.add_article),
    url(r'^backend/edit_article/(?P<article_id>\d+)/$', views.edit_article),
    url(r'^backend/del_article/(?P<article_id>\d+)/$', views.del_article),
    # url(r'^backend/edit_article/(?P<article_id>\d+$)', views.edit_article),

    url(r'^(?P<username>.*)/(?P<condition>tag|category|date)/(?P<para>.*)', views.homesite),
    # http://127.0.0.1:8000/blog/肖碧赤/articles/1/
    url(r'^(?P<username>.*)/articles/(?P<article_id>\d+)', views.article_detail),
    url(r'^(?P<username>.*)/$', views.homesite,name="aaa"),
]
