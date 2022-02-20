from django.urls import path
from rest_framework.routers import DefaultRouter
from tasks import views

app_name = 'tasks'

# router = DefaultRouter()
# router.register(r'taskitems', TaskListViewSet, basename='task')
# router.register(r'taskretrive', TaskRetrieveViewSet, basename='task')
# router.register(r'taskupdate', TaskUpdateViewSet, basename='task')
# router.register(r'task', TaskViewSet, basename='task')


urlpatterns = [
    path('', views.task_list_page, name='task_list_page'),
    path('task/page/detail/<int:pk>', views.task_detail_page, name='task_detail'),
    path('task/page/create/', views.task_create_page, name='task_create_page'),

    path('task/api/retrieve/<int:pk>/', views.TaskRetrieveUpdateDeleteViewSet.as_view({"get": "retrieve"}), name='task-retrieve'),
    path('task/api/update/<int:pk>/', views.TaskRetrieveUpdateDeleteViewSet.as_view({"put": "update"}), name='task-update'),
    path('task/api/delete/<int:pk>/', views.TaskRetrieveUpdateDeleteViewSet.as_view({"delete": "destroy"}), name='task-delete'),

    path('task/api/create/', views.TaskListCreateViewSet.as_view({"post": "create"}), name='task-create'),
    path('task/api/list/', views.TaskListCreateViewSet.as_view({"get": "list"}), name='task-list'),
    # re_path('^', include(router.urls)),
]
