from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Idea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content =models.CharField(max_length=255)
    impact = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    ease = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    confidence = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    @property
    def average_score(self):
        return round((self.impact+self.confidence+self.ease)/3,2) #round average to 2 decimal points

    class Meta:
        ordering:('average_score',)

    def __str__(self):
        return self.content