# NOTE: This is NOT the real models, only a test set
# inspectdb (https://docs.djangoproject.com/en/3.2/howto/legacy-databases/) should probably be rerun and the models fixed

from django.db import models
from django.db.models import options
from django.utils.translation import gettext_lazy as _
from dihup.models import BaseModel


options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('label_fields',)

CERTAINTIES = (
    ('Unknown', 'Uknown'),
    ('Uncertain', 'Uncertain'),
    ('Certain', 'Certain'),
)

YESNO = (
    ('No', 'No'),
    ('Yes', 'Yes'),
)


class NameModel(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Cult(models.Model):
    place = models.ForeignKey('Place', models.RESTRICT, null=True)
    place_unc = models.CharField(max_length=3, blank=True, null=True, choices=YESNO)
    placement = models.CharField(max_length=128)
    placem_unc = models.CharField(max_length=3, blank=True, null=True, choices=YESNO)
    persons = models.ManyToManyField('Person', related_name='cults', through='RelCultPerson')
    parent = models.ForeignKey('self', models.SET_NULL, related_name='children', null=True)
    assoc = models.ForeignKey('self', models.SET_NULL, null=True)
    area = models.ForeignKey('CultArea', models.RESTRICT, null=True)
    type = models.ForeignKey('CultType', models.RESTRICT, null=True)
    type_unc = models.CharField(max_length=3, blank=True, null=True, choices=YESNO)
    feastday = models.CharField(max_length=16)
    notbefore = models.CharField(max_length=32)
    notafter = models.CharField(max_length=32)
    time_period = models.CharField(max_length=32)
    date_note = models.CharField(max_length=128)
    notes = models.TextField(blank=True, null=True)
    article = models.TextField(blank=True, null=True)
    updated = models.DateField(blank=True, null=True)
    version = models.PositiveIntegerField()
    created = models.CharField(max_length=64)
    modified = models.CharField(max_length=64)

    class Meta:
        db_table = 'cult'
        verbose_name = _('cult manifestation')
        verbose_name_plural = _('cult manifestations')
        # Our custom autocomplete view uses this.
        label_fields = ['place__name', 'type__name']

    def __str__(self):
        # TODO Handle id = 0 better (migrate? override models.ForeignKey?)
        return f"{self.type if self.type_id else '?'} at {self.place if self.place_id else '?'}"


class CultArea(models.Model):
    name = models.CharField(max_length=64)
    name_sv = models.CharField(max_length=64)

    class Meta:
        db_table = 'cult_area'

    def __str__(self):
        return self.name


class CultType(models.Model):
    name = models.CharField(max_length=64)
    name_sv = models.CharField(max_length=64)
    aat_code = models.CharField(max_length=32)

    class Meta:
        db_table = 'cult_type'

    def __str__(self):
        return self.name


class Parish(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    variants = models.CharField(max_length=256, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    diocese = models.CharField(max_length=255, blank=True, null=True)
    org_id = models.PositiveIntegerField(blank=True, null=True)
    diocese_med = models.CharField(max_length=255, blank=True, null=True)
    med_org_id = models.PositiveIntegerField(blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    origin_id = models.PositiveIntegerField(blank=True, null=True)
    parent_id = models.PositiveIntegerField(blank=True, null=True)
    notbefore = models.CharField(max_length=16, blank=True, null=True)
    notafter = models.CharField(max_length=16, blank=True, null=True)
    note_year = models.CharField(max_length=128, blank=True, null=True)
    snid_4 = models.PositiveIntegerField(blank=True, null=True)
    wikidata = models.CharField(max_length=64, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    article = models.TextField(blank=True, null=True)
    updated = models.DateField(blank=True, null=True)
    version = models.PositiveIntegerField()
    created = models.CharField(max_length=64)
    modified = models.CharField(max_length=64)

    class Meta:
        db_table = 'parish'
        verbose_name_plural = 'parishes'

    def __str__(self):
        return self.name


class ParishName(models.Model):
    parish = models.ForeignKey(Parish, models.DO_NOTHING, blank=True, null=True)
    lang = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    notbefore = models.CharField(max_length=64, blank=True, null=True)
    updated = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'parish_name'


class Person(BaseModel, NameModel):
    sex = models.CharField(max_length=5, blank=True, null=True)
    type = models.CharField(max_length=5, blank=True, null=True)
    type_alive = models.ForeignKey('PersonTypeAlive', models.SET_NULL, null=True)
    iconclass = models.CharField(max_length=64, blank=True, null=True)
    wikidata = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=64)
    notbefore = models.CharField(max_length=64)
    name_sv = models.CharField(max_length=64, blank=True, null=True)
    name_la = models.CharField(max_length=64, blank=True, null=True)
    old_sw = models.CharField(max_length=64, blank=True, null=True)
    early_sw = models.CharField(max_length=64, blank=True, null=True)
    feastday = models.CharField(max_length=64, blank=True, null=True)
    attributes = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    article = models.TextField(blank=True, null=True)
    updated = models.DateField(blank=True, null=True)
    version = models.PositiveIntegerField()
    created = models.CharField(max_length=64)
    modified = models.CharField(max_length=64)

    class Meta:
        db_table = 'person'


class PersonName(models.Model):
    person_id = models.PositiveIntegerField(blank=True, null=True)
    lang = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    notbefore = models.CharField(max_length=64, blank=True, null=True)
    updated = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'person_name'


class PersonTypeAlive(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    name_sv = models.CharField(max_length=64, blank=True, null=True)
    updated = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'person_type_alive'

    def __str__(self):
        return self.name
    

class Place(BaseModel):
    TYPE_INDICATIONS = (
        ('Artefact', 'Artefact'),
        ('Written', 'Written'),
        ('Oral', 'Oral'),
    )

    name = models.CharField(max_length=255, help_text='The name of the place')
    variants = models.CharField(max_length=256, null=True)
    # By default, Django expects a ForeignKey field named "(name)" to use a db column named "(name)_id"
    # If the column does not end with "_id", correct it with `db_column=(name)`
    type = models.ForeignKey('PlaceType', models.SET_NULL, db_column='type', null=True)
    certainty_type = models.CharField(max_length=9, choices=CERTAINTIES)
    parent = models.ForeignKey('Place', models.SET_NULL, related_name='children', null=True)
    parish = models.ForeignKey('Parish', models.SET_NULL, null=True)
    certainty = models.CharField(max_length=9, choices=CERTAINTIES)
    # date_bebr = models.CharField(max_length=64, null=True, editable=False)
    notbefore = models.CharField(max_length=32, null=True)
    notafter = models.CharField(max_length=32, null=True)
    type_indication = models.CharField(max_length=8, blank=True, null=True, choices=TYPE_INDICATIONS)
    note_year = models.CharField(max_length=128, null=True)
    # bebr = models.ForeignKey('Bebr', models.SET_NULL, null=True, editable=False)
    # fmis = models.ForeignKey('Fmis', models.SET_NULL, null=True, editable=False)
    wikidata = models.CharField(max_length=64, blank=True, null=True)
    # geom = models.TextField()  # This field type is a guess.
    municipality = models.CharField(max_length=256, blank=True, null=True)
    county = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    article = models.TextField(blank=True, null=True)
    exclude = models.CharField(max_length=3, default="No", choices=(('Yes', 'Yes'), ('No', 'No')))

    class Meta:
        db_table = 'place'
        ordering = ['name']
        verbose_name = _('place')
        verbose_name_plural = _('places')
        # Our custom autocomplete view uses this.
        label_fields = ['name']

    def __str__(self):
        return f'{self.name}'


class PlaceName(models.Model):
    place_id = models.ForeignKey('Place', models.SET_NULL, null=True, db_column="place_id")
    lang = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    notbefore = models.CharField(max_length=64, blank=True, null=True)
    updated = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'place_name'


class PlaceType(models.Model):
    name = models.CharField(max_length=64)
    name_sv = models.CharField(max_length=64)

    class Meta:
        db_table = 'place_type'

    def __str__(self):
        return self.name


class RelCultPerson(models.Model):
    cult = models.ForeignKey('Cult', models.CASCADE)
    pers = models.ForeignKey('Person', models.CASCADE)
    pers_unc = models.CharField(max_length=3, blank=True, null=True, choices=YESNO)
    pers_alt = models.CharField(max_length=3, blank=True, null=True, choices=YESNO)
    updated = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'rel_cult_person'
