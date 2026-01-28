from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('room_for_product/<int:product_id>/', views.open_room_for_product, name='open_room_for_product'),
    path('inbox/', views.inbox, name='inbox'),
    path('room/<int:room_id>/', views.room_view, name='room'),
    path('messages/<int:room_id>/', views.messages_api, name='messages_api'),
]
