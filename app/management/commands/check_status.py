from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import Service
from time import sleep
import threading


class CheckingThead(threading.Thread):
    def __init__(self, service: Service):
        threading.Thread.__init__(self)
        self.name = f"{service.name}_{service.next_check}"
        self.service = service

    def run(self):
        self.service.check_service()


class Command(BaseCommand):
    help = 'Checking service status'
    thread_list = []

    def info(self, text):
        dt = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        self.stdout.write(self.style.NOTICE(f"[{dt}] [ INFO ] {text}"))

    def success(self, text):
        dt = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        self.stdout.write(self.style.SUCCESS(f"[{dt}] [SUCCESS] {text}"))

    def waring(self, text):
        dt = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        self.stdout.write(self.style.WARNING(f"[{dt}] [WARNING] {text}"))

    def error(self, text):
        dt = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        self.stdout.write(self.style.ERROR(f"[{dt}] [ ERROR ] {text}"))

    def handle(self, *args, **options):
        try:
            self.main()
        except KeyboardInterrupt:
            self.waring("Detected KeyboardInterrupt, closing...")
            for t in self.thread_list:
                self.info(f"Wait to close thread: {t.name} \tActive threads: {len(self.thread_list)}")
                t.join()
            self.info("Done")

    def main(self):
        self.success("Started service checker")

        while True:
            next_service = Service.objects.all().order_by('next_check').first()
            if next_service is None:
                self.error("Service table is empty. Waiting 30sek maybe you will add Service to check")
                sleep(30)
                continue
            next_check_delta = next_service.next_check - timezone.now()
            # check delta is positive (if negative that means we must check now)
            if next_check_delta.total_seconds() >= 1:
                self.info(f"Next check in {next_check_delta.seconds} sec")

                # minimum sleep is 30sec
                if next_check_delta.seconds > 30:
                    sleep(30)
                else:
                    sleep(next_check_delta.microseconds / 1000000 + 0.1)
            else:
                # if delta is near 0 wait 1 sec
                sleep(next_check_delta.microseconds / 1000000 + 0.1)

            service_list = Service.objects.filter(next_check__lte=timezone.now())

            for s in service_list:
                t = CheckingThead(s)
                self.thread_list.append(t)
                t.start()
                s.next_check = timezone.now() + timedelta(seconds=s.interval)
                s.save()

            for t in self.thread_list:
                t: CheckingThead
                if not t.isAlive():
                    self.thread_list.remove(t)
                    t.join()
                    self.success(f"Thread {t.name} closed")

            self.info(f"Beep Im Alive! Current active threads: {len(self.thread_list)}")
