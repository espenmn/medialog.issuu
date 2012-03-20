from zope.interface import implements, alsoProvides, noLongerProvides
from Products.Five.browser import BrowserView
from medialog.issuu.interfaces import IIssuuUtilProtected, \
    IViewIssuu, IIssuuUtil
from Products.CMFCore.utils import getToolByName

from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import getMultiAdapter

try:
    #For Zope 2.10.4
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #For Zope 2.9
    from zope.app.annotation.interfaces import IAnnotations


class IssuuUtilProtected(BrowserView):
    """
    a protected traverable utility for 
    enabling and disabling issuu
    """
    implements(IIssuuUtilProtected)
    def enable(self):
        utils = getToolByName(self.context, 'plone_utils')
        
        if not IViewIssuu.providedBy(self.context):
            alsoProvides(self.context, IViewIssuu)
            self.context.reindexObject(idxs=['object_provides'])
            utils.addPortalMessage("You have added a issuu to this page. "
                                   " To customize, click the 'Issuu Settings' button.")
            self.request.response.redirect(self.context.absolute_url() + '/@@issuu-settings')
            
        else:  
            self.request.response.redirect(self.context.absolute_url())
        
    def disable(self):
        utils = getToolByName(self.context, 'plone_utils')
        
        if IViewIssuu.providedBy(self.context):
            noLongerProvides(self.context, IViewIssuu)
            self.context.reindexObject(idxs=['object_provides'])
            
            #now delete the annotation
            annotations = IAnnotations(self.context)
            metadata = annotations.get('medialog.issuu', None)
            if metadata is not None:
                del annotations['medialog.issuu']
                
            utils.addPortalMessage("Issuu removed.")
            
        self.request.response.redirect(self.context.absolute_url())
        
        
class IssuuUtil(BrowserView):
    """
    a public traverable utility that checks if a 
    slide is enabled
    """
    implements(IIssuuUtil)

    def enabled(self):
        return IViewIssuu.providedBy(self.context)    


    def view_enabled(self):
        utils = getToolByName(self.context, 'plone_utils')
        try:
            return utils.browserDefault(self.context)[1][0] == "issuuview"
        except:
            return False


    def should_include(self):
        return self.enabled() or self.view_enabled()