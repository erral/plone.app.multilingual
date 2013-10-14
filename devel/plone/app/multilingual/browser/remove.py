# -*- coding: utf-8 -*-
from Acquisition import aq_parent

from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.multilingual import _
from plone.app.multilingual.browser.interfaces import IRemoveTranslation
from plone.directives import form
from z3c.form import button


class RemoveTranslationsForm(form.SchemaForm):

    schema = form.IFormFieldProvider(IRemoveTranslation)
    ignoreContext = True
    label = _(u"label_remove_translations",
              default=u"Remove translations")
    description = _(u"long_description_remove_translations",
                    default=u"This form allows you to remove the existing "
                             "translations of the current object. You can "
                             "just delete the link between the objects "
                             "or you can delete the object itself."
                )

    @button.buttonAndHandler(_(u"unlink selected"))
    def handle_unlink(self, action):
        data, errors = self.extractData()
        manager = ITranslationManager(self.context)
        if not errors:
            for language in data['languages']:
                manager.remove_translation(language)

        return self.request.response.redirect(
            self.context.absolute_url() + '/remove_translations')

    @button.buttonAndHandler(_(u"remove selected"))
    def handle_remove(self, action):
        data, errors = self.extractData()
        manager = ITranslationManager(self.context)
        if not errors:
            for language in data['languages']:
                content = manager.get_translation(language)
                manager.remove_translation(language)
                aq_parent(content).manage_delObjects([content.getId()])

        return self.request.response.redirect(
            self.context.absolute_url() + '/remove_translations')