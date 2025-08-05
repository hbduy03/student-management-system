from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school.urls')),
    path('student/', include('student.urls')),
    path('academic/', include('academic.urls')),
    path('teacher/', include('teacher.urls')),
    path('authentication/', include('home_auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
