from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Notification
from apps.collection_service.models import User

# Create your views here.

def get_notifications(user):
    print(Notification.objects.filter(user=user), flush=True)
    return Notification.objects.filter(user=user)


# input (beispielsweise Event durch post request) kommt von RabbitMQ, 
# geht dann in die Notification Funktion und der User bekommt ausgeprintet

def create_notification(ch, method, properties, body):
    notification = Notification.objects.create(
        user = get_object_or_404(User, username=body['author']),
        title="titel",
        message="message"
    )
    show_notifications(user=notification.user)
    

def show_notifications(user):
    notifications = get_notifications(user)
    for notification in notifications:
        print(notification, flush=True)