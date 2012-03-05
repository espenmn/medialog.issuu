# from Products.CMFPlone.CatalogTool import registerIndexableAttribute

from plone.indexer.decorator import indexer

from Products.ATContentTypes.interface import IATContentType

@indexer(IATContentType)
def titleflagged_indexer(obj):
    """A method for indexing 'hide title' field of Documents
    """
    field = obj.Schema().getField('titleflaggedobject')
    if field is not None:
        return field.get(obj)
    else:
        raise AttributeError            

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
