from zope.formlib import form
from zope.interface import implements
from zope.component import adapts
import zope.lifecycleevent
from zope.component import getMultiAdapter

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from plone.app.form import base as ploneformbase
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

from medialog.issuu.interfaces import IIssuuSettings 
from medialog.issuu import issuu_message_factory as _
from medialog.issuu.settings import IssuuSettings

    
  

class IssuuSettingsForm(ploneformbase.EditForm):
    """
    The page that holds all the issuu settings
    """
    form_fields = form.FormFields(IIssuuSettings)
      
    label = _(u'heading_issuu_settings_form', default=u"Slider Settings")
    description = _(u'description_issuu_settings_form', default=u"Configure the parameters for this issuu.")
    form_name = _(u'title_issuu_settings_form', default=u"Slider settings")
    
    