from rest_framework import serializers
from .models import SiteSettings, CourseRating
class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    class Meta:
        model = SiteSettings
        fields = ["company_name","platform_name","tagline","primary_color","accent_color","beige_color","danger_color","logo_url","logo","support_email","footer_text","updated_at"]
    def get_logo(self, obj): return obj.effective_logo_url
class SiteSettingsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ["company_name","platform_name","tagline","primary_color","accent_color","beige_color","danger_color","logo_url","logo_file","support_email","footer_text"]
class CourseRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.display_name", read_only=True)
    class Meta:
        model = CourseRating
        fields = ["id","course","user","user_name","stars","comment","created_at","updated_at"]
        read_only_fields = ["user"]
