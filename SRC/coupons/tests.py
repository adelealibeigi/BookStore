from .models import CashDiscount,PercentageDiscount
from django.test import TestCase


class DiscountTests(TestCase):
    def test_create_product(self):
        c_discount = CashDiscount.objects.create(
            code='aws-1',
            amount=20,
            active=False
            )
        p_discount = PercentageDiscount.objects.create(
            code='bsd4',
            amount=55,
            active=False
        )
        self.assertEqual(CashDiscount.objects.all().count(), 1)
        self.assertEqual(PercentageDiscount.objects.all().count(), 1)

