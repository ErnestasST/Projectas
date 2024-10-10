import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import ToyDrawing, Cart, CartItem, Toy, Accessory, UserProfile, Order, Review, HomepageReview
from .forms import ToyDrawingForm, UserRegisterForm, ToyForm, AccessoryForm, ReviewForm, UserProfileForm

stripe.api_key = settings.STRIPE_SECRET_KEY

"""
View: home
Description: Displays the homepage with customer reviews. Retrieves all `HomepageReview` objects and orders them by their creation date.
"""


def home(request):
    reviews = HomepageReview.objects.all().order_by('-created_at')
    return render(request, 'toys/home.html', {'reviews': reviews})


"""
View: register
Description: Handles user registration. When a valid form is submitted, it creates a new user and associated `UserProfile`. 
The user is logged in and redirected to the homepage upon successful registration.
"""


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)

            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'toys/register.html', {'form': form})


"""
View: upload_drawing
Description: Handles the upload of toy drawings by authenticated users. It calculates the price based on the dimensions, 
saves the drawing and uploaded image, and sends an email notification to the admin. Displays the form if no submission is made.
"""


@login_required
def upload_drawing(request):
    calculated_price = None

    if request.method == 'POST':
        form = ToyDrawingForm(request.POST, request.FILES)

        if form.is_valid():
            drawing = form.save(commit=False)

            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')
            base_area = 100
            drawing_area = width * height
            calculated_price = (drawing_area / base_area) * drawing.base_price

            if 'submit_drawing' in request.POST:
                drawing.user = request.user
                drawing.price = calculated_price

                if 'image' in request.FILES:
                    drawing.image = request.FILES['image']
                drawing.save()

                send_mail(
                    subject='New Drawing Uploaded',
                    message=f'A new drawing has been uploaded by {request.user.email}.\n\nDrawing: {drawing.name}\nSize: {width} x {height}\nPrice: ${calculated_price:.2f}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['estoyshop21@gmail.com']
                )

                messages.success(request, "Your drawing has been successfully uploaded!")
                return redirect('track_drawings')
        else:
            messages.error(request, "There was an error with your submission.")

    else:
        form = ToyDrawingForm()

    return render(request, 'toys/upload_drawing.html', {'form': form, 'calculated_price': calculated_price})


"""
View: track_drawings
Description: Displays all toy drawings uploaded by the currently authenticated user, allowing them to track their submissions.
"""


@login_required
def track_drawings(request):
    drawings = ToyDrawing.objects.filter(user=request.user)

    return render(request, 'toys/track_drawings.html', {'drawings': drawings})


"""
View: edit_drawing
Description: Allows the user to edit an existing toy drawing. Retrieves the drawing based on the ID and only if it belongs to the logged-in user.
The user can modify and save changes, with validation handling in place.
"""


@login_required
def edit_drawing(request, id):
    drawing = get_object_or_404(ToyDrawing, id=id,
                                user=request.user)

    if request.method == 'POST':
        form = ToyDrawingForm(request.POST, request.FILES,
                              instance=drawing)
        if form.is_valid():
            form.save()
            return redirect('track_drawings')
    else:
        form = ToyDrawingForm(instance=drawing)

    return render(request, 'toys/edit_drawing.html', {'form': form, 'drawing': drawing})


"""
View: view_cart
Description: Displays the contents of the user's shopping cart. It calculates the subtotal and total price of all items in the cart 
and displays them to the user.
"""


