import logging

from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.code_submit.utils import decode_jwt

logger = logging.getLogger(__name__)

class TestAPI(APIView):
    '''Test API to test the JWT token payload.'''
    def get(self, request, format=None):
        payload = decode_jwt(request=request)
        logging.info(f'\npayload is: {payload}') # dict 
        return Response({"ok"})
