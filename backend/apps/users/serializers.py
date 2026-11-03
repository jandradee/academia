from rest_framework import serializers
from .models import User, Role, SyncRun
class RoleSerializer(serializers.ModelSerializer):
    class Meta: model=Role; fields="__all__"
class UserSerializer(serializers.ModelSerializer):
    roles=RoleSerializer(many=True,read_only=True)
    password=serializers.CharField(write_only=True,required=False,min_length=12)
    class Meta: model=User; fields=["id","username","email","display_name","first_name","last_name","department","job_title","office_location","is_active","entra_object_id","last_synced_at","roles","date_joined","password","language","email_notifications"]
    def create(self, validated_data):
        pwd=validated_data.pop("password",None)
        user=super().create(validated_data)
        if pwd: user.set_password(pwd); user.save(update_fields=["password"])
        return user
    def update(self, instance, validated_data):
        pwd=validated_data.pop("password",None)
        user=super().update(instance, validated_data)
        if pwd: user.set_password(pwd); user.save(update_fields=["password"])
        return user
class SyncRunSerializer(serializers.ModelSerializer):
    class Meta: model=SyncRun; fields="__all__"
