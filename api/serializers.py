from rest_framework import serializers 
from api.models import *


class SongSerializer(serializers.ModelSerializer):

	class Meta:
		model = Song
		fields = ('id', 'name', 'duration')	


class PodCastSerializer(serializers.ModelSerializer):

	class Meta:
		model = Podcast
		fields = ('id', 'name', 'duration', 'host', 'participants')


class AudioBookSerializer(serializers.ModelSerializer):

	class Meta:
		model = Audiobook
		fields = ('id', 'title', 'author', 'narrator')


class AudioManagerSerializer(serializers.ModelSerializer):

	class Meta:
		model = AudioManager
		fields = ('id', 'audioFileType', 'audioFileMetadata', 'audio_id')
