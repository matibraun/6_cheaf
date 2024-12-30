import requests
from alerts.models import Alert
from alerts.selectors import get_alert_status
from alerts.serializers import AlertSerializer
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class AlertsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        product_id = request.data.get('product_id')
        days_before_expiration_to_trigger = request.data.get('days_before_expiration_to_trigger')

        if not product_id or not days_before_expiration_to_trigger:
            return Response(
                {'error': "'product_id' and 'days_before_expiration_to_trigger' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        alert = Alert.objects.create(
            product=product,
            days_before_expiration_to_trigger=days_before_expiration_to_trigger
        )

        serializer = AlertSerializer(alert)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None, format=None):

        if pk:

            try:
                alert = Alert.objects.get(pk=pk)
                serializer = AlertSerializer(alert)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Alert.DoesNotExist:
                return Response({'error': 'Alert not found'}, status=status.HTTP_404_NOT_FOUND)

        else:

            alerts = Alert.objects.all()
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk=None, format=None):

        try:

            alert = Alert.objects.get(pk=pk)

        except Alert.DoesNotExist:

            return Response({'error': 'Alert not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlertSerializer(alert, data=request.data, partial=True)

        if serializer.is_valid():

            alert = serializer.save()

            return Response({
                'message': 'Alert updated successfully!',
                'alert': AlertSerializer(alert).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):

        try:

            alert = Alert.objects.get(pk=pk)
            alert.delete()

            return Response({
                'message': 'Alert deleted successfully!'
            }, status=status.HTTP_204_NO_CONTENT)

        except Alert.DoesNotExist:

            return Response({'error': 'Alert not found'}, status=status.HTTP_404_NOT_FOUND)
        

class AlertsByStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        status_param = request.query_params.get('status')


        if status_param not in ["active", "expired"]:

            return Response(
                {'error': "'status' query parameter must be 'active' or 'expired'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        matching_alerts = []

        alerts = Alert.objects.all()

        for alert in alerts:

            alert_status = get_alert_status(
                product_expiration_date=alert.product.expiration_date,
                days_before_expiration_to_trigger=alert.days_before_expiration_to_trigger
            )

            if alert_status == status_param:
                matching_alerts.append(alert)

        paginator = PageNumberPagination()
        paginated_alerts = paginator.paginate_queryset(matching_alerts, request, view=self)

        if paginated_alerts:
            serializer = AlertSerializer(paginated_alerts, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_200_OK)