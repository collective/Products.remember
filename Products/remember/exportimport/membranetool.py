from zope.app.annotation.interfaces import IAnnotations

from persistent.mapping import PersistentMapping

from Products.membrane.exportimport.membranetool import MembraneToolXMLAdapter

from Products.remember.config import ANNOT_KEY, HASHERS


class RememberMembraneToolXMLAdapter(MembraneToolXMLAdapter):
    """
    Custom membrane tool config adapter so we can support storing the
    encryption mechanism in an annotation on the tool.
    """

    def _importNode(self, node):
        """
        Import the settings from the DOM node.
        """

        MembraneToolXMLAdapter._importNode(self, node)
        self._annotateHash(node)

    def _annotateHash(self, node):
        """
        Use the hash type specified in the xml file, and annotate mbtool
        If not specified, use a default hash, iff not already annotated
        """
        for child in node.childNodes:
            if child.nodeName != 'hash-type':
                continue
            htype = str(child.getAttribute('name'))
            if htype not in HASHERS:
                raise ValueError('Unknown hash type: %s - Specify one of %s' %
                                 (htype, HASHERS))
            mbtool = self.context
            annot = IAnnotations(mbtool)
            annot.setdefault(ANNOT_KEY, PersistentMapping())
            annot[ANNOT_KEY]['hash_type'] = htype
            break
