from Globals import InitializeClass

from Products.Archetypes import public as atapi

from Products.remember.content.member import Member as BaseMember
#product
from Products.sampleremember.config import DEFAULT_MEMBER_TYPE

sampleremember_schema = atapi.Schema((
    atapi.StringField(
            'favoriteColor',
            widget=atapi.StringWidget(
                label="Your Favorite Color",
                description="Enter your favorite color."),
            regfield=1,
                ),
    atapi.StringField(
            'espressoDrink',
            widget=atapi.StringWidget(
                label="Your Favorite Espresso Drink",
                description="Enter your favorite Espresso Drink."),
            regfield=0,
                ),
    ))

class SampleRemember(BaseMember):
    """A member with a favorite color."""
    archetype_name = portal_type = meta_type = DEFAULT_MEMBER_TYPE

    schema = BaseMember.schema.copy() + sampleremember_schema

atapi.registerType(SampleRemember)
InitializeClass(SampleRemember)
