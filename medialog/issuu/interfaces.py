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
 
    issuu_id = schema.TextLine(
        title=_(u"label_issuu_id",
            default=u"ID for the document at issuu.com. Dont edit this id unless you know what you are doing"), 
        default=u"101209160738-bfd67b25284249cfb535c886beb7430b",
        required=True
    )
