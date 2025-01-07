from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_form, name='home'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('regform', views.register_form, name='regform'),
    path('register', views. registerView, name='register'),



    path('uabook_form', views.useraddbook_form, name='uabook_form'),
    path('uabook', views.useraddbook, name='uabook'),
    path('uchat', views.UCreateChat.as_view(), name='uchat'),
    path('ulchat', views.UListChat.as_view(), name='ulchat'),
    path('request_form', views.request_form, name='request_form'),
    path('delete_request', views.delete_request, name='delete_request'),
    path('feedback_form', views.feedback_form, name='feedback_form'),
    path('send_feedback', views.send_feedback, name='send_feedback'),
    path('about', views.about, name='about'),
    path('publisher', views.PBookListView.as_view(), name='publisher'),
    path('displaybook', views.displaybookview.as_view(), name='displaybook'),
    path('uviewbook/<int:pk>', views.UViewBook.as_view(), name='uviewbook'),
    path('add', views.add_profile, name='add_profile'),



    path('librarian', views.librarian, name='librarian'),
    path('laddbook_form', views.laddbook_form, name='laddbook_form'),
    path('laddbook', views.laddbook, name='laddbook'),
    path('librarianbook', views.LBookListView.as_view(), name='librarianbook'),
    path('ldeleterequest', views.LDeleteRequest.as_view(), name='ldeleterequest'),
    path('lmanagebook', views.LManageBook.as_view(), name='lmanagebook'),
    path('ldeleteview/<int:pk>', views.LDeleteView.as_view(), name='ldeleteview'),
    path('lviewbook/<int:pk>', views.LViewBook.as_view(), name='lviewbook'),
    path('leditview/<int:pk>', views.LEditView.as_view(), name='leditview'),
    path('lchat', views.LCreateChat.as_view(), name='lchat'),
    path('llchat', views.LListChat.as_view(), name='llchat'),




    path('dashboard', views.dashboard, name='dashboard'),
    path('achat', views.ACreateChat.as_view(), name='achat'),
    path('alchat', views.AListChat.as_view(), name='alchat'),
    path('adminbook_form', views.adminaddbook_form, name='adminbook_form'),
    path('adminaddbook', views.adminaddbook, name='adminaddbook'),
    path('adminbook', views.ABookListView.as_view(), name='adminbook'),
    path('amanagebook', views.AManageBook.as_view(), name='amanagebook'),
    path('aviewbook/<int:pk>', views.AViewBook.as_view(), name='aviewbook'),
    path('aeditview/<int:pk>', views.AEditView.as_view(), name='aeditview'),
    path('adeleteview/<int:pk>', views.ADeleteView.as_view(), name='adeleteview'),
    path('adeleterequest', views.ADeleteRequest.as_view(), name='adeleterequest'),
    path('afeedback', views.AFeedback.as_view(), name='afeedback'),
    path('create_user_form', views.create_user_form, name='create_user_form'),
    path('listuserview', views.ListUserView.as_view(), name='listuserview'),
    path('create_user', views.create_user, name='create_user'),
    path('aviewuser/<int:pk>', views.AViewUser.as_view(), name='aviewuser'),
    path('aedituser/<int:pk>', views.AEditUser.as_view(), name='aedituser'),
    path('adeleteuser/<int:pk>', views.ADeleteUser.as_view(), name='adeleteuser'),

    path('logout', views.logout, name='logout'),
]
