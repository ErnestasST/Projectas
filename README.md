This is a Django-based e-commerce project for a Toy Shop. It allows users to browse toys, upload custom toy drawings, 
and purchase products like toys and accessories. 
The project includes user authentication, cart management, and a review system.

# Features
- **User Authentication**: Users can register, login, and manage their profiles.
- **Toy Uploads**: Users can upload custom toy drawings with calculated prices based on dimensions.
- **Cart System**: Add toys, accessories, or custom drawings to the shopping cart and proceed to checkout.
- **Admin Dashboard**: Admins can approve toy drawings, manage toys, and accessories.
- **Customer Reviews**: Users can leave reviews and ratings for toys.
- **Email Notifications**: Users and admins receive email notifications for important actions like uploads and approvals.

## Installation

### Prerequisites
- Python 3.x
- Django 3.x or 4.x
- PostgreSQL (or SQLite for local development)

### Steps




1. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2. **Set up the Database**
   Update the `settings.py` file with your database configuration.
   
   For local development with SQLite, no configuration changes are needed. For PostgreSQL, update your database settings.

    Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Create a Superuser (Admin Account)**
    ```bash
    python manage.py createsuperuser
    ```

4. **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

5. **Open the Project in Your Browser**
    Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the project.

---

## Usage

### User Features:
- Register a new account or log in.
- Browse and shop for factory-made toys and accessories.
- Upload custom toy drawings and track their approval status.
- Add items to the cart and proceed to checkout.

### Admin Features:
- Approve user-uploaded toy drawings.
- Manage products, accessories, and reviews from the admin dashboard.

---

## Tech Stack

- **Backend**: Django, Python
- **Database**: SQLite (for development), PostgreSQL (recommended for production)
- **Frontend**: HTML, CSS (Bootstrap or custom styling)
- **Email**: Integrated with SMTP for sending email notifications (e.g., via Gmail)
- **Payment Gateway**: Stripe (optional, if integrated)

---

## Project Structure

```plaintext
toy-shop/
│
├── toys/                        # Main Django app for toy functionality
│   ├── migrations/              # Database migrations
│   ├── templates/               # HTML templates
│   ├── static/                  # Static files (CSS, JS, Images)
│   ├── models.py                # Models (Toy, Drawing, Cart, etc.)
│   ├── views.py                 # Views (business logic)
│   ├── forms.py                 # Forms (ToyDrawingForm, UserRegisterForm)
│   └── urls.py                  # URL routing
│
├── manage.py                    # Django management commands
├── requirements.txt             # Project dependencies
└── README.md                    # Project readme (this file)