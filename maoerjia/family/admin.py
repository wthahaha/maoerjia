from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
from .models import HomeBasicInfo, PersionBasicInfo, HomePhoto, PersonPhoto, PersonIdCard, BasicLodgeServiceFee, VipServiceFee, LongTermLive, AdditionalInfo, PetInfo

# Register your models here.


class HomePhotoInline(admin.TabularInline):
    model = HomePhoto
    extra = 1

    def upload_img(self, obj):
        try:
            img = mark_safe('<img src="%s" width="200px" />' % (obj.image.url))
        except Exception as e:
            img = ''
        return img
    upload_img.short_description = '家庭照片'
    upload_img.allow_tags = True

    list_display = ['id', 'photo_name', 'upload_img', 'home']
    readonly_fields = ['upload_img']


class BasicLodgeServiceFeeInline(admin.TabularInline):
    model = BasicLodgeServiceFee
    extra = 1
    filedsets = [
        ("每日寄养费用",{"fields":("small_dog_price_per_day","mid_dog_price_per_day","big_dog_price_per_day")})
    ]

class VipServiceFeeInline(admin.TabularInline):
    model = VipServiceFee
    extra = 1
    fieldsets = [
        ('洗澡', {'fields': ['bathe_small_dog_price_per_time', 'bathe_mid_dog_price_per_time', 'bathe_big_dog_price_per_time']}),
        ('接送', {'fields': ['shuttle_small_dog_price_per_time',  'shuttle_mid_dog_price_per_time', 'shuttle_big_dog_price_per_time']}),
        ('美容', {'fields': ['good_look_small_dog_price_per_time', 'good_lookshuttle_mid_dog_price_per_time', 'good_lookshuttle_big_dog_price_per_time']}),
    ]

class PetInfoAdmin(admin.ModelAdmin):

    list_per_page = 10

    search_fields = ['name', 'origin', 'age', 'sex', 'weight', 'home']

    def upload_vaccin_info_of_4_image(self, obj):
        try:
            img = mark_safe('<img src="%s" width="200px" />' % (obj.vaccin_info_of_4_image.url))
        except Exception as e:
            img = ''
        return img
    upload_vaccin_info_of_4_image.short_description = '四联证明图片'
    upload_vaccin_info_of_4_image.allow_tags = True

    def upload_vaccin_info_of_crazy(self, obj):
        try:
            img = mark_safe('<img src="%s" width="200px" />'  % (obj.vaccin_info_of_crazy_image.url))
        except Exception as e:
            img = ''
        return img
    upload_vaccin_info_of_crazy.short_description = '狂犬疫苗证明图片'
    upload_vaccin_info_of_crazy.allow_tags = True

    def upload_dog_card_image(self, obj):
        try:
            img = mark_safe('<img src="%s" width="200px" />'  % (obj.dog_card_image.url))
        except Exception as e:
            img = ''
        return img
    upload_dog_card_image.short_description = '狗证图片'
    upload_dog_card_image.allow_tags = True

    def show_avar_image(self, obj):
        try:
            img = mark_safe('<img src="%s" width="200px" />' % (obj.avar_image.url))
        except Exception as e:
            img = ''
        return img
    show_avar_image.short_description = '宠物头像'
    show_avar_image.allow_tags = True
    # readonly_fields = ('get_vaccin_info_of_crazy_image', 'dog_card_image')
    # fieldsets = [
    #     (u'狂犬疫苗证明图片', {'fields': ['get_vaccin_info_of_crazy_image']}),
    #     (u'狗证图片', {'fields': ['dog_card_image']}),
   
    # ]

    list_display =['id', 'name', 'show_avar_image', 'origin', 'age', 'sex', 'weight', 'home',
     'upload_vaccin_info_of_4_image', 'upload_vaccin_info_of_crazy', "upload_dog_card_image"]
   

class HomeBasicInfoAdmin(admin.ModelAdmin):
    list_per_page = 10

    search_fields = ['home_nick_name', 'id']
    list_display = ["home_nick_name","home_of_city","home_members_num"]
    fieldsets = [
        ("家庭基本信息", {"fields":["home_nick_name", "home_of_city","home_address_detail","home_facility",
        "home_members_num",("is_have_pet_zone","is_have_old_man","is_have_child")]}),
        
    ]
    inlines = [HomePhotoInline,BasicLodgeServiceFeeInline,VipServiceFeeInline]


class PersonPhotoInline(admin.TabularInline):
    model = PersonPhoto
    extra = 1

class PersonIdCardInline(admin.TabularInline):
    model = PersonIdCard
    extra = 1


class PersionBasicInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ['person_name', 'id', "phone_number","home"]
    list_display = ["id",'person_name',"phone_number","home"]
    fieldsets = [
        ("寄养家庭主人信息", {"fields":["person_name", "phone_number","home","feed_exp_pet_type",
        "feed_exp_pet_yesrs"]}),
    ]
    inlines = [PersonPhotoInline, PersonIdCardInline]

admin.site.site_title = '毛儿家'
admin.site.site_header = 'MaoErJia后台管理系统'



admin.site.register(LongTermLive)
admin.site.register(AdditionalInfo)
admin.site.register(PetInfo, PetInfoAdmin)
admin.site.register(HomeBasicInfo, HomeBasicInfoAdmin)
admin.site.register(PersionBasicInfo, PersionBasicInfoAdmin)
