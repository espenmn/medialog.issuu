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
        self.key='y70fz64msx5z2v2hwvo0i2qno1la4vdt'
        self.secret='2dx2stidj8auzzm3i1rcr8wmrnpyiq6q'
        self.title = context.title
        self.context=context
        
        
        
        self.request = request
        self.settings = IssuuSettings(context)
        
        
        #thanks to nathan for this line
        #remember 'open' takes a file (ONLY)
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
        #set some settings from 'upload'
        self.settings.issuu_id = '122343'
        self.request.response.redirect(self.context.absolute_url() + '/selectViewTemplate?templateId=issuuview')
        
       
    def upload_document(self):
        """
        Upload the given ``file``.
        """
        response = self._query(
            url = 'http://upload.issuu.com/1_0',
            action = 'issuu.document.upload',
            data = {
                'file': self.file,
                'title': self.title
            }
        )
        

        return response['_content']['document']['documentId']

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
            action = 'issuu.documents.list'
        )

    def delete_document(self, context):
        """
        Delete a document.

        :param id: A string describing a document ID.
        """
        self.context = context
        self.settings = IssuuSettings(context)
        id = self.issuu_id
        
        self.delete_documents([id])

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


        

class IIssuuEmbedView(Interface):
    """
    issuu view interface
    """

    def settings():
        """ settings method"""


class IssuuEmbedView(BrowserView):
    """
    issuu browser that shows the embedded 'pdf' 
    """
    implements(IIssuuEmbedView)    
 
    
    def __init__(self, context, request):
    	"""
    		Maybe do something here ? 
    	"""
    	self.context = context
        self.request = request
        self.settings = IssuuSettings(context)
        self.width = self.settings.width 
        self.height = self.settings.height 
        self.issuu_id = self.settings.issuu_id

    

    

    