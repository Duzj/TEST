from django.contrib import admin
from firstapp.models import Event, Guest

#Django 后台管理用户/用户组
# Register your models here.
#设置页面显示更多的信息
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_time', 'id']  #定义在列表中显示哪些字段
    search_fields = ['name']     # 生成搜索栏
    list_filter = ['status']     # 生成过滤器

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']
    list_filter = ['sign']

admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)







