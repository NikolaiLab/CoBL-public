from django.db import models

class Source(models.Model):

    TYPE_CHOICES = (
            ("P", "Publication"),
            ("U", "URL"),
            ("E", "Expert"),
            )
    RELIABILITY_CHOICES = ( # used by Citation classes
            #("X", "Unclassified"), # change "X" to "" will force users to make
            ("A", "High"),         # a selection upon seeing this form
            ("B", "Good, but needs checking by an expert"),
            ("C", "Doubtful"),
            )
    citation_text = models.TextField()
    type_code = models.CharField(max_length=1, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["type_code", "citation_text"]

class Language(models.Model):
    iso_code = models.CharField(max_length=3)
    ascii_name = models.CharField(max_length=999)
    utf8_name = models.CharField(max_length=999)
    sort_key = models.IntegerField(null=True, unique=True)

    def __unicode__(self):
        return self.ascii_name

    class Meta:
        ordering = ["sort_key", "utf8_name"]

class DyenName(models.Model):
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=999)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Meaning(models.Model):
    gloss = models.CharField(max_length=64) # one word name
    description = models.CharField(max_length=64) # show name
    notes = models.TextField()

    def __unicode__(self):
        return self.gloss.upper()

    class Meta:
        ordering = ["gloss"]

class CognateSet(models.Model):
    alias = models.CharField(max_length=3)
    notes = models.TextField()
    modified = models.DateTimeField(auto_now=True)

    # def _get_meaning_set(self):
    #     return set([cj.lexeme.meaning for cj in self.cognatejudgement_set.all()])
    # meaning_set = property(_get_meaning_set)

    # def _get_meaning(self):
    #     """This will cause problems when/if the database has cognate sets
    #     providing reflexes for more than one meaning"""
    #     return self._get_meaning_set().pop()
    # meaning = property(_get_meaning) # treat as an attribute

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        ordering = ["alias"]

class Lexeme(models.Model):
    language = models.ForeignKey(Language)
    meaning = models.ForeignKey(Meaning)
    cognate_class = models.ManyToManyField(CognateSet,
            through="CognateJudgement")
    source_form = models.CharField(max_length=999)
    phon_form = models.CharField(max_length=999)
    gloss = models.CharField(max_length=999)
    notes = models.TextField()
    source = models.ManyToManyField(Source, through="LexemeCitation")
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.phon_form or self.source_form or "Lexeme"

    class Meta:
        order_with_respect_to = "language"

class CognateJudgement(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    cognate_class = models.ForeignKey(CognateSet)
    source = models.ManyToManyField(Source, through="CognateJudgementCitation")
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.id)

class LanguageList(models.Model):
    """A named, ordered list of languages for use in display and output. A
    default list, named 'all' is (re)created on save/delete of the Language
    table (cf. ielex.models.update_language_list_all)"""
    name = models.CharField(max_length=999)
    language_ids = models.CommaSeparatedIntegerField(max_length=999)
    modified = models.DateTimeField(auto_now=True)

    def _get_list(self):
        return [int(i) for i in self.language_ids.split(",")]
    def _set_list(self, listobj):
        self.language_ids = ",".join([str(i) for i in listobj])
        return
    language_id_list = property(_get_list, _set_list)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class CognateJudgementCitation(models.Model):
    cognate_judgement = models.ForeignKey(CognateJudgement)
    source = models.ForeignKey(Source)
    pages = models.CharField(max_length=999)
    reliability = models.CharField(max_length=1, choices=Source.RELIABILITY_CHOICES)
    comment = models.CharField(max_length=999)
    modified = models.DateTimeField(auto_now=True)

class LexemeCitation(models.Model):
    lexeme = models.ForeignKey(Lexeme)
    source = models.ForeignKey(Source)
    pages = models.CharField(max_length=999)
    reliability = models.CharField(max_length=1, choices=Source.RELIABILITY_CHOICES)
    comment = models.CharField(max_length=999)
    modified = models.DateTimeField(auto_now=True)



def update_language_list_all(sender, instance, **kwargs):
    """Update the LanguageList 'all' whenever Language objects are saved or
    deleted"""
    # it should just be when created or deleted, but the extra overhead is
    # tiny, since changes in the Language table are rare
    try:
        ll = LanguageList.objects.get(name="all")
    except:
        ll = LanguageList.objects.create(name="all")
    ll.language_id_list = [l.id for l in Language.objects.all()]
    ll.save(force_update=True)
    return
models.signals.post_save.connect(update_language_list_all, sender=Language)
models.signals.post_delete.connect(update_language_list_all, sender=Language)
