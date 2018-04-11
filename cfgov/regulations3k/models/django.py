# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import FieldPanel
# from wagtail.wagtailcore.fields import RichTextField
# from regulations3k.models.fields import RegDownTextField


@python_2_unicode_compatible
class Section(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    contents = models.TextField(blank=True)

    panels = [
        FieldPanel('label'),
        FieldPanel('title'),
        FieldPanel('contents', classname="full"),
    ]

    def __str__(self):
        return "{} {}".format(self.label, self.title)

    class Meta:
        ordering = ['label']


class Subpart(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    version = models.ForeignKey(
        'EffectiveVersion', blank=True, null=True,
        related_name='subpart_version')
    sections = models.ForeignKey(Section, blank=True, null=True)

    panels = [
        FieldPanel('label'),
        FieldPanel('title'),
        FieldPanel('version'),
        FieldPanel('sections'),
    ]

    def __str__(self):
        return "{} {}".format(self.label, self.title)

    class Meta:
        ordering = ['label']


class EffectiveVersion(models.Model):
    authority = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    effective_date = models.DateField(blank=True, null=True)
    part = models.ForeignKey('Part', blank=True, null=True)
    subparts = models.ForeignKey(Subpart, blank=True, null=True)

    panels = [
        FieldPanel('authority'),
        FieldPanel('source'),
        FieldPanel('effective_date'),
        FieldPanel('part'),
        FieldPanel('subparts'),
    ]

    def __str__(self):
        return "{}, effective {}".format(
            self.part, self.effective_date)

    class Meta:
        ordering = ['effective_date']


class Part(models.Model):
    cfr_title = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    letter_code = models.CharField(max_length=10)
    versions = models.ForeignKey(
        EffectiveVersion, blank=True, null=True,
        related_name='part_version')

    panels = [
        FieldPanel('cfr_title'),
        FieldPanel('title'),
        FieldPanel('part_number'),
        FieldPanel('letter_code'),
        FieldPanel('versions'),
        FieldPanel('chapter'),
    ]

    def __str__(self):
        name = "12 CFR Part {}".format(self.part_number)
        if self.letter_code:
            name += " (Regulation {})".format(self.letter_code)
        return name

    class Meta:
        ordering = ['letter_code']

    # def get_parts_with_effective_version(self):
    #     pass

    # def get_current_effective_version(self):
    #     pass
