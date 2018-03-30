from __future__ import absolute_import, unicode_literals

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
from regulations3k.models import Part, Subpart, Section
from regulations3k.regdown import regdown
from v1.models import CFGOVPage, CFGOVPageManager
from v1.atomic_elements import molecules
from v1.util.util import get_secondary_nav_items


# def get_regs_nav_items(request, current_page):
#     return [
#         {
#             'title': section.title,
#             'url': '/regulations3k/{}/{}/'.format(
#                 section.label[:4], section.label),
#             'active': False if not hasattr(current_page, 'ask_category')
#             else section.name == current_page.ask_category.name,
#             'expanded': True
#         }
#         for section in Section.objects.all()
#     ], True


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
    """A routable page for serving an eregulations page by subpart ID"""

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
        context.update({'get_secondary_nav_items': get_secondary_nav_items})
        context.update({'regulation': self.regulation})
        return context

    @route(r'^(?P<section_label>[0-9A-Za-z-]+)/$')
    def section_page(self, request, section_label):

        self.template = 'regulations3k/browse-regulation.html'

        # part = Part.objects.get(part_number=part_label)
        section = Section.objects.get(label=section_label)
        context = self.get_context(request)
        context.update({
            # 'part': part.get_effective_version(),
            'subpart': Subpart.objects.get(
                label=section_label.replace('-', '.')),
            'section': Section.objects.get(label=section_label),
            'content': regdown(section.contents),
        })

        return TemplateResponse(
            request,
            self.template,
            context)
