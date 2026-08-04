from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from search_engine.models import Query, Document, ScoreDoc
from search_engine.forms import CustomQueryForm

# def home_screen(request):
#     return render(request, "search_engine/home.html")

class Home(FormView):
    template_name = "search_engine/home.html"
    form_class = CustomQueryForm

class QueriesView(ListView):
    model = Query
    template_name = "search_engine/general_queries_view.html"
    context_object_name = "queries"

    paginate_by = 50

class DocumentsView(ListView):
    model = Document
    template_name = "search_engine/general_documents_view.html"
    context_object_name = "documents"

    paginate_by = 50

class DocumentDetailView(DetailView):
    model = Document
    template_name = "search_engine/document_detail.html"
    context_object_name = "document"