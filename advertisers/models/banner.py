import uuid
from django.db import models, connection
from advertisers.models.campaign import Campaign
from publishers.models.format import Format


def generate_unique_code():
    return uuid.uuid4().hex[:15].upper()


class Banner(models.Model):
    campaign = models.ForeignKey(Campaign, default=None)
    format = models.ForeignKey(Format)
    image = models.ImageField(upload_to='banners')
    url = models.URLField()

    def __unicode__(self):
        return "%d - %s" % (self.id, self.format.name)

    def get_html(self):
        return '<a href="%s" target="_blank"><img src="/media/%s"></a>'%(self.url, self.image)

    def get_stats(self):
        cursor = connection.cursor()
        query = "SELECT ab.id, \
                               coalesce(shw.shows,0) AS shows, \
                               coalesce(clck.clicks,0) AS clicks \
                        FROM advertisers_banner AS ab \
                        LEFT JOIN \
                          (SELECT banner_id, \
                                  count(*) AS shows \
                           FROM banner_show_stats \
                           WHERE banner_id IN (%d) and created>date_trunc('day', NOW() - interval '1 month') \
                           GROUP BY banner_id) AS shw ON ab.id=shw.banner_id \
                        LEFT JOIN \
                          (SELECT banner_id, \
                                  count(*) AS clicks \
                           FROM banner_clicks \
                           WHERE banner_id IN (%d) and created>date_trunc('day', NOW() - interval '1 month') \
                           GROUP BY banner_id) AS clck ON ab.id=clck.banner_id \
                           WHERE ab.id in (%d);"%(self.id, self.id, self.id)
        print query
        cursor.execute(query)
        row = cursor.fetchone()

        stats = {"shows": row[1], "clicks": row[2],}
        stats["ctr"] = float(stats["clicks"]) / stats["shows"] if stats["shows"] else ""
        return stats