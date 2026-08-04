from django.urls import path
from search_engine.views import QueriesView, DocumentsView, DocumentDetailView, Home, ResultsView

app_name = "search_engine"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("queries/", QueriesView.as_view(), name="query_list"),
    path("documents/", DocumentsView.as_view(), name="document_list"),
    path("documents/<str:pk>/", DocumentDetailView.as_view(), name="document_detail"),
    path("results/", ResultsView.as_view(), name="results")
]