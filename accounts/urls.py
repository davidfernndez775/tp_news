from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views
# from news_service import views as news_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('delete_journalist/<int:pk>',
         views.UserConfirmDelete.as_view(), name='delete_journalist'),
    path('journalist_update/<int:pk>',
         views.UserUpdate.as_view(), name='user_update'),
    path('board/<slug:slug>', views.BoardView.as_view(), name='board'),
    path('journalists', views.JournalistsListView.as_view(),
         name='journalists_list'),
    path('unactive_journalists', views.UnactiveJournalistsListView.as_view(),
         name='unactive_journalists_list'),
    path('reactive_journalist/<int:pk>',
         views.UserConfirmReactivate.as_view(), name='reactive_journalist'),
    path('change_password', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('client_signup', views.ClientSignup.as_view(),
         name='client_signup'),
]
