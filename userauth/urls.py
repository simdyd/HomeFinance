from django.conf.urls import patterns#, url, include

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('userauth',
     (r'login/', 'views.agenti_login'),
     (r'logout/', 'views.logout_view'),
     #(r'change_pwd/', 'views.password_change'),
     #(r'pwd_change_done/', 'views.password_change_done'),
     #(r'pwd_reset/', 'views.password_reset'),
     #(r'pwd_reset_done/', 'views.password_reset_done'),
     #(r'change_user_info/', 'views.cambia_info_utente'),
     #(r'utility_user/', 'views.user_utility_tool'),
)