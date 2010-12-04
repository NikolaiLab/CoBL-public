from django.conf.urls.defaults import *
from ielex.views import *
from ielex import settings
from ielex.lexicon.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# additional arguments can be passed with a dictionary

urlpatterns = patterns('',
    # Front Page
    url(r'^$', view_frontpage, name="view-frontpage"),
    url(r'^backup/$', make_backup),
    url(r'^changes/$', view_changes, name="view-changes"),
    # url(r'^touch/(?P<model_name>[a-zA-Z0-9_ ]+)/(?P<model_id>\d+)/', touch),

    # Languages
    url(r'^languages/$', view_language_list, name="view-languages"),
    url(r'^languages/reorder/$', view_language_reorder, name="language-reorder"),
    url(r'^languages/add-new/$', view_language_add_new, name="language-add-new"),
    url(r'^languages/sort/(?P<ordered_by>sort_key|utf8_name)/$', sort_languages,
            name="language-sort"),
    # TODO add something to edit language_list descriptions

    # Language
    url(r'^language/([a-zA-Z0-9_ -]+)/$', report_language,
            name="language-report"), # usage {% url language-report English %}
    url(r'^language/(?P<language>[a-zA-Z0-9_ -]+)/edit/$', edit_language,
            name="language-edit"),
    url(r'^language/(?P<language>[a-zA-Z0-9_ -]+)/add-lexeme/',
            lexeme_add, {"return_to":"/language/%(language)s/"}),
    url(r'^language/(?P<language>[a-zA-Z0-9_ -]+)/add-lexeme/(?P<meaning>[a-zA-Z0-9_ ]+)/',
            lexeme_add, {"return_to":"/language/%(language)s/"}),

    # Meanings
    url(r'^meanings/$', view_meanings, name="view-meanings"),
    url(r'^meanings/add-new/$', view_meaning_add_new, name="meaning-add-new"), # NEW
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+)/edit/$', edit_meaning,
            name="meaning-edit"), # NEW

    # Meaning
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+)/add-lexeme/$', lexeme_add,
            {"return_to":"/meaning/%(meaning)s/"}),
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+|\d+)/$', report_meaning,
            name="meaning-report"),
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+|\d+)/add/$', report_meaning,
            name="meaning-add-lexeme"),
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+|\d+)/(?P<lexeme_id>\d+)/$',
            report_meaning, {"action":"goto"}),
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+|\d+)/(?P<lexeme_id>\d+)/add/$',
            report_meaning, {"action":"add"}),
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+|\d+)/(?P<lexeme_id>\d+)/(?P<cogjudge_id>\d+)/$',
            report_meaning),
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+|\d+)/add-lexeme/',
            lexeme_add, {"return_to":"/meaning/%(meaning)s/"}),
    url(r'^meaning/(?P<meaning>[a-zA-Z0-9_ ]+|\d+)/add-lexeme/(?P<language>[a-zA-Z0-9_ ]+)/',
            lexeme_add, {"return_to":"/meaning/%(meaning)s/"}),

    # Lexemes
    url(r'^lexeme/add/', lexeme_add, {"return_to":"/meanings/"}),
    url(r'^lexeme/search/$', search_lexeme, name="search-lexeme"),

    url(r'^lexeme/(?P<lexeme_id>\d+)/duplicate/$', lexeme_duplicate),
    url(r'^lexeme/(?P<lexeme_id>\d+)/$',
            view_lexeme, name="view-lexeme"),
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>add-citation|edit-lexeme|add-cognate|add-new-citation)/$',
            edit_lexeme),
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>edit-citation|delink-citation)/(?P<citation_id>\d+)/$',
            edit_lexeme),
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>delink-cognate)/(?P<cogjudge_id>\d+)/$',
            edit_lexeme),
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>edit-cognate-citation)/(?P<citation_id>\d+)/$',
            edit_lexeme), # just use <cogjudge_id>
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>delink-cognate-citation)/(?P<citation_id>\d+)/$',
            edit_lexeme),
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>add-cognate-citation|add-new-cognate-citation)/(?P<cogjudge_id>\d+)/$',
            edit_lexeme),
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>add-new-cognate)/$', edit_lexeme),
    url(r'^lexeme/(?P<lexeme_id>\d+)/(?P<action>delete)/$', edit_lexeme),

    # Sources
    url(r'^sources/$', source_list, name="view-sources"),
    url(r'^source/(?P<source_id>\d+)/$', source_edit),
    url(r'^source/(?P<source_id>\d+)/(?P<action>edit|delete)/$', source_edit),
    url(r'^source/(?P<action>add)/$', source_edit),
    url(r'^source/(?P<action>add)/cognate-judgement/(?P<cogjudge_id>\d+)/$', source_edit),
    url(r'^source/(?P<action>add)/lexeme/(?P<lexeme_id>\d+)/$', source_edit),

    # Cognates
    url(r'^cognate/(?P<cognate_id>\d+)/$', cognate_report, name="cognate-set"),
    url(r'^cognate/(?P<cognate_id>\d+)/(?P<action>edit)/$', cognate_report),
    url(r'^cognate/(?P<meaning>[a-zA-Z0-9_ ]+)/(?P<code>[A-Z]+)/$',
            cognate_report),

    url(r'^revert/(?P<version_id>\d+)/$', revert_version),
    url(r'^object-history/(?P<version_id>\d+)/$', view_object_history),

    # Semantic domains
    url(r'^domains/$', view_domains, name="view-domains"),
    url(r'^domain/add-new/$', edit_relation_list, name="add-relation-list"),
    #url(r'^domain/(?P<domain>[a-zA-Z0-9_ ]+)/edit/$', edit_relation_list),
    url(r'^lexeme/(?P<lexeme_id>\d+)/extensions/(?P<domain>[a-zA-Z0-9_ ]+)/$',
            edit_lexeme_semantic_extensions, name="view-lexeme-extensions"),
    url(r'^language/(?P<language>[a-zA-Z0-9_ -]+)/domain/(?P<domain>[a-zA-Z0-9_ ]+)/$',
            edit_language_semantic_domain, name="view-extensions"),

    # Example:
    # (r'^ielex/', include('ielex.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    )

urlpatterns += patterns('',
        (r'^nexus/$', 'ielex.lexicon.views.list_nexus'),
        (r'^nexus-data/$', 'ielex.lexicon.views.write_nexus'),
        )

urlpatterns += patterns('django.contrib.auth',
    (r'^accounts/login/$','views.login', {'template_name':
        'profiles/login.html'}),
    (r'^accounts/logout/$','views.logout', {'template_name':
        'profiles/logout.html'}),
    )

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/profile/$', 'ielex.profiles.views.view_profile'),
    (r'^accounts/alter/profile/$', 'ielex.profiles.views.alter_profile'),
    (r'^accounts/change-password/$', 'ielex.profiles.views.change_password'),
    (r'^accounts/profile/(?P<username>.+)/$',
        'ielex.profiles.views.view_profile'),
    (r'^accounts/alter/profile/(?P<username>.+)/$',
        'ielex.profiles.views.alter_profile'),
    )

if settings.DEBUG: # additional urls for testing purposes
    urlpatterns += patterns('',
    # this is needed for running the development server
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    )

# vim:nowrap
