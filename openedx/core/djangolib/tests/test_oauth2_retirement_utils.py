import datetime
from uuid import uuid4

from django.test import TestCase
from openedx.core.djangoapps.oauth_dispatch.tests import factories
from student.tests.factories import UserFactory
from oauth2_provider.models import AccessToken, Application, RefreshToken, Grant

from ..data_retirement_utils import (
    delete_from_oauth2_provider_accesstoken,
    delete_from_oauth2_provider_application,
    delete_from_oauth2_provider_grant,
    delete_from_oauth2_provider_refreshtoken,
)

class TestRetireUserFromOauth2Application(TestCase):

    def setUp(self):
        super(TestRetireUserFromOauth2Application, self).setUp()
        self.user = UserFactory.create()

    def test_delete_from_oauth2_application(self):
        factories.ApplicationFactory(user=self.user)
        delete_from_oauth2_provider_application(self.user)
        applications = Application.objects.filter(user_id=self.user.id)
        self.assertFalse(applications.exists())

class TestRetireUserFromOauth2AccessToken(TestCase):

    def setUp(self):
        super(TestRetireUserFromOauth2AccessToken, self).setUp()
        self.user = UserFactory.create()
        self.app = factories.ApplicationFactory(user=self.user)

    def test_delete_from_oauth2_accesstoken(self):
        factories.AccessTokenFactory(
            user=self.user,
            application=self.app
        )
        delete_from_oauth2_provider_accesstoken(self.user)
        access_tokens = AccessToken.objects.filter(user_id=self.user.id)
        self.assertFalse(access_tokens.exists())

class TestRetireUserFromOauth2RefreshToken(TestCase):

    def setUp(self):
        super(TestRetireUserFromOauth2RefreshToken, self).setUp()
        self.user = UserFactory.create()
        self.app = factories.ApplicationFactory(user=self.user)

    def test_delete_from_oauth2_accesstoken(self):
        access_token = factories.AccessTokenFactory(
            user=self.user,
            application=self.app,
        )
        factories.RefreshTokenFactory(
            user=self.user,
            application=self.app,
            access_token=access_token,
        )
        delete_from_oauth2_provider_refreshtoken(self.user)
        refresh_tokens = RefreshToken.objects.filter(user_id=self.user.id)
        self.assertFalse(refresh_tokens.exists())


class TestRetireUserFromOauth2Grant(TestCase):

    def setUp(self):
        super(TestRetireUserFromOauth2Grant, self).setUp()
        self.user = UserFactory.create()
        self.app = factories.ApplicationFactory(user=self.user)

    def test_delete_from_oauth2_accesstoken(self):
        Grant.objects.create(
            user=self.user,
            application=self.app,
            expires=datetime.datetime(2018, 1, 1),
        )
        delete_from_oauth2_provider_grant(self.user)
        grants = Grant.objects.filter(
            user=self.user,
        )
        self.assertFalse(grants.exists())
