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
    objektid = models.CharField(max_length=128, blank=True, null=True)
    main_image = models.ForeignKey(Image, models.DO_NOTHING, db_column='main_image')
    museum = models.CharField(max_length=128, blank=True, null=True)
    inventarienummer = models.CharField(max_length=128, blank=True, null=True)
    undernummer = models.CharField(max_length=128, blank=True, null=True)
    invnr = models.CharField(max_length=128, blank=True, null=True)
    landskap = models.CharField(max_length=128, blank=True, null=True)
    ort = models.CharField(max_length=128, blank=True, null=True)
    sakord = models.CharField(max_length=128, blank=True, null=True)
    typ = models.CharField(max_length=128, blank=True, null=True)
    undertyp = models.CharField(max_length=128, blank=True, null=True)
    cdh_category = models.CharField(max_length=16)
    objekt = models.CharField(max_length=128, blank=True, null=True)
    namntyp = models.PositiveIntegerField(blank=True, null=True)
    upphovsman = models.CharField(max_length=128, blank=True, null=True)
    tid = models.CharField(max_length=128, blank=True, null=True)
    lk_tid = models.CharField(max_length=128, blank=True, null=True)
    dat_min = models.PositiveSmallIntegerField(blank=True, null=True)
    dat_max = models.PositiveSmallIntegerField(blank=True, null=True)
    hojd = models.CharField(max_length=128, blank=True, null=True)
    bredd = models.CharField(max_length=128, blank=True, null=True)
    material = models.CharField(max_length=128, blank=True, null=True)
    delar = models.CharField(max_length=128, blank=True, null=True)
    urtappning = models.CharField(max_length=128, blank=True, null=True)
    inskrift = models.CharField(max_length=256, blank=True, null=True)
    kondition = models.CharField(max_length=512, blank=True, null=True)
    farg = models.CharField(max_length=256, blank=True, null=True)
    ovrigt = models.TextField(blank=True, null=True)
    sokord = models.CharField(max_length=512, blank=True, null=True)
    motiv = models.TextField(blank=True, null=True)
    litteratur = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)
    titel = models.CharField(max_length=128, blank=True, null=True)
    parish = models.ForeignKey('Parish', models.DO_NOTHING, blank=True, null=True)
    place = models.ForeignKey('Place', models.DO_NOTHING, blank=True, null=True)

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

