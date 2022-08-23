from django.urls import path
from accounts import views
app_name = 'accounts'

urlpatterns = [
    path('register/user', views.signup, name='signup'),
    path('view/user/profile', views.view_user_profile, name='view_user_profile'),
    path('edit/user/profile', views.edit_user_profile, name='edit_user_profile'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('change-password', views.change_password, name='change_password'),
    path('reset_password_email', views.reset_password_email,
         name='reset_password_email'),
    path('password_reset_success/<str:email>', views.password_reset_success,
         name='password_reset_success'),
    path('reset/password/<uidb64>/<token>/',
         views.reset_password, name='reset_password'),
    path("resend/password/reset/email/<str:email>", views.resend_password_reset_email,
         name="resend_password_reset_email"),
    path('reset/password/form/',
         views.reset_password_form, name='reset_password_form'),
    
    path('reset_password_success/<str:email>', views.reset_password_success,
         name='reset_password_success'),

]
