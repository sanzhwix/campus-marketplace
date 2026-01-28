from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatRoom(models.Model):
    # Room between buyer and seller for a specific product
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE, related_name='chat_rooms')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_rooms_as_buyer')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_rooms_as_seller')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('product', 'buyer', 'seller')
        ordering = ('-created_at',)

    def __str__(self):
        return f"ChatRoom(product={self.product_id}, buyer={self.buyer_id}, seller={self.seller_id})"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"Message(room={self.room_id}, sender={self.sender_id}, ts={self.timestamp})"
