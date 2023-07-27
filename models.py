from django.db import models
import uuid

# Create your models here.

class Recipient(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField("date of birth")
    gender = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    addressDetails = models.CharField(max_length=200)
    medicalCondition = models.CharField(max_length=200, null=True, blank=True)
    specialNeeds = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Donor(models.Model):
    name = models.CharField(max_length=200)
    addressDetails = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)

class Donation(models.Model):
    name = models.ForeignKey(Donor, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    donationDate = models.DateTimeField("donation date")

    def __str__(self):
        return str(self.id)

class ItemCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Size (models.Model):
    size = models.CharField(max_length=20)

    def __str__(self):
        return str(self.size)

class Item (models.Model):
    name = models.CharField(max_length=200 , default=0)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name = "%(class)s_stock_category", default=0)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name = "%(class)s_size", null=True, blank=True)
    ingredients = models.CharField(max_length=200, null=True, blank=True)
    expiryDate = models.DateTimeField("expiry date", null=True, blank=True)

    def __str__(self):
        if self.size is not None:
            return str(self.name) + ' ' + str(self.size)
        else:
            return str(self.name)

class Stock (models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name = "%(class)s_stock_item", default=0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.item)






class Order (models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.PROTECT, blank=True, null=True)

    def delete(self, *args, **kwargs):
        items = self.items.all()
        for item in items:
            item.item.quantity += 1
            item.item.save()

        kit_items = self.order_kit.kit.item
        for item in kit_items:
            item.quantity += 1
            item.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.id)

class OrderItem (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", blank=True, null=True)
    item = models.ForeignKey(Stock, on_delete=models.PROTECT,  blank=True, null=True)

    def save(self, *args, **kwargs):
        self.item.quantity -= 1
        self.item.save()
        super(OrderItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.item.quantity += 1
        self.item.save()
        super().delete(*args, **kwargs)
    def __str__(self):
        return str(self.id)


class Kit(models.Model):
    name = models.CharField(max_length=200)
    item = models.ManyToManyField(Stock, related_name='kit_item')

    def __str__(self):
        return self.name

# class KitItem(models.Model):
#     kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="%(class)s_kit_items", default=0, blank=True, null=True)
#     item = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="%(class)s_item", default=0, blank=True, null=True)
#
#     def __str__(self):
#         return str(self.item)


class OrderKit(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="%(class)s_kit", default=0, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_kit", default=0, blank=True, null=True)

    def save(self, *args, **kwargs):
        items = self.kit.item.all()
        for item in items:
            item.quantity -= 1
            item.save()
        super(OrderKit, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        items = self.kit_items.all()
        for item in items:
            item.item.quantity += 1
            item.item.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.kit)





