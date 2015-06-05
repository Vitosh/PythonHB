from django.conf.urls import include, url
from django.contrib import admin

from counter import urls as word_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(word_urls))
]