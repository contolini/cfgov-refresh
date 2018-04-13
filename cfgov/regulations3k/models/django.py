# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime

from django.db import models
from django.utils.functional import cached_property
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import FieldPanel
# from wagtail.wagtailcore.fields import RichTextField
# from regulations3k.models.fields import RegDownTextField


@python_2_unicode_compatible
class Part(models.Model):
    cfr_title = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    letter_code = models.CharField(max_length=10)

    panels = [
        FieldPanel('cfr_title'),
        FieldPanel('title'),
        FieldPanel('part_number'),
        FieldPanel('letter_code'),
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

    @cached_property
    def effective_version(self):
        """ Return the current effective version of the regulation.
        This selects based on effective_date being less than the current
        date. """
        effective_version = self.versions.filter(
            effective_date__lte=datetime.now()
        ).order_by(
            '-effective_date'
        ).first()
        return effective_version


@python_2_unicode_compatible
class EffectiveVersion(models.Model):
    authority = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    effective_date = models.DateField(blank=True, null=True)
    part = models.ForeignKey(Part, related_name="versions")

    panels = [
        FieldPanel('authority'),
        FieldPanel('source'),
        FieldPanel('effective_date'),
        FieldPanel('part'),
    ]

    def __str__(self):
        return "{}, effective {}".format(
            self.part, self.effective_date)

    class Meta:
        ordering = ['effective_date']


@python_2_unicode_compatible
class Subpart(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    version = models.ForeignKey(EffectiveVersion, related_name="subparts")

    panels = [
        FieldPanel('label'),
        FieldPanel('title'),
        FieldPanel('version'),
    ]

    def __str__(self):
        return "{} {}, effective {}".format(
            self.label, self.title, self.version.effective_date)

    class Meta:
        ordering = ['label']


@python_2_unicode_compatible
class Section(models.Model):
    label = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    contents = models.TextField(blank=True)
    subpart = models.ForeignKey(Subpart, related_name="sections")

    panels = [
        FieldPanel('label'),
        FieldPanel('subpart'),
        FieldPanel('title'),
        FieldPanel('contents', classname="full"),
    ]

    def __str__(self):
        return "{} {}".format(self.label, self.title)

    class Meta:
        ordering = ['label']

    @property
    def numeric_label(self):
        part, number = self.label.split('-')
        return '\xa7\xa0{}.{}'.format(part, number)

    @property
    def section_number(self):
        part, number = self.label.split('-')
        return number

    @property
    def title_content(self):
        part, number = self.label.split('-')
        return self.title.replace(self.numeric_label, '')
