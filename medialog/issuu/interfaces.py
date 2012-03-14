from zope.interface import Interface, Attribute
from zope import schema
from medialog.issuu import issuu_message_factory as _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from OFS.interfaces import IItem


class IIssuuLayer(Interface):
    """
    marker interface for issuu layer
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
        checks if issuu is enabled on the peice of content
        """

    def view_enabled():
        """
        checks if the issuu view is selected
        """

    
class IIssuuSettings(Interface):
    """
    The actual issuu settings
    """

    id = schema.Text(
        title=_(u'label_id_title_issuu_setting', default=u"Id"),
        description=_(u"label_id_description_issuu_setting", 
            default=u"The issuu id."),
        default="",
        required=True
    )

class IIssuu(Interface):
    """
    The copy of actual issuu settings
    """

    id = schema.Text(
        title=_(u'label_id_title_issuu_setting', default=u"Id"),
        description=_(u"label_id_description_issuu_setting", 
            default=u"The issuu id."),
        default="",
        required=True
    )

   