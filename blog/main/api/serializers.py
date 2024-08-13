from rest_framework import serializers
from main.models import Blog   

class BlogSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()  # Display the username in the browsable API
    # user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.CharField(source='user.username', read_only=True)    
    
    class Meta:
        model=Blog
        fields="__all__"
        # exclude=['updated_at']    


