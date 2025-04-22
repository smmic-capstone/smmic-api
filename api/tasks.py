from celery import shared_task
from .models import *
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from django.conf import settings

@shared_task
def send_notifications(device_id, soil_moisture):
    sensor = SensorNode.objects.select_related('sink_node__User').get(device_id = device_id)

    userID = sensor.sink_node.User.UID
    strUID = str(userID)

    devices = FCMDevice.objects.filter(user = strUID)

    notificationn_title = "Soil Moisture is Low"
    notification_message = f"Soil Moisture is at {soil_moisture}%."
    soil_moisture = soil_moisture

    devices.send_message(
        message = Message(
            notification=Notification(
                title= notificationn_title,
                body= f"Soil Moisture is at {soil_moisture}%."
            ),
        ),
        app=settings.FCM_DJANGO_SETTINGS['DEFAULT_FIREBASE_APP']
    )

    print(notificationn_title)
    print(notification_message)
    print(soil_moisture)