@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)

    cart_items = []
    total_price = 0

    for cart_item in cart.cartitem_set.all():
        item = cart_item.item

        subtotal = item.price * cart_item.quantity
        total_price += subtotal

        cart_items.append({
            'item': item,
            'quantity': cart_item.quantity,
            'price': item.price,
            'subtotal': subtotal,
        })

    return render(request, 'toys/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


"""
View: add_to_cart
Description: Adds an item (toy, accessory, or drawing) to the user's cart. It checks the item type and quantity, 
then adds the appropriate item to the user's cart. If the item already exists in the cart, the quantity is updated.
"""


@login_required
def add_to_cart(request, item_id, item_type):
    if item_type == 'toy':
        model = Toy
    elif item_type == 'accessory':
        model = Accessory
    elif item_type == 'drawing':
        model = ToyDrawing
    else:
        return redirect('toy_list')

    content_type = ContentType.objects.get_for_model(model)

    item = get_object_or_404(model, id=item_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=item.id
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


"""
View: toy_list
Description: Displays a list of all toys available in the store. Retrieves all `Toy` objects and renders them on the toy listing page.
"""


def toy_list(request):
    toys = Toy.objects.all()
    return render(request, 'toys/toy_list.html', {'toys': toys})


"""
View: toy_details
Description: Displays the details of a specific toy, including its accessories and customer reviews. 
It also handles review submission for authenticated users.
"""


def toy_details(request, id):
    toy = get_object_or_404(Toy, id=id)
    accessories = toy.accessories.all()
    reviews = toy.reviews.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.toy = toy
                review.user = request.user
                review.save()
                messages.success(request, "Thank you for your review!")
                return redirect('toy_details', id=toy.id)
        else:
            messages.error(request, "You must be logged in to submit a review.")
            return redirect('login')
    else:
        form = ReviewForm()

    return render(request, 'toys/toy_details.html', {
        'toy': toy,
        'accessories': accessories,
        'reviews': reviews,
        'form': form
    })


"""
View: add_toy
Description: Allows authenticated users to add a new toy to the database. Handles form submission, including file uploads for images. 
Redirects to the toy list upon successful submission.
"""


@login_required
def add_toy(request):
    if request.method == 'POST':
        form = ToyForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('toys_list')
    else:
        form = ToyForm()
    return render(request, 'toys/add_toy.html', {'form': form})


"""
View: add_accessory
Description: Allows authenticated users to add a new accessory for toys. It handles form submission and file uploads, 
saving the accessory to the database and redirecting to the toy list after successful submission.
"""


@login_required
def add_accessory(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('toy_list')
    else:
        form = AccessoryForm()
    return render(request, 'toys/add_accessory.html', {'form': form})


"""
View: update_cart
Description: Updates the quantity of an item in the user's cart. Increases or decreases the quantity based on the user's action 
and saves the updated cart item.
"""


@login_required
def update_cart(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if action == 1:
        cart_item.quantity += 1
    elif action == 0 and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('view_cart')


"""
View: remove_from_cart
Description: Allows the user to remove an item from their cart. The item is deleted from the cart, and the user is redirected to the cart page.
"""


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')


"""
View: user_profile
Description: Displays the user's profile, including their uploaded toy drawings and any orders (if applicable). 
Fetches the user profile, creating one if it does not exist, and renders the profile page with the relevant data.
"""


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    drawings = ToyDrawing.objects.filter(user=request.user)

    orders = []

    return render(request, 'toys/user_profile.html', {
        'profile': profile,
        'drawings': drawings,
        'orders': orders
    })


"""
View: edit_profile
Description: Allows users to update their profile information. It fetches the user's profile and displays a form to make updates.
"""


@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'toys/edit_profile.html', {'form': form})


"""
View: checkout
Description: Displays the checkout page with the items currently in the user's cart. It calculates the total price and shows the list of items.
"""


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    cart_items = []
    total_price = 0
    for cart_item in cart.cartitem_set.all():
        subtotal = cart_item.item.price * cart_item.quantity
        total_price += subtotal
        cart_items.append({
            'item': cart_item.item,
            'quantity': cart_item.quantity,
            'price': cart_item.item.price,
            'subtotal': subtotal,
        })

    return render(request, 'toys/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


"""
View: payment
Description: Initiates the payment process using Stripe for the most recent order. It creates a checkout session with Stripe 
and redirects the user to Stripe's payment page.
"""


@login_required
def payment(request):
    order = Order.objects.filter(user=request.user).order_by('-created_at').first()

    if not order:
        return redirect('checkout')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"Order {order.id}",
                    },
                    'unit_amount': int(order.total_price * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/payment/success/'),
        cancel_url=request.build_absolute_uri('/payment/cancel/'),
    )

    return redirect(session.url, code=303)


"""
View: payment_success
Description: Displays a success message when the payment is completed successfully. Redirects to a confirmation page after payment.
"""


@login_required
def payment_success(request):
    return render(request, 'toys/payment_success.html')


"""
View: payment_cancel
Description: Displays a cancellation message if the user cancels the payment process. Redirects to the cancellation page.
"""


@login_required
def payment_cancel(request):
    return render(request, 'toys/payment_cancel.html')


"""
View: review_detail
Description: Displays detailed information about a specific review. It fetches the review and shows details, 
such as the user’s name and the review content.
"""


def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    user_name = review.user.get_full_name() or review.user.username  # Use get_full_name or fallback to username

    return render(request, 'toys/review_detail.html', {'review': review, 'user_name': user_name})
