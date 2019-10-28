from rest_framework import serializers
from django.conf import settings
from .utils import get_token_from_request
from .models import *


class HomeBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


