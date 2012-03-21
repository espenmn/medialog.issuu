from zope.interface import Interface, Attribute
from zope import schema
from medialog.issuu import issuuMessageFactory  as _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from OFS.interfaces import IItem


class IIssuuLayer(Interface):
    """
    marker interface for issuu layer
    
    """
class IIssuu(Interface):
    """
    marker interface for content types that can use
    easyissuu view
    """

class IIssuuUtilProtected(Interface):

    def enable():
        """
        enable issuu on this object
        """

    def disable():
        """
        disable issuu on this object
        """


class IIssuuUtil(Interface):

    def enabled():
        """
        checks if issuu is enabled  
        """

    def view_enabled():
        """
        checks if the issuu view is selected
        """

class IIssuuSettings(Interface):
    """
    The actual issuuview settings
    """


    issuu_id = schema.TextLine(
        title=_(u'label_issuu_id_title_issuu_setting', default=u"Width"),
        description=_(u"label_issuu_id_description_issuu_setting", 
            default=u"The id for the document at issuu.com"),
        default='fd5164eb-0529-85ce-3b39-b61220296dc9',
       
    width = schema.Int(
        title=_(u'label_width_title_issuu_setting', default=u"Width"),
        description=_(u"label_width_description_issuu_setting", 
            default=u"The fixed width of the issuu."),
        default=600,
        required=True
    )

    height = schema.Int(
        title=_(u'label_height_title_issuu_setting', default=u"Height"),
        description=_(u"label_height_description_issuu_setting", 
            default=u"The fixed height of the issuu."),
        default=400,
        required=True
    )
 
