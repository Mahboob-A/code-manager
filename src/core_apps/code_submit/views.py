from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.code_submit.utils import decode_jwt


class TestAPI(APIView):
    def get(self, request, format=None):
        example_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.VT7kThFVMrwsZrMkshgynU9wVpcdWMc0ksqc2xjgRHo"
        payload = decode_jwt(example_token)
        print("payload: ", payload)
        return Response({"ok"})
