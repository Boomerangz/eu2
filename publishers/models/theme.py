from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%d - %s"%(self.id,self.name)