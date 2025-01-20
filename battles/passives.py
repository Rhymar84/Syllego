import battles.battles as battles
import battles.statuses as statuses
import copy
from enum import Enum
from dataclasses import dataclass, field

@dataclass
class BasePassive():
    """
    Provides a base class for passive abilities that can be attached to characters.
    Subclass this to create new passive abilities. Subclasses need only define the events they use.
    """
    name: str
    user: battles.Character = field(default=None, init=False)
    passive_statuses: list = field(default_factory=list, init=False)

    def copy(self):
        return copy.deepcopy(self)
    
    def set_user(self, user):
        self.user = user

    async def battle_start(self):
        """Triggers once, at the start of the battle."""
        pass

    async def round_start(self):
        """Triggers at the start of each round."""
        pass

    async def round_end(self):
        """Triggers at the end of each round."""
        pass

    async def turn_start(self):
        """Triggers at the start of each turn."""
        pass

    async def turn_end(self):
        """Triggers at the end of each turn."""
        pass

    async def switch_in(self):
        """Triggers when the user switches in."""
        pass

    async def switch_out(self):
        """Triggers when the user switches out."""
        pass

    async def activate_card(self, card: battles.BaseCard):
        """Triggers when the user activates a card."""
        pass

    async def targeted_by_attack(self):
        """
        Triggers when the user is targeted by an attack.
        This function runs before the attack resolves.
        """
        pass

    async def on_hit_attack(self, damage: int):
        """Triggers when the user successfully hits an attack."""
        pass

    async def hit_by_attack(self):
        """Triggers after the user is hit by an attack."""
        pass

    async def on_death(self):
        """Triggers when the user is defeated."""
        pass

    async def on_kill(self):
        """Triggers when the user defeats an opponent."""
        pass


######## UNIQUE PASSIVES ########


### DRAGON BALL Z


### Re:Zero


### Attack on Titan

class ErenPassive(BasePassive):
    """Each turn, recover 3% Max Health.
    **Switch in**: Apply the following effects:
    - Gain 20 Shield.
    - Negate Attribute Disadvantage for the rest of the round.
    Upon using **[Titan Shift]**, transform into the *Attack Titan*.
    """
    name: str = "Unrivalled Tenacity"

    async def turn_end(self):
        await self.user.heal(int(self.user.max_health * 0.03))

    async def switch_in(self):
        await self.user.add_shield(20)
        await self.user.apply_status(statuses.NegateAttributeDisadvantage(0))

@dataclass
class SashaPassive(BasePassive):
    """+35% Damage Inflicted by *Projectile* Attacks."""
    name: str = 'Marksman'
    
    def __post_init__(self):
        self.passive_statuses.append(statuses.TagSpecificDamageInflicted(0.35, ['projectile']))

@dataclass
class ConniePassive(BasePassive):
    """Negate the application of the *Trapped* status effect to this character."""
    name: str = "Omni-Directional Expert"

    def __post_init__(self):
        self.passive_statuses.append(statuses.StatusImmunity(statuses.Trapped))

### Jujutsu Kaisen


### One Punch Man


### My Hero Academia


### Demon Slayer
    