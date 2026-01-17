from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta

from .models import BlackList, HoneyPotHit
from .app_settings import (
    HONEYPOT_RATE_LIMIT,
    HONEYPOT_RATE_WINDOW_SECONDS,
    HONEYPOT_LOGIN_TRYOUT,
)
from .utils import dispatch_alert

class HoneyPotMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, "session"), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        
        client_ip = self.get_client_ip(request)
        if BlackList.objects.filter(ip_address=client_ip).exists():
            return HttpResponseForbidden("You are not allowed to call the website anymore. YOU ARE BANNED!")
        
        # Only rate-limit /admin/ honeypot endpoint
        if request.path.startswith("/admin"):
            resp = self.apply_rate_limit(client_ip, request)
            if resp:
                return resp
            HoneyPotHit.objects.create(
                ip_address=client_ip,
                user_agent=request.META.get("HTTP_USER_AGENT"),
                path=request.path,
                session_key=getattr(request, "session", None) and request.session.session_key,
            )
    def get_client_ip(self, request):
        """Prefer X-Forwarded-For (client IP behind proxy) else REMOTE_ADDR."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # X-Forwarded-For can be a comma-separated list; first is the client
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def apply_rate_limit(self, ip, request):
        if not ip:
            return
        key = f"honeypot:rate:{ip}"
        current = cache.get(key, 0) + 1
        cache.set(key, current, timeout=HONEYPOT_RATE_WINDOW_SECONDS)
        if current > HONEYPOT_RATE_LIMIT:
            # lockout and alert
            BlackList.objects.get_or_create(ip_address=ip)
            dispatch_alert(ip=ip, reason="Honeypot rate limit exceeded")
            return HttpResponseForbidden("Too many attempts. You are blocked.")

        