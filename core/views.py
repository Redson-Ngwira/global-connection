from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Conversation, Message
from .ai import generate_reply


@api_view(["POST"])
def incoming_sms(request):
    phone = request.data.get("phone")
    text = request.data.get("message")

    if not phone or not text:
        return Response(
            {"error": "phone and message required"},
            status=400
        )

    convo, _ = Conversation.objects.get_or_create(phone=phone)

    Message.objects.create(
        conversation=convo,
        role="user",
        content=text
    )

    history = Message.objects.filter(
        conversation=convo
    ).order_by("created_at")[:6]

    reply = generate_reply(history)

    Message.objects.create(
        conversation=convo,
        role="assistant",
        content=reply
    )

    return Response({"status": "ok"})


@api_view(["GET"])
def outgoing_sms(request):
    replies = Message.objects.filter(
        role="assistant",
        sent=False
    ).order_by("created_at")[:10]

    data = []
    for r in replies:
        data.append({
            "id": r.id,
            "phone": r.conversation.phone,
            "message": r.content
        })

    return Response(data)


@api_view(["POST"])
def mark_sent(request):
    msg_id = request.data.get("id")

    if not msg_id:
        return Response({"error": "id required"}, status=400)

    Message.objects.filter(id=msg_id).update(sent=True)
    return Response({"status": "ok"})
