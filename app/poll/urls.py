from django.urls import path, include

from rest_framework.routers import DefaultRouter

from poll import views

router = DefaultRouter()
router.register('questions', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet)
router.register('polls', views.PollViewSet)

app_name = 'poll'

urlpatterns = [
    path('', include(router.urls))
]
