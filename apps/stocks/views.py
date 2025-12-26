from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Min, Max, StdDev
from django.utils import timezone
from datetime import timedelta

# Internal Imports
from apps.accounts.permissions import IsAdminUserTier
from .models import Stock
from apps.pricing.models import StockPrice
from apps.watchlists.models import Watchlist, WatchlistItem
from .serializers import (
    StockSerializer, 
    WatchlistItemSerializer, 
    StockPriceSerializer, 
    WatchlistSerializer
)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def stock_list_create_view(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if request.user.account_tier != 'ADMIN':
            return Response(
                {"detail": "Only Admins can create stock master data."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid(): # Fixed typo: was .valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def stock_detail_view(request, symbol):
    try:
        stock = Stock.objects.get(symbol=symbol.upper())
    except Stock.DoesNotExist:
        return Response({"detail": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    if request.user.account_tier != 'ADMIN':
        return Response(
            {"detail": "Only Admins can modify stock master data."},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method in ['PUT', 'PATCH']:
        serializer = StockSerializer(stock, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_price_history_view(request, symbol):
    queryset = StockPrice.objects.filter(stock__symbol=symbol.upper())

    if request.user.account_tier == 'STANDARD':
        cutoff = timezone.now() - timedelta(days=30)
        queryset = queryset.filter(timestamp__gte=cutoff)
        msg = "Standard Tier: Viewing last 30 days."
    else:
        msg = "Premium/Admin Tier: Full history access."

    serializer = StockPriceSerializer(queryset, many=True)
    return Response({
        "info": msg,
        "count": queryset.count(),
        "results": serializer.data
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watchlist_list_create_view(request):
    if request.method == 'GET':
        watchlists = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        existing_count = Watchlist.objects.filter(user=request.user).count()
        if request.user.account_tier == 'STANDARD' and existing_count >= 1:
            return Response(
                {"detail": "Standard accounts are limited to 1 watchlist."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def modify_watchlist_items(request, watchlist_id):
    try:
        watchlist = Watchlist.objects.get(id=watchlist_id, user=request.user)
    except Watchlist.DoesNotExist:
        return Response({"detail": "Watchlist not found."}, status=status.HTTP_404_NOT_FOUND)

    symbol = request.data.get('symbol')
    if not symbol:
        return Response({"detail": "Symbol is required."}, status=400)

    if request.method == 'POST':
        try:
            stock = Stock.objects.get(symbol=symbol.upper())
        except Stock.DoesNotExist:
            return Response({"detail": "Stock not found."}, status=404)

        if WatchlistItem.objects.filter(watchlist=watchlist, stock=stock).exists():
            return Response({"detail": "Already in watchlist."}, status=400)

        WatchlistItem.objects.create(
            watchlist=watchlist, 
            stock=stock, 
            alert_thresholds=request.data.get('alert_thresholds', {})
        )
        return Response({"message": f"{symbol} added."}, status=201)

    if request.method == 'DELETE':
        WatchlistItem.objects.filter(watchlist=watchlist, stock__symbol=symbol.upper()).delete()
        return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stock_stats_view(request, symbol):
    queryset = StockPrice.objects.filter(stock__symbol=symbol.upper())

    if request.user.account_tier == 'STANDARD':
        cutoff = timezone.now() - timedelta(days=30)
        queryset = queryset.filter(timestamp__gte=cutoff)

    stats = queryset.aggregate(
        min_price=Min('price'),
        max_price=Max('price'),
        avg_price=Avg('price'),
        volatility=StdDev('price')
    )

    if stats['min_price'] is None:
        return Response({"detail": "No data found."}, status=404)

    return Response({
        "symbol": symbol.upper(),
        "tier_applied": request.user.account_tier,
        "statistics": stats
    })