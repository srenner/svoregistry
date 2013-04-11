from django.contrib.sitemaps import Sitemap
from registry.models import Car

class CarSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Car.objects.all()
