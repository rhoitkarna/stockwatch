from rest_framework import serializers
from .models import Stock
from apps.pricing.models import StockPrice
from apps.watchlists.models import Watchlist, WatchlistItem

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'symbol', 'name', 'exchange', 'currency', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_symbol(self, value):
        return value.upper()

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ['price', 'source', 'timestamp']

class WatchlistItemSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.ReadOnlyField(source='stock.symbol')
    stock_name = serializers.ReadOnlyField(source='stock.name')

    class Meta:
        model = WatchlistItem
        fields = ['id', 'stock_symbol', 'stock_name', 'added_at', 'alert_thresholds']

class WatchlistSerializer(serializers.ModelSerializer):
    # This nested serializer allows us to see the stocks in the list
    items = WatchlistItemSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'name', 'is_default', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'created_at']