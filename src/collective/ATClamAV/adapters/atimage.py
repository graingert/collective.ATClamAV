from archetypes.schemaextender.interfaces import ISchemaExtender
from plone.app.blob.subtypes.image import ExtensionBlobField
from Products.Archetypes.atapi import ImageWidget, AnnotationStorage
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.interfaces.image import IATImage
from Products.ATContentTypes import ATCTMessageFactory as _
from Products.validation import V_REQUIRED
from zope.component import adapts
from zope.interface import implements


class VirusFreeATImageExtender(object):
    """
    """
    adapts(IATImage)
    implements(ISchemaExtender)

    fields = [
        ExtensionBlobField('image',
            required = True,
            primary = True,
            accessor = 'getImage',
            mutator = 'setImage',
            sizes = None,
            languageIndependent = True,
            storage = AnnotationStorage(migrate=True),
            swallowResizeExceptions = zconf.swallowImageResizeExceptions.enable,
            pil_quality = zconf.pil_config.quality,
            pil_resize_algo = zconf.pil_config.resize_algo,
            original_size = None,
            max_size = zconf.ATImage.max_image_dimension,
            default_content_type = 'image/png',
            allowable_content_types = ('image/gif', 'image/jpeg', 'image/png'),
            validators = (('isVirusFree', V_REQUIRED),
                          ('isNonEmptyFile', V_REQUIRED),
                          ('checkImageMaxSize', V_REQUIRED)),
            widget = ImageWidget(label = _(u'label_image', default=u'Image'),
                                 description=_(u''),
                                 show_content_type = False,)),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
