from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    )

    nickname = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField('핸드폰 번호', max_length=15)
    address = models.CharField(max_length=200)
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(max_length=11, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    # point 고려

    REQUIRED_FIELDS = ['email']


# class Profile(models.Model):
#     COUPON_CHOICES = (
#         ('A', '[신규가입쿠폰] 10% 할인'),
#         ('B', '[농할갑시다] 햇농산물 20%'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     grade = models.OneToOneField(User, on_delete=models.CASCADE)
#     coupon = models.CharField('쿠폰', max_length=1, choices=COUPON_CHOICES)
#     accumulated_money = models.IntegerField('적립금', default=0)
#     point = models.IntegerField('포인트', default=0)
#
#




