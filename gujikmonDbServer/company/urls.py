from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('insert/', views.companyDbInsert, name='insert'),
    path('update/', views.companyDBupdate, name='update'),
    path('regionTest/', views.regionTest, name='region_test'),
    # url(r'^v1/tasks/$', views.tasks, name='tasks'),
    # path('v1/tasks/', views.tasks, name='tasks'),
    # path('', views.index , name='index'),
    # path('test/', views.test, name='test'),
    # path('sTest/', views.sTest, name='stest')
]