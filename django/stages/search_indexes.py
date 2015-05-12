import datetime
from haystack import indexes
from .models import Stage

class StageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, model_attr='description')
    sujet = indexes.CharField(model_attr='sujet')

    def get_model(self):
        return Stage

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
