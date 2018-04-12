from __future__ import absolute_import, unicode_literals
import re

from django.core.paginator import Paginator
from django.db import models
from django.template.response import TemplateResponse
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import PageManager

# Our RegDownTextField field doesn't generate a good widget yet
# from regulations3k.models.fields import RegDownTextField
from ask_cfpb.models.pages import SecondaryNavigationJSMixin
from regulations3k.models import Part, Section  # , Subpart
from regulations3k.regdown import regdown
from v1.models import CFGOVPage, CFGOVPageManager
from v1.atomic_elements import molecules


class RegulationLandingPage(CFGOVPage):
    """landing page for eregs"""
    objects = CFGOVPageManager()
    regs = Part.objects.exclude(letter_code='DD')

    def get_context(self, request, *args, **kwargs):
        context = super(CFGOVPage, self).get_context(request, *args, **kwargs)
        context.update({
            'regs': self.regs,
            'dd': Part.objects.get(letter_code='DD')
        })
        return context

    def get_template(self, request):
        return 'regulations3k/base.html'


class RegulationPage(RoutablePageMixin, SecondaryNavigationJSMixin, CFGOVPage):
    """A routable page for serving an eregulations page by Section ID"""

    objects = PageManager()

    template = 'browse-basic/index.html'

    header = StreamField([
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([], null=True)
    regulation = models.ForeignKey(
        Part,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='eregs3k_page')

    content_panels = CFGOVPage.content_panels + [
        StreamFieldPanel('header'),
        FieldPanel('regulation', Part),
    ]

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    sidefoot_panels = CFGOVPage.sidefoot_panels + [
        FieldPanel('secondary_nav_exclude_sibling_pages'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar'),
        ObjectList(CFGOVPage.settings_panels, heading='Configuration'),
    ])

    def get_context(self, request, *args, **kwargs):
        context = super(CFGOVPage, self).get_context(request, *args, **kwargs)
        context.update({
            'get_secondary_nav_items': get_reg_nav_items,
            'regulation': self.regulation,
        })
        return context

    @route(r'^(?P<section_label>[0-9A-Za-z-]+)/$')
    def section_page(self, request, section_label):
        section = Section.objects.filter(
            subpart__version=self.regulation.effective_version,
        ).get(label=section_label)
        self.template = 'regulations3k/browse-regulation.html'
        paginator = Paginator(
            sorted_section_nav_list(self.regulation.effective_version),
            100
        )
        context = self.get_context(request)
        context.update({
            'version': self.regulation.effective_version,
            'content': regdown(section.contents),
            'get_secondary_nav_items': get_reg_nav_items,
            'paginator': paginator,
            'section': section,
        })

        return TemplateResponse(
            request,
            self.template,
            context)


def sorted_section_nav_list(version):
    numeric_check = re.compile('\d{4}\-(\d{1,2})')
    section_query = Section.objects.filter(
        subpart__version=version,
    )
    numeric_sections = sorted(
        [sect for sect in section_query
         if re.match(numeric_check, sect.label)],
        key=lambda x: float(re.match(numeric_check, x.label).group(1)))
    alpha_sections = sorted(
        [sect for sect in section_query
         if sect not in numeric_sections])
    return numeric_sections + alpha_sections


def get_reg_nav_items(request, current_page):
    current_label = [bit for bit in request.url.split('/') if bit][-1]
    return [
        {
            'title': gathered_section.title,
            'url': '/eregulations3k/{}/{}/'.format(
                current_page.regulation.part_number, gathered_section.label),
            'active': gathered_section.label == current_label,
            'expanded': True
        }
        for gathered_section in Section.objects.filter(
            subpart__version=current_page.regulation.effective_version
        )
    ], True
