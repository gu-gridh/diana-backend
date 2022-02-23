# from django.contrib import admin
from django.contrib.gis.db import models
from .models import *
from django.utils.html import format_html
from django.contrib.gis import admin

@admin.register(Image)
class ImageModel(admin.ModelAdmin):
    fields = get_fields(Image).append('image_preview')
    readonly_fields = ('image_preview',)
    list_display = ('bild', 'thumbnail_preview')

    def image_preview(self, obj):
        return format_html(f'<img src="https://img.dh.gu.se/art/pyr/{obj.bild}.tif/full/full/0/default.jpg" height="300" />')

    def thumbnail_preview(self, obj):
        return format_html(f'<img src="https://img.dh.gu.se/art/pyr/{obj.bild}.tif/full/full/0/default.jpg" height="100" />')


    image_preview.short_description = 'Image preview'
    image_preview.allow_tags = True
    thumbnail_preview.short_description = 'Image thumbnail'
    thumbnail_preview.allow_tags = True

@admin.register(Motive)
class MotiveAdmin(admin.ModelAdmin):
    fields = get_fields(Motive)

@admin.register(Parish)
class ParishAdmin(admin.ModelAdmin):
    fields = get_fields(Parish) 
    list_display = ['name', 'id', 'parent', 'origin', 'province', 'county']
    list_filter = ['province',]


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin): 
    fields = get_fields(Object) 
    list_display = ['objektid', 'objekt', 'undertyp', 'motiv']
    list_filter = ['dat_min', 'dat_max']


@admin.register(Place)
class PlaceAdmin(admin.OSMGeoAdmin):
    fields = get_fields(Place)
    list_display = ['name', 'county', 'country', 'parish']
    list_filter = ['country']
    search_fields = ['name', 'country']
