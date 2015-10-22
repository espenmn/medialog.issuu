# -*- coding: utf-8 -*-

from Acquisition import aq_inner

import random
import requests
from hashlib import md5
from cStringIO import StringIO

from zope.interface import implements, Interface, alsoProvides, noLongerProvides
from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import IBrowserRequest

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from plone.app.customerize import registration

from medialog.issuu import issuuMessageFactory as _
from medialog.issuu.settings import IssuuSettings, IIssuuSettings
from medialog.issuu.interfaces import IIssuuUtilProtected, \
    IIssuu, IIssuuUtil
    
from plone.app.contenttypes.interfaces import IFile
from plone import api
 
try :
   # python 2.6
   import json
except ImportError:
   # plone 3.3
   import simplejson as json
   
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
            IssuuView(self.context, self.request).upload_document()
        else:  
            self.request.response.redirect(self.context.absolute_url()) + '/@@file_view'

        
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
            
            IssuuView(self.context, self.request).delete_document()
            utils.addPortalMessage("Issuu removed.")
            
        self.context.setLayout("file_view")
        self.request.response.redirect(self.context.absolute_url() + '/@@file_view')
       

        
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
        
    
    def is_right_type(self, context=None):
        if context is None:
            context = self.context
            
        if self.enabled()==False and IFile.providedBy(context):
            return context.file.contentType in ('application/pdf', 'application/x-pdf', 'image/pdf', 'application/vnd.oasis.opendocument.text-master', 'application/vnd.oasis.opendocument.text', 'application/vnd.wordperfect', 'application/x-wordperfect', 'application/vnd.sun.xml.writer', 'application/wordperfect', 'application/vnd.sun.xml.impress', 'application/vnd.oasis.opendocument.presentation', 'application/vnd.ms-powerpoint', 'application/powerpoint, application/mspowerpoint', 'application/x-mspowerpoint', 'application/rtf', 'application/msword')
        else:
            return False    

    
    



class IIssuuView(Interface):
    """
    issuu view interface
    """
    
    def javascript():
        """
        content to be included in javascript area of template
        """


