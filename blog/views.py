import markdown
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm
import pygments

# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})



def detail(request,pk):
    # 视图函数很简单，它根据我们从 URL 捕获的文章 id（也就是 pk，这里 pk 和 id 是等价的）
    # 获取数据库中文章 id 为该值的记录，然后传递给模板。
    # 注意这里我们用到了从 django.shortcuts 模块导入的 get_object_or_404 方法，
    # 其作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，
    # 如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。
    post = get_object_or_404(Post,pk=pk)
    #
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 在顶部到入 CommentForm
    form = CommentForm()
    # 获取这篇文章下的所有评论
    comment_list = post.comment_set.all()
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
               }
    return render(request, 'blog/detail.html', context=context) #{'post': post}


def archives(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
    # 我们使用了模型管理器（objects）的 filter 函数来过滤文章。
    # 由于是按照日期归档，因此这里根据文章发表的年和月来过滤。
    # 具体来说，就是根据 created_time 的 year 和 month 属性过滤，
    # 筛选出文章发表在对应的 year 年和 month 月的文章。
    # 注意这里 created_time 是 Python 的 date 对象，其有一个 year 和 month 属性，


def category(request, pk):
    #记得在开始部分导入Category类
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})
    # 我们首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类。
    # get_object_or_404 函数和 detail 视图中一样，其作用是如果用户访问的分类不存在，
    # 则返回一个 404 错误页面以提示用户访问的资源不存在。
    # 然后我们通过 filter 函数过滤出了该分类下的全部文章。
    # 同样也和首页视图中一样对返回的文章列表进行了排序。

def index1(request):
    # return HttpResponse("欢迎来到我的博客首页！")  # 直接把字符串传给 HttpResponse

    # 我们首先把 HTTP 请求传了进去，
    # 然后 render 根据第二个参数的值 blog/index.html 找到这个模板文件并读取模板中的内容。
    # 之后 render 根据我们传入的 context 参数的值把模板中的变量替换为我们传递的变量的值，
    # {{ title }} 被替换成了 context 字典中 title 对应的值，同理 {{ welcome }} 也被替换成相应的值。
    return render(request,'blog/index.html',context={
        'title':'我的博客首页',
        'welcome':'欢迎访问我的博客首页'

    })