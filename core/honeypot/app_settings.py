from django.conf import settings


HONEYPOT_LOGIN_TRYOUT = getattr(settings, "HONEYPOT_LOGIN_TRYOUT", 3)
HONEYPOT_RATE_LIMIT = getattr(settings, "HONEYPOT_RATE_LIMIT", 10)  # hits per window
HONEYPOT_RATE_WINDOW_SECONDS = getattr(settings, "HONEYPOT_RATE_WINDOW_SECONDS", 60)
HONEYPOT_ALERT_EMAIL = getattr(settings, "HONEYPOT_ALERT_EMAIL", None)
HONEYPOT_ALERT_WEBHOOK = getattr(settings, "HONEYPOT_ALERT_WEBHOOK", None)
HONEYPOT_ALERT_THRESHOLD = getattr(settings, "HONEYPOT_ALERT_THRESHOLD", None)
