from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

class Register(APIView):
    def get(self, request):
        return Response({'success':'ok'},status=status.HTTP_200_OK)