from django.db import connection
from django.views.generic import ListView
from advertisers.models import Campaign

__author__ = 'igor'


class CampaignList(ListView):
    model = Campaign
    template_name = "advertisers/campaign_list.html"

    def get_context_data(self, **kwargs):
        data = super(CampaignList, self).get_context_data(**kwargs)
        data['stats_data'] = self.get_stats_data()
        return data

    def get_stats_data(self):
        id_list = [str(i.id) for i in self.get_queryset()]
        if len(id_list) > 0:
            id_string = ",".join(id_list)
            cursor = connection.cursor()
            query = "select dt.date, count(distinct bss.id) as shows, count(distinct bc.id) as clicks from \
                    (select Now()::date - s.a AS date from Generate_series(30, 0, -1) AS s(a)) as dt \
                    inner join  \
                    advertisers_banner as ab \
                    on 1=1 \
                    left join \
                    banner_show_stats as bss \
                    on bss.banner_id = ab.id and date(bss.created)=dt.date \
                    left join \
                    banner_clicks as bc \
                    on bc.banner_id = ab.id and date(bc.created)=dt.date \
                    where ab.campaign_id in (%s) \
                    group by dt.date \
                    order by dt.date;" % (id_string)
            cursor.execute(query)
            rows = cursor.fetchall()
            data = {}
            data['dates'] = [r[0].isoformat() for r in rows]
            data['shows'] = [int(r[1]) for r in rows]
            data['clicks'] = [int(r[2]) for r in rows]
            return data
        else:
            return None