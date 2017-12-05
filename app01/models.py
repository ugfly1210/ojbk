import time
from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    def __str__(self):
        return self.username

class Userinfo(models.Model):
    nickname = models.CharField(max_length=64)
    tel = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    email = models.EmailField(verbose_name='邮箱地址')
    avatar = models.FileField(verbose_name='头像',upload_to='avatar',default='/avatar/default.png')
                                  #avatar接收的就是一个文件对象, 接收过来就放到upload_to指定的位置去
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    user = models.OneToOneField(to='User')
    # fans = models.ManyToManyField(verbose_name='粉丝们',
    #                               to='Userinfo',
    #                               through='UserFans',
    #                               related_name='f',
    #                               through_fields=('user', 'follower'))
    def __str__(self):
        return self.nickname

class Blog(models.Model):
    # url = models.CharField(max_length=64)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    user = models.OneToOneField(to='Userinfo')

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    create_time = models.DateTimeField(verbose_name='创建日期',auto_now_add=True)
    # update_time = models.DateTimeField(verbose_name='最后修改',default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    summary = models.CharField(max_length=128,verbose_name='文章摘要')
    poll_count = models.IntegerField(verbose_name='点赞数',default=0)
    comment_count = models.IntegerField(verbose_name='评论数',default=0)
    read_count = models.IntegerField(verbose_name='阅读数',default=0)
    is_essence = models.BooleanField(verbose_name='是否精华',default=False)
    is_top = models.BooleanField(verbose_name='是否置顶',default=False)

    category = models.ForeignKey(verbose_name='文章类型', to='Category',null=True)
    user = models.ForeignKey(verbose_name='所属用户', to='Userinfo')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    #关联文章具体的分类
    site_article_category = models.ForeignKey("SiteArticleCategory", null=True)

    def __str__(self):
        return self.title

# class Classfication(models.Model):
#     name = models.CharField(max_length=32,verbose_name='文章类别')
#     def __str__(self):
#         return self.name
class Category(models.Model):
    """
    博主个人文章分类表
    """
    # nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'category'
        ordering = ['title']

class ArticleDetail(models.Model):
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章', to='Article')

    def __str__(self):
        return self.content

# class Comment(models.Model):
#     content = models.TextField(verbose_name='评论内容')
#     content_time = models.DateTimeField(verbose_name='评论时间',default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#
#
#     user = models.ForeignKey(verbose_name='评论者',to='Userinfo',default=None,null=True)
#     article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
#
#     '''评论和评论建立一个自关联,可以在评论下面继续评论'''
#     commentself = models.ForeignKey(to='Comment',null=True)
#     def __str__(self):
#         return self.content
class Comment(models.Model):
    """
    评论表
    """
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    up_count = models.IntegerField(default=0)

    user = models.ForeignKey(verbose_name='评论者', to='Userinfo')
    article = models.ForeignKey(verbose_name='评论文章', to='Article')
    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    def __str__(self):
        return self.content

class CommentUp(models.Model):
    """
    点赞表
    """
    user = models.ForeignKey('Userinfo', null=True)
    comment = models.ForeignKey("Comment", null=True)

class ArticleUp(models.Model):
    """
    点赞表
    """
    user = models.ForeignKey('Userinfo', null=True)
    article = models.ForeignKey("Article", null=True)

class Tag(models.Model):
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog')
    def __str__(self):
        return self.title

class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article")
    tag = models.ForeignKey(verbose_name='标签', to="Tag")

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

class SiteCategory(models.Model):
    '''大类'''
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class SiteArticleCategory(models.Model):
    '''小类,具体的文章分类'''
    name = models.CharField(max_length=32)

    site_category = models.ForeignKey("SiteCategory")

    def __str__(self):
        return self.name
# class Poll(models.Model):
#     poll_time = models.DateTimeField(verbose_name='点赞时间',default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#
#     userinfo = models.ForeignKey(verbose_name='谁点的赞',to='Userinfo')
#     article = models.ForeignKey(to='Article',verbose_name='点赞的是哪篇文章')
#     comment = models.ForeignKey(to='Comment',verbose_name='对评论点赞')
#
#     class Meta:
#         unique_together = ('userinfo','article','comment')
#
#
# class UserFans(models.Model):
#     """
#     互粉关系表
#     """
#     user = models.ForeignKey(verbose_name='博主', to='Userinfo',related_name='users')
#     follower = models.ForeignKey(verbose_name='粉丝', to='Userinfo',related_name='followers')
#
#     class Meta:
#         unique_together = [
#             ('user', 'follower'),
#         ]
