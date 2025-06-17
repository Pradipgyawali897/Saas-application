from django.db import models

class Page_visit(models.Model):
    path=models.TextField(blank=True,null=True)
    time_stamp=models.DateTimeField(auto_now_add=True)

