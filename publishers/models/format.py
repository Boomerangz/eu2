from django.db import models


class Format(models.Model):
    name = models.CharField(max_length=255)

    def check_banner(self, banner):
        return True

    def __unicode__(self):
        return "%d - %s"%(self.id,self.name)