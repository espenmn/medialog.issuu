"""import requests
import md5
import json"""
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.app.form import base as ploneformbase
from zope.formlib import form

from Acquisition import aq_inner
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.ATContentTypes.interface.topic import IATTopic
from Products.ATContentTypes.interface.folder import IATFolder, IATBTreeFolder


class IssuuAPI(BrowserView  ):
    """
    not sure if this is needed
    """    
    template = ViewPageTemplateFile('issuuview.pt')

    def __init__(self, context, request):
        """
        Initialize an API client with the given     def __init__(self, key, secret): ``key`` and ``secret``.
        """
        self.key = 'eg6rrqqvabzzkkxfdqqz52tzi7m2fsbv'
        self.secret = 'ektdvd0zzoj74nk837vfvqbur3jylvlz'
        

