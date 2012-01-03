from __future__ import division
from string import uppercase, lowercase
from django.db import models
from django.db.models import Max, F
from django.core.urlresolvers import reverse
## from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import connection, transaction ### testing
# from django.contrib import admin
import reversion
from reversion.errors import RegistrationError
# from reversion.admin import VersionAdmin
from ielex.lexicon.validators import *

TYPE_CHOICES = (
        ("P", "Publication"),
        ("U", "URL"),
        ("E", "Expert"),
        )

RELIABILITY_CHOICES = ( # used by Citation classes
        #("X", "Unclassified"), # change "X" to "" will force users to make
        ("A", "High"),         # a selection upon seeing this form
        ("B", "Good (e.g. should be double checked)"),
        ("C", "Doubtful"),
        ("L", "Loanword"),
        ("X", "Exclude (e.g. not the Swadesh term)"),
        )

class Source(models.Model):

    citation_text = models.TextField(unique=True)
    type_code = models.CharField(max_length=1, choices=TYPE_CHOICES,
            default="P")
    description = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/source/%s/" % self.id

    def __unicode__(self):
        return self.citation_text[:64]

    class Meta:
        ordering = ["type_code", "citation_text"]

class Language(models.Model):
    iso_code = models.CharField(max_length=3, blank=True)
    ascii_name = models.CharField(max_length=999, unique=True,
            validators=[suitable_for_url])
    utf8_name = models.CharField(max_length=999, unique=True)
    sort_key = models.FloatField(null=True, blank=True, editable=False)
    description = models.TextField(blank=True, null=True)

    language_list_name = None

    def get_absolute_url(self):
        return "/language/%s/" % self.ascii_name

    def __unicode__(self):
        return self.utf8_name

    class Meta:
        ordering = ["ascii_name"]

class DyenName(models.Model):
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=999)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Meaning(models.Model):
    gloss = models.CharField(max_length=64, validators=[suitable_for_url])
    description = models.CharField(max_length=64, blank=True) # show name
    notes = models.TextField(blank=True)
    percent_coded = models.FloatField(editable=False)

    def get_absolute_url(self):
        return "/meaning/%s/" % self.gloss

    def set_percent_coded(self):
        uncoded = self.lexeme_set.filter(cognate_class=None).count()
        total = self.lexeme_set.filter().count()
        try:
            self.percent_coded = 100.0 * (total - uncoded) / total
        except ZeroDivisionError:
            self.percent_coded = 0
        self.save()
        return

    def __unicode__(self):
        return self.gloss.upper()

    class Meta:
        ordering = ["gloss"]

class CognateClass(models.Model):
    alias = models.CharField(max_length=3)
    notes = models.TextField()
    modified = models.DateTimeField(auto_now=True)

    def update_alias(self, save=True):
        """Reset alias to the first unused letter"""
        codes = set(uppercase) | set([i+j for i in uppercase for j in
            lowercase])
        meanings = Meaning.objects.filter(lexeme__cognate_class=self).distinct()
        current_aliases = CognateClass.objects.filter(
                lexeme__meaning__in=meanings).distinct().exclude(
                id=self.id).values_list("alias", flat=True)
        codes -= set(current_aliases)
        self.alias = sorted(codes, key=lambda i:(len(i), i))[0]
        if save:
            self.save()
        return

    def get_meanings(self):
        # some cognate classes have more than one meaning, e.g. "right" ~
        # "rightside", "in" ~ "at"
        meanings = Meaning.objects.filter(lexeme__cognate_class=self).distinct()
        return meanings

    def get_meaning(self):
        # for nexus files it doesn't matter what gloss we use, so long as there
        # is only one per cognate set
        try:
            return self.get_meanings().order_by("gloss")[0]
        except IndexError:
            return None

    def get_absolute_url(self):
        return "/cognate/%s/" % self.id

    def __unicode__(self):
        return "CognateClass %s" % self.id

    class Meta:
        ordering = ["alias"]

class DyenCognateSet(models.Model):
    cognate_class = models.ForeignKey(CognateClass)
    name = models.CharField(max_length=8)
    doubtful = models.BooleanField(default=0)

    def __unicode__(self):
        if self.doubtful:
            qmark = " ?"
        else:
            qmark =""
        return "%s%s" % (self.name, qmark)

