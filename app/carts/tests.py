import os
from django.contrib.auth import get_user_model
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from carts.models import CartItem
from config import settings
from config.settings.base import ROOT_DIR
from goods.models import Goods

User = get_user_model()


class CartTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User(username='test_user', password='1111', email='test_user@test.com')
        self.user.set_password(self.user.password)
        self.user.save()

        image = settings.base.MEDIA_ROOT + '/pycharm.png'
        for i in range(5):
            test_file = SimpleUploadedFile(name='test_image.jpeg', content=open(image, 'rb', ).read(),
                                           content_type="image/jpeg"
                                           )
            test_file2 = SimpleUploadedFile(name='test_image.jpeg', content=open(image, 'rb', ).read(),
                                            content_type="image/jpeg"
                                            )

            self.goods = Goods.objects.create(img=test_file, info_img=test_file2, title='상품명',
                                              short_desc='간단설명', price='555')

    def test_cart_create(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)

        response = self.client.get(f'/api/cart/{test_user.pk}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_user.pk, test_user.cart.pk)

    def test_cart_list(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        test_goods = Goods.objects.all()

        for i in test_goods:
            self.cart = CartItem.objects.create(goods=i, cart=test_user.cart, quantity=3)

        cartitem = CartItem.objects.values()

        response = self.client.get(f'/api/cart/{test_user.pk}/item')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for cart_data, response_data in zip(cartitem, response.data):
            self.assertEqual(cart_data['goods_id'], response_data['goods']['id'])

    def test_cart_update(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        test_goods = Goods.objects.all()
        goods1 = Goods.objects.first()

        data = {
            "goods": goods1.pk,
            "quantity": 3,
            "cart": test_user.pk
        }
        response = self.client.post(f'/api/cart/{test_user.pk}/item', data=data)

        data2 = {
            "goods": goods1.pk,
            "quantity": 5,
            "cart": test_user.pk
        }

        response2 = self.client.patch(f'/api/cart/{test_user.pk}/item/{goods1.pk}', data=data2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)