from zope.interface import implements
from zope.component import getMultiAdapter

from Acquisition import aq_inner
from Products.Five import BrowserView

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plonetheme.das.browser.interfaces import IThemeView

from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from plone.app.layout.viewlets import common

from plone.app.layout.viewlets.content import DocumentActionsViewlet

_marker = []

class LogoViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/logo.pt')
    
    def languages(self):
         """Returns list of languages."""
         if self.tool is None:
             return []
         bound = self.tool.getLanguageBindings()
         current = bound[0]

class LanguageViewlet(TranslatableLanguageSelector):
    render = ViewPageTemplateFile('templates/language_bar.pt')

class SearchboxViewlet(common.SearchBoxViewlet):
    render = ViewPageTemplateFile('templates/searchbox.pt')

class Quicklinks(ViewletBase):
    render = ViewPageTemplateFile('templates/quicklinks.pt')

class ThemeView(BrowserView):
    implements(IThemeView)

class FooterViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/footer.pt')

class DocumentactionsViewlet(DocumentActionsViewlet):
    render = ViewPageTemplateFile("templates/documentactionsIco.pt")

    # Utility methods

    def getColumnsClass(self, view=None):
        """Determine whether a column should be shown. The left column is called
        plone.leftcolumn; the right column is called plone.rightcolumn.
        """
        context = aq_inner(self.context)
        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        sl = plone_view.have_portlets('plone.leftcolumn', view=view);
        sr = plone_view.have_portlets('plone.rightcolumn', view=view);
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')

        if not sl and not sr:
            # we don't have columns, thus conten takes the whole width
            return "cell width-full position-0"
        elif sl and sr:
            # In case we have both columns, content takes 50% of the whole
            # width and the rest 50% is spread between the columns
            return "cell width-1:2 position-1:4"
        elif (sr and not sl) and (portal_state.is_rtl()):
            # We have right column and we are in RTL language
            return "cell width-3:4 position-1:4"
        elif (sr and not sl) and (not portal_state.is_rtl()):
            # We have right column and we are NOT in RTL language
            return "cell width-3:4 position-0"
        elif (sl and not sr) and (portal_state.is_rtl()):
            # We have left column and we are in RTL language
            return "cell width-3:4 position-0"
        elif (sl and not sr) and (not portal_state.is_rtl()):
            # We have left column and we are in NOT RTL language
            return "cell width-3:4 position-1:4"
