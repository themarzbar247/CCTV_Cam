import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Notification(models.Model):
    # Fields
    notificationId = models.models.CharField(max_length=20, help_text='A unique alert notification ID', primary_key=True)
    alertId = models.ForeignKey("Alert", on_delete=models.RESTRICT, help_text='foreign key for the alert table')
    typeId = models.ForeignKey("Type", on_delete=models.RESTRICT, help_text='foreign key for the type table')
    confidence = models.IntegerField(help_text='Confidence score given to the alert that fired', default=0)
    firedDateTime = models.DateTimeField(auto_now=False, auto_now_add=False, help_text='Date Time that the alert was triggered')
    sentDateTime = models.DateTimeField(auto_now=True, auto_now_add=False, help_text='Date Time that the alert was sent')
    description = models.CharField(max_length=20, help_text='description of the alert with metadata around triggered features')
    alertContentLocation = models.CharField(max_length=20, help_text='a path to the content that trggered the alert for review')

    # Metadata
    class Meta:
        ordering = ['confidence','-firedDateTime']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.alertId} ({self.Alert.alertId})'

class Type(models.Model):
    # Fields
    typeId = models.IntegerField(help_text='ID for type')
    typeName = models.CharField(max_length=20, help_text="Type Name")

    # Metadata
    class Meta:
        ordering = ['typeId']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.typeName

class Alert(models.Model):
    # Fields
    alertId = models.IntegerField()
    alertName = models.CharField()
    alertDescription = models.CharField()
    typeId = models.IntegerField()
    # Metadata
    class Meta:
        ordering = ['alertId']

    # Methods
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.alertName