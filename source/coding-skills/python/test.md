# Read code

<!-- TOC -->

- [Read code](#read-code)
    - [Property demo](#property-demo)
    - [`Sentry` code snippet](#sentry-code-snippet)
    - [`Django` auth user model](#django-auth-user-model)
    - [`Requests` code show](#requests-code-show)

<!-- /TOC -->

> 收集代码世界里的吉光片羽

## Property demo

```python
import math

class Square(object):
    """A square with two properties: a writable area and a read-only perimeter.

    To use:
    >>> sq = Square(3)
    >>> sq.area
    9
    >>> sq.perimeter
    12
    >>> sq.area = 16
    >>> sq.side
    4
    >>> sq.perimeter
    16
    """

    def __init__(self, side):
        self.side = side

    @property
    def area(self):
        """Gets or sets the area of the square."""
        return self._get_area()

    @area.setter
    def area(self, area):
        return self._set_area(area)

    def _get_area(self):
        """Indirect accessor to calculate the 'area' property."""
        return self.side ** 2

    def _set_area(self, area):
        """Indirect setter to set the 'area' property."""
        self.side = math.sqrt(area)

    @property
    def perimeter(self):
        return self.side * 4
```

## `Sentry` code snippet

```python
from __future__ import absolute_import

from datetime import datetime

from sentry.integrations.github.utils import get_jwt
from sentry.integrations.client import ApiClient


class GitHubClientMixin(ApiClient):
    allow_redirects = True

    base_url = 'https://api.github.com'

    def get_jwt(self):
        return get_jwt()

    def get_last_commits(self, repo, end_sha):
        # return api request that fetches last ~30 commits
        # see https://developer.github.com/v3/repos/commits/#list-commits-on-a-repository
        # using end_sha as parameter
        return self.get(
            u'/repos/{}/commits'.format(
                repo,
            ),
            params={'sha': end_sha},
        )

    def compare_commits(self, repo, start_sha, end_sha):
        # see https://developer.github.com/v3/repos/commits/#compare-two-commits
        # where start sha is oldest and end is most recent
        return self.get(u'/repos/{}/compare/{}...{}'.format(
            repo,
            start_sha,
            end_sha,
        ))

    def get_pr_commits(self, repo, num):
        # see https://developer.github.com/v3/pulls/#list-commits-on-a-pull-request
        # Max: 250 Commits
        return self.get(u'/repos/{}/pulls/{}/commits'.format(
            repo,
            num
        ))

    def repo_hooks(self, repo):
        return self.get(u'/repos/{}/hooks'.format(repo))

    def get_commits(self, repo):
        return self.get(u'/repos/{}/commits'.format(repo))

    def get_repo(self, repo):
        return self.get(u'/repos/{}'.format(repo))

    def get_repositories(self):
        repositories = self.get(
            '/installation/repositories',
            params={'per_page': 100},
        )
        return repositories['repositories']

    def search_repositories(self, query):
        return self.get(
            '/search/repositories',
            params={'q': query},
        )

    def get_assignees(self, repo):
        return self.get(u'/repos/{}/assignees'.format(repo))

    def get_issues(self, repo):
        return self.get(u'/repos/{}/issues'.format(repo))

    def search_issues(self, query):
        return self.get(
            '/search/issues',
            params={'q': query},
        )

    def get_issue(self, repo, number):
        return self.get(u'/repos/{}/issues/{}'.format(repo, number))

    def create_issue(self, repo, data):
        endpoint = u'/repos/{}/issues'.format(repo)
        return self.post(endpoint, data=data)

    def create_comment(self, repo, issue_id, data):
        endpoint = u'/repos/{}/issues/{}/comments'.format(repo, issue_id)
        return self.post(endpoint, data=data)

    def get_user(self, gh_username):
        return self.get(u'/users/{}'.format(gh_username))

    def request(self, method, path, headers=None, data=None, params=None):
        if headers is None:
            headers = {
                'Authorization': 'token %s' % self.get_token(),
                # TODO(jess): remove this whenever it's out of preview
                'Accept': 'application/vnd.github.machine-man-preview+json',
            }
        return self._request(method, path, headers=headers, data=data, params=params)

    def get_token(self):
        """
        Get token retrieves the active access token from the integration model.
        Should the token have expried, a new token will be generated and
        automatically presisted into the integration.
        """
        token = self.integration.metadata.get('access_token')
        expires_at = self.integration.metadata.get('expires_at')

        if expires_at is not None:
            expires_at = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S')

        if not token or expires_at < datetime.utcnow():
            res = self.create_token()
            token = res['token']
            expires_at = datetime.strptime(
                res['expires_at'],
                '%Y-%m-%dT%H:%M:%SZ',
            )

            self.integration.metadata.update({
                'access_token': token,
                'expires_at': expires_at.isoformat(),
            })
            self.integration.save()

        return token

    def create_token(self):
        return self.post(
            u'/installations/{}/access_tokens'.format(
                self.integration.external_id,
            ),
            headers={
                'Authorization': 'Bearer %s' % self.get_jwt(),
                # TODO(jess): remove this whenever it's out of preview
                'Accept': 'application/vnd.github.machine-man-preview+json',
            },
        )


class GitHubAppsClient(GitHubClientMixin):

    def __init__(self, integration):
        self.integration = integration
        super(GitHubAppsClient, self).__init__()

```

## `Django` auth user model

> **胖 model 瘦 control**

```python
class UserManager(models.Manager):

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def create_user(self, username, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        u = self.create_user(username, email, password)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        """
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(username=username)



class User(models.Model):
    """
    Users within the Django authentication system are represented by this
    model.
    Username and password are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True)
    password = models.CharField(_('password'), max_length=128)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'),
        blank=True, help_text=_('The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'his/her group.'))
    user_permissions = models.ManyToManyField(Permission,
        verbose_name=_('user permissions'), blank=True,
        help_text='Specific permissions for this user.')
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def natural_key(self):
        return (self.username,)

    def get_absolute_url(self):
        return "/users/%s/" % urllib.quote(smart_str(self.username))

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = u'%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through his/her
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                if obj is not None:
                    permissions.update(backend.get_group_permissions(self,
                                                                     obj))
                else:
                    permissions.update(backend.get_group_permissions(self))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache
```

## `Requests` code show

```python
from .compat import OrderedDict, Mapping, MutableMapping


class CaseInsensitiveDict(MutableMapping):
    """A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive::

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.
    """

    def __init__(self, data=None, **kwargs):
        self._store = OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return str(dict(self.items()))
```
