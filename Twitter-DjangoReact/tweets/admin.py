from .models import Tweet, TweetLike
from django.contrib import admin

class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike

class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content' ,'user__username', 'user__email']
    class Meta:
        model = Tweet
        

admin.site.register(Tweet, TweetAdmin)