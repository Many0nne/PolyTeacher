from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.models import Translation
from translator.serializers import TranslationSerializer
from drf_yasg.utils import swagger_auto_schema
import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = ""
api_key = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

class AllTranslationsViewSet(APIView):

    @swagger_auto_schema(responses={200: TranslationSerializer(many=True)})
    def get(self, request):

        result = Translation.objects.all()
        serializer_data = TranslationSerializer(result, many=True)

        return Response(data=serializer_data.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(responses={201: TranslationSerializer})
    def post(self, request):

        # définir les champs obligatoires et les valeurs par défaut
        source_language = "FR"
        source_text = "test de la fonction de traduction"
        target_language = "ES"

        # vérifier si les champs obligatoires sont présents
        if not source_language or not target_language or not source_text:
            return Response({"detail": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # vérifier si la traduction existe déjà
        if Translation.objects.filter(source_language=source_language, source_text=source_text, target_language=target_language).exists():
            return Response({"detail": "Translation already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Envoi de la requête à l'API Gemini
        prompt = f'Traduis "{source_text}" de {source_language} en {target_language}. La réponse ne doit contenir que la traduction.'
        response = model.generate_content(prompt)

        # vérifier si la réponse est vide ou non présente
        if not response or not response.text:
            return Response({"detail": "Error from Gemini API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        target_text = response.text.strip()

        # enregistrer la traduction dans la base de données
        translation = Translation.objects.create(
            source_language=source_language,
            source_text=source_text,
            target_language=target_language,
            target_text=target_text
        )
        serializer_data = TranslationSerializer(translation)

        return Response(data=serializer_data.data, status=status.HTTP_201_CREATED)
        


def index(request):
    return render(request, 'index.html', context={})