
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index_view.as_view()),
    path('login/', views.Login_Phonenumber_view.as_view()),
    path('send_to_mobile/', views.Request_otp.as_view()),
    path('details/', views.Details_view.as_view()),
    path('submit-image/', views.Image_submit_view.as_view()),
    path('submit-name/', views.Name_submit_view.as_view()),
    path('checkotp/', views.Check_otp.as_view()),
    path('status/', views.Status_view.as_view()),
    path('group/', views.NewGroup_view.as_view()),
    path('create/', views.CreateGroup_view.as_view(),name="creategroup"),
    path('profile/', views.Personal_Profile_view.as_view()),
    path('chat/', views.Chat_Profile_view.as_view()),
    path('contact/', views.Contact_list_view.as_view()),
    path('contact-save/', views.Contact_save_view.as_view()),
    path('settings/', views.Settings_view.as_view()),
    path('check/', views.Contact_view.as_view()),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
