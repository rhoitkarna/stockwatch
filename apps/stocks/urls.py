from django.urls import path
from . import views

urlpatterns = [
    # 1. FIXED: Static paths MUST come before dynamic <str:symbol> paths
    path('watchlists/', views.watchlist_list_create_view),
    path('watchlists/<int:watchlist_id>/items/', views.modify_watchlist_items),
    
    # 2. Market Data paths
    path('', views.stock_list_create_view),
    path('<str:symbol>/', views.stock_detail_view),
    path('<str:symbol>/history/', views.stock_price_history_view),
    path('<str:symbol>/stats/', views.stock_stats_view),
]