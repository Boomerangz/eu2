from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import TemplateView
from publishers.models import Site

__author__ = 'igor'




class OneSiteView(TemplateView):
    model = Site
    template_name = "publishers/site.html"

    def get_context_data(self, pk, **kwargs):
        data = super(OneSiteView, self).get_context_data(**kwargs)
        try:
            site = Site.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        if not (site.user==self.request.user or self.request.user.is_superuser):
            raise Http404
        data['site']=site
        return data