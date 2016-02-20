from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import TemplateView
from advertisers.models import Campaign
from publishers.models import Site

__author__ = 'igor'


class OneCampaignView(TemplateView):
    template_name = "advertisers/campaign.html"

    def get_context_data(self, pk, **kwargs):
        data = super(OneCampaignView, self).get_context_data(**kwargs)
        try:
            campaign = Campaign.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        if not (campaign.user == self.request.user or self.request.user.is_superuser):
            raise Http404
        data['campaign'] = campaign
        return data