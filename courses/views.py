from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Category, Course, Lesson, Slide
from .serializers import CategorySerializer, CourseSerializer, LessonSerializer, SlideSerializer

from core.permissions import IsStudent, IsTeacher
from rest_framework.permissions import IsAuthenticated

#------------------------------Categories
class CategoryList(ListAPIView):
    queryset = Category.objects.all().order_by('slug')
    serializer_class = CategorySerializer

class CategoryCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


#-----------------------------Courses
class CourseList(ListAPIView):
    queryset = Course.objects.all().order_by('title')
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('category',)
    search_fields = ('title', 'lessons__item', )

class CourseCreate(CreateAPIView):
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        try:
            title = request.data.get('title')
            if title is not None and not isinstance(title, str):
                raise ValidationError({ 'title': 'Must be a valid title' })
        except ValueError:
            raise ValidationError({ 'title' : 'Needs to be a string', })

        try:
            description = request.data.get('description')
            if description is not None and not isinstance(description, str) and len(description) > 150:
                raise ValidationError({ 'description': 'Must be a string lesser than 150 characters'})
        except ValueError:
            raise ValidationError({ 'title' : 'Needs to be a string', })

        return super().create(request, *args, **kwargs)

class CourseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'id'


#-----------------------------Lessons
class LessonList(ListAPIView):
    queryset = Lesson.objects.all().order_by('position')
    serializer_class = LessonSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('course',)
    search_fields = ('title', 'item',)

class LessonCreate(CreateAPIView):
    permissions = (IsAuthenticated, IsTeacher)
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permissions = (IsAuthenticated, IsTeacher)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'id'


#---------------------------Slides
class SlideList(ListAPIView):
    permissions = (IsAuthenticated, IsStudent)
    serializer_class = SlideSerializer

    def get_queryset(self):
        lesson = self.kwargs.get('id')
        slides = Slide.objects.filter(lesson=lesson)
        return slides

class SlideCreate(CreateAPIView):
    permissions = (IsAuthenticated, IsTeacher)
    serializer_class = SlideSerializer

    def create(self, request, *args, **kwargs):
        lesson_instance = Lesson.objects.get(id=self.kwargs.get('id'))
        serializer = SlideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(lesson=lesson_instance)
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class SlideRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permissions = (IsAuthenticated, IsTeacher)
    serializer_class = SlideSerializer

    def get_queryset(self):
        lesson_instance = Lesson.objects.get(id=self.kwargs.get('id'))
        slides = Slide.objects.filter(lesson=lesson_instance)
        return slides