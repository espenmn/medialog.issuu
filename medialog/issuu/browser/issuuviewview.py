import requests
from hashlib import md5
import urllib

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


class IissuuviewView(Interface):
    """
    issuuview view interface
    """

    def test():
        """ test method"""


class issuuviewView(BrowserView):
    """
    issuu browser view
    """
    implements(IissuuviewView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.key='y70fz64msx5z2v2hwvo0i2qno1la4vdt'
        self.secret='2dx2stidj8auzzm3i1rcr8wmrnpyiq6q'
        self.title = context.title
        self.file = str(context.getFile())
        

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()



    def __call_(self, file, title=''):
        """
        Upload the given ``file``.
        """
        response = self._query(
            url = 'http://upload.issuu.com/1_0',
            action = 'issuu.document.upload',
            data = {
                'file': self.get_data,
                'title': title
            }
        )

        return response['_content']['document']['documentId']



    def add_bookmark(self):
        """
        Add a bookmark.
        """
        raise NotImplementedError()

    def list_bookmarks(self):
        """
        List bookmarks.
        """
        raise NotImplementedError()

    def update_bookmark(self):
        """
        Update a bookmark.
        """
        raise NotImplementedError()

    def delete_bookmark(self, names):
        """
        Delete a bookmark.
        """
        raise NotImplementedError()

    def list_documents(self):
        """
        List documents for this user.
        """
        return self._query(
            url = 'http://api.issuu.com/1_0',
            action = 'issuu.documents.list'
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

    def update_document(self):
        """
        Update a document.
        """
        raise NotImplementedError()

    def delete_document(self, id):
        """
        Delete a document.

        :param id: A string describing a document ID.
        """
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

    def add_folder(self):
        """
        Create a folder.
        """
        raise NotImplementedError()

    def list_folders(self):
        """
        List folders.
        """
        raise NotImplementedError()

    def update_folder(self):
        """
        Update a folder.
        """
        raise NotImplementedError()

    def delete_folder(self):
        """
        Delete a folder.
        """
        raise NotImplementedError()

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
        
        print response

        try:
            data = json.loads(response.content)['rsp']
        except ValueError:
            raise self.Error('API response could not be parsed as JSON: %s' % response.content)

        if data['stat'] == 'fail':
            raise self.Error(data['_content']['error']['message'])
        else:
            return data

    def _sign(self):
        """
        Create a signature of the given ``data``.
        """
        signature = self.secret
        data = {}
        data.update({
            'apiKey': self.key,
            'format': 'json',
            'action': 'issuu.document.upload',
        })


        keys = data.keys()

        for key in sorted(keys):
            if isinstance(data[key], (str, unicode)):
                signature += key + data[key]

        mysign = md5(signature).hexdigest()
        return {'mysign': mysign, 'key' : self.key, 'file': self.context}

    class Error(StandardError):
        pass
