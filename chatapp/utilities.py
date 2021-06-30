from .models import Notification

def create_notification(to_user, notification_type,created_by,room, extra_id=0):
    notification = Notification.objects.create(to_user=to_user, notification_type=notification_type, created_by=created_by, extra_id=extra_id,room=room)
   