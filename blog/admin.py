from django.contrib import admin
from .models import Post,Category,Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','create_time','modified_time','category','author']



# Register your models here.
# 要在后台注册我们自己创建的几个模型，这样 Django Admin 才能知道它们的存在
# 注册非常简单，只需要在 blog\admin.py 中加入下面的代码：
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
