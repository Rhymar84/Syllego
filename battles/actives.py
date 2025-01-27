import battles.battles as battles
import battles.statuses as statuses
import copy
from enum import Enum
from dataclasses import dataclass, field
from inspect import cleandoc

@dataclass
class BaseActive():
    """ Provides a base class for active abilities that can be attached to characters.
    Subclass this to create new active abilities. Subclasses need only define the events they use.
    """
    name: str
    user: battles.Character = field(default=None, init=False)
    requirements: dict = field(default_factory=dict, init=False)
    has_been_used: bool = field(default=False, init=False)

    def copy(self):
        return copy.deepcopy(self)
    
    def set_user(self, user):
        self.user = user

    async def on_activation(self):
        """Triggers when the ability is activated."""
        pass

    async def resolve(self):
        """Effect of the ability when it resolves."""
        pass

    def can_be_used(self) -> bool:
        """Determines if the ability can be used."""
        return (not self.has_been_used) and self.user.requirements_met(self.requirements)
    
    @classmethod
    def display(cls):
        return '\n'.join([f"> {line}" for line in cleandoc(cls.__doc__).split('\n')])


@dataclass
class SashaActive(BaseActive):
    """All allies recover 30% Max Health.
    Requirements: Round 3+
    """
    name: str = "Potato Girl's Treat"
    requirements: dict = field(default_factory=lambda: {"round_min": 3}, init=False)

    async def resolve(self):
        for character in self.user.owner.characters:
            await character.heal(character.max_health * 0.3)

@dataclass
class LethalBlow(BaseActive):
    """Apply the following effect to self:
    - +100% damage inflicted by the user's next attack.
    Requirements: Round 5+
    """
    name: str = "Lethal Blow"
    requirements: dict = field(default_factory=lambda: {"round_min": 5}, init=False)

    async def resolve(self):
        await self.user.apply_status(statuses.DamageInflictedBuff(1, duration=1, duration_type='cards'))

@dataclass
class JeanActive(BaseActive):
    """Apply the following effect to self:
    - -40% damage received for the rest of the round.
    Requirements: Round 3+
    """
    name: str = "Scout's Vitality"
    requirements: dict = field(default_factory=lambda: {"round_min": 3}, init=False)

    async def resolve(self):
        await self.user.apply_status(statuses.DamageInflictedBuff(1, duration=1, duration_type='cards'))

@dataclass
class NobaraActive(BaseActive):
    """Create 3 **[Iron Nail]** in your discard pile.
    Requirements: Round 6+
    """
    name: str = "Straw Doll: Hairpin"
    requirements: dict = field(default_factory=lambda: {"round_min": 6}, init=False)

    async def resolve(self):
        raise NotImplementedError("This ability has not been implemented yet.")

@dataclass
class InumakiActive(BaseActive):
    """Discard all cards in your hand, then create five *Cursed Commands*.
    Requirements: Round 4+
    """
    name: str = "Cursed Speech"
    requirements: dict = field(default_factory=lambda: {"round_min": 4}, init=False)

    async def resolve(self):
        raise NotImplementedError("This ability has not been implemented yet.")

@dataclass
class MakiActive(BaseActive):
    """Apply the following effects to self:
    - +50% damage inflicted.
    - -30% damage received.
    Requirements: Round 7+
    """
    name: str = "Destroy Everything, Big Sis"
    requirements: dict = field(default_factory=lambda: {"round_min": 7}, init=False)

    async def resolve(self):
        raise NotImplementedError("This ability has not been implemented yet.")
    