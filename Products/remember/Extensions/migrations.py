from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from Products.remember.config import ANNOT_KEY


def migrate_bcrypt_password_storage(self):
    """
    Migrate the bcrypt salts from living in member.member_salt to
    being an annotation to BaseMember.

    Migrate the hashes from just a password hash to a format containing
    hash_type:hashed.
    """

    output = ['Beginning bcrypt salt Migration', '']

    mtool = getToolByName(self, 'portal_membership')

    for mem_id in mtool.listMemberIds():
        member = mtool.getMemberById(mem_id)
        salt = getattr(member.aq_base, 'member_salt', None)
        if salt is not None:
            annot = IAnnotations(member)
            annot[ANNOT_KEY]['bcrypt_salt'] = salt
            delattr(member, 'member_salt')

            password = member.getPassword()
            htype = 'bcrypt'
            pwfield = member.getField('password')
            pwfield.set(member, ':'.join((htype, password)))

            output.append('Migrated user: %s' % member.Title())

    output.extend(['', 'Migration Complete'])

    return '\n'.join(output)