class IssuuView(BrowserView):
    """
    issuu browser view that takes care of communication with issuu.com
    """
    implements(IIssuuSettings)
    
    def __init__(self, context, request):
        """views for managing isssuu content"""
        portal_state = getMultiAdapter((context, request), name='plone_portal_state')
        self.portal_url = portal_state.portal_url()
        
        #the issuu login settings are stored in the registry
        self.key = api.portal.get_registry_record('medialog.issuu.interfaces.IIssuuLoginSettings.issuu_key')
        self.secret = api.portal.get_registry_record('medialog.issuu.interfaces.IIssuuLoginSettings.issuu_secret')
        self.domain = api.portal.get_registry_record('medialog.issuu.interfaces.IIssuuLoginSettings.domain')

        self.title = context.title.encode("utf-8")
        self.context=context               
        self.request = request
        self.settings = IssuuSettings(context)  
        self.issuu_id = self.settings.issuu_id
        self.file =  StringIO(context.file.data)
        
    @property
    def portal_catalog(self):
        #api.portal.get_tool(['portal_catalog'])
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
        
       
    def upload_document(self):
        """
        Upload the given ``file``.
        """
        self.issuu_name = str(random.randint(1000000000000,9000000000000))

        name = self.issuu_name 
        file = self.context.file.data
        
        response = self._query(
            url = 'http://upload.issuu.com/1_0',
            action = 'issuu.document.upload',
            data = {
                'file' : self.file,
                'title': self.title,
                'name' : name,
            }
        )        

        #save settings we got back from from 'the upload to issuu' and the name
        issuu_response = response['_content']['document']
        my_issuu_id = issuu_response['documentId']
        #pagecount = issuu_response['pageCount']
        #my_issuu_id = issuu_response['ep']
        
        self.settings.issuu_name = self.issuu_name
        self.settings.issuu_id = my_issuu_id
        
        self.context.setLayout("issuuview")
        self.request.response.redirect(self.context.absolute_url() + '/view')
        
    def _query(self, url, action, data=None):
        """
        Low-level access to the Issuu API.
        """
        
        if not data:
            data = {}

        data.update({
            'apiKey': self.key,
            'format': 'json',
            'action': action
        })

        data['signature'] = self._sign(data)

        files = {}

        for key in data:
            if hasattr(data[key], 'read'):
                files[key] = data[key]

        for key in files:
            data.pop(key)

        response = requests.post(
            url = url,
            data = data,
            files = files
        )

        try:
            data = json.loads(response.content)['rsp']
        except ValueError:
            raise self.Error('API response could not be parsed as JSON: %s' % response.content)

        if data['stat'] == 'fail':
            raise self.Error(data['_content']['error']['message'])
        else:
            return data

    def _sign(self, data):
        """
        Create a signature of the given ``data``.
        """
        signature = self.secret

        data.update({
            'apiKey': self.key
        })

        keys = data.keys()

        for key in sorted(keys):
            if isinstance(data[key], (str, unicode)):
                signature += key + data[key]

        mysign = md5(signature).hexdigest()
        return mysign
        
    def list_documents(self):
        """
        List documents for this user.
        """
        return self._query(
            url = 'http://api.issuu.com/1_0',
            action = 'issuu.documents.list',
        )

    def delete_document(self, context=None):
        """
        Delete a document.

        :param id: A string describing a document ID.
        """
        if context is None:
            context = self.context

        #do I need the next line ?
        self.settings = IssuuSettings(context)
        issuu_id = self.settings.issuu_id
        
        #find document name on issuu.com would be better, but havent sorted this out yet.
        #if the name changes after the file has been processed.        
        #response = self.list_documents()['_content']['result'] 
        #for doc in response ['_content']: 
        #    if doc['document']['documentId'] == issuu_id: 
        #        self.delete_documents(doc['document']['name'])
        
        self.delete_documents([self.settings.issuu_name])       
        IssuuUtilProtected(self.context, self.request).disable()
        self.context.restrictedTraverse('/@@view') 
       
        
    def delete_documents(self, ids):
        """
        Delete the documents with the given ``ids``.

        :param ids: A list of strings describing document IDs.
        """
        issuu_id = self.settings.issuu_id
                
        self._query(
            url = 'http://api.issuu.com/1_0',
            action = 'issuu.document.delete',
            data = {
                'names': ','.join(ids)
            }
        )
        
    
    def embed_add(self):
        """
        Create embed (for html5) ``ids``.

        :param ids: ID and size
        """
        issuu_id = self.settings.issuu_id
        #issuu_name = self.settings.issuu_name
        response = self._query(
            url = 'http://api.issuu.com/1_0',
            action = 'issuu.document_embed.add',
            data = {
                'documentId' :  issuu_id,
                'height' : 600,
                'width': 600,
                'readerStartPage' : 1,
            }
        )        

        #save settings we got back 
        issuu_response = response['_content']['document']
        my_issuu_embedid = issuu_response['dataConfigId']

    
    class Error(StandardError):
        """
        To do: Give feedback if issuu.com error.
        """
        pass

    
    def javascript(self):
        """
          We need this javascript for the swf view
        """
        return u"""
        <script type="text/javascript">
                var attributes = {
                    id: 'issuuViewer'
                };
    
                var params = {
                    allowfullscreen: '%(allowfullscreen)s',
                    allowScriptAccess: 'always',
                    menu: '%(menu)s',
                };
 
                var flashvars = {
                    jsAPIClientDomain: '%(domain)s',
                    mode: '%(mode)s',
                    backgroundColor : '%(backgroundcolor)s',
                    documentId: '%(issuu_id)s',
                    layout: '%(portal_url)s/++resource++issuu.resources/%(layout)s-theme/issuu/%(layout)s/layout.xml',
                    loadingInfoText: '%(loadinginfotext)s',
                    showFlipBtn: '%(showflipbtn)s',
                    docName: '%(name)s',

                };    
                swfobject.embedSWF("http://static.issuu.com/webembed/viewers/style1/v1/IssuuViewer.swf", "myContent1", "%(width)s", "%(height)s", "9.0.0", "swfobject/expressInstall.swf", flashvars, params, attributes);    
            </script>
"""  % {
 		'issuu_id': self.settings.issuu_id,
 		'width': self.settings.width,
 		'height': self.settings.height,
 		'domain' : self.settings.domain,
 		'backgroundcolor' : self.settings.backgroundcolor,
 		'mode' : self.settings.mode,
 		'menu' : self.settings.menu,
 		'layout' : self.settings.layout,
 		'mode' : self.settings.mode,
 		'allowfullscreen' : self.settings.allowfullscreen,
 		'loadinginfotext': self.settings.loadinginfotext,
 		'name' : self.settings.issuu_name,
 		'showflipbtn' : self.settings.showflipbtn,
 		'portal_url': self.portal_url,
}
     
     
                 
