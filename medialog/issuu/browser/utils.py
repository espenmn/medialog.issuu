from zope.interface import implements, alsoProvides, noLongerProvides
from Products.Five.browser import BrowserView
from medialog.issuu.interfaces import IIssuuUtilProtected, \
    IIssuu, IIssuuUtil
from Products.CMFCore.utils import getToolByName

from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import getMultiAdapter

#from medialog.issuu.settings import IssuuSettings


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

        if not IIssuu.providedBy(self.context):
            alsoProvides(self.context, IIssuu)
            self.context.reindexObject(idxs=['object_provides'])
            utils.addPortalMessage("You have uploaded this file to issuu.com. You will have to wait a little before before the doucment is found (issuu.com has to process it).")
            self.request.response.redirect(self.context.absolute_url() + '/@@issuu_upload')
            
        else:  
            self.request.response.redirect(self.context.absolute_url())
        
    def disable(self):
        utils = getToolByName(self.context, 'plone_utils')
        
        if IIssuu.providedBy(self.context):
            noLongerProvides(self.context, IIssuu)
            self.context.reindexObject(idxs=['object_provides'])
            
            #now delete the annotation
            annotations = IAnnotations(self.context)
            metadata = annotations.get('medialog.issuu', None)
            if metadata is not None:
                del annotations['medialog.issuu']
                
            utils.addPortalMessage("Issuu removed.")
            
        #self.request.response.redirect(self.context.absolute_url() + '/@@issuu_delete')
        self.request.response.redirect(self.context.absolute_url() + '/selectViewTemplate?templateId=file_view')
        
class IssuuUtil(BrowserView):
    """
    a public traverable utility that checks if it is enabled etc
    """
    implements(IIssuuUtil)

    def enabled(self):
        return IIssuu.providedBy(self.context)    


    def view_enabled(self):
        utils = getToolByName(self.context, 'plone_utils')
        try:
            return utils.browserDefault(self.context)[1][0] == "issuuview"
        except:
            return False

    def should_include(self):
        return self.enabled() or self.view_enabled()
        
    
    def is_pdf(self, context=None):
        if context is None:
            context = self.context
            
        if self.enabled()==False and hasattr(context, 'getContentType'):
            return context.getContentType() in ('application/pdf', 'application/x-pdf', 'image/pdf')
        else:
            return False    
