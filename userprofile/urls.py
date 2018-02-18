from django.conf.urls import url
from .views import user_profile


app_name = 'userprofile'

urlpatterns = [
    url(r'^profile/$', user_profile),
]
