from decimal import Decimal
from uuid import uuid4

from django.db import models


def generate_code():
    return uuid4().hex[:20]

class MoneyField(models.IntegerField):

    def to_python(self, value):
        try:
            return super(MoneyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
            return None

    
class BaseModel(models.Model):
    class Meta:
        abstract = True

    code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        default=generate_code,
        editable=False,
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"[{self.code}] - [{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}]"

def upload_path(instance, filename) -> str:
    code = instance.code
    now = instance.created_at.strftime("%Y_%m_%d__%H_%M_%S")
    return f"{code}_{now}_{filename}"


class File(BaseModel):
    class Source(models.TextChoices):
        NOT_DEFINED = "NOT_DEFINED", "Not Defined"
        ACCOUNT_IMAGE = "ACCOUNT_IMAGE", "Account Image"

    file = models.FileField(upload_to=upload_path)
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.NOT_DEFINED,
    )
