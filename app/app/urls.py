from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view


API_TITLE = 'Poll API'
API_DESC = 'A Web API for the passage of polls'
schema_view = get_schema_view(title=API_TITLE)


urlpatterns = [
    path('', include_docs_urls(title=API_TITLE, description=API_DESC)),
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/polls/', include('poll.urls')),
    path('schema/', schema_view),
]
