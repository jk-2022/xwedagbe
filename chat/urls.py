from django.urls import path
from .views import GetOrCreateRoomView, RoomMessagesView, UserRoomsView

urlpatterns = [
    path("get_or_create_room/", GetOrCreateRoomView.as_view(), name="get_or_create_room"),
    path("my-rooms/", UserRoomsView.as_view()),
    path("<int:room_id>/messages/", RoomMessagesView.as_view(), name="room-messages"),

]
