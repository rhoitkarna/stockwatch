from django.db import models
from django.conf import settings
from apps.stocks.models import Stock

# Create your models here.
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

class WatchlistItem(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='items')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    # JSONField for flexible alert logic (e.g., {"above": 150, "below": 100})
    alert_thresholds = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('watchlist', 'stock')