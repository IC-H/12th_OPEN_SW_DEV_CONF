from django.conf import settings
from common.models import User
from django.utils.crypto import constant_time_compare
from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured
from django.middleware.csrf import rotate_token
from .signals import user_logged_in, user_logged_out, user_login_failed

SESSION_KEY = '_auth_email_id'
BACKEND_SESSION_KEY = '_auth_email_backend'
HASH_SESSION_KEY = '_auth_email_hash'


def _get_user_session_key(request):
    return User._meta.pk.to_python(request.session[SESSION_KEY])


def load_backend(path):
    return import_string(path)()


def _get_backends(return_tuples=False):
    backends = []
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No authentication backends have been defined. Does '
            'AUTHENTICATION_BACKENDS contain anything?'
        )
    return backends


class Auth:

    @staticmethod
    def authenticate(request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(User.EMAIL_FIELD)
        try:
            user = User.objects.filter(email__exact=email).get()
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            return None
        else:
            if user.check_password(password):
                return user

    @staticmethod
    def login(request, user, backend=None):
        """
        Persist a user id and a backend in the request. This way a user doesn't
        have to reauthenticate on every request. Note that data set during
        the anonymous session is retained when the user logs in.
        """
        session_auth_hash = ''
        if user is None:
            user = request.user
        if hasattr(user, 'get_session_auth_hash'):
            session_auth_hash = user.get_session_auth_hash()

        if SESSION_KEY in request.session:
            if _get_user_session_key(request) != user.pk or (
                    session_auth_hash and
                    not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
                # To avoid reusing another user's session, create a new, empty
                # session if the existing session corresponds to a different
                # authenticated user.
                request.session.flush()
        else:
            request.session.cycle_key()

        try:
            backend = backend or user.backend
        except AttributeError:
            backends = _get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, backend_path = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument or set the '
                    '`backend` attribute on the user.'
                )
        else:
            if not isinstance(backend_path, str):
                raise TypeError('backend must be a dotted import path string (got %r).' % backend_path)

        request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
        request.session[BACKEND_SESSION_KEY] = backend_path
        request.session[HASH_SESSION_KEY] = session_auth_hash
        if hasattr(request, 'user'):
            request.user = user
        rotate_token(request)
        user_logged_in.send(sender=user.__class__, request=request, user=user)

    @staticmethod
    def get_user(request):
        try:
            user = User.objects.filter(pk__exact = _get_user_session_key(request)).get()
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Please Log In')
            return redirect(reverse_lazy('sign_in'))
        return user