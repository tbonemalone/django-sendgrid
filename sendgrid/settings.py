from django.conf import settings

# This is experimental, use with caution.
SENDGRID_CREATE_EVENTS_AND_EMAILS_FOR_NEWSLETTERS = getattr(settings, "SENDGRID_CREATE_EVENTS_AND_EMAILS_FOR_NEWSLETTERS", False)