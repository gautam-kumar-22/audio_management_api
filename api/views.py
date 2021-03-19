from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
import json
# Create your views here.


class AudioManagerViewSet(viewsets.ModelViewSet):
    queryset = AudioManager.objects.all().order_by('-uploaded_time')
    serializer_class = AudioManagerSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            if "audioFileType" in self.request.data:
                serializer_list = {'song': SongSerializer, 'podcast': PodCastSerializer, 'audiobook': AudioBookSerializer}
                serializer_class = serializer_list[self.request.data["audioFileType"]]
                return serializer_class
        print(self.request.data)
        if self.request.method == "GET":
            serializer_class = AudioManagerSerializer
        return AudioManagerSerializer

    def create(self, request, *args, **kwargs):
        if self.request.method != 'GET':
            serializer = self.get_serializer(data=json.loads(request.data["audioFileMetadata"]))
        else:
            serializer = self.get_serializer()
        if serializer.is_valid():
            audio_id = serializer.save().id
            manager_data = request.data
            audio_type = manager_data["audioFileType"]
            audio_meta_data = manager_data["audioFileMetadata"]
            tmp = {"audioFileType": audio_type, "audioFileMetadata": audio_meta_data, "audio_id": audio_id}
            manager_serializer = AudioManagerSerializer(data = tmp)
            if manager_serializer.is_valid():
                manager_serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Successfully created',
                'data': manager_serializer.data,
                'status': 'HTTP_201_CREATED',
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'message': 'Can not create',
                'data': serializer.errors,
                'status': 'HT',
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        print("UPDATE++++++++++++++++++++", self.request.method)
        if self.request.method == "PUT":
            serializer = self.get_serializer(data=json.loads(request.data["audioFileMetadata"]))
            if serializer.is_valid():
                # self.perform_update(serializer)
                audio_id = request.data["audio_id"]
                model_set = {"song": Song, "podcast": Podcast, "audiobook": Audiobook}
                valid_model = model_set[request.data["audioFileType"]]
                if request.data["audioFileType"] == "song":
                    tmp_data = json.loads(request.data["audioFileMetadata"])
                    valid_model.objects.filter(pk=audio_id).update(name=tmp_data["name"], duration=tmp_data["duration"])
                if request.data["audioFileType"] == "podcast":
                    tmp_data = json.loads(request.data["audioFileMetadata"])
                    valid_model.objects.filter(pk=audio_id).update(name=tmp_data["name"], duration=tmp_data["duration"], host=tmp_data["host"], participants=tmp_data["participants"])
                if request.data["audioFileType"] == "audiobook":
                    tmp_data = json.loads(request.data["audioFileMetadata"])
                    valid_model.objects.filter(pk=audio_id).update(title=tmp_data["title"], author=tmp_data["author"], narrator=tmp_data["narrator"], duration=tmp_data["duration"])
                manager_serializer = AudioManagerSerializer(data=request.data)
                if manager_serializer.is_valid():
                    AudioManager.objects.filter(pk=self.get_object().id).update(audioFileType=request.data["audioFileType"], audioFileMetadata=request.data["audioFileMetadata"])
                headers = self.get_success_headers(serializer.data)
                return Response({
                    'message': 'Successfully updated',
                    'data': manager_serializer.data,
                    'status': 'HTTP_201_CREATED',
                }, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({
                    'message': 'Can not create',
                    'data': serializer.errors,
                    'status': 'HT',
                }, status=status.HTTP_400_BAD_REQUEST)
