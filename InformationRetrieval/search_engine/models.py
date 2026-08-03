from django.db import models

class Document(models.Model):
    doc_id = models.CharField(max_length=255, primary_key=True)
    text = models.TextField()

    def __str__(self):
        return f"Doc {self.doc_id}"

class Query(models.Model):
    query_id = models.CharField(max_length=255, primary_key=True)
    text = models.TextField()
    relevant_documents = models.ManyToManyField(Document, through='ScoreDoc')

    def __str__(self):
        return f"Query: {self.text}"

class ScoreDoc(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name="score_doc")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="score_doc")
    score = models.FloatField()

    class Meta:
        constraints = (models.UniqueConstraint(fields=["query", "document"], name="query_document_uniqueness"),)

    def __str__(self):
        return f"{self.query}  {self.document}  Score: {self.score}"