class Lexeme(models.Model):
    language = models.ForeignKey(Language)
    meaning = models.ForeignKey(Meaning, blank=True, null=True)
    cognate_class = models.ManyToManyField(CognateClass,
            through="CognateJudgement", blank=True)
    source_form = models.CharField(max_length=999)
    phon_form = models.CharField(max_length=999, blank=True)
    gloss = models.CharField(max_length=999, blank=True)
    notes = models.TextField(blank=True)
    source = models.ManyToManyField(Source, through="LexemeCitation",
            blank=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/lexeme/%s/" % self.id

    def __unicode__(self):
        return self.phon_form or self.source_form or ("Lexeme %s" % self.id)

    class Meta:
        order_with_respect_to = "language"

class CognateJudgement(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    cognate_class = models.ForeignKey(CognateClass)
    source = models.ManyToManyField(Source, through="CognateJudgementCitation")
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/meaning/%s/%s/%s/" % (self.lexeme.meaning.gloss,
                self.lexeme.id, self.id)

    @property
    def reliability_ratings(self):
        return set(self.cognatejudgementcitation_set.values_list("reliability", flat=True))

    @property
    def long_reliability_ratings(self):
        """An alphabetically sorted list of (rating_code, description) tuples"""
        descriptions = dict(RELIABILITY_CHOICES)
        return [(rating, descriptions[rating]) for rating in sorted(self.reliability_ratings)]

    @property
    def is_loanword(self):
        # only calculate this value if it hasn't been worked out recently
        ## -- disable cache
        ## key = "is_loanword_%s" % self.lexeme.id
        ## is_loanword = cache.get(key)
        ## try:
        ##     assert is_loanword is not None
        ## except AssertionError:
        ##     is_loanword = "L" in self.reliability_ratings
        ##     cache.set(key, is_loanword, 300)
        is_loanword = "L" in self.reliability_ratings
        return is_loanword

    def __unicode__(self):
        return u"%s-%s-%s" % (self.lexeme.meaning.gloss,
                self.cognate_class.alias, self.id)

def update_meaning_percent_coded(sender, instance, **kwargs):
    instance.lexeme.meaning.set_percent_coded()
    return

models.signals.post_save.connect(update_meaning_percent_coded,
        sender=CognateJudgement)

class LanguageList(models.Model):
    """A named, ordered list of languages for use in display and output. A
    default list, named 'all' is (re)created on save/delete of the Language
    table (cf. ielex.models.update_language_list_all)

    To get an order list of language from LanguageList `ll`::

        ll.languages.all().order_by("languagelistorder")

    # TODO how can I make this the default ordering?
    """
    DEFAULT = "all"

    name = models.CharField(max_length=999, validators=[suitable_for_url])
    description = models.TextField(blank=True, null=True)
    languages = models.ManyToManyField(Language, through="LanguageListOrder")
    modified = models.DateTimeField(auto_now=True)

    def append(self, language):
        """Add another language to the end of a LanguageList ordering"""
        N = self.languagelistorder_set.aggregate(Max("order")).values()[0]
        try:
            N += 1
        except TypeError:
            assert N is None
            N = 0
        LanguageListOrder.objects.create(
                language=language,
                language_list=self,
                order=N)
        return

    def insert(self, N, language):
        """Insert another language into a LanguageList ordering at position N"""
        llo = LanguageListOrder.objects.get(
                language=language,
                language_list=self)
        target = self.languagelistorder_set.all()[N]
        llo.order = target.order - 0.0001
        llo.save()
        return

    def sequentialize(self):
        """Sequentialize the order fields of a LanguageListOrder set
        with a separation of approximately 1.0.  This is a bit slow, so
        it should only be done from time to time."""
        count = self.languagelistorder_set.count()
        def jitter(N, N_list):
            """Return a number close to N such that N is not in N_list"""
            while True:
                try:
                    assert N not in N_list
                    return N
                except AssertionError:
                    N += 0.0001
            return
        if count:
            order_floats = self.languagelistorder_set.values_list("order", flat=True)
            for i, llo in enumerate(self.languagelistorder_set.all()):
                if i != llo.order:
                    llo.order = jitter(i, order_floats)
                    llo.save()
        return

    def swap(self, languageA, languageB):
        """Swap the order of two languages"""
        orderA = LanguageListOrder.objects.get(
                language=languageA,
                language_list=self)
        orderB = LanguageListOrder.objects.get(
                language=languageB,
                language_list=self)
        orderB.delete()
        orderA.order, orderB.order = orderB.order, orderA.order
        orderA.save()
        orderB.save()
        return

    def get_absolute_url(self):
        return "/languages/%s/" % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class LanguageListOrder(models.Model):

    language = models.ForeignKey(Language)
    language_list = models.ForeignKey(LanguageList)
    order = models.FloatField()

    def __unicode__(self):
        return u"%s:%s(%s)" % (self.language_list.name, 
                self.order,
                self.language.ascii_name)

    class Meta:
        ordering = ["order"]
        unique_together = (("language_list", "language"),
                ("language_list", "order"))

class MeaningList(models.Model):
    """Named lists of meanings, e.g. 'All' and 'Swadesh_100'"""
    DEFAULT = "all"

    name = models.CharField(max_length=999, validators=[suitable_for_url])
    description = models.TextField(blank=True, null=True)
    meaning_ids = models.CommaSeparatedIntegerField(max_length=999)
    modified = models.DateTimeField(auto_now=True)

    def _get_list(self):
        try:
            return [int(i) for i in self.meaning_ids.split(",")]
        except ValueError:
            return []
    def _set_list(self, listobj):
        self.meaning_ids = ",".join([str(i) for i in listobj])
        return
    meaning_id_list = property(_get_list, _set_list)

    def get_absolute_url(self):
        return "/meanings/%s/" % self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class GenericCitation(models.Model):
    # This would have been a good way to do it, but it's going to be too
    # difficult to convert the ManyToMany fields in the current models to use
    # this instead of the old classes.
    source = models.ForeignKey(Source)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type',
                    'object_id')
    pages = models.CharField(max_length=999)
    reliability = models.CharField(max_length=1, choices=RELIABILITY_CHOICES)
    comment = models.CharField(max_length=999)
    modified = models.DateTimeField(auto_now=True)

    def long_reliability(self):
        try:
            description = dict(RELIABILITY_CHOICES)[self.reliability]
        except KeyError:
            description = ""
        return description

    class Meta:
        unique_together = (("content_type", "object_id", "source"),)
        ## Can't use a "content_object" in a unique_together constraint

