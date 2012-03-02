""" docs http://docs.python.org/library/hashlib.html#module-hashlib""" 
from hashlib import md5
"""import json """


from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from cStringIO import StringIO
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class IIssuuview(Interface):
    """
    Colorized Image View view interface
    """

    def test():
        """ test method"""

class Issuuview(BrowserView):
    """ To Issuu or not to issuu, thats the question """    
    def __call__(self, REQUEST):
        self.key = 'eg6rrqqvabzzkkxfdqqz52tzi7m2fsbv'
        self.secret = 'ektdvd0zzoj74nk837vfvqbur3jylvlz'
        
        upload = self.upload_document
        return '<p><b>hello</b> world</p>'
        
        
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

        return md5.new(signature).hexdigest()

    class Error(StandardError):
        pass