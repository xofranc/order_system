from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Max # Import Max for getting the highest client number

# Create your models here.

class CustomUserManager(BaseUserManager):
    '''
    Custom user manager for the custom user model.
    '''
    #! Creates a user with the email and password, ensuring the email is mandatory
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    #! Creates a superuser with the email and password, ensuring the email sea obligatorio
    #! and that the superuser has administrator permissions
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', User.ADMIN)  # Default user type for superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

#! This is your main user model, based on AbstractUser, but customized to use email as login.
class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    #! We define user types as constants
    #! to avoid spelling errors and facilitate code maintenance
    #! and code readability
    MESERO = 'mesero'
    COCINERO = 'cocinero'
    ADMIN = 'administrador'
    CLIENTE = 'cliente'
    GERENTE = 'gerente'

    # Remove the default username field from AbstractUser
    username = None

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True) # Ensure email is unique and used for login

    USERNAME_FIELD = 'email' # Set email as the field used for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Fields required when creating a user via createsuperuser

    USER_TYPE_CHOICES = (
        (MESERO, 'Mesero'),
        (COCINERO, 'Cocinero'),
        (ADMIN, 'Administrador'),
        (CLIENTE, 'Cliente'),
        (GERENTE, 'Gerente'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=CLIENTE)

    # New field added to store the numerical identifier for the user type. START: MODIFICATION
    # 'blank=True, null=True' allows it to be initially empty for existing data during migrations
    # It will be populated automatically in the save method.
    user_type_id = models.SmallIntegerField(blank=True, null=True, db_index=True)
    # END: MODIFICATION

    # Map string user types to numerical IDs. START: ADDITION
    USER_TYPE_ID_MAP = {
        MESERO: 1,
        COCINERO: 2,
        ADMIN: 3,
        CLIENTE: 4,
        GERENTE: 5,
    }
    # END: ADDITION

    objects = CustomUserManager() # Assign the custom manager

    def save(self, *args, **kwargs):
        """
        Custom save method to set the numerical user_type_id based on user_type.
        """
        # Automatically set user_type_id based on the user_type string. START: MODIFICATION
        if self.user_type in self.USER_TYPE_ID_MAP:
            self.user_type_id = self.USER_TYPE_ID_MAP[self.user_type]
        else:
            # Handle cases where user_type might not be in the map, perhaps default to None
            self.user_type_id = None
        # END: MODIFICATION

        super().save(*args, **kwargs) # Call the original save method

    def __str__(self):
        """
        String representation of the User model, using the email.
        """
        # Modified __str__ to include the new user_type_id. START: MODIFICATION
        return f"{self.email} ({self.user_type.capitalize()} - ID: {self.user_type_id or 'N/A'})"
        # END: MODIFICATION


#! This model is linked to the user model, and is used to store client information
#! and client membership information, if active
class Cliente(models.Model):
    """
    Model representing a client.
    """
    # One-to-one relationship with the custom User model.
    # 'related_name' allows accessing the Cliente profile from a User instance (e.g., user.cliente_profile).
    # Added related_name for clarity and easier reverse lookups. START: MODIFICATION
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente_profile')
    # END: MODIFICATION

    # 'mail' field is often redundant if 'user.email' is always used and preferred.
    # I've added logic in save to populate it from user.email if empty.
    # Added null=True to allow the field to be empty in the database. START: MODIFICATION
    mail = models.EmailField(unique=True, blank=True, null=True)
    # END: MODIFICATION
    phone = models.CharField(max_length=10, blank=True, null=True) # Phone number field, optional
    birth_date = models.DateField(blank=True, null=True)
    # Added auto_now_add for entry_date to automatically set on creation. START: MODIFICATION
    entry_date = models.DateField(auto_now_add=True)
    # END: MODIFICATION

    # New field to store a unique, sequential number for each client. START: ADDITION
    # 'null=True, blank=True' allows it to be initially empty before saving.
    # 'unique=True' ensures no two clients have the same client_number.
    client_number = models.PositiveIntegerField(unique=True, null=True, blank=True, db_index=True)
    # END: ADDITION

    # This field defines the type of membership.
    # It currently uses the same choices as User.USER_TYPE_CHOICES, which might be redundant
    # if a 'Cliente' instance always implies a 'CLIENTE' user_type.
    # Consider if 'type_of_membership' should define different membership levels (e.g., 'Gold', 'Silver')
    # distinct from the general 'user_type'.
    type_of_membership = models.CharField(max_length=20, choices=User.USER_TYPE_CHOICES, default=User.CLIENTE)

    membership_start = models.DateField(default=timezone.now)
    membership_end = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure consistency and auto-assign values.
        """
        # --- Consistency for User Type ---
        # Ensure the linked User's user_type is 'CLIENTE' if a Cliente profile is being saved.
        # This will trigger the User's save method, which in turn will set the user_type_id. START: MODIFICATION
        if self.user.user_type != User.CLIENTE:
            self.user.user_type = User.CLIENTE
            # Note: self.user.save() will now automatically set user_type_id for the User.
            self.user.save()
        # END: MODIFICATION

        # --- Auto-assign Client Number --- START: ADDITION
        # If client_number is not set, find the highest existing client_number
        # and assign the next sequential number.
        # NOTE: This approach can lead to race conditions in high-concurrency environments.
        # For a personal project, it's generally acceptable. For production, consider
        # a more robust solution like a database sequence or UUIDField.
        if self.client_number is None:
            # Aggregate to find the maximum existing client_number
            max_client_number = Cliente.objects.aggregate(Max('client_number'))['client_number__max']
            if max_client_number is not None:
                self.client_number = max_client_number + 1
            else:
                self.client_number = 1 # Start from 1 if no clients exist yet
        # END: ADDITION

        # --- Populate 'mail' from User's email if not set --- START: ADDITION
        if not self.mail and self.user and self.user.email:
            self.mail = self.user.email
        # END: ADDITION

        # --- Auto-assign Membership End Date ---
        # If membership_start is set but membership_end is not, default to 30 days later.
        # Modified this block to correctly set membership_end. START: MODIFICATION
        if self.membership_start and not self.membership_end:
            self.membership_end = self.membership_start + timedelta(days=30)
        # END: MODIFICATION

        # Ensure type_of_membership matches User.CLIENTE if it's still default, or align if necessary
        # This line ensures consistency if type_of_membership should always match the user's type.
        # If type_of_membership has a different purpose (e.g., membership tier), remove this line.
        # Added this block for membership type consistency. START: ADDITION
        if self.type_of_membership != self.user.user_type:
            self.type_of_membership = self.user.user_type
        # END: ADDITION

        # Call the original save method of the Model
        super().save(*args, **kwargs)

    def is_membership_active(self):
        """
        Check if the membership is active.
        Returns True if membership_end is set and is in the future or today, False otherwise.
        """
        # Refined the logic for checking membership activity. START: MODIFICATION
        if self.membership_end:
            return self.membership_end >= timezone.now().date()
        return False # Membership is not active if membership_end is not set
        # END: MODIFICATION

    def __str__(self):
        """
        String representation of the Cliente model.
        """
        # Modified __str__ to include the new client_number. START: MODIFICATION
        return f"Cliente: {self.user.email} (No. {self.client_number or 'N/A'})"
        # END: MODIFICATION

# For now, we will leave the other user types as empty models.
# When the models are defined, we can uncomment this section and use it.

class Mesero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add specific fields for Mesero
    def __str__(self):
        return self.user.email

# class Cocinero(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add specific fields for Cocinero
#     def __str__(self):
#         return self.user.email

# class Gerente(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add specific fields for Gerente
#     def __str__(self): # Original comment was 'self' - fixed to 'self' for Python 3. START: FIX
#         return self.user.email
# END: FIX

# class AdminProfile(models.Model): # Naming it AdminProfile to avoid clash with User.ADMIN constant
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add specific fields for Admin
#     def __str__(self):
#         return self.user.email

