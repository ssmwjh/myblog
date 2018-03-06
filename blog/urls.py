from django.conf.urls import url
from .import views
app_name = 'blog'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    # url(r'^post/(?P<pk>[0-9]+/$)',views.detail,name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'), # P要大写！
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),
]

# 这个 reverse 函数，它的第一个参数的值是 'blog:detail'，
# 意思是 blog 应用下的 name=detail 的函数，
# 由于我们在上面通过 app_name = 'blog' 告诉了 Django 这个 URL 模块是属于 blog 应用的，
# 因此 Django 能够顺利地找到 blog 应用下 name 为 detail 的视图函数，
# 于是 reverse 函数会去解析这个视图函数对应的 URL，
# 我们这里 detail 对应的规则就是 post/(?P<pk>[0-9]+)/ 这个正则表达式，
# 而正则表达式部分会被后面传入的参数 pk 替换，
# 所以，如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，
# 那么 get_absolute_url 函数返回的就是 /post/255/ ，
# 这样 Post 自己就生成了自己的 URL。