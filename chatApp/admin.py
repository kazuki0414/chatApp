from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from chatApp.models import User
from chatApp.models import Profile,FriendTable,TalkMessageList

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(FriendTable)
admin.site.register(TalkMessageList)
