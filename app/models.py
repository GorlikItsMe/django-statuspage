from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save, post_init
from .check_service import check_http


class CheckMethod:
    HTTP = 'HTTP'

    CHOICES = (
        (HTTP, 'HTTP'),
    )


class Service(models.Model):
    name = models.CharField(
        verbose_name="Name",
        max_length=120
    )
    desc = models.TextField(
        verbose_name="Description",
        null=True,
        blank=True
    )
    link = models.URLField(
        verbose_name="Link",
        help_text="Link to your service / app (used to create link on status page)",
        null=True,
        blank=True
    )
    interval = models.IntegerField(
        verbose_name="Interval (in seconds)",
        default=30,
    )
    timeout = models.IntegerField(
        verbose_name="Timeout (in seconds)",
        default=30
    )
    pos = models.IntegerField(
        verbose_name="Positon on statuspage",
        default=0
    )

    check_method = models.CharField(
        choices=CheckMethod.CHOICES,
        default=CheckMethod.HTTP,
        max_length=10,
        verbose_name="Check service method"
    )
    url = models.URLField(
        verbose_name="Url",
        help_text="Url to checking your service",
        null=True,
        blank=True
    )

    status = models.BooleanField(verbose_name="Service Status", default=False)

    # used by checking system
    next_check = models.DateTimeField(default=timezone.now)
    last_check_time = models.DateTimeField(default=timezone.now)

    @property
    def status_html(self):
        if self.status:
            return "green"
        return "red"

    def __str__(self) -> str:
        return f"Service ({self.name})"

    @staticmethod
    def check_is_online_too_long(sender, **kwargs):
        """Checking is service too long online and correct it (make it offline)"""
        instance: Service = kwargs.get('instance')
        if instance.id is None:
            instance.is_new = True
            return
        instance.is_new = False

        # if check is too old auto change to offline
        if all((
            # if last check + interval is older than now
            instance.last_check_time + timedelta(seconds=instance.interval * 3) < timezone.now(),
            instance.status is True
        )):
            instance.status = False
            instance.save()
            last_servicecheck = ServiceCheck.objects.filter(service=instance).order_by('datetime').last()
            if last_servicecheck:
                first_missing_dt = last_servicecheck.datetime + timedelta(seconds=instance.interval)
            else:
                # if last ServiceCheck is missing use now date
                first_missing_dt = timezone.now()
            ServiceCheck.objects.create(
                service=instance,
                latency=0,
                online=False,
                datetime=first_missing_dt
            )

    def check_service(self) -> bool:
        """Checking service function"""
        self.last_check_time = timezone.now()

        if self.check_method == CheckMethod.HTTP:
            c = check_http(self.url, self.timeout)
            self.status = c.is_online
            # self.last_check_time = timezone.now()
            self.save()
            ServiceCheck.objects.create(
                service=self,
                latency=c.time_ms,
                online=c.is_online,
            )
            return c.is_online

        raise Exception("Unknown check_method")


class ServiceCheck(models.Model):
    """Used to store information about checks history"""
    id = models.BigAutoField(primary_key=True)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='servicechecks',
        related_query_name='servicecheck',
        db_index=True,
    )
    latency = models.IntegerField(default=0)
    online = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)  # created_at

    def __str__(self) -> str:
        online_str = "Online" if self.online else "Offline"
        return f"{self.pk}. [{self.datetime}] ({self.service}) {self.latency}ms {online_str}"


post_init.connect(Service.check_is_online_too_long, sender=Service)
