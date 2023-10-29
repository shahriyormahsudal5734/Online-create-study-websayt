from . import views
from django.urls import path

urlpatterns = [
    path('', views.homepage, name='home'),
    path('scholl/<int:id>/', views.markaz, name='room'),
    path('kurslar/<int:id>/', views.detailkurs, name='detailkurs'),
    path('removekurs/<int:id>/', views.removekurs, name='removekurs'),
    path('ariza_true/<int:id>/', views.ariza_true, name='ariza_true'),
    path('ariza_false/<int:id>/', views.ariza_false, name='ariza_false'),
    path('all_shcoll/', views.all_shcoll, name='all_shcoll'),    
    path('updateoquv/<int:pk>/', views.Updateoquv.as_view(), name='updateoquv'),  
    path('delete_true/<int:id>/', views.delete_true, name='delete_true'),  
    path('oquv_true/<int:id>/', views.oquv_true, name='oquv_true'),  


    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),  

]