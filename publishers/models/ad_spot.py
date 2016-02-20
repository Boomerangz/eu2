import uuid
from django.db import models, connection
from publishers.models.site import Site
from publishers.models.format import Format


def generate_unique_code():
    return uuid.uuid4().hex[:15].upper()


class AdSpot(models.Model):
    name = models.CharField(max_length=255)
    site = models.ForeignKey(Site, default=None)
    format = models.ForeignKey(Format)
    code = models.CharField(max_length=255, unique=True, default=generate_unique_code)

    def __unicode__(self):
        return "%d - %s" % (self.id, self.name)


    def get_html(self):
        return '<div id="euph_spot" euph="%s"></div> \
                <script type="text/javascript" src="http://euphorbia.co/static/js/sdk.js"></script>'%self.code

    def get_stats(self):
        cursor = connection.cursor()
        query = "SELECT pa.id, \
                               coalesce(shw.shows,0) AS shows, \
                               coalesce(clck.clicks,0) AS clicks \
                        FROM publishers_adspot AS pa \
                        LEFT JOIN \
                          (SELECT spot_code, \
                                  count(*) AS shows \
                           FROM banner_show_stats \
                           WHERE spot_code IN ('%s') and created>date_trunc('day', NOW() - interval '1 month') \
                           GROUP BY spot_code) AS shw ON pa.code=shw.spot_code \
                        LEFT JOIN \
                          (SELECT spot_code, \
                                  count(*) AS clicks \
                           FROM banner_clicks \
                           WHERE spot_code IN ('%s') and created>date_trunc('day', NOW() - interval '1 month') \
                           GROUP BY spot_code) AS clck ON pa.code=clck.spot_code \
                           WHERE pa.id in (%d);"%(self.code, self.code, self.id)
        cursor.execute(query)
        row = cursor.fetchone()

        stats = {"shows": row[1], "clicks": row[2],}
        stats["ctr"] = float(stats["clicks"]) / stats["shows"] if stats["shows"] else ""
        return stats