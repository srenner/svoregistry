from django.conf.urls import patterns, include, url #@UnresolvedImport
from django.conf import settings
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from registry.models import Car

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

info_dict = {
    'queryset': Car.objects.all(),
}

sitemaps = {
    'CarSitemap': GenericSitemap(info_dict, priority=0.6),
}

urlpatterns = patterns('',
    #url(r'^$', 'registry.views.coming_soon'),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    url(r'^$', 'registry.views.index'),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^lookup/(?P<vin>\w{17})/', 'registry.views.does_vin_exist'),
    
    url(r'^download/$', 'registry.views.download_index'),
    
    url(r'^download/(?P<download_format>[a-z]*)/$', 'registry.views.download'),
    
    url(r'^about/$', 'registry.views.about'),
    
    url(r'^flag/(?P<entry_id>\d+)/$', 'registry.views.flag_entry'),
    
    url(r'^flagged/$', 'registry.views.flagged'), 
    
    url(r'^(?P<vin>\w{17})/$', 'registry.views.view_car'),
    
    #url(r'^(?P<vin>\w{17})/add/$', 'registry.views.add_entry'),
    
    url(r'^forsale/$', 'registry.views.for_sale'),
    
    url(r'^save/$', 'registry.views.save'),
    
    #url(r'^search/$', 'registry.views.search'),
    
    url(r'^new/$', 'registry.views.new'),
    
    url(r'^explore/$', 'registry.views.explore'),
    
    url(r'^explore/forsale/$', 'registry.views.explore_forsale'),
    
    url(r'^explore/new/$', 'registry.views.explore_new'),
    
    url(r'^explore/save/$', 'registry.views.explore_save'),
    
    url(r'^explore/low/$', 'registry.views.explore_low'),
    
    url(r'^map/', 'registry.views.index_map'),
    
    url(r'^stats/colors/', 'registry.views.stats_colors'),
    
    url(r'^stats/year/', 'registry.views.stats_year'),
    
    url(r'^stats/status/', 'registry.views.stats_status'),
    
    url(r'^stats/', 'registry.views.stats'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))