import logging

from django.conf import settings
from django.core import mail
from django.core.mail.message import EmailMessage

# django-sendgrid imports
from signals import sendgrid_email_sent


SENDGRID_EMAIL_BACKEND = getattr(settings, "SENDGRID_EMAIL_BACKEND", "sendgrid.backends.SendGridEmailBackend")

logger = logging.getLogger(__name__)


class SendGridEmailMessage(EmailMessage):
	"""
	Adapts Django's ``EmailMessage`` for use with SendGrid.
	"""
	sendgrid_headers = None
	
	def __init__(self, *args, **kwargs):
		super(SendGridEmailMessage, self).__init__(*args, **kwargs)
		
	def _get_sendgrid_connection(self, backend=None):
		"""docstring for _get_sendgrid_connection"""
		logger.debug("Getting SendGrid connection")
		
		if not backend:
			backend = SENDGRID_EMAIL_BACKEND
			
		connection = mail.get_connection(backend)
		return connection
		
	def send(self, *args, **kwargs):
		"""Sends the email message."""
		connection = self._get_sendgrid_connection()
		self.connection = connection
		logger.debug("Connection: {c}".format(c=connection))
		
		response = super(SendGridEmailMessage, self).send(*args, **kwargs)
		logger.debug("Tried to send an email with SendGrid and got response {r}".format(r=response))
		sendgrid_email_sent.send(sender=self, response=response)
		# sendgrid_email_sent.send(sender=SendGridEmailMessage, instance=self, response=response)
		
		return response
