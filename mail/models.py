from django.contrib.auth.models import AbstractUser
from django.db import models

# Rozszerzony model użytkownika
class User(AbstractUser):
    # Możesz dodać inne pola, jeśli chcesz w przyszłości rozszerzyć model User
    pass

# Model Email
class Email(models.Model):
    # Odwołanie do użytkownika (odbiorca)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    recipients = models.ManyToManyField("User", related_name="emails_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)  # Możesz to zmienić na null=True, jeśli wolisz NULL w bazie
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def serialize(self):
        """
        Funkcja do serializacji emaila, aby wysłać go jako JSON.
        """
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "archived": self.archived
        }
    
    def __str__(self):
        # Wydrukowanie wiadomości, lista odbiorców oddzielona przecinkami
        recipient_emails = ', '.join([user.email for user in self.recipients.all()])
        return f"Email from {self.sender.email} to {recipient_emails} - {self.subject}"
