import zope.interface

class ITreeSelectURLProvider(zope.interface.Interface):
    """
    Adapter to look up tree select AJAX source urls for DGFTreeSelectWidget.

    Look-up syntax is ()
    """

