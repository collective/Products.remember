from Products.membrane.at import useridprovider


class UserIdProvider(useridprovider.UserIdProvider):
    """
    Adapts from IUserAuthProvider to IMembraneUserObject.  Uses the
    object id instead of the UID.
    """

    def getUserId(self):
        return self.context.getId()
