from django.urls import path
from .views import CustomTokenObtainPairView, DemandeDemarcheurView, RegisterView, LoginView, UserMeView, UserStatutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("me/", UserMeView.as_view(), name="user-me"),
    path('statut/', UserStatutView.as_view(), name='user-statut'),
    path('demande-demarcheur/', DemandeDemarcheurView.as_view(), name='demande_demarcheur')
]
