from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getData(request):
    activitie = {'atividade':'atividade1', 'servico':'servico1'}
    return Response(activitie)