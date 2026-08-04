from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, FormView, TemplateView
from search_engine.models import Query, Document, ScoreDoc
from search_engine.forms import CustomQueryForm
from django.contrib import messages
from django.apps import apps
from search_engine.preprocessings.token_and_lemmatize import cross_encoding
from django.db.models import Q

class Home(FormView):
    template_name = "search_engine/home.html"
    form_class = CustomQueryForm

class QueriesView(ListView):
    model = Query
    template_name = "search_engine/general_queries_view.html"
    context_object_name = "queries"

    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q_search')

        if search_term:
            queryset = queryset.filter(
                Q(query_id__icontains=search_term) |
                Q(text__icontains=search_term)
            )

        return queryset

class DocumentsView(ListView):
    model = Document
    template_name = "search_engine/general_documents_view.html"
    context_object_name = "documents"

    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('d_search')

        if search_term:
            queryset = queryset.filter(
                Q(doc_id__icontains=search_term) |
                Q(text__icontains=search_term)
            )

        return queryset

class DocumentDetailView(DetailView):
    model = Document
    template_name = "search_engine/document_detail.html"
    context_object_name = "document"

class ResultsView(TemplateView):
    template_name = "search_engine/results.html"

    def get(self, request, *args, **kwargs):
        q_id = request.GET.get('q_id')
        custom_q = request.GET.get('q')

        if not q_id and not custom_q:
            messages.warning(self.request, message="You selected nothing!")
            return redirect('search_engine:home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q_id = self.request.GET.get('q_id')
        custom_q = self.request.GET.get('q')

        search_text = ""
        is_ready_query = False

        if q_id:
            query_obj = get_object_or_404(Query, query_id=q_id)
            search_text = query_obj.text
            is_ready_query = True
        elif custom_q:
            search_text = custom_q.strip()

        result_list = cross_encoding(search_text)
        unsorted_documents = Document.objects.filter(doc_id__in=result_list)
        doc_dict_for_order = {doc.doc_id: doc for doc in unsorted_documents}
        ordered_results = [doc_dict_for_order[doc_id] for doc_id in result_list if doc_id in doc_dict_for_order]

        context["searched_text"] = search_text
        context["is_ready_query"] = is_ready_query
        context["results"] = ordered_results

        if is_ready_query:
            context["actual_documents"] = query_obj.score_doc.all()

        return context