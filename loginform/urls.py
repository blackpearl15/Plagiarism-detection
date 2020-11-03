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
    path('gnr', views.genrep , name='genrep'),
    path('dnr', views.dowrep , name='dowrep'),
]

urlpatterns += staticfiles_urlpatterns()