from __future__ import unicode_literals

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from regulations3k.models import Part, Subpart, Section, EffectiveVersion


class PartModelAdmin(ModelAdmin):
    model = Part
    menu_label = 'Regulation part'
    menu_icon = 'list-ul'
    list_display = (
        'cfr_title',
        'title',
        'part_number',
        'letter_code')


class SubpartModelAdmin(ModelAdmin):
    model = Subpart
    menu_label = 'Regulation subpart'
    menu_icon = 'list-ul'
    list_display = (
        'label',
        'title',
        'version')
    # list_filter = ('label',)


class SectionModelAdmin(ModelAdmin):
    model = Section
    menu_label = 'Regulation section content'
    menu_icon = 'list-ul'
    list_display = (
        'label',
        'title')
    search_fields = (
        'label', 'title')
    # list_filter = ('label',)


class EffectiveVersionModelAdmin(ModelAdmin):
    model = EffectiveVersion
    menu_label = 'Regulation effective versions'
    menu_icon = 'list-ul'
    list_display = (
        'part',
        'subparts',
        'effective_date')
    list_filter = ('effective_date', 'part')


@modeladmin_register
class Regulations3kModelAdminGroup(ModelAdminGroup):
    menu_label = 'Regulations3k'
    menu_icon = 'list-ul'
    items = (
        PartModelAdmin, SubpartModelAdmin,
        SectionModelAdmin, EffectiveVersionModelAdmin)
