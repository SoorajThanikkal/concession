from.import views
from django.urls import path

urlpatterns=[
    path('',views.index_view,name='index'),
    path('signup/',views.register,name='signup'),
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name='profile'),
    path('edit/<int:uid>/',views.edit,name='edit'),
    path('locations/', views.set_locations, name='locations'),
    path('showmywallet/',views.ShowWallet,name='showmywallet'),
    path('initiate-payment/<amount>/', views.initiate_payment, name='initiate-payment'),
    path('confirm-payment/<str:order_id>/<str:payment_id>/', views.confirm_payment, name='confirm-payment'),
    path('book_bus/', views.book_bus_pass, name='book_bus_pass'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('userlist/',views.user_list,name='userlist'),
    path('delete_userlist/<int:did>/',views.delete_userlist,name='delete_userlist'),
    path('feedback_rate/',views.feedback,name='feedback_rate'),
    path('just/',views.just,name='just'),

    path('logout/',views.logout,name='logout'),
    path('cindex/',views.cindex,name='cindex'),
    path('conductorRegister/',views.conductorRegister,name='conductorRegister'),
    path('scan-qr/', views.scan_qr_code, name='scan_qr_code'),
    path('conductorprofile/',views.conductorprofile,name='conductorProfile'),

    
]