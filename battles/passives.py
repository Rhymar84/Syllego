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
    passive_statuses: list[statuses.BaseStatus] = field(default_factory=list, init=False)
    permissions: dict[str, bool] = field(default_factory=dict, init=False)

    def copy(self):
        return copy.deepcopy(self)
    
    def set_user(self, user):
        self.user = user

    def can_use_card(self, card: cards.BaseCard):
        """Determines if the user can use the card."""
        return True
    
    def log_activation(self):
        self.user.owner.battle.log(f"- **{self.user.name}: *{self.name}***")

    async def battle_start(self):
        """Triggers once, at the start of the battle."""
        pass

    async def round_start(self):
        """Triggers at the start of each round."""
        pass
    async def round_start_global(self):
        """Same as round_start, but also triggers for characters on standby."""
        pass

    async def round_end(self):
        """Triggers at the end of each round."""
        pass
    async def round_end_global(self):    
        """Same as round_end, but also triggers for characters on standby."""
        pass

    async def turn_start(self):
        """Triggers at the start of each turn."""
        pass
    async def turn_start_global(self):
        """Same as turn_start, but also triggers for characters on standby."""
        pass

    async def turn_end(self):
        """Triggers at the end of each turn."""
        pass
    async def turn_end_global(self):
        """Same as turn_end, but also triggers for characters on standby."""
        pass

    async def switch_in(self, ally: battles.Character):
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

    async def hit_by_attack(self, damage: int):
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
    """**Turn Start**
    - Recover 3% Max Health.
    **Switch In**
    - Gain 20 Shield.
    - Negate Attribute Disadvantage for the rest of the round.
    **Adaptive Card**
    **[Titan Shift]:** Transform into the *Attack Titan*.
    """
    name: str = "Unrivalled Tenacity"

    async def turn_end(self):
        await self.user.heal(int(self.user.max_health * 0.03))

    async def switch_in(self, ally):
        await self.user.add_shield(20)
        await self.user.apply_status(statuses.NegateAttributeDisadvantage(0))

@dataclass
class Safeguard(BasePassive):
    """**Switch Out**
    - Next ally takes -50% damage for 1 turn.
    """
    name: str = "Safeguard"

    async def switch_out(self, ally: battles.Character):
        await ally.apply_status(statuses.DamageReceivedBuff(-0.5, duration=1, duration_type='turns'))

@dataclass
class SashaPassive(BasePassive):
    """**Base Effects**
    This character's *Projectile* attacks deal +35% damage."""
    name: str = 'Marksman'
    
    def __post_init__(self):
        self.passive_statuses.append(statuses.TagSpecificDamageInflicted(0.35, 'projectile'))

@dataclass
class ConniePassive(BasePassive):
    """**Base Effects**
    This character is immune to the *Trapped* status effect."""
    name: str = "Omni-Directional Expert"

    def __post_init__(self):
        self.passive_statuses.append(statuses.StatusImmunity(statuses.Trapped))






### Jujutsu Kaisen

@dataclass
class NobaraPassive(BasePassive):
    """**When Hit**
    - Echo 50% of damage taken back to the opponent."""
    name: str = "Straw Doll: Resonance"

    async def hit_by_attack(self, damage: int):
        opponent = self.user.owner.opponent.active_character
        if opponent:
            await opponent.inflict_damage(int(damage * 0.5))

@dataclass
class HeavenlyRestriction(BasePassive):
    """**Base Effects**
    - This character's *Contact* attacks deal +50% damage.
    - This character cannot use non-attack cards.
    """
    name: str = 'Heavenly Restriction'
    
    def __post_init__(self):
        self.passive_statuses.append(statuses.TagSpecificDamageInflicted(0.5, 'contact'))

    def can_use_card(self, card: cards.BaseCard):
        return isinstance(card, cards.BaseAttack)

