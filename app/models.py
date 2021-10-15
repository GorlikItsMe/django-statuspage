from datetime import timedelta
from django.utils import timezone
from django.db import models
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

    def __str__(self) -> str:
        return f"Service ({self.name})"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if check is too old auto change to offline
        if all((
            self.next_check + timedelta(minutes=1) < timezone.now(),  # last check +1min is older than now
            self.status == True
        )):
            self.status = False
            self.save()



    def check_service(self) -> bool:
        """checking service function"""
        
        if self.check_method == CheckMethod.HTTP:
            c = check_http(self.url, self.timeout)
            print(c)
            self.status = c.is_online
            self.save()
        return True
