from django.urls import path
from .views import NotificationListAPIView, MarkNotificationReadAPIView

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notifications-list'),
    path('<int:pk>/read/', MarkNotificationReadAPIView.as_view(), name='notifications-mark-read'),
]
