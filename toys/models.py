from decimal import Decimal
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class ToyDrawing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='customer_drawings/', blank=True, null=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    height = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('20.00'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    color = models.CharField(max_length=50, blank=True)
    special_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calculate the price based on the drawing's area
        base_area = Decimal('100.00')  # Base area of 10x10 cm
        drawing_area = self.width * self.height
        self.price = (drawing_area / base_area) * self.base_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"


class Toy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='toys/')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item}"


class Accessory(models.Model):
    toy = models.ForeignKey(Toy, related_name='accessories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='accessories/')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} for {self.toy.name}"


class Review(models.Model):
    toy = models.ForeignKey(Toy, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.get_full_name() or self.user.username} for {self.toy.name} - {self.rating} Stars"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    shipping_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(ToyDrawing)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='unpaid')

    def __str__(self):
        return f"Order{self.id} by {self.user.name}"


class HomepageReview(models.Model):
    customer_name = models.CharField(max_length=250)
    email = models.EmailField()
    review_TEXT = models.TextField()
    image = models.ImageField(upload_to='homepage_review/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"review by {self.customer_name}"