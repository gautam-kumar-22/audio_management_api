from django.db import models
from django.core.validators import MinValueValidator
import json


# Create your models here.
class TimeStampedModel(models.Model):
    """TimeStampedModel.
    An abstract base class model that provides self-managed "created" and
    "updated" fields.
    """
    uploaded_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        get_latest_by = 'modified_time'
        ordering = ('-modified_time', '-uploaded_time',)
        abstract = True


class Song(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, null=False)

    def set_foo(self, x):
        self.foo = json.dumps(x)

    def get_foo(self):
        return json.loads(self.foo)

class Podcast(TimeStampedModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, null=False)
    host = models.CharField(max_length=100, blank=False, null=False)
    participants = models.CharField(max_length=1024, blank=True, null=True)

    def set_foo(self, x):
        self.foo = json.dumps(x)

    def get_foo(self):
        return json.loads(self.foo)

class Audiobook(TimeStampedModel):
    title = models.CharField(max_length=100, blank=False, null=False)
    author = models.CharField(max_length=100, blank=False, null=False)
    narrator = models.CharField(max_length=100, blank=False, null=False)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, null=False)

    def set_foo(self, x):
        self.foo = json.dumps(x)

    def get_foo(self):
        return json.loads(self.foo)


AUDIO_TYPE = (
	('song', 'Song'),
	('podcast', 'Podcast'),
	('audiobook', 'AudioBook')
)


class AudioManager(TimeStampedModel):
	audioFileType = models.CharField(max_length = 20, choices = AUDIO_TYPE, default = 'song', blank=False, null=False) 
	audioFileMetadata = models.TextField(blank=False, null=False)
	audio_id = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, null=False, default=0)
