from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible

class Category(models.Model):
    """
    Django要求模型必须继承models.Model类
    category 只要求一个简单的分类名name就可以了
    CharField 指定了分类名name的数据类型，即字符型
    max_length指定其最大长度，超出长度不能被存入数据库
    """
    name = models.CharField(max_length=100)

class Tag(models.Model):
    """
    文章标签类和Category类一样，要继承models.Model类
    """
    name = models.CharField(max_length=100)
class Post(models.Model):
    """
    文章的数据库表稍微复杂一些，主要涉及的字段更多
    """
    # 文章标签
    title = models.CharField(max_length=70)
    # 文章正文，我们使用了TextField
    # 文章正文可能会是大段文字，使用TextField来存储
    body = models.TextField()

    # 这两个表示文章的创建时间和最后一次修改时间，用DateTimeField 来存储时间字段
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，默认情况下 CharField 会要求必须存入数据，否则就会报错
    # 指定blank = True 参数值后就可以允许空值了
    excerpt = models.CharField(max_length=200,blank=True)

    # 这是分类与标签，分类与标签已经在上面定义
    # 把文章对应的数据库表和 分类、标签关联起来，但关联形式稍微有点不同
    # 我们规定一篇文章对应一个分类，但一个分类下可以有多篇文章，使用ForeignKey，即一对多的关联表示
    # 一篇文章可以有多个标签，同一个标签也可有多个文章，使用ManyToManyField，即多对多关联表示
    # 规定文章可以没有标签， blank = True
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里User 是从django.contrib.auth.models导入的
    # django.contrib.auth.models是Django的内置应用，专门用于处理网站用户的注册、登陆等流程
    # 同样，我们通过ForeignKey把文章和作者关联起来
    # 一篇文章只有一个作者，而一个作者可以写多篇文章，所以是一对多的关系，和Category类似
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    # 自定义get_absolute_url 方法
    # 记得从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
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


    class Meta:
        ordering = ['-create_time','title']
        # ordering 属性用来指定文章排序方式，['-created_time'] 指定了依据哪个属性的值进行排序，
        # 这里指定为按照文章发布时间排序，且负号表示逆序排列。列表中可以用多个项，
        # 比如 ordering = ['-created_time', 'title'] ，那么首先依据 created_time 排序，
        # 如果 created_time 相同，则再依据 title 排序。
        # 这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序，
        # 因此可以删掉视图函数中对文章列表中返回结果进行排序的代码了。








