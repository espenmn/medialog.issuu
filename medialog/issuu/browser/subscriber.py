from zope.interface import implements, alsoProvides 
from medialog.issuu.interfaces import IIsPDFLayer

#with help fro Jens W. Klein (13 april 2012)
def apply_pdfmarker(obj, event):
    if context.unrestrictedTraverse('@@issuu_util/is_pdf')():
        alsoProvides(event.request, IIsPDFLayer)
