from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate,signup,activate
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView

registration_patterns = ([
    
    #path('signup/', SignUpView.as_view(), name="signup"),
    path('profile/', ProfileUpdate.as_view(), name="profile"),
    path('profile/email/', EmailUpdate.as_view(), name="profile_email"),
    path('signup', signup, name='signup'),
    path('activate/()/(<token>/',activate, name='activate'),
    path('account/password/reset/',PasswordResetView.as_view(),name="password_reset"),
    path('password/reset/done/',PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('account/password/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('account/password/done',PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('password_change/', PasswordChangeView.as_view(),name="password_change"),

    
], 'registration')