from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from dihup.models import BaseModel


# NOTE: This is NOT all the tables. Originally created with inspectdb https://docs.djangoproject.com/en/3.2/howto/legacy-databases/) 
# Not all of the tables are tested. Autom, Photo and Locations are pretty much done.

# TODO Lots of columns should actually be foreign keys (does not have to be enforced by DB to work)
# Check collabels table to get information about:
# - foreign keys => models.ForeignKey
# - labels => verbose_name=_("obj_type"), put actual labels in translation files if translation is wanted
# - help texts => help_text=_("obj_type_help")

class Autom(BaseModel):
    obj_type = models.SmallIntegerField(verbose_name=_("autom_obj_type"))
    loc_nr = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True, db_column="loc_nr")
    loc_sign = models.CharField(max_length=30)
    build1 = models.IntegerField()
    build2 = models.IntegerField()
    build3 = models.IntegerField()
    owner = models.IntegerField()
    date1 = models.CharField(max_length=10)
    date2 = models.CharField(max_length=10, help_text="Denna används om datum är känt")
    date_sign = models.CharField(max_length=4, help_text="Kan vara tomt eller <-->")
    loc_in_bui = models.CharField(max_length=60)
    act_type = models.SmallIntegerField()
    act_info = models.TextField()
    aut_title = models.CharField(max_length=100)
    intro = models.TextField()
    hist_info = models.TextField()
    clock_info = models.TextField()
    case_info = models.TextField()
    no_div = models.SmallIntegerField()
    no_stop = models.SmallIntegerField()
    gen_info = models.TextField()


    class Meta:
        db_table = 'autom'


class Photo(BaseModel):
    list_nr = models.SmallIntegerField(blank=True, null=True)
    displ_stat = models.SmallIntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    tag1 = models.SmallIntegerField(blank=True, null=True)
    tag2 = models.SmallIntegerField(blank=True, null=True)
    tag3 = models.SmallIntegerField(blank=True, null=True)
    tag4 = models.SmallIntegerField(blank=True, null=True)
    tag5 = models.SmallIntegerField(blank=True, null=True)
    tag6 = models.SmallIntegerField(blank=True, null=True)
    tag = models.CharField(max_length=200, blank=True, null=True)
    filename = models.CharField(max_length=100)
    stop_nr = models.IntegerField(blank=True, null=True)
    barrel_nr = models.IntegerField(blank=True, null=True)
    autom_nr = models.ForeignKey(Autom, on_delete=models.SET_NULL, blank=True, null=True, db_column="autom_nr")
    ph_grapher = models.CharField(max_length=50, blank=True, null=True)
    year_da = models.CharField(max_length=10, blank=True, null=True)
    copyright = models.CharField(max_length=150, blank=True, null=True)
    orig_name = models.CharField(max_length=80, blank=True, null=True)
    orig_file = models.CharField(max_length=3)
    ph_design = models.CharField(max_length=200, blank=True, null=True)
    ph_loc = models.CharField(max_length=100, blank=True, null=True)
    ph_folder = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'photo'


class Location(BaseModel):
    country = models.CharField(max_length=50)
    count_info = models.TextField()
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    build_name = models.CharField(max_length=50)
    name_info = models.TextField()
    inter_info = models.TextField()
    loc_info = models.TextField()
    geom = models.GeometryField(spatial_index=True)

    class Meta:
        db_table = 'location'


class Actype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'actype'


class Audio(models.Model):
    filename = models.CharField(max_length=100)
    barrel = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        db_table = 'audio'


class Autdoc(BaseModel):
    nr1 = models.IntegerField()
    nr2 = models.IntegerField()
    info = models.TextField()
    source = models.TextField()

    class Meta:
        db_table = 'autdoc'


class Authist(BaseModel):
    nr1 = models.IntegerField()
    nr2 = models.IntegerField()
    info = models.TextField()
    source = models.TextField()

    class Meta:
        db_table = 'authist'


