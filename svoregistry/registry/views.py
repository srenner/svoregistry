from django.http import HttpResponse #@UnresolvedImport
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from random import randint
from registry.models import Entry, Car, models
from django.core import serializers
from registry.forms import AddEntryForm
import json
from django.utils import simplejson
import datetime
import csv
from django.core.serializers import xml_serializer
from django.utils.encoding import smart_unicode
from django.db import connection
from django.contrib.auth.decorators import login_required

def coming_soon(request):
    return HttpResponse('Welcome to the future home of the Mustang SVO registry')

def index(request):
    #avoiding order_by('?') because it is a very expensive db call
    entries = Entry.objects.exclude(photo__isnull=True).exclude(photo__exact='')
    last = entries.count() - 1
    if last >= 0:
        index = randint(0, last)
        random_entry = entries[index]
        strJson = serializers.serialize("json", [random_entry,], excludes=('scrape_id', 'entry_flag', 'ip', 'car'))
    else:
        random_entry = None
        strJson = None    
    form = AddEntryForm()
    return render_to_response("registry/index.html", {'entry': random_entry, 'json': strJson, 'form': form}, context_instance=RequestContext(request))

def index_map(request):
    locations = Entry.objects.exclude(geo_lat__isnull=True)#.exclude(geo_long__isnull=True)
    json = serializers.serialize('json', locations, excludes=('comments', 'slappers', 'photo', 'sunroof', 'actual_entry_datetime',
                                                              'interior', 'mileage', 'wing_delete', 'comp_prep', 'option_delete',
                                                              'scrape_id', 'ip', 'for_sale', 'deceased', 'entry_flag', 'has_23', 'on_road',
                                                              'zipcode', 'country', 'state', 'city'))
    return HttpResponse(json, 'application/json')

def view_car(request, vin):
    user_ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        form = AddEntryForm(request.POST)
        if form.is_valid():
            #data = form.cleaned_data
            car = Car(vin=vin, year=form.cleaned_data['year'], slappers=form.cleaned_data['slappers'], color=form.cleaned_data['color'], 
                      interior=form.cleaned_data['interior'], sunroof=form.cleaned_data['sunroof'], comp_prep=form.cleaned_data['comp_prep'], 
                      option_delete=form.cleaned_data['option_delete'], wing_delete=form.cleaned_data['wing_delete'], 
                      has_23=form.cleaned_data['has_23'], on_road=form.cleaned_data['on_road'], deceased=form.cleaned_data['deceased'])
            car.save()

            #TODO: reduce db calls
            new_entry = form.save()
            new_entry.ip = user_ip
            new_entry.save()
            if request.FILES.get("photo"):
                new_entry.photo = request.FILES['photo']
                new_entry.save()
    else:
        pass
    car = get_object_or_404(Car, pk=vin)
    entries = Entry.objects.filter(car=car).order_by('-entry_datetime')
    form = AddEntryForm()
    strJson = serializers.serialize("json", entries, excludes=('scrape_id', 'entry_flag', 'ip', 'car'))
    colors = simplejson.dumps(Entry.COLOR_CHOICES)
    return render_to_response("registry/car.html", {'car': car, 'entries': entries, 'json': strJson, 'colors': colors, 'form': form}, context_instance=RequestContext(request))

def search(request):    
    return render_to_response("registry/search.html", {}, context_instance=RequestContext(request))

def new(request):
    entries = Entry.objects.order_by('-entry_datetime', '-id')[:10]
    strJson = serializers.serialize("json", entries, excludes=('scrape_id', 'entry_flag', 'ip', 'comments'))
    return render_to_response("registry/new.html", { 'entries': entries, 'json': strJson }, context_instance=RequestContext(request))


def for_sale(request):
    filter_date = datetime.datetime.now() + datetime.timedelta(-30)
    entries = Entry.objects.filter(for_sale=True).filter(entry_datetime__gte = filter_date).order_by('-entry_datetime')
    strJson = serializers.serialize("json", entries, excludes=('comments', 'geo_lat', 'geo_long'))
    return render_to_response("registry/forsale.html", { 'entries': entries, 'json': strJson }, context_instance=RequestContext(request))

def save(request):
    cars = Car.objects.extra(where=["(has_23=0 OR (on_road=0 AND deceased=0)) AND deceased <> 1"])
    strJson = serializers.serialize("json", cars)
    return render_to_response("registry/save.html", { 'cars': cars, 'json': strJson }, context_instance=RequestContext(request))

def explore(request):
    return render_to_response("registry/explore.html", { }, context_instance=RequestContext(request))


def explore_new(request):
    if request.is_ajax():
        entriesNew = Entry.objects.order_by('-entry_datetime')[:10]
        jsonNew = serializers.serialize("json", entriesNew, excludes=('scrape_id', 'entry_flag', 'ip', 'comments'))
        return HttpResponse(jsonNew, 'application/json')
    else:
        return HttpResponse('This view is only available through an AJAJ call')

def explore_forsale(request):    
    if request.is_ajax():
        filter_date = datetime.datetime.now() + datetime.timedelta(-30)
        entriesForSale = Entry.objects.filter(for_sale=True).filter(entry_datetime__gte = filter_date).order_by('-entry_datetime')    
        jsonForSale = serializers.serialize("json", entriesForSale, excludes=('comments', 'geo_lat', 'geo_long'))
        return HttpResponse(jsonForSale, 'application/json')
    else:
        return HttpResponse('This view is only available through an AJAJ call')

