from zope.formlib import form
from zope.interface import implements
from zope.component import adapts
import zope.lifecycleevent
from zope.component import getMultiAdapter

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from plone.app.form import base as ploneformbase

from medialog.issuu.interfaces import IIssuuSettings 
from medialog.issuu import issuuMessageFactory as _
from medialog.issuu.settings import IssuuSettings
 
from Products.SmartColorWidget.Widget import SmartColorWidget

 

class IssuuSettingsForm(ploneformbase.EditForm):
    """
    The page that holds all the issuu settings
    """
    form_fields = form.FormFields(IIssuuSettings)
      
    label = _(u'heading_issuu_settings_form', default=u"Issuu Settings")
    description = _(u'description_issuu_settings_form', default=u"Configure the parameters for this file.")
    form_name = _(u'title_issuu_settings_form', default=u"Issuu settings")
            
    #Wanted to use another widget, but its not working at the moment
    #form_fields['backgroundcolor'].custom_widget = SmartColorWidget