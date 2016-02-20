from django.db import connection
from django.views.generic import ListView
from publishers.models import Site

__author__ = 'igor'


class SiteList(ListView):
    model = Site
    template_name = "publishers/site_list.html"

    def get_context_data(self, **kwargs):
        data = super(SiteList, self).get_context_data(**kwargs)
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
                    publishers_adspot as pa \
                    on 1=1 \
                    left join \
                    banner_show_stats as bss \
                    on bss.spot_code = pa.code and date(bss.created)=dt.date \
                    left join \
                    banner_clicks as bc \
                    on bc.spot_code = pa.code and date(bc.created)=dt.date \
                    where pa.site_id in (%s) \
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