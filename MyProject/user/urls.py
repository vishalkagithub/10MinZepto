from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns=[
    path('api/', include(router.urls)),
    path('index/',views.index),
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('signin/',views.signin),
    path('signup/',views.signup),
    path('product/',views.product),
    path('event/',views.event),
    path('signout/',views.signout),
    path('myprofile/',views.myprofile),
    path('mycart/',views.mycart),
    path('cartitems/',views.cartitems),
    path('order/',views.morder),
    path('indexcart/',views.indexcart),

]