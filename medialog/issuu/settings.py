from zope.interface import implements
from persistent.dict import PersistentDict
try:
    #For Zope 2.10.4
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    #For Zope 2.9
    from zope.app.annotation.interfaces import IAnnotations

from interfaces import IIssuuSettings


class IssuuSettings(object):
    """
    Copied from Nathan, let's see if it works.  
    """
    implements(IIssuuSettings)
    
    interfaces = []

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)

        self._metadata = annotations.get('medialog.issuu', None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            annotations['medialog.issuu'] = self._metadata
    
    @property
    def __parent__(self):
        return self.context

    @property
    def __roles__(self):
        return self.context.__roles__

    def __setattr__(self, name, value):
        if name[0] == '_' or name in ['context', 'interfaces']:
            self.__dict__[name] = value
        else:
            self._metadata[name] = value

    def __getattr__(self, name):
       value = self._metadata.get(name)
       if value is None:
           v = IIssuuSettings.get(name)
           if v:
               return v.default
       return value