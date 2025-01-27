import battles.battles as battles
import battles.statuses as statuses
import battles.cards as cards
import copy
from enum import Enum
from dataclasses import dataclass, field
from inspect import cleandoc

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

    async def switch_out(self, ally: battles.Character):
        """Triggers when the user switches out.
        Args:
            ally (battles.Character): The character that is switching in.
        """
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

    async def took_damage(self, damage: int):
        """Triggers when the user takes damage."""
        pass

    async def on_death(self):
        """Triggers when the user is defeated."""
        pass

    async def on_kill(self):
        """Triggers when the user defeats an opponent."""
        pass
    
    @classmethod
    def display(cls):
        return '\n'.join([f"> {line}" for line in cleandoc(cls.__doc__).split('\n')])



######## UNIQUE PASSIVES ########


### DRAGON BALL Z


### Re:Zero


### Attack on Titan

@dataclass
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
class Safeguard(BasePassive):
    """**Switch Out**: Apply the following effects to switching ally:
    - -50% Damage Received for 1 turn.
    """
    name: str = "Safeguard"

    async def switch_out(self, ally: battles.Character):
        await ally.apply_status(statuses.DamageReceivedBuff(-0.5, duration=1, duration_type='turns'))

@dataclass
class SashaPassive(BasePassive):
    """+35% Damage Inflicted by *Projectile* attacks."""
    name: str = 'Marksman'
    
    def __post_init__(self):
        self.passive_statuses.append(statuses.TagSpecificDamageInflicted(0.35, ['projectile']))

@dataclass
class ConniePassive(BasePassive):
    """Negate the application of the *Trapped* status effect to this character."""
    name: str = "Omni-Directional Expert"

    def __post_init__(self):
        self.passive_statuses.append(statuses.StatusImmunity(statuses.Trapped))

@dataclass
class NobaraPassive(BasePassive):
    """Upon taking damage, also inflict 50% of the damage received to the opponent."""
    name: str = "Straw Doll: Resonance"

    async def took_damage(self, damage: int):
        opponent = self.user.owner.opponent.active_character
        if opponent:
            await opponent.inflict_damage(int(damage * 0.5))

@dataclass
class HeavenlyRestriction(BasePassive):
    """+50% Damage Inflicted by *Contact* attacks.
    Negate the activation of any non-attack cards used by this character.
    """
    name: str = 'Heavenly Restriction'
    
    def __post_init__(self):
        self.passive_statuses.append(statuses.TagSpecificDamageInflicted(0.5, ['contact']))

    async def activate_card(self, card):
        if not isinstance(card, cards.BaseAttack):
            await card.negate()

@dataclass
class MusterEnergy(BasePassive):
    """The first time this character expends your last energy, activate the following effect:
    - Replenish 1 energy.
    """
    name: str = "Muster Energy"
    effect_used: bool = field(default=False, init=False)

    async def activate_card(self, card):
        if self.user.owner.energy == 0 and not self.effect_used:
            self.effect_used = True
            await self.user.owner.gain_energy(1)

### Jujutsu Kaisen


### One Punch Man


### My Hero Academia


### Demon Slayer
    