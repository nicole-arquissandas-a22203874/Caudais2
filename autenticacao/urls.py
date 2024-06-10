from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'autenticacao'
urlpatterns = [
    path('registoA/', views.registo_viewA, name="registoA"),
    path('registoB/', views.registo_viewB, name="registoB"),
    path('registoC/', views.registo_viewC, name="registoC"),
    path('loginB/', views.login_viewB, name="loginB"),
    path('loginC/', views.login_viewC, name="loginC"),
    path('loginA/', views.login_viewA, name="loginA"),
    path('logoutA/', views.logoutA_view, name="logoutA"),
    path('logoutB/', views.logoutB_view, name="logoutB"),
    path('logoutC/', views.logoutC_view, name="logoutC"),


    # recuperação de password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/custom_password_reset_formA.html'), name='reset_passwordA'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/custom_password_reset_doneA.html'), name='password_reset_doneA'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/custom_password_reset_confirmA.html'), name='password_reset_confirmA'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/custom_password_reset_completeA.html'), name='password_reset_completeA'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/custom_password_reset_formB.html'), name='reset_passwordB'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/custom_password_reset_doneB.html'), name='password_reset_doneB'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/custom_password_reset_confirmB.html'), name='password_reset_confirmB'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/custom_password_reset_completeB.html'), name='password_reset_completeB'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/custom_password_reset_formC.html'), name='reset_passwordC'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/custom_password_reset_doneC.html'), name='password_reset_doneC'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/custom_password_reset_confirmC.html'), name='password_reset_confirmC'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/custom_password_reset_completeC.html'), name='password_reset_completeC'),

]