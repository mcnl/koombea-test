from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("add_page/", views.AddPageView.as_view(), name="add_page"),
    path("page/<int:pk>/", views.PageDetailView.as_view(), name="page_detail"),
]
