from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserSerializer, ItemSerializer
from rest_framework.authtoken.models import Token
from .models import Item
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import requests

class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_item(request):
    user = request.user.id
    try:
        items = Item.objects.filter(user=user).values('name')
        serializer = ItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_content(request):
    user = request.user.id
    try:

        item = Item.objects.filter(user=user).values_list('name')
        user_subscribed_item = [i for sublist in item for i in sublist]

        all_items = {'mobile':['mobiles','Mobile','smartphones'],'tv':['led-tv','televisions','led-tvs'],'drone':['drones-and-accessories','Drones-Gimbles','drones']}
        display_items = {item: value for (item, value) in all_items.items() if item in user_subscribed_item}


        proudct = []
        data = {}

        for key, value in display_items.items():
            source = requests.get('https://www.okdam.com/category/' + value[0]).text
            source2 = requests.get('https://smartdoko.com/products/' + value[1]).text
            source3 = requests.get('https://thulo.com/' + value[2]).text

            soup = BeautifulSoup(source, 'lxml')
            soup2 = BeautifulSoup(source2, 'lxml')
            soup3 = BeautifulSoup(source3, 'lxml')

            for item in soup.findAll("div", {"class": "product-box"}):
                name = item.div.div.text
                price = item.div.p.span.text
                image = item.img['data-src']
                data = {
                    "name": name,
                    "price": price,
                    "image": image
                }
                proudct.append(data)

            for item in soup2.findAll("div", {"class": "single-products"}):
                name = item.div.a.img['alt']
                price = item.div.h2.text
                image = item.div.a.img['src']
                data = {
                    "name": name,
                    "price": price,
                    "image": image
                }
                proudct.append(data)

            for item in soup3.findAll("div", {"class": "ty-column4"}):
                name = item.find('div', {'class':'ty-grid-list__item-name'})
                price = item.find('span', {'class':'ty-price'}).text
                price = price.split(' ')[1]
                name = name.a.text
                image = item.div.form.div.a.img['src']
                data = {
                    "name": name,
                    "price": price,
                    "image": image
                }
                proudct.append(data)
        return JsonResponse(proudct, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
