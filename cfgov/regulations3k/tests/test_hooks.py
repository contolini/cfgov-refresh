from __future__ import unicode_literals

from django.test import TestCase

from regulations3k.wagtail_hooks import (
    PartModelAdmin, SubpartModelAdmin,
    SectionModelAdmin, EffectiveVersionModelAdmin
)
from regulations3k.models import Part, Subpart, Section, EffectiveVersion


class TestRegs3kHooks(TestCase):

    def test_reg_model_hooks(self):
        self.assertEqual(PartModelAdmin.model, Part)
        self.assertEqual(SubpartModelAdmin.model, Subpart)
        self.assertEqual(SectionModelAdmin.model, Section)
        self.assertEqual(EffectiveVersionModelAdmin.model, EffectiveVersion)
