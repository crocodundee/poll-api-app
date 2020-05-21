from django.urls import path, include

from rest_framework.routers import DefaultRouter

from poll import views

router = DefaultRouter()
router.register('questions', views.QuestionViewSet)

app_name = 'poll'

polls_list = views.PollViewSet.as_view({'get': 'list', 'post': 'create'})
polls_detail = views.PollViewSet.as_view(
    {
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    }
)
polls_qestion = views.PollViewSet.as_view({'post': 'add_question'})

polls_complete = views.PollViewSet.as_view(
    {'post': 'complete', 'get': 'complete'}
)

polls_completed_list = views.PollDoneViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('', polls_list, name='poll-list'),
    path('<int:pk>/', polls_detail, name='poll-detail'),
    path('<int:pk>/add-question/', polls_qestion, name='poll-add-question'),
    path(
        '<str:user_id>/<int:pk>/<int:question_id>/',
        polls_complete,
        name='poll-complete',
    ),
    path('done/', polls_completed_list, name='poll-done-list'),
    path('', include(router.urls)),
]
