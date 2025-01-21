from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.base.models import RegistroAtividade
from .serializers import RegistroAtividadeSerializer

@api_view(['GET'])
def getData(request):
    atividade_object = RegistroAtividade.objects.all()
    serializer = RegistroAtividadeSerializer(atividade_object, many=True)
    return Response(serializer.data)