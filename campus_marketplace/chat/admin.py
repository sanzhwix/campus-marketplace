from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'buyer', 'seller', 'created_at')
    search_fields = ('product__name', 'buyer__email', 'seller__email')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'timestamp')
    search_fields = ('sender__email', 'content')

