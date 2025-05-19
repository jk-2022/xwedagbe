

from django.db import models

from django.conf import settings

User= settings.AUTH_USER_MODEL

    




class Product(models.Model):
    name=models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    type=models.ForeignKey("Type", on_delete=models.CASCADE)
    category=models.ForeignKey("Category", on_delete=models.CASCADE)
    ville=models.ForeignKey("Ville", on_delete=models.CASCADE)
    quartier=models.CharField(max_length=100)
    image=models.ImageField(upload_to="media", blank=True, null=True, default="")
    description=models.JSONField(default=dict)
    prix=models.DecimalField(max_digits=15, decimal_places=2)
    avance=models.IntegerField(default=1)
    visite=models.DecimalField(max_digits=15, decimal_places=2, default=2000)
    disponibilite = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product.name} Image"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.CharField(max_length=100, default='admin')
    review = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Review for {self.product.name} by {self.user}"