class Avl(models.Model):
    mus_nr = models.IntegerField()
    tone = models.CharField(max_length=3)
    meas = models.IntegerField()
    ref = models.IntegerField()

    class Meta:
        db_table = 'avl'


class Barmus(BaseModel):
    nr1 = models.IntegerField()
    nr2 = models.IntegerField()
    list_nr = models.IntegerField()

    class Meta:
        db_table = 'barmus'


class Barrel(BaseModel):
    i_nr = models.IntegerField()
    li_nr = models.SmallIntegerField()
    const = models.SmallIntegerField()
    no_piece = models.CharField(max_length=2)
    piece_info = models.TextField()
    lab_note = models.CharField(max_length=200)
    bar_title = models.CharField(max_length=200)
    sec_note = models.CharField(max_length=150)
    diam = models.CharField(max_length=6)
    length = models.CharField(max_length=6)
    mpin_h = models.CharField(max_length=5)
    rpin_h = models.CharField(max_length=5)
    rpin_pos = models.SmallIntegerField()
    dim_uhole = models.CharField(max_length=20)
    dim_dhole = models.CharField(max_length=20)
    mount_mark = models.TextField()
    surf_treat = models.SmallIntegerField()
    strea_info = models.TextField()
    grid = models.CharField(max_length=3)
    grid_info = models.TextField()
    stamp = models.CharField(max_length=3)
    stamp_desc = models.SmallIntegerField()
    stamp_info = models.TextField()
    groove = models.CharField(max_length=3)
    groove_inf = models.TextField()
    bar_info = models.TextField()

    class Meta:
        db_table = 'barrel'


class Barrtype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'barrtype'


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
        db_table = 'col_labels'


