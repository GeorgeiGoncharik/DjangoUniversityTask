from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, order, timestamp):
        return (
                six.text_type(order.pk) + six.text_type(timestamp) +
                six.text_type(order.verified)
        )

order_activation_token = TokenGenerator()