def explore_save(request):
    if request.is_ajax():
        carsSave = Car.objects.extra(where=["(has_23=0 OR (on_road=0 AND deceased=0)) AND deceased <> 1"])
        jsonSave = serializers.serialize("json", carsSave)
        return HttpResponse(jsonSave, 'application/json')
    else:
        return HttpResponse('This view is only available through an AJAJ call')

def explore_low(request):
    if request.is_ajax():
        carsLow = Car.objects.raw("""SELECT car.*
                                        FROM
                                          (SELECT car_id, MAX(mileage) AS mileage FROM registry_entry GROUP BY car_id) AS entry
                                        INNER JOIN
                                          registry_car car
                                            ON  car.vin  = entry.car_id
                                        WHERE entry.mileage IS NOT NULL AND entry.mileage > 0 AND entry.mileage < 25000
                                        ORDER BY entry.mileage
                                        LIMIT 50""")
        jsonLow = serializers.serialize("json", carsLow)
        return HttpResponse(jsonLow, 'application/json')
        
    else:
        return HttpResponse('This view is only available thorugh an AJAJ call')

def does_vin_exist(request, vin):
    exists = Car.objects.filter(vin=vin).exists()
    if not exists:
        car = Car(vin=vin)
        car.save()
    return HttpResponse('{"exists":' + str(exists).lower() + '}', mimetype='application/json')
    
def flag_entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    entry.entry_flag += 1
    entry.save()
    return HttpResponse("")

def download_index(request):
    return render_to_response("registry/download.html", context_instance=RequestContext(request))

def about(request):
    return render_to_response("registry/about.html", context_instance=RequestContext(request))

def download(request, download_format):
    if download_format == "csv":
        excludes = ['scrape_id', 'entry_flag', 'ip']
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=svo_export.csv'
        writer = csv.writer(response)
        headers = []
        for field in Entry._meta.fields: #@UndefinedVariable
            do_write = True
            pass
            for exclude in excludes:
                if exclude == field.name:
                    do_write = False
                    break
            if do_write:
                headers.append(field.name)
        writer.writerow(headers)
        print Entry.objects.all()
        for obj in Entry.objects.all().order_by("id"):
            row = []
            for field in Entry._meta.fields: #@UndefinedVariable
                do_write = True
                for exclude in excludes:
                    if exclude == field.name:
                        do_write = False
                        break
                if do_write:
                    row.append(smart_unicode(getattr(obj, field.name)))
            writer.writerow(row)
        return response
    if download_format == "json":
        mimetype = "application/json"
        outputFormat = "json"
        data = serializers.serialize(outputFormat, Entry.objects.all(), excludes=('scrape_id', 'entry_flag', 'ip'))
        return HttpResponse(data, mimetype)
    if download_format == "xml":
        mimetype = "application/xml"
        outputFormat = "xml"
        data = serializers.serialize(outputFormat, Entry.objects.all(), excludes=('scrape_id', 'entry_flag', 'ip'))
        return HttpResponse(data, mimetype)   
    return HttpResponse("Requested format " + download_format + " but I don't know how to handle that")

def stats(request):
    
    cursor = connection.cursor()
    cursor.execute("select count(*) as 'cars' from registry_car")
    cars = cursor.fetchall()[0][0]
    
    cursor = connection.cursor()
    cursor.execute("select count(*) as 'entries' from registry_entry")
    entries = cursor.fetchall()[0][0]
    
    return render_to_response("registry/stats/stats_index.html", {'cars': cars, 'entries': entries}, context_instance=RequestContext(request))

def stats_colors(request):
    cursor = connection.cursor()
    cursor.execute("""select color, count(color) as 'count'
                        from registry_car
                        where color is not null
                        group by color""")
    report = dictfetchall(cursor)
    if request.is_ajax():
        return HttpResponse(json.dumps(report), 'application/json')
    else:
        return render_to_response("registry/stats/colors.html", { 'report': report }, context_instance=RequestContext(request))

def stats_year(request):
    cursor = connection.cursor()
    cursor.execute("""select year, count(year) as 'count',
                          case year
                            when '1984' then 4506
                            when '1985' then 1512
                            when '1985.5' then 439
                            when '1986' then 3378
                          end as 'total_production'
                        from registry_car
                        where year is not null
                        group by year""")
    report = dictfetchall(cursor)
    if request.is_ajax():
        return HttpResponse(json.dumps(report), 'application/json')
    else:
        return render_to_response("registry/stats/year.html", { 'report': report }, context_instance=RequestContext(request))

def stats_status(request):
    cursor = connection.cursor()
    cursor.execute("""select
                          case deceased
                            when 1 then 'Deceased'
                            when 0 then 'Alive'
                          end as 'status',
                          count(deceased) as 'count'
                        from registry_car
                        where deceased is not null
                        group by deceased
                        union all
                        select 
                          'Unknown' as 'status', 
                          (select count(*) from registry_car where deceased is null) as 'count'""")
    report = dictfetchall(cursor)
    if request.is_ajax():
        return HttpResponse(json.dumps(report), 'application/json')
    else:
        return render_to_response("registry/stats/status.html", { 'report': report }, context_instance=RequestContext(request))

@login_required
def flagged(request):
    entries = Entry.objects.filter(entry_flag__gt=0)
    strJson = serializers.serialize("json", entries, excludes=('scrape_id', 'ip', 'comments'))
    return render_to_response("registry/flagged.html", { 'entries': entries, 'json': strJson }, context_instance=RequestContext(request))
    
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]