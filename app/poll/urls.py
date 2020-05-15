from django.urls import path, include

from rest_framework.routers import DefaultRouter

from poll import views

router = DefaultRouter()
router.register('questions', views.QuestionViewSet)

app_name = 'poll'

urlpatterns = [
    path('', include(router.urls))
]
