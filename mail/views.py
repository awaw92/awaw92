import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import User, Email
import traceback


@login_required(login_url="/login/")
def index(request):
    return HttpResponseRedirect(reverse("mailbox-home"))


@login_required(login_url="/login/")
def mailbox_home(request):
    return render(request, "mail/layout.html")


@csrf_exempt
@login_required(login_url="/login/")
def compose(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    emails = [email.strip() for email in data.get("recipients", "").split(",") if email.strip()]
    if not emails:
        return JsonResponse({"error": "At least one recipient required."}, status=400)

    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({"error": f"User with email {email} does not exist."}, status=400)

    subject = data.get("subject", "")
    body = data.get("body", "")

    # Tworzymy jeden Email dla nadawcy
    email_obj = Email.objects.create(
        user=request.user,
        sender=request.user,
        subject=subject,
        body=body,
        read=False
    )

    # Dodajemy wszystkich odbiorców, w tym siebie jeśli wysyłamy do samego siebie
    email_obj.recipients.add(*recipients if recipients else request.user)

    # Tworzymy kopie dla odbiorców (INBOX) tylko jeśli ktoś inny niż nadawca
    for recipient in recipients:
        if recipient != request.user:
            recipient_email = Email.objects.create(
                user=recipient,
                sender=request.user,
                subject=subject,
                body=body,
                read=False
            )
            recipient_email.recipients.add(recipient)

    return JsonResponse({"message": "Email sent successfully."}, status=201)


@login_required(login_url="/login/")
def mailbox(request, mailbox):
    if mailbox == "inbox":
        # Maile, gdzie użytkownik jest odbiorcą
        emails = Email.objects.filter(
            user=request.user,
            archived=False,
            recipients=request.user
        ).order_by("-timestamp")

    elif mailbox == "sent":
        # Maile wysłane przez użytkownika
        emails = Email.objects.filter(user=request.user, sender=request.user).order_by("-timestamp")

    elif mailbox == "archived":
        emails = Email.objects.filter(user=request.user, archived=True).order_by("-timestamp")

    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    emails_serialized = [
        {
            "id": email.id,
            "sender": email.sender.email,
            "recipients": [u.email for u in email.recipients.all()],
            "subject": email.subject,
            "body": email.body,
            "timestamp": email.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": email.read,
            "archived": email.archived
        }
        for email in emails
    ]
    return JsonResponse(emails_serialized, safe=False)


@csrf_exempt
@login_required(login_url="/login/")
def email_view(request, email_id):
    try:
        email_obj = Email.objects.get(pk=email_id, user=request.user)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "id": email_obj.id,
            "sender": email_obj.sender.email,
            "recipients": [u.email for u in email_obj.recipients.all()],
            "subject": email_obj.subject,
            "body": email_obj.body,
            "timestamp": email_obj.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": email_obj.read,
            "archived": email_obj.archived
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body) if request.body else {}
            updated = False

            if "read" in data:
                email_obj.read = bool(data["read"])
                updated = True
            if "archived" in data:
                email_obj.archived = bool(data["archived"])
                updated = True

            if updated:
                email_obj.save()

            return JsonResponse({"message": "Email updated successfully."}, status=200)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": "Error updating email."}, status=500)

    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mail/login.html", {"message": "Invalid email and/or password."})
    return render(request, "mail/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            return render(request, "mail/register.html", {"message": "Passwords must match."})

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "mail/register.html", {"message": "Email address already taken."})

        return HttpResponseRedirect(reverse("login"))
    return render(request, "mail/register.html")


@csrf_exempt
@login_required(login_url="/login/")
@require_POST
def test_mark_read(request):
    try:
        email_obj = Email.objects.get(pk=30, user=request.user)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    email_obj.read = True
    email_obj.save()
    return JsonResponse({"message": "Email marked as read successfully."})


def test_view(request):
    return HttpResponse("Test działa!")