class Collection(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'collection'


class CollectionAutom(models.Model):
    collection_id = models.PositiveIntegerField()
    autom_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'collection_autom'


class Constype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'constype'


class Division(BaseModel):
    inst_nr = models.IntegerField()
    l_nr = models.IntegerField()
    so_source = models.SmallIntegerField()
    barr_act = models.SmallIntegerField()
    no_arms = models.SmallIntegerField()
    comp_lo = models.CharField(max_length=50)
    comp_hi = models.CharField(max_length=50)
    comp_com = models.CharField(max_length=50)
    no_tones = models.SmallIntegerField()
    no_reg = models.SmallIntegerField()
    reg_pos = models.SmallIntegerField()
    no_stop = models.SmallIntegerField()
    div_info = models.TextField()

    class Meta:
        db_table = 'division'


class Docfac(BaseModel):
    nr = models.IntegerField()
    list_nr = models.IntegerField()
    f_caption = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    dig_by = models.CharField(max_length=50)
    year_da = models.CharField(max_length=10)
    copyright = models.CharField(max_length=150)
    orig_name = models.CharField(max_length=80)
    fac_loc = models.CharField(max_length=100)
    fac_folder = models.CharField(max_length=100)
    descr = models.TextField()
    comment = models.CharField(max_length=200)

    class Meta:
        db_table = 'docfac'


class Doclink(BaseModel):
    nr = models.IntegerField()
    list_nr = models.SmallIntegerField()
    lname = models.CharField(max_length=100)
    laddr = models.CharField(max_length=200)
    comment = models.TextField()

    class Meta:
        db_table = 'doclink'


class Doctype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'doctype'


class Document(BaseModel):
    subject = models.CharField(max_length=150)
    date1 = models.CharField(max_length=10)
    date2 = models.CharField(max_length=10)
    date_sign = models.CharField(max_length=14)
    country = models.CharField(max_length=30)
    region = models.CharField(max_length=40)
    countr_inf = models.CharField(max_length=254)
    location = models.CharField(max_length=50)
    loc_info = models.CharField(max_length=254)
    parish = models.CharField(max_length=50)
    descr = models.TextField()
    doc_type = models.SmallIntegerField()
    docty_info = models.CharField(max_length=254)
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    doc_text = models.TextField()
    signum = models.CharField(max_length=254)
    signum_inf = models.TextField()
    form = models.SmallIntegerField()

    class Meta:
        db_table = 'document'


class Extlink(BaseModel):
    nr = models.IntegerField()
    list_nr = models.SmallIntegerField()
    lname = models.CharField(max_length=100)
    laddr = models.CharField(max_length=200)
    comment = models.TextField()

    class Meta:
        db_table = 'extlink'


class Formtype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'formtype'


class Functext(models.Model):
    nr = models.SmallAutoField(primary_key=True)
    text_id = models.CharField(max_length=15)
    f_text = models.CharField(max_length=50)
    expln = models.CharField(max_length=254)
    lang = models.CharField(max_length=2)

    class Meta:
        db_table = 'functext'


class Hcomp(models.Model):
    type = models.CharField(primary_key=True, max_length=50)
    expl = models.TextField()

    class Meta:
        db_table = 'hcomp'


class Label(models.Model):
    nr = models.SmallAutoField(primary_key=True)
    text_id = models.CharField(max_length=22)
    f_text = models.CharField(max_length=50)
    expln = models.CharField(max_length=254)
    lang = models.CharField(max_length=2)

    class Meta:
        db_table = 'label'


class Lcomp(models.Model):
    type = models.CharField(primary_key=True, max_length=50)
    expl = models.TextField()

    class Meta:
        db_table = 'lcomp'


class Loclink(BaseModel):
    nr = models.IntegerField()
    list_nr = models.SmallIntegerField()
    lname = models.CharField(max_length=100)
    laddr = models.CharField(max_length=200)
    comment = models.TextField()

    class Meta:
        db_table = 'loclink'


class Media(BaseModel):
    nr = models.IntegerField()
    list_nr = models.SmallIntegerField()
    text = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    media_type = models.SmallIntegerField()
    copyright = models.CharField(max_length=150)
    orig_name = models.CharField(max_length=80)
    m_folder = models.CharField(max_length=100)
    m_info = models.TextField()
    comment = models.TextField()

    class Meta:
        db_table = 'media'


class Met(BaseModel):
    mus_nr = models.IntegerField()
    frekv = models.IntegerField()
    num_tone = models.IntegerField()
    samp_tick = models.IntegerField()
    treshold = models.IntegerField()

    class Meta:
        db_table = 'met'


class Mnote(models.Model):
    note_label = models.CharField(max_length=3)
    midi_note = models.IntegerField()

    class Meta:
        db_table = 'mnote'


class Music(BaseModel):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    comp = models.IntegerField(blank=True, null=True)
    work_no = models.CharField(max_length=40)
    arr = models.IntegerField(blank=True, null=True)
    text = models.TextField()
    auth = models.IntegerField(blank=True, null=True)
    mus_info = models.TextField()

    class Meta:
        db_table = 'music'


class Muslink(BaseModel):
    nr = models.IntegerField()
    list_nr = models.SmallIntegerField()
    lname = models.CharField(max_length=100)
    laddr = models.CharField(max_length=200)
    comment = models.TextField()

    class Meta:
        db_table = 'muslink'


class Notetype(models.Model):
    type = models.CharField(max_length=50)
    expl = models.TextField()

    class Meta:
        db_table = 'notetype'


class Objtype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'objtype'


class Pagetext(models.Model):
    nr = models.SmallAutoField(primary_key=True)
    page_id = models.CharField(max_length=30)
    headline = models.CharField(max_length=150)
    p_text1 = models.TextField()
    p_text2 = models.TextField()
    button1 = models.CharField(max_length=50)
    button2 = models.CharField(max_length=50)
    button3 = models.CharField(max_length=50)
    button4 = models.CharField(max_length=50)
    button5 = models.CharField(max_length=50)
    button6 = models.CharField(max_length=50)
    lang = models.CharField(max_length=2)

    class Meta:
        db_table = 'pagetext'


class Persdoc(BaseModel):
    nr1 = models.IntegerField()
    nr2 = models.IntegerField()
    info = models.TextField()
    source = models.TextField()

    class Meta:
        db_table = 'persdoc'


class Perslink(BaseModel):
    nr = models.IntegerField()
    list_nr = models.SmallIntegerField()
    lname = models.CharField(max_length=100)
    laddr = models.CharField(max_length=200)
    comment = models.TextField()

    class Meta:
        db_table = 'perslink'


class Person(BaseModel):
    fam_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=30)
    famn_info = models.CharField(max_length=100)
    firn_info = models.CharField(max_length=100)
    prof1 = models.SmallIntegerField()
    prof2 = models.SmallIntegerField()
    prof3 = models.SmallIntegerField()
    prof4 = models.SmallIntegerField()
    bdate1 = models.CharField(max_length=10)
    bdate2 = models.CharField(max_length=10)
    bdate_sign = models.CharField(max_length=8)
    bcountry = models.CharField(max_length=30)
    bregion = models.CharField(max_length=40)
    bcoreg_inf = models.CharField(max_length=254)
    bplace = models.CharField(max_length=50)
    bplace_inf = models.CharField(max_length=254)
    ddate1 = models.CharField(max_length=10)
    ddate2 = models.CharField(max_length=10)
    ddate_sign = models.CharField(max_length=16)
    dcountry = models.CharField(max_length=30)
    dregion = models.CharField(max_length=40)
    dcoreg_inf = models.CharField(max_length=254)
    dplace = models.CharField(max_length=50)
    dplace_inf = models.CharField(max_length=254)
    biogr = models.TextField()
    source = models.TextField()
    lit = models.TextField()
    int_info = models.TextField()

    class Meta:
        db_table = 'person'


