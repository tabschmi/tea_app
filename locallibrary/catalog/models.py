from django.db import models

#Import for created models
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

import uuid # Required for unique tea instances

# Create your models here.

#Type model
class Type(models.Model):
    """Model representing a tea type."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a tea type (e.g. green, black etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular type instance."""
        return reverse('type-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='type_name_case_insensitive_unique',
                violation_error_message = "Type already exists (case insensitive match)"
            ),
        ]

#Tea model
class Tea(models.Model):
    """Model representing a tea."""
    ingredients = models.CharField(max_length=200)
    shop = models.ForeignKey('Shop', on_delete=models.RESTRICT, null=True)
    # Foreign Key used because tea can only have one shop, but shops can have multiple teas.
    # Shop as a string rather than object because it hasn't been declared yet in file.

    taste = models.TextField(
        max_length=1000, help_text="Enter a brief description of the taste")
    name = models.CharField('Name', max_length=130,
                            unique=True,
                            help_text='130 Characters for the name of the tea')

    # ManyToManyField used because Type can contain many Teas. Teas can cover many types.
    # Type class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Type, help_text="Select a type for this tea")

    def __str__(self):
        """String for representing the Model object."""
        return self.ingredients

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this tea."""
        return reverse('tea-detail', args=[str(self.id)])
    
#TeaInstance model

class TeaInstance(models.Model):

    """Model representing a specific copy of a tea."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular tea")
    tea = models.ForeignKey('Tea', on_delete=models.RESTRICT, null=True)

    LOAN_STATUS = (
        ('e', 'Empty'),
        ('a', 'Available'),
        ('f', 'Favorite'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Tea availability',
    )

    class Meta:
        ordering = ['status']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.tea.ingredients})'
    
#Shop model
class Shop(models.Model):
    """Model representing an author."""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        ordering = ['location', 'name']

    def get_absolute_url(self):
        """Returns the URL to access a particular tea instance."""
        return reverse('tea-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.location}, {self.name}'
