from rest_framework import serializers
from .models import CourseProgress, ModuleProgress, VideoProgress, ResourceProgress
class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta: model=CourseProgress; fields="__all__"
class ModuleProgressSerializer(serializers.ModelSerializer):
    class Meta: model=ModuleProgress; fields="__all__"
class VideoProgressSerializer(serializers.ModelSerializer):
    percent=serializers.ReadOnlyField()
    class Meta: model=VideoProgress; fields="__all__"

class ResourceProgressSerializer(serializers.ModelSerializer):
    class Meta: model=ResourceProgress; fields="__all__"
