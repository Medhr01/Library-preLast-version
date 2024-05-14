from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home , name="home"),
    path('login/', user_login , name="login"),
    path('logout/', user_logout , name="logout"),
    path('Clients/', views.clients, name='Clients'),
    path('Client/<int:id>', views.edit_client, name='Client'),
    path('Delete_client/<int:id>', views.delete_client, name='Delete_user'),
    path('Modifier_client/<int:id>', views.actdes, name='Modifier_Client'),
    path('Exemplaires/', views.exemplaires, name='Exemplaires'),
    path('Modifier_exmp/<int:id>', views.modifier_exmp, name='Modifier_exmp'),
    path('Livres/', views.livres, name='Livres'),
    path('Livre/<str:ISBN>', views.livre, name='Livre'),
    path('pret/<int:id>', views.pret, name='pret'),
    path('add/<int:id>', views.acheter_plus, name='add'),
    path('Client_emprunt/<int:id>/', views.emprunt_client , name='Client_emprunt'),
    path('Livre_emprunt/<int:id>', views.emprunt_livre, name="Livre_emprunt"),
    path('Emprunt/<int:id>', views.emprunt, name='Emprunt'),
    path('Emprunt_hist/', views.emps_hist , name="Emprunt_hist"),
    path('Delete_livre/<int:id>',views.delete_livre,name="delete_livre"),
    path('return/<int:id>', views.return_emp, name='return'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
