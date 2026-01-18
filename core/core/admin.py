from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from honeypot.models import LoginAttempt, BlackList, HoneyPotHit


class HoneyPotAdminSite(admin.AdminSite):
    site_header = "Django HoneyPot Administration"
    site_title = "HoneyPot Admin"
    index_title = "Welcome to Django HoneyPot Admin"
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Add statistics to context
        extra_context['user_count'] = User.objects.count()
        extra_context['honeypot_hits'] = HoneyPotHit.objects.count()
        extra_context['login_attempts'] = LoginAttempt.objects.count()
        extra_context['blocked_ips'] = BlackList.objects.count()
        
        return super().index(request, extra_context)


# Create custom admin site instance
admin_site = HoneyPotAdminSite(name='admin')

# Register User and Group with custom admin
admin_site.register(User, BaseUserAdmin)
admin_site.register(Group, BaseGroupAdmin)
