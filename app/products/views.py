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

            # Ensure you are paginating the queryset
            if paginated_products is not None:
                serializer = ProductSerializer(paginated_products, many=True)
                return paginator.get_paginated_response(serializer.data)

            # If no pagination (for some reason), return all products
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
        # Extract start_date and end_date from query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate dates
        if not start_date or not end_date:
            raise ValidationError("Both 'start_date' and 'end_date' query parameters are required.")

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError("Dates must be in the format 'YYYY-MM-DD'.")

        # Ensure start_date is earlier than or equal to end_date
        if start_date > end_date:
            raise ValidationError("'start_date' must be earlier than or equal to 'end_date'.")

        # Filter products by expiration_date
        products = Product.objects.filter(expiration_date__range=(start_date, end_date))

        # Paginate results
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request, view=self)

        if paginated_products is not None:
            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Return all matching products if no pagination
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ProductsByDaysAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Extract days from query parameters
        days = request.query_params.get('days')

        # Validate the input
        if not days:
            raise ValidationError("'days' query parameter is required.")

        try:
            days = int(days)
        except ValueError:
            raise ValidationError("'days' must be an integer.")

        if days < 0:
            raise ValidationError("'days' must be a non-negative integer.")

        # Calculate the date range
        today = date.today()
        end_date = today + timedelta(days=days)

        # Filter products by expiration_date
        products = Product.objects.filter(expiration_date__range=(today, end_date))

        # Paginate results
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request, view=self)

        if paginated_products is not None:
            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Return all matching products if no pagination
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductsByAlertStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Extract 'status' from query parameters
        status_param = request.query_params.get('status')

        # Validate 'status' parameter
        if status_param not in ["active", "expired"]:
            return Response(
                {'error': "'status' query parameter must be 'active' or 'expired'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get today's date for comparison
        today = date.today()

        # List to hold products that match the status
        matching_products = []

        # Loop through all products and check their associated alerts
        products = Product.objects.all()
        for product in products:
            # Filter alerts based on the status (active or expired)
            alerts = product.alerts.all()
            for alert in alerts:
                # Use get_alert_status to determine if the alert is "active" or "expired"
                alert_status = get_alert_status(
                    product_expiration_date=alert.product.expiration_date,
                    days_before_expiration_to_trigger=alert.days_before_expiration_to_trigger
                )
                
                # If the alert status matches the requested status, add the product
                if alert_status == status_param:
                    matching_products.append(product)
                    break  # Once we find a matching alert for the product, no need to check further

        # Paginate the results
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(matching_products, request, view=self)

        # Serialize and return the results
        if paginated_products:
            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If no products are found, return an empty list
        return Response([], status=status.HTTP_200_OK)