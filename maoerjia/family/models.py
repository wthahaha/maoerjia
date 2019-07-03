# -*- coding: utf-8 -*-

import uuid as uuid_lib
from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.html import format_html


# 寄养家庭基本信息
class HomeBasicInfo(models.Model):
    home_nick_name = models.CharField(max_length=128, verbose_name="家庭昵称")
    home_of_city = models.CharField(max_length=128, verbose_name="城市")
    home_address_detail = models.CharField(max_length=128, verbose_name="家庭详细地址")
    home_facility = models.CharField(max_length=128, verbose_name="家庭配套设施")
    home_members_num = models.IntegerField(default=1, verbose_name="家庭成员数量")
    is_have_pet_zone = models.BooleanField(default=True, verbose_name="是否有宠物活动区域")
    is_have_old_man = models.BooleanField(default=True, verbose_name="是否有老人")
    is_have_child = models.BooleanField(default=True, verbose_name="是否有儿童")

    def __str__(self):  
        return self.home_nick_name
    
    class Meta:
        verbose_name = "寄养家庭基本信息"
        verbose_name_plural = "寄养家庭基本信息"
    

# 寄养家庭服务人基本信息
class PersionBasicInfo(models.Model):
    MAN = "M"
    WOMEN = "W"
    SEX_CHOICES = (
        (MAN, "男"),
        (WOMEN, "女")
    )
    person_name = models.CharField(max_length=128, verbose_name="寄养家庭主人名称")
    person_sex = models.CharField(max_length=64, choices=SEX_CHOICES, default=MAN, verbose_name="性别")
    person_birthday = models.DateField(verbose_name="出生日期")
    phone_number = models.CharField(max_length=512, verbose_name="电话号码")
    feed_exp_pet_type = models.CharField(max_length=512, default="", blank=True, verbose_name="曾养宠物类型")
    feed_exp_pet_yesrs = models.CharField(max_length=128, default="", blank=True, verbose_name="曾养宠物时间")
    home = models.OneToOneField(HomeBasicInfo, on_delete=models.CASCADE, verbose_name="寄养家庭")
    def __str__(self):  
        return self.person_name

    class Meta:
        verbose_name = "寄养家庭主人基本信息"
        verbose_name_plural = "寄养家庭主人基本信息"


# 寄养家庭图片存储
class HomePhoto(models.Model):

    def default_photo_name():
        return "照片名称"

    photo_name = models.CharField(max_length=512, blank=True, null=True, default=default_photo_name, verbose_name="照片名称")
    url_height = models.PositiveIntegerField(default=75, verbose_name="照片高度")
    url_width = models.PositiveIntegerField(default=75, verbose_name="照片宽度")
    image = models.ImageField(upload_to='home/%Y/%m', height_field='url_height', 
    width_field='url_width')
    home = models.ForeignKey(HomeBasicInfo, on_delete=models.CASCADE, verbose_name="寄养家庭")

    def __str__(self):  
        return self.image.url or ''
    
    

    class Meta:
        verbose_name = "寄养家庭图片"
        verbose_name_plural = "寄养家庭图片"


# 寄养家庭服务人头像图片存储
class PersonPhoto(models.Model):
    photo_name = models.CharField(max_length=512, verbose_name="照片名称")
    avar_image = models.ImageField(upload_to='images/person/avar/%Y/%m')
    person = models.ForeignKey(PersionBasicInfo, on_delete=models.CASCADE, verbose_name="寄养家庭主人")
    
    def __str__(self):  
        return self.photo_name

    class Meta:
        verbose_name = "寄养家庭主人头像图片"
        verbose_name_plural = "寄养家庭主人头像图片"


# 寄养家庭服务人身份证信息存储
class PersonIdCard(models.Model):
    photo_name = models.CharField(max_length=512, verbose_name="照片名称")
    id_card_number = models.CharField(max_length=512, verbose_name="身份证号码")
    id_card_front_url_height = models.PositiveIntegerField(default=225, verbose_name="身份证正面高度")
    id_card_front_url_width = models.PositiveIntegerField(default=225, verbose_name="身份证正面宽度")
    id_card_back_url_height = models.PositiveIntegerField(default=225, verbose_name="身份证反面高度")
    id_card_back_url_width = models.PositiveIntegerField(default=225, verbose_name="身份证反面宽度")
    id_card_front = models.ImageField(upload_to='images/person/id_card/%Y/%m', height_field='id_card_front_url_height', 
    width_field='id_card_front_url_width', verbose_name="身份证正面")
    id_card_back = models.ImageField(upload_to='images/person/id_card/%Y/%m', height_field='id_card_back_url_height', 
    width_field='id_card_back_url_width', verbose_name="身份证反面")
    persion = models.ForeignKey(PersionBasicInfo, on_delete=models.CASCADE, verbose_name="寄养家庭主人")
    
    def __str__(self):  
        return self.photo_name

    class Meta:
        verbose_name = "寄养家庭主人身份证信息"
        verbose_name_plural = "寄养家庭主人身份证信息"



# 基础寄养服务
class BasicLodgeServiceFee(models.Model):
    small_dog_price_per_day = models.FloatField(default="40.0", verbose_name="小型犬每日寄养费用")
    mid_dog_price_per_day = models.FloatField(default="80.0", verbose_name="中型犬每日寄养费用")
    big_dog_price_per_day = models.FloatField(default="100.0", verbose_name="大型犬每日寄养费用")
    home = models.ForeignKey(HomeBasicInfo, on_delete=models.CASCADE, verbose_name="寄养家庭")
    def __str__(self):  
        return "基础寄养价格"

    class Meta:
        verbose_name = "基础寄养服务"
        verbose_name_plural = "基础寄养服务"


