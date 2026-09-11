from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from redis import Redis


redis_client = Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
)


@login_required
def chat_page(request):
    users = User.objects.all()

    online_users = set()

    for user in users:
        if redis_client.exists(f"user_online:{user.id}"):
            online_users.add(user.id)

    return render(
        request,
        "chat/index.html",
        {
            "users": users,
            "online_users": online_users,
        },
    )


@login_required
def heartbeat(request):
    key = f"user_online:{request.user.id}"

    # Пользователь считается онлайн 15 секунд
    redis_client.setex(key, 15, "online")

    return JsonResponse({"status": "ok"})


@login_required
def online_users(request):
    users = User.objects.all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "online": bool(
                redis_client.exists(f"user_online:{user.id}")
            ),
        })

    return JsonResponse({"users": result})