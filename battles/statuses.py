import battles.battles as battles
import copy
from enum import Enum
from dataclasses import dataclass, field

@dataclass
class BaseStatus():
    """
    Provides a base class for status effects that can be applied to characters.
    Subclass this to create new status effects. Subclasses need only define the events they use.
    """
    name: str
    duration: int = field(default=999, kw_only=True)
    duration_type: str = field(default='rounds', kw_only=True)
    display_emoji: str = field(default=None, kw_only=True)
    user: battles.Character = field(default=None, init=False)

    def copy(self):
        return copy.deepcopy(self)
    
    def set_user(self, user: battles.Character):
        self.user = user
    
    async def on_apply(self):
        """Triggers when the status is applied."""
        pass

    async def on_expire(self):
        """Triggers when the status expires. Also triggers on_remove()."""
        await self.on_remove()

    async def on_remove(self):
        """Triggers when the status is removed."""
        pass

    async def tick(self):
        """Triggers at the start of each round."""
        pass

    async def on_negation(self):
        """Triggers when the application of the status is negated."""
        pass


# Statuses
@dataclass
class Trapped(BaseStatus):
    """Prevents the user from switching out."""
    name: str = field(default='Trapped', init=False)
    display_emoji: str = field(default='🔒', init=False)

@dataclass
class NegateAttributeDisadvantage(BaseStatus):
    """
    Status that negates the user's attribute disadvantage.
    This status does not actively do anything, but damage calculation checks for its presence.
    """
    name: str = field(default='Immune to Attribute Disadvantage', init=False)

@dataclass
class StatusImmunity(BaseStatus):
    """Status that negates the application of a specified status effect to the user.

    Args:
        immune_to (BaseStatus): Status effect that the user is immune to.
    """
    immune_to: BaseStatus
    name: str = field(default='Status Immunity', init=False)


# Buffs
@dataclass
class DamageInflictedBuff(BaseStatus):
    """Basic damage buff.
    
    Args:
        multiplier (float): Bonus percentage to damage inflicted.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns' or 'cards'.
    """
    multiplier: float
    name: str = field(default='Damage Inflicted', init=False)
    display_emoji: str = field(default='💪', init=False)

    async def applicable_to_card(self, card: battles.BaseCard):
        """Interface method for checking if the buff applies to a card."""
        return True
    
@dataclass
class TagSpecificDamageInflicted(DamageInflictedBuff):
    """Conditional damage buff that only applies to cards with a specified tag.

    Args:
        multiplier (float): Bonus percentage to damage inflicted.
        condition_tag (str): List of tags that the buff applies to.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns'.
    """
    condition_tag: list

    async def applicable_to_card(self, card: battles.BaseCard):
        """Returns True if the card has the specified tag."""
        return self.condition_tag in card.tags

# Buffs
@dataclass
class DamageReceivedBuff(BaseStatus):
    """Basic damage received buff.
    
    Args:
        multiplier (float): Bonus percentage to damage received.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns' or 'cards'.
    """
    multiplier: float
    name: str = field(default='Damage Inflicted', init=False)
    display_emoji: str = field(default='🦾', init=False)

    async def applicable_to_card(self, card: battles.BaseCard):
        """Interface method for checking if the buff applies to a card."""
        return True