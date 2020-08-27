from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from goods.models import Goods

User = get_user_model()


class CartItem(models.Model):
    quantity = models.IntegerField(default=1,
                                   validators=[MinValueValidator(1), MaxValueValidator(50)])
    user = models.ForeignKey(User, on_delete=CASCADE)
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
        related_query_name='cartitems',
    )

    def sub_total(self):
        return self.goods.price * self.quantity
