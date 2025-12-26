from django.db import models
from apps.stocks.models import Stock

# Create your models here.
class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=20, decimal_places=4)
    source = models.CharField(max_length=50) # e.g., 'YahooFinance', 'AlphaVantage'
    timestamp = models.DateTimeField(db_index=True)

    class Meta:
        # Crucial for time-series performance
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['stock', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.stock.symbol}: {self.price} @ {self.timestamp}"
