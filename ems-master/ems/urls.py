from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.conf.urls.static import static

from django.conf import settings


from employee.views import ( index, user_login, user_logout,
    success, ProfileUpdate, MyProfile, LoginView, LogoutView)

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('poll/', include('poll.urls')),
    path('api/v1/', include('poll.api_urls')),
    path('api/v1/', include('employee.api_urls')),
    # path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/auth/login/', LoginView.as_view()),
    path('api/v1/auth/logout/', LogoutView.as_view()),
    path('employee/', include('employee.urls')),

    path('login/', user_login, name="user_login"),
    path('success/', success, name="user_success"),
    path('logout/', user_logout, name="user_logout"),
    path('profile/', MyProfile.as_view(), name="my_profile"),
    path('profile/update', ProfileUpdate.as_view(), name="update_profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
