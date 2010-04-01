from zope.annotation.interfaces import IAnnotations

from persistent.mapping import PersistentMapping

from Products.CMFCore.utils import getToolByName

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
            mbtool = getToolByName(self.context, 'membrane_tool')
            annot = IAnnotations(mbtool)
            annot.setdefault(ANNOT_KEY, PersistentMapping())
            annot[ANNOT_KEY]['hash_type'] = htype
            self._logger.info("Remember hash-type imported: %s" % htype)
            break

    def _exportNode(self):
        """
        Export the contents as an xml node
        """
        node = MembraneToolXMLAdapter._exportNode(self)
        mbtool = getToolByName(self.context, 'membrane_tool')
        annot = IAnnotations(mbtool)
        try:
            htype = annot[ANNOT_KEY]['hash_type']
            child = self._doc.createElement('hash-type')
            child.setAttribute('name', htype)
            fragment = self._doc.createDocumentFragment()
            fragment.appendChild(child)
            node.appendChild(fragment)
            self._logger.info("Remember hash-type exported: %s" % htype)
        except KeyError:
            # no hash_type annotated on mbtool, no need to add node
            pass
        return node