class Photoautom(models.Model):
    photo = models.IntegerField()
    autom = models.IntegerField()
    list_nr = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'photoautom'


class Photobarrel(models.Model):
    photo = models.IntegerField()
    barrel = models.IntegerField()
    list_nr = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'photobarrel'


class Photostop(models.Model):
    photo = models.IntegerField()
    stop = models.IntegerField()
    list_nr = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'photostop'


class Pinpostype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'pinpostype'


class Proftype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'proftype'


class Regpostype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'regpostype'


class SimilarAutom(models.Model):
    instr_id = models.IntegerField()
    similar_instr_id = models.IntegerField()
    updated = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'similar_autom'


class Soundtype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'soundtype'


class Stamptype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'stamptype'


class Stop(BaseModel):
    nr = models.IntegerField()
    list_nr = models.SmallIntegerField()
    stop_name = models.CharField(max_length=50)
    stop_type = models.SmallIntegerField()
    stop_mat = models.SmallIntegerField()
    stop_con = models.SmallIntegerField()
    stop_size = models.CharField(max_length=15)
    pos_chest = models.SmallIntegerField()
    stop_pos = models.SmallIntegerField()
    stop_info = models.TextField()

    class Meta:
        db_table = 'stop'


class Stopcon(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'stopcon'


class Stopmat(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'stopmat'


class Stopname(models.Model):
    type = models.CharField(primary_key=True, max_length=50)
    expl = models.TextField()

    class Meta:
        db_table = 'stopname'


class Stoppos(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'stoppos'


class Stoptype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'stoptype'


class Tagtype(models.Model):
    type_nr = models.SmallIntegerField()
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'tagtype'


class Tone(BaseModel):
    m_nr = models.IntegerField()
    tone_nr = models.IntegerField()
    note_lab = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'tone'


class Treatype(models.Model):
    type = models.CharField(max_length=60)
    expl = models.TextField()

    class Meta:
        db_table = 'treatype'
