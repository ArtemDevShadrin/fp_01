from django.urls import path
from .views import (
    AnalyticsView,
    ReportListView,
    ReportDetailView,
    ReportManagementView,
    AnalyticsOverviewView,
    ReportCreateView,
)

urlpatterns = [
    path("reports/", ReportListView.as_view(), name="report_list"),
    path("reports/<int:pk>/", ReportDetailView.as_view(), name="report_detail"),
    path("manage/", ReportManagementView.as_view(), name="report_management"),
    path("analytics/", AnalyticsOverviewView.as_view(), name="analytics_overview"),
    path("reports/create/", ReportCreateView.as_view(), name="report_create"),
    path("analytics_product/", AnalyticsView.as_view(), name="analytics_product"),
]
