from django.urls import path

from .views import CategoryList, CategoryCreate, CategoryRetrieveUpdateDestroy
from .views import CourseList, CourseCreate, CourseRetrieveUpdateDestroy
from .views import LessonList, LessonCreate, LessonRetrieveUpdateDestroy
from .views import SlideList, SlideCreate, SlideRetrieveUpdateDestroy

app_name = 'courses'
urlpatterns = [
    #Categories
    path('cat/', CategoryList.as_view(), name="cat-list"),
    path('cat/new', CategoryCreate.as_view(), name="cat-create"),
    path('cat/<int:id>/', CategoryRetrieveUpdateDestroy.as_view(), name="cat-rud"),

    #Courses
    path('course/', CourseList.as_view(), name="course-list"),
    path('course/new', CourseCreate.as_view(), name="course-create"),
    path('course/<int:id>/', CourseRetrieveUpdateDestroy.as_view(), name="course-rud"),

    #Lessons
    path('lesson/', LessonList.as_view(), name="lesson-list"),
    path('lesson/new', LessonCreate.as_view(), name="lesson-create"),
    path('lesson/<int:id>/', LessonRetrieveUpdateDestroy.as_view(), name="lesson-rud"),

    #Slides
    path('lesson/<int:id>/slides/', SlideList.as_view(), name="slide-list"),
    path('lesson/<int:id>/slides/new', SlideCreate.as_view(), name="slide-create"),
    path('lesson/<int:id>/slides/<int:position>/', SlideRetrieveUpdateDestroy.as_view(), name="slide-rud"),
]