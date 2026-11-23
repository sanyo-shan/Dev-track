from django.urls import path
from issues import views

urlpatterns = [
    path('api/issues/', views.issues, name='get_issue'),
    path('api/issues/<int:issue_id>/', views.get_issue_by_id, name='get_issue_by_id'),
    path('api/reporters/', views.reporter, name='get_reporter'),
    path('api/reporters/<int:reporter_id>/', views.get_reporter_by_id, name='get_reporter_by_id'),
    path('api/reporters/', views.reporter, name='create_reporter'),
    path('api/issues/<str:status>/', views.get_issue_by_status, name='get_issue_by_status'),
    path('api/issues/', views.issues, name='create_issue'),
]