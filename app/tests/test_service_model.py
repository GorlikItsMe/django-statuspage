from datetime import timedelta
from django.utils import timezone
from django.test.testcases import TestCase
from app.models import Service


class TestServiceModel(TestCase):

    def test_service_str(self):
        s = Service.objects.create(
            name='Moja strona',
        )
        s: Service
        s.save()
        self.assertEqual(s.__str__(), "Service (Moja strona)")

    def test_service_auto_offline(self):
        s = Service.objects.create(name='Moja strona', status=True)
        s: Service
        s.last_check_time = timezone.now() - timedelta(days=1)
        self.assertEqual(s.status, True)
        s.save()

        serv: Service = Service.objects.all().first()
        self.assertEqual(serv.status, False)

    def test_service_status_check_for_http(self):
        s1 = Service.objects.create(name='Wrong website', url='https://wrongdomain.gorlik.pl')
        s1: Service
        self.assertEqual(s1.check_service(), False)
        self.assertEqual(s1.status, False)

        s2 = Service.objects.create(name='Wrong website', url='https://google.com')
        s2: Service
        self.assertEqual(s2.check_service(), True)
        self.assertEqual(s2.status, True)

        se = Service.objects.create(name='Unknown check method', check_method="blabla")
        se: Service
        with self.assertRaisesMessage(Exception, "Unknown check_method"):
            se.check_service()
