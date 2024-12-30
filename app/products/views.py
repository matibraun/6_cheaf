import requests

from alerts.selectors import get_alert_status
from alerts.serializers import AlertSerializer
from alerts.services import create_alert
from datetime import date, timedelta
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from datetime import datetime
from rest_framework.exceptions import ValidationError


class ProductsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():

            product = serializer.save(user=request.user)
            
            create_alert(product_id=product.id, days_before_expiration_to_trigger=5)
            create_alert(product_id=product.id, days_before_expiration_to_trigger=10)

            return Response({
                'message': 'Product created successfully!',
                'product': ProductSerializer(product).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):

        if pk:

            try:

                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except Product.DoesNotExist:

                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        else:

            filters = Q()
            name = request.query_params.get('name', None)
            description = request.query_params.get('description', None)
            min_stock = request.query_params.get('min_stock', None)
            max_stock = request.query_params.get('max_stock', None)

            if name:
                filters &= Q(name__icontains=name)
            if description:
                filters &= Q(description__icontains=description)
            if min_stock:
                filters &= Q(stock_quantity__gte=min_stock)
            if max_stock:
                filters &= Q(stock_quantity__lte=max_stock)

            products = Product.objects.filter(filters)

            paginator = PageNumberPagination()
            paginated_products = paginator.paginate_queryset(products, request, view=self)

            if paginated_products is not None:

                serializer = ProductSerializer(paginated_products, many=True)

                return paginator.get_paginated_response(serializer.data)

            serializer = ProductSerializer(products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk=None, format=None):

        try:

            product = Product.objects.get(pk=pk)

        except Product.DoesNotExist:

            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():

            product = serializer.save()

            return Response({
                'message': 'Product updated successfully!',
                'product': ProductSerializer(product).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):

        try:

            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({
                'message': 'Product deleted successfully!'
            }, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist:

            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        

class ProductAlertsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):

        if pk:

            try:

                product = Product.objects.get(pk=pk)
                alerts = product.alerts.all()
                serializer = AlertSerializer(alerts, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)

            except Product.DoesNotExist:

                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)


class ProductsByDateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:

            raise ValidationError("Both 'start_date' and 'end_date' query parameters are required.")

        try:

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        except ValueError:

            raise ValidationError("Dates must be in the format 'YYYY-MM-DD'.")

        if start_date > end_date:

            raise ValidationError("'start_date' must be earlier than or equal to 'end_date'.")

        products = Product.objects.filter(expiration_date__range=(start_date, end_date))

        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request, view=self)

        if paginated_products is not None:

            serializer = ProductSerializer(paginated_products, many=True)

            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductsByDaysAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        days = request.query_params.get('days')

        if not days:
            raise ValidationError("'days' query parameter is required.")

        try:
            days = int(days)

        except ValueError:
            raise ValidationError("'days' must be an integer.")

        if days < 0:
            raise ValidationError("'days' must be a non-negative integer.")

        today = date.today()
        end_date = today + timedelta(days=days)

        products = Product.objects.filter(expiration_date__range=(today, end_date))

        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request, view=self)

        if paginated_products is not None:

            serializer = ProductSerializer(paginated_products, many=True)

            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductsByAlertStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        status_param = request.query_params.get('status')

        if status_param not in ["active", "expired"]:

            return Response(
                {'error': "'status' query parameter must be 'active' or 'expired'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        today = date.today()

        matching_products = []

        products = Product.objects.all()

        for product in products:

            alerts = product.alerts.all()

            for alert in alerts:

                alert_status = get_alert_status(
                    product_expiration_date=alert.product.expiration_date,
                    days_before_expiration_to_trigger=alert.days_before_expiration_to_trigger
                )
                
                if alert_status == status_param:

                    matching_products.append(product)
                    break

        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(matching_products, request, view=self)

        if paginated_products:

            serializer = ProductSerializer(paginated_products, many=True)

            return paginator.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_200_OK)