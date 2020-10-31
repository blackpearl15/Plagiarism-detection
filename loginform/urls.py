from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index , name='index'),
    path('accounts/',include('accounts.urls')),
    path('accounts/',include('allauth.urls')),
    path('result', views.result , name='result'),
]

urlpatterns += staticfiles_urlpatterns()