from django.test.client import Client
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.urls.resolvers import RegexPattern, URLPattern, URLResolver
from djstatuspage.urls import urlpatterns


class TestRenderSomePages(TestCase):
    print_to_console = False
    blacklist = [
        "/admin/",
        ":pk>",
        "<uuid:",
        "<path:",
        "<int:",
        "<str:",
    ]

    def setUp(self):
        self.client = Client()
        User.objects.create_superuser('admin', 'admin@mail.com', 'secret_password')
        self.client.login(username='admin', password='secret_password')

    def should_i_skip(self, url):
        for blackword in self.blacklist:
            if blackword in url:
                return True
        return False

    def check_url_resolver(self, url_patterns, base_route):
        for url_p in url_patterns:
            if type(url_p) == URLResolver:
                url = f"{base_route}{url_p.pattern._route}"
                self.check_url_resolver(
                    url_patterns=url_p.url_patterns,
                    base_route=url
                )
                continue
            elif type(url_p) == URLPattern:
                if type(url_p.pattern) == RegexPattern:
                    # RegexPattern not supported
                    continue
                url = f"{base_route}{url_p.pattern._route}"
                if self.should_i_skip(url):
                    continue

                if self.print_to_console:
                    print(f'url:{url}', end="\tstatus_code:")
                self.client.login(username='admin', password='secret_password')
                r = self.client.get(url)
                if self.print_to_console:
                    print(r.status_code)
                if r.status_code == 500 or r.status_code == 405:
                    print(f"ERROR url: {url}")
                self.assertNotEqual(r.status_code, 500)
                self.assertNotEqual(r.status_code, 405)
            else:
                # RegexPattern not supported
                pass

    def test_render_pages(self):
        if self.print_to_console:
            print("Find broken pages")
        self.check_url_resolver(
            url_patterns=urlpatterns,
            base_route="/"
        )
