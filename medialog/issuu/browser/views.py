from Acquisition import aq_inner

import random
import requests
from hashlib import md5
#import json
from cStringIO import StringIO

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from medialog.issuu import issuuMessageFactory as _
from medialog.issuu.settings import IssuuSettings
from medialog.issuu.settings import IIssuuSettings

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



class IIssuuView(Interface):
    """
    issuu view interface
    """

    def settings():
        """ settings method"""


class IssuuView(BrowserView):
    """
    issuu browser view that takes care of communication with issuu.com
    """
    implements(IIssuuSettings)
        
    def __init__(self, context, request):
        #the issuu settings are stored in portal properties
        issuu_properties = getToolByName(context, 'portal_properties').issuu_properties  
        self.key=issuu_properties.issuu_key
        self.secret=issuu_properties.issuu_secret
        self.title = context.title
        self.context=context               
        self.request = request
        self.settings = IssuuSettings(context)
        
        #thanks to nathan for this line
        #remember 'open' takes a file (ONLY)
        #PS it is probably easier to use upload with URL (issuu.com supportst that)
        #but this would not work on closed networks / intranet.
        self.file = StringIO(str(context.getFile().data))
        
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
        
        
    def __call__(self):
        """
        Upload current (pdf) file.
        """        
        upload = self.upload_document()
        #change view now that the pdf exists on issuu.com
        self.request.response.redirect(self.context.absolute_url() + '/selectViewTemplate?templateId=issuuview')
        
       
    def upload_document(self):
        """
        Upload the given ``file``.
        """
        self.issuu_name = self.title + str(random.randint(10000,99999))
        response = self._query(
            url = 'http://upload.issuu.com/1_0',
            action = 'issuu.document.upload',
            data = {
                'file': self.file,
                'title': self.title,
                'name' : self.issuu_name,
            }
        )        

        #save settings we got back from from 'the upload to issuu' and the name
        issuu_response = response['_content']['document']
        my_issuu_id = issuu_response['documentId']
        self.settings.issuu_name = self.issuu_name
        self.settings.issuu_id = my_issuu_id
        
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
        
        
    class Error(StandardError):
        pass
        

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
        #if the name changes after the pdf has been processed.        
        #response = self.list_documents()['_content']['result'] 
        self.delete_documents([self.settings.issuu_name])
        self.request.response.redirect(self.context.absolute_url() + '/@@disable_issuu')


    def delete_documents(self, ids):
        """
        Delete the documents with the given ``ids``.

        :param ids: A list of strings describing document IDs.
        """
        self._query(
            url = 'http://api.issuu.com/1_0',
            action = 'issuu.document.delete',
            data = {
                'names': ','.join(ids)
            }
        )


class IssuuEmbedView(BrowserView):
    """
    issuu browser that shows the embedded 'pdf' 
    """

    def __init__(self, context, request):
    	"""
    		Think all this is needed, should probably add some more, like background color, menu etc. 
    	"""
    	self.context = context
        self.request = request
        self.settings = IssuuSettings(context)
        self.width = self.settings.width 
        self.height = self.settings.height 
        self.issuu_id = self.settings.issuu_id


class IIssuuFlashView(Interface):
    """
    issuu flashview interface
    """

    def javascript():
        """
        content to be included in javascript area of template
        """

class IssuuFlashView(BrowserView):
    """
    issuu browser view that shows the embedded 'pdf' 
    """
    implements(IIssuuFlashView)
        
    def __init__(self, context, request):
    	"""
    		Not sure about this   
    	"""
    	self.context = context
    	self.request = request
        self.settings = IssuuSettings(context)
        self.width = self.settings.width 
        self.height = self.settings.height 
        self.issuu_id = self.settings.issuu_id


 	def javascript(self):
 	    
		return """<script type="text/javascript" src="http://www.theajmonline.com.au/iir/book/book1/swfobject.js" />
        <script type="text/javascript">
                var attributes = {
                    id: 'issuuViewer1'
                };
    
                var params = {
                    allowfullscreen: 'true',
                    allowScriptAccess: 'always',
                    menu: 'false'
                };
    
                var flashvars = {
                    jsAPIClientDomain: 'issuu.com',
                    mode: 'embed',
                    layout: 'http%3A%2F%2Fskin.issuu.com%2Fv%2Flight%2Flayout.xml',
                    showFlipBtn: 'true',
                    documentId: %(issuu_id)s,
                };
    
                swfobject.embedSWF("http://static.issuu.com/webembed/viewers/style1/v1/IssuuViewer.swf", "myContent1", "200", "600", "9.0.0", "swfobject/expressInstall.swf", flashvars, params, attributes);
    
            </script>
"""  % {
 		'issuu_id': self.settings.issuu_id,
 		'width': self.settings.width,
 		'height': self.settings.height,
}