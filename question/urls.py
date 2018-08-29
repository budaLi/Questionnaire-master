
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^add_questionnaire/$', views.add),
    url(r'^login/$', views.login),
    url(r'^edit_questionnaire/(\d+)/$', views.edit_questionnaire),
    url(r'^student/evaluate/(\d+)/(\d+)/$', views.score),

]
