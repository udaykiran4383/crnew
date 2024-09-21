from django.urls import path
from . import views

urlpatterns = [
    # Existing URLs
    path('api/google-login/', views.google_login, name='google_login'),
    path('api/districts/<str:state_name>/', views.GetDistrictsView.as_view(), name='get_districts'),
    path('api/colleges/<str:state_name>/<str:district_name>/', views.GetCollegesView.as_view(), name='get_colleges'),
    path('api/schools/<str:state_name>/<str:district_name>/', views.GetSchoolsView.as_view(), name='get_schools'),
    path('api/submit-form/', views.SubmitFormView.as_view(), name='submit_form'),

    # New URLs for task management
    path('api/tasks/', views.get_tasks, name='get_tasks'),  # Fetch all tasks
    path('api/user_tasks/', views.get_user_tasks, name='get_user_tasks'),  # Fetch user's submitted tasks
    path('api/submit_task/<int:task_id>/', views.submit_task, name='submit_task'),  # Submit or update task
    path('api/verify_task/<int:user_task_id>/', views.verify_task, name='verify_task'),  # Verify task and award points (admin only)
]
