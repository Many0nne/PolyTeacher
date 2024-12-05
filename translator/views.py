from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.models import Translation
from translator.serializers import TranslationSerializer

# Create your views here.

class FrenchSpanishTranslationViewSet(APIView):

    def get(self, request):

        data = Translation.objects.filter(source_language='FR', target_language='ES')
        serializer_data = TranslationSerializer(data, many=True)

        return Response(data=serializer_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response(data={}, status=None)
    
    def put(self, request, pk):
        return Response(data={}, status=None)
    
    def delete(self, request, pk):
        return Response(data={}, status=None)
    
class FrenchEnglishTranslationViewSet(APIView):

    def get(self, request):

        data = Translation.objects.filter(source_language='EN', target_language='FR')
        serializer_data = TranslationSerializer(data, many=True)

        return Response(data=serializer_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response(data={}, status=None)
    
    def put(self, request, pk):
        return Response(data={}, status=None)
    
    def delete(self, request, pk):
        return Response(data={}, status=None)


class AllTranslationsViewSet(APIView):

    def get(self, request):

        # get the french to spanish translations and the french to english translations
        result = Translation.objects.all()
        serializer_data = TranslationSerializer(result, many=True)

        return Response(data=serializer_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response(data={}, status=None)
    
    def put(self, request, pk):
        return Response(data={}, status=None)
    
    def delete(self, request, pk):
        return Response(data={}, status=None)
    


def index(request):
    return render(request, 'index.html', context={})