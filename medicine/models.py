from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# 话题
@python_2_unicode_compatible  # 兼容python2
class Subject(models.Model):
    name = models.CharField(max_length=70, blank=True)
    content = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    TYPE_CHOICES = (
        ("01", '中医'),
        ("02", '西医'),
    )

    type = models.CharField(max_length=70, blank=True, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_time']
