from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views
# from news_service import views as news_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('delete_journalist/<int:pk>', views.JournalistDeleteView.as_view(),
         name='delete_journalist')
]
