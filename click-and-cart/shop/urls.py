from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='shophome'),
    path('about/',views.about,name='Aboutus'),
    path('backup/',views.backup,name='backup'),
    path('contact/',views.contacts,name='Contactus'),
    path('tracker/',views.track,name='trackingstatus'),
    path('search/',views.search,name='searching'),
    path('productview/<int:myid>',views.productview,name='productview'),
    path('checkout/',views.checkout,name='checkout'),
    path('get_cart_products/', views.get_cart_products, name='get_cart_products'),
]