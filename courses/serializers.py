from rest_framework import serializers
from .models import Category, Course, Lesson, Slide

class SlideSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Slide
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    #courses = CourseListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'