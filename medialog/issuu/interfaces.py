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
    issuu view  
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
        self.request.response.redirect(self.context.absolute_url() + '/selectViewTemplate?templateId=file_view')


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
    
    width = schema.TextLine(
        title=_(u"label_width_title_issuu_setting", default=u"Width"),
        description=_(u"label_width_description_issuu_setting", 
            default=u"The fixed width of the issuu."),
        default=u"600px",
        required=True
    )

    height = schema.TextLine(
        title=_(u'label_height_title_issuu_setting', default=u"Height"),
        description=_(u"label_height_description_issuu_setting", 
            default=u"The fixed height of the issuu."),
        default=u"400px",
        required=True
    )
 
    pagecount = schema.Int(
        title=_(u"label_pagecount",
            default=u"Number of (images of) pages of document to show in flashview.... when flash is disabled"), 
        default=1,
        required=True
    )
        
    mode = schema.Choice (
        title=_(u"label_mode",
            default=u"Mode"),
        default="mini",
        vocabulary=SimpleVocabulary([
            SimpleTerm("mini", "mini",
                _(u"label_mini", default=u"Mini")),
            SimpleTerm("embed", "embed",
                _(u"label_embed", default=u"Embed")
            )
        ])
    )
    
    menu = schema.Choice (
        title=_(u"label_menu",
            default=u"Show menu"),
        default="false",
        vocabulary=SimpleVocabulary([
            SimpleTerm("false", "false",
                _(u"label_false", default=u"No")),
            SimpleTerm("true", "true",
                _(u"label_true", default=u"Yes")
            )
        ])
    )
    
    allowfullscreen = schema.Choice (
        title=_(u"label_allowfullscreen",
            default=u"Allow fullscreen"),
        default="false",
        vocabulary=SimpleVocabulary([
            SimpleTerm("false", "false",
                _(u"label_false", default=u"No ")),
            SimpleTerm("true", "true",
                _(u"label_true", default=u"Yes ")
            )
        ])
    )
    
    layout = schema.Choice (
        title=_(u"label_layout",
            default=u"Layout (currently not working... could need some help on this"),
        default="basicBlue",
        vocabulary=SimpleVocabulary([
            SimpleTerm("basicBlue", "basicBlue",
                _(u"label_layout1", default=u"basicBlue")),
            SimpleTerm("basicGrey", "basicGrey",
                _(u"label_layout2", default=u"basicGrey")),
            SimpleTerm("crayon", "crayon",
                _(u"label_layout3", default=u"crayon")),
            SimpleTerm("whiteMenu", "whiteMenu",
                _(u"label_layout4", default=u"whiteMenu")),
            SimpleTerm("wood", "wood",
                _(u"label_layout5", default=u"wood")),
            SimpleTerm("white", "http%3A%2F%2Fskin.issuu.com%2Fv%2Flight%2Flayout.xml",
                _(u"label_layout6", default=u"white")
            )
        ])
    )
    
    backgroundcolor = schema.TextLine(
        title=_(u"label_backgroundcolor,",
            default=u"Background color (does not work with all layouts)"), 
        default=u"#FFFFFF",
        required=True
    )

    
    loadinginfotext = schema.TextLine(
        title=_(u"label_loadinginfotext",
            default=u"Text to show while loading"), 
        default=u"Loading",
        required=False,
    )    

    showflipbtn = schema.Choice (
        title=_(u"label_showflipbtn",
            default=u"Show Flipbtnu"),
        default="true",
        vocabulary=SimpleVocabulary([
            SimpleTerm("false", "false",
                _(u"label_false", default=u"No")),
            SimpleTerm("true", "true",
                _(u"label_true", default=u"Yes")
            )
        ])
    )
    
    issuu_id = schema.TextLine(
        title=_(u"label_issuu_id",
            default=u"ID for the document at issuu.com. Dont edit this id unless you know what you are doing!!"), 
        default=u"101209160738-bfd67b25284249cfb535c886beb7430b",
        required=True,
    )

    issuu_name = schema.TextLine(
        title=_(u"label_issuu_name",
            default=u"Name for the document at issuu.com. Dont edit this name unless you know what you are doing!!"), 
        default=u"1234",
        required=True,
    )
