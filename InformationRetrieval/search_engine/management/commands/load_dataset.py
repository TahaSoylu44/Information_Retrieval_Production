from django.core.management.base import BaseCommand
import ir_datasets
from search_engine.models import Document, Query, ScoreDoc

class Command(BaseCommand): # python manage.py ile çalış
    help = 'Load the dataset into the database'

    def handle(self, *args, **kwargs):
        dataset = ir_datasets.load("wikir/en1k/training")

        self.stdout.write(self.style.SUCCESS("Dataset is loaded."))

        BATCH_SIZE = 5000

        #! DOCUMENTS
        self.stdout.write("Documents saving...")
        docs_to_save = []

        for doc in dataset.docs_iter():
            docs_to_save.append(
                Document(
                    doc_id=doc.doc_id,
                    text=doc.text
                )
            )

            if len(docs_to_save) >= BATCH_SIZE:
                Document.objects.bulk_create(docs_to_save, ignore_conflicts=True)
                self.stdout.write(f"{BATCH_SIZE} documents saved!")
                docs_to_save = []

        if docs_to_save:
            Document.objects.bulk_create(docs_to_save, ignore_conflicts=True)
            self.stdout.write(f"{len(docs_to_save)} documents saved!")

        #! QUERIES
        self.stdout.write("Queries saving...")
        queries_to_save = []

        for query in dataset.queries_iter():
            queries_to_save.append(
                Query(
                    query_id=query.query_id,
                    text=query.text
                )
            )

            if len(queries_to_save) >= BATCH_SIZE:
                Query.objects.bulk_create(queries_to_save, ignore_conflicts=True)
                self.stdout.write(f"{BATCH_SIZE} queries saved!")
                queries_to_save = []

        if queries_to_save:
            Query.objects.bulk_create(queries_to_save, ignore_conflicts=True)
            self.stdout.write(f"{len(queries_to_save)} queries saved!")

        #! SCOREDOC
        self.stdout.write("Scoredocs saving...")
        scoredocs_to_save = []

        for scoredoc in dataset.scoreddocs_iter():
            scoredocs_to_save.append(
                ScoreDoc(
                    query_id=scoredoc.query_id,
                    document_id=scoredoc.doc_id,
                    score=scoredoc.score
                )
            )

            if len(scoredocs_to_save) >= BATCH_SIZE:
                ScoreDoc.objects.bulk_create(scoredocs_to_save, ignore_conflicts=True)
                self.stdout.write(f"{BATCH_SIZE} scoredocs saved!")
                scoredocs_to_save = []

        if scoredocs_to_save:
            ScoreDoc.objects.bulk_create(scoredocs_to_save, ignore_conflicts=True)
            self.stdout.write(f"{len(scoredocs_to_save)} scoredocs saved!")

        self.stdout.write(self.style.SUCCESS("All database are uploaded!"))