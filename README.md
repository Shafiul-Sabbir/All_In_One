# All In One

## Overview
All In One is a Django-based e-commerce project that provides category-based product listings, user authentication, shopping cart functionality, and payment processing. This project includes an admin panel, user profile management, and search functionality.

## Features
- User authentication (login, logout, registration, profile update, password change)
- Product listing by categories
- Shopping cart system
- Order processing
- Payment integration
- Search functionality
- Admin panel for product and order management

## Installation

### Prerequisites
Ensure you have the following installed:
- Python (>= 3.x)
- Django (>= 4.x)
- PostgreSQL (or SQLite for development)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Shafiul-Sabbir/All_In_One.git
   cd ecom
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Create a `.env` file in the project root
   - Add database and secret key configurations
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
7. Run the server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Access the application at `http://127.0.0.1:8000/`
- Log in as an admin at `http://127.0.0.1:8000/admin/`



## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a Pull Request

## License
This project is licensed under this Github owner.

## Contact
For any inquiries, please contact [Shafiul Sabbir] at [sabbirvai82@gmail.com].

