from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'Cats', views.CategoryViewSet)
urlpatterns=[
    path('',views.home,name='home'),
    path('detail/<str:slug>/<int:id>',views.detail,name='detail'),
    path('category',views.category,name='category'),
    path('celebrity',views.celebrity,name='celebrity'),
    path('category/<str:slug>/<int:id>',views.category_movies,name='category-movies'),
    path('celebrity/<str:slug>/<int:id>',views.celebrity_movies,name='celebrity-movies'),
    path('recent-released',views.recent_released,name='recent-released'),
    path('upcoming',views.upcoming_movies,name='upcoming'),
    path('accounts/register',views.register,name='register'),
    path('accounts/profile',views.profile,name='profile'),
    path('accounts/changepassword',views.change_password,name='changepassword'),
    path('my-reviews',views.my_reviews,name='my-reviews'),
    path('delete-review/<int:id>',views.delete_review,name='delete-review'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)