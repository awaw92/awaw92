from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Email

# --- Rejestracja modelu User ---
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Pola, które będą widoczne w liście użytkowników
    list_display = ('id', 'email', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()  # brak relacji ManyToMany do filtrowania
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

# --- Rejestracja modelu Email ---
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'subject', 'timestamp', 'read', 'archived', 'display_recipients')
    list_filter = ('read', 'archived', 'timestamp')
    search_fields = ('sender__email', 'recipients__email', 'subject', 'body')
    filter_horizontal = ('recipients',)  # pozwala wybierać odbiorców w formularzu edycji

    def display_recipients(self, obj):
        """
        Zwraca listę odbiorców jako string, żeby pokazać w liście maili.
        """
        return ", ".join([user.email for user in obj.recipients.all()])

    display_recipients.short_description = 'Recipients'
