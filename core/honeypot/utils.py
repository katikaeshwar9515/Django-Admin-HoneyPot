import json
import logging
import urllib.request
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .app_settings import HONEYPOT_ALERT_EMAIL, HONEYPOT_ALERT_WEBHOOK

logger = logging.getLogger(__name__)


def dispatch_alert(ip: str, reason: str = "Honeypot activity"):
    """Send alerts via email and/or webhook. Best-effort, non-blocking failures logged."""
    subject = "Honeypot alert"
    body = f"Time: {timezone.now()}\nIP: {ip}\nReason: {reason}"

    if HONEYPOT_ALERT_EMAIL:
        try:
            send_mail(subject, body, getattr(settings, "DEFAULT_FROM_EMAIL", "alerts@example.com"), [HONEYPOT_ALERT_EMAIL])
        except Exception as exc:  # pragma: no cover - notification best-effort
            logger.warning("Honeypot email alert failed: %s", exc)

    if HONEYPOT_ALERT_WEBHOOK:
        try:
            data = json.dumps({"ip": ip, "reason": reason, "timestamp": timezone.now().isoformat()}).encode()
            req = urllib.request.Request(HONEYPOT_ALERT_WEBHOOK, data=data, headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5)
        except Exception as exc:  # pragma: no cover
            logger.warning("Honeypot webhook alert failed: %s", exc)
