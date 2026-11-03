from rest_framework import serializers
from .models import Category, Course, Module, Video, Resource, Assignment, Enrollment

def cover_url(obj):
    if not getattr(obj, "cover_key", ""): return ""
    v = ""
    try:
        import os
        from apps.core.files import media_path
        v = f"?v={int(os.path.getmtime(media_path(obj.cover_key)))}"
    except Exception:
        v = ""
    return f"/api/courses/{obj.id}/cover-image/{v}"
class CategorySerializer(serializers.ModelSerializer):
    class Meta: model=Category; fields="__all__"
class VideoSerializer(serializers.ModelSerializer):
    class Meta: model=Video; fields="__all__"
class ResourceSerializer(serializers.ModelSerializer):
    class Meta: model=Resource; fields="__all__"
class ModuleSerializer(serializers.ModelSerializer):
    videos=VideoSerializer(many=True,read_only=True); resources=ResourceSerializer(many=True,read_only=True)
    class Meta: model=Module; fields="__all__"
class CourseSerializer(serializers.ModelSerializer):
    modules=ModuleSerializer(many=True,read_only=True)
    cover=serializers.SerializerMethodField()
    class Meta: model=Course; fields="__all__"
    def get_cover(self, obj):
        return cover_url(obj)
class CourseListSerializer(serializers.ModelSerializer):
    cover=serializers.SerializerMethodField()
    class Meta: model=Course; fields=["id","code","title","short_description","category","course_type","status","estimated_duration_minutes","recognized_duration_minutes","available_from","available_until","version","cover"]
    def get_cover(self, obj):
        return cover_url(obj)
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta: model=Assignment; fields="__all__"
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta: model=Enrollment; fields="__all__"
