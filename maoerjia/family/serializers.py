from django.conf import settings
from rest_framework import serializers

from .models import (AdditionalInfo, BasicLodgeServiceFee, HomeBasicInfo,
                     HomePhoto, LongTermLive, PersionBasicInfo, PersonIdCard,
                     PersonPhoto, PetInfo, VipServiceFee)
from .utils import get_token_from_request


class HomeBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBasicInfo
        fields = "__all__"
