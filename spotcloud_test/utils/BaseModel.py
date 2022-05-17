# Django imports
from django.db import models


class BaseModel(models.Model):
    """
    Class Base for legacy other classes
    """
    create_at = models.DateTimeField(verbose_name="Date Created",
                                     auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Date Update",
                                     auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(verbose_name='State', default=True)

    class Meta:
        """
        Sub Class Meta
        """
        abstract = True
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"
