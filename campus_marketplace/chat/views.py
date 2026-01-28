from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import ChatRoom, Message
from main.models import Product
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


@login_required
def open_room_for_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller = product.seller
    if seller is None:
        return HttpResponseForbidden('Product does not have a seller')

    buyer = request.user
    # Prevent owners from opening a chat to their own product
    if buyer == seller:
        # Redirect back to product detail (button should be hidden, but guard here too)
        return redirect(product.get_absolute_url())

    room, _ = ChatRoom.objects.get_or_create(product=product, buyer=buyer, seller=seller)
    return redirect('chat:room', room_id=room.id)


@login_required
def room_view(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user != room.buyer and request.user != room.seller:
        return HttpResponseForbidden('Not a participant of this chat')

    messages = room.messages.all()
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})


@login_required
def inbox(request):
    # List chat rooms where the user is a participant
    rooms = ChatRoom.objects.filter(models.Q(buyer=request.user) | models.Q(seller=request.user)).prefetch_related('messages', 'product')

    # Build a lightweight structure: room + last_message or None
    inbox_items = []
    for r in rooms:
        last = r.messages.order_by('-timestamp').first()
        inbox_items.append({'room': r, 'last_message': last})

    return render(request, 'chat/inbox.html', {'inbox_items': inbox_items})


@login_required
def messages_api(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user != room.buyer and request.user != room.seller:
        return HttpResponseForbidden('Not a participant')

    if request.method == 'GET':
        # Return messages as JSON
        messages = room.messages.select_related('sender').order_by('timestamp')
        data = [
            {
                'id': m.id,
                'sender_id': m.sender_id,
                'sender_name': getattr(m.sender, 'first_name', '') or getattr(m.sender, 'email', ''),
                'content': m.content,
                'timestamp': m.timestamp.isoformat(),
            }
            for m in messages
        ]
        return JsonResponse({'messages': data})

    if request.method == 'POST':
        text = request.POST.get('message') or ''
        text = text.strip()
        if not text:
            return JsonResponse({'error': 'Empty message'}, status=400)

        message = Message.objects.create(room=room, sender=request.user, content=text, timestamp=timezone.now())
        return JsonResponse({
            'id': message.id,
            'sender_id': message.sender_id,
            'sender_name': getattr(message.sender, 'first_name', '') or getattr(message.sender, 'email', ''),
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
        })

    return JsonResponse({'error': 'Method not allowed'}, status=405)
