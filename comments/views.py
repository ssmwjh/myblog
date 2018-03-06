from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request,post_pk):
    # 先获取被评论的文章，后面需要评论和该文章关联起来
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post,pk=post_pk)

    # HTTP 请求有GET和POST两种，一般用户通过表单提交数据通过POST请求
    # 因此，只有当用户的请求为POST时才需要处理表单数据
    if request.method == 'POST':
        # 用户提交的数据在request.POST中，这是一个类字典对象
        # 我们利用这些数据构造了CommentForm的实例，这样DJANGO的表单就生成了
        form = CommentForm(request.POST)
        # form .is_valid()方法自动帮助我们检查表单是否符合格式要求
        if form .is_valid():
            # 检查到数据合法时，调用表单的save功能保存数据到数据库
            # commit=False 的作用是仅仅利用表单的数据生成comment模型类的实例，
            # 但还不保存评论数据到数据库
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来
            comment.post = post

            # 最终将评论数据保存到数据库中
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = post.comment_set.all() # Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list

            }
            return render(request,'blog/detail.html',context=context)

    return redirect(post)
    # 我们使用了 redirect 函数。这个函数位于 django.shortcuts 模块中，
    # 它的作用是对 HTTP 请求进行重定向（即用户访问的是某个 URL，但由于某些原因，服务器会将用户重定向到另外的 URL）。
    # redirect 既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数（例如这里的 post）。
    # 如果接收一个模型的实例，那么这个实例必须实现了 get_absolute_url 方法，
    # 这样 redirect 会根据 get_absolute_url 方法返回的 URL 值进行重定向。