from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(CartItem)




class PostAdmin(admin.ModelAdmin):
    list_display = ('name','caption','created_at','shop','show_image')
    list_filter = ('created_at','shop')
    search_fields = ('name','caption')
    date_hierarchy = ('created_at')

    # @admin.display(empty_value='-',description="title desc")
    # def view_title_desc(self, obj):
    #     if (obj.image):
    #         print(obj.image.url)
    #     print(type(obj))
    #     return format_html(
    #          '<span style="color: red;">{} {}</span>',
    #         obj.name,
    #         obj.caption,
    #     )
    #     # return obj.shortdesc obj.title
    #     # return f'{} {}'
    @admin.display(empty_value='-',description="show image")
    def show_image(self, obj):
        if (obj.image):
            print(obj.image.url)
        
            return format_html(
                '<img src="{}" width=50 height=50/>',
                obj.image.url,
                
            )
        return '-'
    
    # fields = (('title','shortdesc'),'desc',('owner','status'))
    # save_on_top =True
admin.site.register(Product,PostAdmin)



class ShopAdmin(admin.ModelAdmin):
    list_display = ('name','status')
    actions = ['make_published']
    @admin.action(description='Mark selected stories as published')
    def make_published(modeladmin, request, queryset):
        queryset.update(status='Pub')
admin.site.register(Shop,ShopAdmin)