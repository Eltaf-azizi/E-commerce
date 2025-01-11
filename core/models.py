from django.conf import settings # type: ignore
from django.db import models # type: ignore
from django.shortcuts import reverse  # type: ignore


CATEGORY_CHOICES = (
    ('S', 'Shirt')
    ('SW', 'sport wear')
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary')
    ('S', 'secondary')
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


    def get_absolute_url(self):
        return reverse("core:prduct", kwargs={
            'slug': self.slug
        })
    
    def add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs = {
            'slug': self.slug
        })
    

    def remove_tfrom_cart_url(self):
        return reverse("core:remove_from_cart", kwargs = {
            'slug': self.slug
        })


class OrderItem(models.Model):

    user = models.foreignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.foreignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.title