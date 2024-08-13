from django.urls import path

from grades.views import course, inscription, subject

app_name = 'grades'

urlpatterns = [
    path('courses/', course.CourseListView.as_view(), name='course_list'),
    path('inscriptions/', inscription.create_inscription,
         name='inscription_creation'),
    path('students/<str:username>/current-subjects/',
         subject.list_current_student_subjects, name='current_student_subjects')
]