# 增值寄养服务
class VipServiceFee(models.Model):
    # 洗澡
    bathe_small_dog_price_per_time = models.FloatField(default="40.0", verbose_name="洗澡费(小)")
    bathe_mid_dog_price_per_time = models.FloatField(default="80.0", verbose_name="洗澡费(中)")
    bathe_big_dog_price_per_time = models.FloatField(default="100.0", verbose_name="洗澡费(大)")
    # 接送
    shuttle_small_dog_price_per_time = models.FloatField(default="40.0", verbose_name="接送费(小)")
    shuttle_mid_dog_price_per_time = models.FloatField(default="80.0", verbose_name="接送费(中)")
    shuttle_big_dog_price_per_time = models.FloatField(default="100.0", verbose_name="接送费(大)")
    # 美容
    good_look_small_dog_price_per_time = models.FloatField(default="40.0", verbose_name="美容费(小)")
    good_lookshuttle_mid_dog_price_per_time = models.FloatField(default="80.0", verbose_name="美容费(中)")
    good_lookshuttle_big_dog_price_per_time = models.FloatField(default="100.0", verbose_name="美容费(大)")
    home = models.ForeignKey(HomeBasicInfo, on_delete=models.CASCADE, verbose_name="寄养家庭")

    class Meta:
        verbose_name = "增值寄养服务"
        verbose_name_plural = "增值寄养服务"


# 长住优惠
class LongTermLive(models.Model):
    more_than_7_days = models.CharField(max_length=32, default="9.5", verbose_name="大于7天")
    more_than_7_days = models.CharField(max_length=32, default="9.0", verbose_name="大于15天")
    more_than_7_days = models.CharField(max_length=32, default="8.0", verbose_name="大于30天")

    class Meta:
        verbose_name = "长住优惠"
        verbose_name_plural = "长住优惠"

# 附加信息
class AdditionalInfo(models.Model):
    BED = "bed"
    BEDROOM = "bedroom"
    SAFA = "safa"
    ZONE_CHOICES = (
        (BED, "床"),
        (BEDROOM, "卧室"),
        (SAFA, "沙发"),
    )
    can_feed_max_num = models.IntegerField(default=2, verbose_name="可寄养最大数量")
    can_pet_touch = models.CharField(max_length=64, choices=ZONE_CHOICES,
     default=SAFA, verbose_name="宠物可接触")
    can_pet_use = models.TextField(default="餐盘", verbose_name="宠物可使用")

    class Meta:
        verbose_name = "附加信息"
        verbose_name_plural = "附加信息"


# 宠物信息
class PetInfo(models.Model):
    DOG = "dog"
    CAT = "cat"
    ANIMAL_CHOICES = (
        (DOG, "狗"),
        (CAT, "猫")
    )
    MAN = "M"
    WOMEN = "W"
    SEX_CHOICES = (
        (MAN, "公"),
        (WOMEN, "母")
    )
    name = models.CharField(max_length=512, verbose_name="宠物名字")
    origin = models.CharField(max_length=512, verbose_name="宠物品种")
    type = models.CharField(max_length=64, choices=ANIMAL_CHOICES,
     default=DOG, verbose_name="宠物类型")
    sex = models.CharField(max_length=64, choices=SEX_CHOICES,
     default=MAN, verbose_name="宠物性别")
    avar_image = models.ImageField(upload_to='images/pet/avar_image/%Y/%m', verbose_name="宠物头像")
    age = models.IntegerField(verbose_name="宠物年龄")
    weight = models.IntegerField(verbose_name="宠物重量")
    vaccin_info_of_4_time= models.DateTimeField(verbose_name="四联注射日期时间")
    vaccin_info_of_4_image = models.ImageField(upload_to='images/pet/vaccin_info_of_4_image/%Y/%m', verbose_name="四联证明图片")
    vaccin_info_of_crazy_time= models.DateTimeField(verbose_name="狂犬疫苗注射日期时间")
    vaccin_info_of_crazy_image = models.ImageField(upload_to='images/pet/vaccin_info_of_crazy_image/%Y/%m', verbose_name="狂犬疫苗证明图片")
    insect_inner_time = models.DateTimeField(verbose_name="体内驱虫时间")
    insect_outter_time = models.DateTimeField(verbose_name="体外驱虫时间")
    is_sterilized = models.BooleanField(default=True, verbose_name="是否绝育")
    is_dog_card = models.BooleanField(default=True, verbose_name="是否有狗证")
    dog_card_image = models.ImageField(upload_to='images/pet/dog_card_image/%Y/%m', verbose_name="狗证图片")
    is_control_shit = models.BooleanField(default=True, verbose_name="是否能控制大小便")
    is_timid = models.BooleanField(default=True, verbose_name="是否胆小")
    is_tricky = models.BooleanField(default=True, verbose_name="是否调皮")
    is_attack = models.BooleanField(default=True, verbose_name="是否具有攻击性")
    is_peace_with_other_dog = models.BooleanField(default=True, verbose_name="是否与其他狗和谐相处")
    is_peace_with_other_cat = models.BooleanField(default=True, verbose_name="是否与其他猫和谐相处")
    is_peace_with_other_child = models.BooleanField(default=True, verbose_name="是否与儿童和谐相处")
    home = models.ForeignKey(HomeBasicInfo, blank=True, on_delete=models.CASCADE, verbose_name="寄养家庭")


    class Meta:
        verbose_name = "宠物信息"
        verbose_name_plural = "宠物信息"