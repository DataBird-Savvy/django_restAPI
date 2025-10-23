from rest_framework import serializers
from .models import People,Team
from django.contrib.auth.models import User



class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=150)
    password=serializers.CharField(max_length=128,write_only=True)
    email=serializers.EmailField()
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        return data
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=150)
    password=serializers.CharField(max_length=128,write_only=True)
    

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_name','city']
        
        

class PeopleSerializer(serializers.ModelSerializer):
    team=TeamSerializer(read_only=True)
    team_info=serializers.SerializerMethodField()
    
    class Meta:
        model = People
        fields = '__all__'
        depth = 1
    
    def get_team_info(self, obj):
        if obj.team:
            return f"{obj.team.team_name} from {obj.team.city}"
        return "No Team Assigned"
        
    def validate(self, value):
        special_characters = "!@#$%^&*()_+-=[]{}|;':\",.<>/?`~"
   
        if any(char in special_characters for char in value.get('name', '')):
            raise serializers.ValidationError("Name should not contain special characters.")    
        if value.get('age', 0) < 0:
            raise serializers.ValidationError("Age must be a non-negative integer.")
        
        return value