from django.urls import path

from grades.views import course, inscription

app_name = 'grades'

urlpatterns = [
    path('courses/', course.CourseListView.as_view(), name='course_list'),
    path('inscriptions/', inscription.create_inscription,
         name='inscription_creation')
]
