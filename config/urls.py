from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls', namespace='user')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('student/', include('student.urls', namespace='student')),
    path('teacher/', include('teacher.urls', namespace='teacher')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Digi Academy Admin'
admin.site.site_title = 'Digi Academy Admin'
admin.site.index_title = 'Digi Academy Admin'
