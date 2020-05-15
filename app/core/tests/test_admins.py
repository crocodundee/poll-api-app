from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

ADMIN_URL = reverse('admin:index')
USER_ADMIN_URL = reverse('admin:auth_user_changelist')


class UserAdminTests(TestCase):
    """Testing UserAdmin"""

    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            'testadmin', 'testadminpass'
        )
        self.client.force_login(user=self.admin)
        self.user = get_user_model().objects.create_user(
            'testuser', 'testuserpass'
        )

    def test_admin_access_to_site(self):
        """Test only staff user can view admin panel"""
        res = self.client.get(ADMIN_URL)

        self.assertEqual(res.status_code, 200)

    def test_user_admin_page(self):
        """Test is UserAdmin page is available"""
        res = self.client.get(USER_ADMIN_URL)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.username)
