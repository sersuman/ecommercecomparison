from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserSerializer,ItemSerializer
from rest_framework.authtoken.models import Token
from .models import Item
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_item(request):
    payload = request.data
    user = request.user
    try:

        item = Item.objects.create(
            name=payload["name"],
            user=user
        )
        serializer = ItemSerializer(item)
        return JsonResponse({'item': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
# @permission_classes([IsAuthenticated])
def get_item(request):
    user = request.user.id
    items = Item.objects.filter(user=user)
    serializer = ItemSerializer(items, many=True)
    return JsonResponse({'items': serializer.data}, safe=False, status=status.HTTP_200_OK)

