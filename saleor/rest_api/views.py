from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from saleor.account.models import User
from saleor.product.models import Product
from django.core.paginator import Paginator
from django.http import JsonResponse
from saleor.checkout.models import Checkout

# Create your views here.

# 1. Get user details by metadata
class UserByMetadataView(APIView):
    def get(self, request, meta_key, meta_value):
        try:
            user = User.objects.get(metadata__contains={meta_key: meta_value})
            return Response({
                "id": user.id,
                "email": user.email,
                "metadata": user.metadata,
            })
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# 2. Paginated product list
class ProductListView(APIView):
    def get(self, request):
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 10))
        products = Product.objects.all()
        paginator = Paginator(products, per_page)
        page_obj = paginator.get_page(page)
        data = [
            {"id": p.id, "name": p.name, "slug": p.slug} for p in page_obj
        ]
        return Response({
            "results": data,
            "page": page,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        })

# 3. Checkout endpoint (simplified, expects POST with checkout data)
class CheckoutView(APIView):
    def post(self, request):
        # This is a placeholder. You should implement your own logic here.
        # For now, just echo the posted data.
        data = request.data
        # You would typically create a Checkout object, validate, and return order info.
        return Response({"message": "Checkout received", "data": data}, status=status.HTTP_201_CREATED)
