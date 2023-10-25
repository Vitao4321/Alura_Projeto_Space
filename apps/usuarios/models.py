from django.contrib.contenttypes.models import ContentType
from django.db import models

# ACTION FLAG
# 1: Adição - foto criado
# 2: Alteração - foto editada
# 3: Exclusão - foto excluida

class CustomLogEntry(models.Model):
    
    action_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ('-action_time',)


