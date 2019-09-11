from django.db import models

# Create your models here.
class Dialog(models.Model):
    def __str__(self):
        return str(self.id)

class Record(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    RECORD_TYPES = [
        ('Q', 'Question'),
        ('A', 'User Command'),
        ('G', 'Graph Json')
    ]
    record_type = models.CharField(max_length=1, choices=RECORD_TYPES)
    content = models.TextField()
    def __str__(self):
        return '[%d, %s, %s]' % (self.dialog.id, self.record_type, self.content)
