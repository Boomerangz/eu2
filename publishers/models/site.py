from django.contrib.auth.models import User
from django.db import models, connection
from publishers.models.theme import Theme


class Site(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    themes = models.ManyToManyField(Theme)
    user = models.ForeignKey(User, default=1)

    def __unicode__(self):
        return "%d - %s" % (self.id, self.name)

    def get_stats(self):
        stats = {"clicks": 0, "shows": 0}
        for spot in self.adspot_set.all():
            spot_stats = spot.get_stats()
            stats["clicks"] += spot_stats["clicks"]
            stats["shows"] += spot_stats["shows"]
        stats["ctr"] = float(stats["clicks"]) / stats["shows"] if stats["shows"] else ""
        return stats


    stats_data={}
    def get_stats_data(self):
        if not self.stats_data:
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
                    where pa.site_id in (%d) \
                    group by dt.date \
                    order by dt.date;"%(self.id)
            cursor.execute(query)
            rows = cursor.fetchall()
            data = {}
            data['dates'] = [r[0].isoformat() for r in rows]
            data['shows'] = [int(r[1]) for r in rows]
            data['clicks'] = [int(r[2]) for r in rows]
            self.stats_data = data
        return self.stats_data