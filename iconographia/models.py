# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
from django.contrib.gis.db import models
from django.utils.html import mark_safe

def get_fields(model: models.Model, exclude=['id']):
    return [field.name for field in model._meta.fields if field.name not in exclude]


class ColLabels(models.Model):
    tab = models.CharField(max_length=32)
    col = models.CharField(max_length=32)
    label = models.CharField(max_length=255, blank=True, null=True)
    label_sv = models.CharField(max_length=255, blank=True, null=True)
    ftab = models.CharField(max_length=32, blank=True, null=True)
    fcol = models.CharField(max_length=32, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    hidden = models.PositiveIntegerField()
    readonly = models.PositiveIntegerField()
    searchable = models.PositiveIntegerField()
    help = models.CharField(max_length=256)
    help_sv = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'col_labels'


class Image(models.Model):
    bild = models.CharField(max_length=128, blank=True, null=True)
    bildfil = models.CharField(max_length=128, blank=True, null=True)
    mb_object = models.ForeignKey('Object', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'image'

    def __str__(self) -> str:
        return f"{self.mb_object} ({self.bildfil})"

class Motive(models.Model):
    mb_image = models.ForeignKey(Image, models.DO_NOTHING)
    motive = models.CharField(max_length=175, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motive'

    def __str__(self) -> str:
        return f"{self.motive}: {self.mb_image}"

class Object(models.Model):
    objektid = models.CharField(max_length=128, blank=True, null=True, verbose_name="Objekt ID")
    main_image = models.ForeignKey(Image, models.DO_NOTHING, db_column='main_image', verbose_name="Huvudbild")
    museum = models.CharField(max_length=128, blank=True, null=True, verbose_name="Museum")
    inventarienummer = models.CharField(max_length=128, blank=True, null=True, verbose_name="Inventarienummer")
    undernummer = models.CharField(max_length=128, blank=True, null=True, verbose_name="Undernummer")
    invnr = models.CharField(max_length=128, blank=True, null=True, verbose_name="Inventarienummer")
    landskap = models.CharField(max_length=128, blank=True, null=True, verbose_name="Landskap")
    ort = models.CharField(max_length=128, blank=True, null=True, verbose_name="Ort")
    sakord = models.CharField(max_length=128, blank=True, null=True, verbose_name="Sakord")
    typ = models.CharField(max_length=128, blank=True, null=True, verbose_name="Typ")
    undertyp = models.CharField(max_length=128, blank=True, null=True, verbose_name="Undertyp")
    cdh_category = models.CharField(max_length=16, verbose_name="CDH-Kategori")
    objekt = models.CharField(max_length=128, blank=True, null=True, verbose_name="Objekt")
    namntyp = models.PositiveIntegerField(blank=True, null=True, verbose_name="Namntyp")
    upphovsman = models.CharField(max_length=128, blank=True, null=True, verbose_name="Upphovsperson")
    tid = models.CharField(max_length=128, blank=True, null=True, verbose_name="Tid")
    lk_tid = models.CharField(max_length=128, blank=True, null=True, verbose_name="Tid (lk)")
    dat_min = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Tidigaste datum")
    dat_max = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Senaste datum")
    hojd = models.CharField(max_length=128, blank=True, null=True, verbose_name="Höjd")
    bredd = models.CharField(max_length=128, blank=True, null=True, verbose_name="Bredd")
    material = models.CharField(max_length=128, blank=True, null=True, verbose_name="Material")
    delar = models.CharField(max_length=128, blank=True, null=True, verbose_name="Delar")
    urtappning = models.CharField(max_length=128, blank=True, null=True, verbose_name="Urtappning")
    inskrift = models.CharField(max_length=256, blank=True, null=True, verbose_name="Inskrift")
    kondition = models.CharField(max_length=512, blank=True, null=True, verbose_name="Kondition")
    farg = models.CharField(max_length=256, blank=True, null=True, verbose_name="Färg")
    ovrigt = models.TextField(blank=True, null=True, verbose_name="Övrigt")
    sokord = models.CharField(max_length=512, blank=True, null=True, verbose_name="Sökord")
    motiv = models.TextField(blank=True, null=True, verbose_name="Motiv")
    litteratur = models.TextField(blank=True, null=True, verbose_name="Litteratur")
    status = models.CharField(max_length=128, blank=True, null=True, verbose_name="Status")
    titel = models.CharField(max_length=128, blank=True, null=True, verbose_name="Titel")
    parish = models.ForeignKey('Parish', models.DO_NOTHING, blank=True, null=True, verbose_name="Socken")
    place = models.ForeignKey('Place', models.DO_NOTHING, blank=True, null=True, verbose_name="Plats")

    class Meta:
        managed = False
        db_table = 'object'

    def __str__(self) -> str:
        return f"{self.objekt}, {self.cdh_category}"


class Parish(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    variants = models.CharField(max_length=256, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    diocese = models.CharField(max_length=255, blank=True, null=True)
    diocese_med = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    # origin = models.ManyToManyField('self', related_name='id')
    # parent = models.ManyToManyField('self', related_name='id')
    origin = models.ForeignKey('iconographia.Parish', models.DO_NOTHING, blank=True, null=True)
    parent = models.ForeignKey('iconographia.Parish', models.DO_NOTHING, blank=True, null=True, related_name='parish_id')
    notbefore = models.CharField(max_length=16, blank=True, null=True)
    notafter = models.CharField(max_length=16, blank=True, null=True)
    note_year = models.CharField(max_length=128, blank=True, null=True)
    snid_4 = models.PositiveIntegerField(blank=True, null=True)
    wikidata = models.CharField(max_length=64, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parish'
        verbose_name_plural= 'parishes'

    def __str__(self) -> str:
        return f"{self.name}, {self.diocese}"


class Place(models.Model):
    name = models.CharField(max_length=255)
    type = models.PositiveIntegerField()
    certainty_type = models.CharField(max_length=9)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    # parent = models.ManyToManyField('self')
    parish = models.ForeignKey(Parish, models.DO_NOTHING, blank=True, null=True)
    certainty = models.CharField(max_length=9)
    date_bebr = models.CharField(max_length=64)
    notbefore = models.CharField(max_length=32)
    notafter = models.CharField(max_length=32)
    type_indication = models.CharField(max_length=8)
    note_year = models.CharField(max_length=128)
    wikidata = models.CharField(max_length=64, blank=True, null=True)
    geom = models.GeometryField()
    municipality = models.CharField(max_length=256, blank=True, null=True)
    county = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    exclude = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place'

    def __str__(self) -> str:
        return f"{self.name} in {self.county}, {self.country}"