# reversion.register(GenericCitation)

class AbstractBaseCitation(models.Model):
    """Abstract base class for citation models
    The source field has to be in the subclasses in order for the
    unique_together constraints to work properly"""
    pages = models.CharField(max_length=999, blank=True)
    reliability = models.CharField(max_length=1, choices=RELIABILITY_CHOICES)
    comment = models.CharField(max_length=999, blank=True)
    modified = models.DateTimeField(auto_now=True)

    def long_reliability(self):
        try:
            description = dict(RELIABILITY_CHOICES)[self.reliability]
        except KeyError:
            description = ""
        return description

    class Meta:
        abstract = True


class CognateJudgementCitation(AbstractBaseCitation):
    cognate_judgement = models.ForeignKey(CognateJudgement)
    source = models.ForeignKey(Source)

    def get_absolute_url(self):
        return reverse("cognate-judgement-citation-detail",
                kwargs={"pk":self.id})

    def __unicode__(self):
        return u"CJC src=%s cit=%s" % (self.source.id, self.id)

    class Meta:

        unique_together = (("cognate_judgement", "source"),)


class LexemeCitation(AbstractBaseCitation):
    lexeme = models.ForeignKey(Lexeme)
    source = models.ForeignKey(Source)

    def get_absolute_url(self):
        return "/lexeme/citation/%s/" % self.id

    def __unicode__(self):
        return u"%s %s src:%s" % (self.id, self.lexeme.source_form, self.source.id)

    class Meta:
        unique_together = (("lexeme", "source"),)

class CognateClassCitation(AbstractBaseCitation):
    cognate_class = models.ForeignKey(CognateClass)
    source = models.ForeignKey(Source)

    def __unicode__(self):
        return u"%s cog=%s src=%s" % (self.id, self.cognate_class.id,
                self.source.id)

    def get_absolute_url(self):
        return reverse("cognate-class-citation-detail",
                kwargs={"pk":self.id})

    class Meta:
        unique_together = (("cognate_class", "source"),)

def update_language_list_all(sender, instance, **kwargs):
    """Update the LanguageList 'all' whenever Language table is changed"""
    ll, _ = LanguageList.objects.get_or_create(name=LanguageList.DEFAULT)
    ll.sequentialize()

    missing_langs = set(Language.objects.all()) - set(ll.languages.all())
    for language in missing_langs:
        ll.append(language)

    # make alphabetized list
    default_alpha = LanguageList.DEFAULT+"-alpha"
    try: # zap the old one
        ll_alpha = LanguageList.objects.get(name=default_alpha)
        ll_alpha.delete()
    except LanguageList.DoesNotExist:
        pass
    ll_alpha = LanguageList.objects.create(name=default_alpha)
    for language in Language.objects.all().order_by("ascii_name"):
        ll_alpha.append(language)
    return

models.signals.post_save.connect(update_language_list_all, sender=Language)
models.signals.post_delete.connect(update_language_list_all, sender=Language)

def update_meaning_list_all(sender, instance, **kwargs):
    ml, _ = MeaningList.objects.get_or_create(name=MeaningList.DEFAULT)
    missing_ids = set(Meaning.objects.values_list("id", flat=True)) - set(ml.meaning_id_list)
    if missing_ids:
        ml.meaning_id_list = sorted(missing_ids) + ml.meaning_id_list
        ml.save(force_update=True)

    # make alphabetized list
    default_alpha = MeaningList.DEFAULT+"-alpha"
    ids = [i for n, i in sorted([(n.lower(), i) for n, i
        in Meaning.objects.values_list("gloss", "id")])]
    ml_alpha, _ = MeaningList.objects.get_or_create(name=default_alpha)
    ml_alpha.meaning_id_list = ids
    ml_alpha.save(force_update=True)
    return

models.signals.post_save.connect(update_meaning_list_all, sender=Meaning)
models.signals.post_delete.connect(update_meaning_list_all, sender=Meaning)

# -- Reversion registration ----------------------------------------

for modelclass in [Source, Language, Meaning, CognateClass, Lexeme,
        CognateJudgement, LanguageList, LanguageListOrder,
        CognateJudgementCitation, CognateClassCitation, LexemeCitation,
        MeaningList]:
    try:
        reversion.register(modelclass)
    except RegistrationError, e:
        if "has already been registered" in e.message:
            pass
        else:
            raise