@dataclass
class MusterEnergy(BasePassive):
    """**Spend Energy**
    - If your last energy was spent, replenish 1 energy (once per battle).
    """
    name: str = "Muster Energy"
    effect_used: bool = field(default=False, init=False)

    async def activate_card(self, card):
        if self.user.owner.energy == 0 and not self.effect_used:
            self.log_activation()
            self.effect_used = True
            await self.user.owner.gain_energy(1)

@dataclass
class NanamiPassive(BasePassive):
    """**Base Effects**
    - This character deals +70% damage on round 10 or later.
    """
    name: str = field(default="Overtime", init=False)

    def __post_init__(self):
        self.passive_statuses.append(statuses.RoundConditionalDamageInflicted(0.7, 10))

### One Punch Man


### My Hero Academia


### Demon Slayer


# HxH

@dataclass
class GonPassive(BasePassive):
    """**Land Attack**
    - This character takes -5% damage (persistent).
    **When Hit**
    - This character deals +5% damage (persistent).
    - This character's *Jajanken* attacks deal +10% damage (persistent).
    """
    name: str = "Ramping Determination"
    inflicted_buff: statuses.DamageInflictedBuff = field(default=None, init=False)
    received_buff: statuses.DamageReceivedBuff = field(default=None, init=False)
    jajanken_buff: statuses.TagSpecificDamageInflicted = field(default=None, init=False)
    

    async def hit_by_attack(self, damage: int):
        if self.inflicted_buff is None:
            self.inflicted_buff = statuses.DamageInflictedBuff(0)
            self.jajanken_buff = statuses.TagSpecificDamageInflicted(0, 'jajanken')
            self.passive_statuses.append(self.inflicted_buff)
            self.passive_statuses.append(self.jajanken_buff)

        self.inflicted_buff.multiplier += 0.05
        self.jajanken_buff.multiplier += 0.1
        await self.user.owner.battle.log(f"> *{self.user.name}*'s **damage dealt** was increased by 5%.")
        await self.user.owner.battle.log(f"> *{self.user.name}*'s ***\"Jajanken\"* damage** was increased by 10%.")

    async def on_hit_attack(self):
        if self.inflicted_buff is None:
            self.inflicted_buff = statuses.DamageInflictedBuff(0)
            self.passive_statuses.append(self.inflicted_buff)

        self.inflicted_buff.multiplier -= 0.05
        await self.user.owner.battle.log(f"> *{self.user.name}*'s **damage taken** was decreased by 5%.")

@dataclass
class PitouPassive(BasePassive):
    """**Switch In**
    The following effects activate if the active ally is below 50% health, or *Tag: Chimera Ant*:
    - This character gains 50 shield.
    - Draw 1 card.
    - Reduce enemy energy by 1 (once per battle).
    **Turn End**
    - If an enemy was defeated this turn, permanently reveal the opponent's hand and the top 5 cards of their deck.
    This effect still activates when the user is on standby.
    """
    name: str = "Puppeteering"
    disrupt_used: bool = field(default=False, init=False)
    living_enemies: list[battles.Character] = field(default_factory=list, init=False)

    async def switch_in(self, ally: battles.Character):
        if ally is not None and (ally.health / ally.max_health <= 0.5 or 'Chimera Ant' in ally.tags):
            await self.user.add_shield(50)
            await self.user.owner.draw(1)

            if not self.disrupt_used and self.user.owner.opponent.energy > 0:
                self.disrupt_used = True
                await self.user.owner.opponent.reduce_energy(1)

    async def turn_start_global(self):
        self.living_enemies = [x for x in self.user.owner.opponent.characters]

    async def turn_end_global(self):
        if len(self.user.owner.opponent.characters) < len(self.living_enemies):
            self.log_activation()
            to_reveal = [x for x in self.user.owner.opponent.zones.hand] + [y for y in self.user.owner.opponent.zones.deck[:5]]
            if to_reveal:
                for card in to_reveal:
                    await card.reveal(True)
                await self.user.owner.battle.log(f"> **{len(to_reveal)}** cards were permanently revealed.")

    
