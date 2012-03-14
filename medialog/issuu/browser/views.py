import requests
from hashlib import md5
import json

 
try :
   # python 2.6
   import json
except ImportError:
   # plone 3.3
   import simplejson as json

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from medialog.issuu import issuuMessageFactory as _


from Products.Archetypes.Field import FileField
from Acquisition import aq_inner



class IissuuView(Interface):
    """
    issuu view interface
    """

    def test():
        """ test method"""


class issuuView(BrowserView):
    """
    issuu browser view
    """
    def __init__(self, context, request):
        self.key='y70fz64msx5z2v2hwvo0i2qno1la4vdt'
        self.secret='2dx2stidj8auzzm3i1rcr8wmrnpyiq6q'
        self.title = context.title
        context = aq_inner(context)
        self.field = context.path
        #self.field = context.getField('file') or context.getPrimaryField()
        
    def __call__(self):
        """
        Upload the given ``file``.
        /Users/g4/src/xmedialog.issuu/medialog/issuu/tests/fixtures/parrot.pdf'
        """
        
        upload = self.upload_document(
        	file = open('/Users/g4/src/xmedialog.issuu/medialog/issuu/tests/fixtures/parrot.pdf'),
        	title = self.title
        )

    def upload_document(self, file, title=''):
        """
        Upload the given ``file``.
        """
        response = self._query(
            url = 'http://upload.issuu.com/1_0',
            action = 'issuu.document.upload',
            data = {
                'file': file,
                'title': title
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
        
