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
    unique_id: str = field(default=None, kw_only=True)
    user: "battles.Character" = field(default=None, init=False)
    permissions: dict[str, bool] = field(default_factory=dict, init=False)

    def copy(self):
        return copy.deepcopy(self)
    
    def display(self):
        return self.name
    
    def set_user(self, user: "battles.Character"):
        self.user = user

    def is_positive(self):
        """Method for determining if the status is a positive effect."""
        return True
    
    async def on_apply(self):
        """Triggers when the status is applied."""
        self.user.owner.battle.log(f"> *{self.user.name}* was **{self.name}**{f' for {self.duration} {self.duration_type}' if self.duration < 99 else ''}.")

    async def on_expire(self):
        """Triggers when the status expires. Also triggers on_remove()."""
        pass

    async def on_remove(self):
        """Triggers when the status is removed."""
        pass

    async def tick(self):
        """Decreases duration by 1 and runs any bonus effects."""
        if self.duration <= 0:
            await self.on_expire()
            await self.user.remove_status(self)
        else:
            self.duration -= 1

    async def on_negation(self):
        """Triggers when the application of the status is negated."""
        pass

    async def applicable_to_card(self, card: "battles.BaseCard"):
        """Interface method for checking if the buff applies to a card."""
        return True
    
@dataclass
class StackingStatus(BaseStatus):
    """Class for status effects that stack with further applications."""
    stacks: int

    async def on_apply(self, stacks_added: int = None):
        """Triggers when the status is applied."""
        self.user.owner.battle.log(f"> *{self.user.name}* gained **{self.stacks if stacks_added is None else stacks_added}** stacks of **{self.name}**{f' for {self.duration} {self.duration_type}' if self.duration < 99 else ''}.")

# Statuses
@dataclass
class Trapped(BaseStatus):
    """Prevents the user from switching out."""
    name: str = field(default='Trapped', init=False)
    display_emoji: str = field(default='🔒', init=False)
    permissions: dict[str, bool] = field(default_factory=lambda: {"switch_out": False}, init=False)

    def is_positive(self):
        return False
    
@dataclass
class Poison(StackingStatus):
    """Stacking status. Deals 1% max health per stack damage to the user at the end of each turn."""
    name: str = field(default='Poison', init=False)
    display_emoji: str = field(default='☣️', init=False)
    duration_type: str = field(default='turns', init=False)

    def is_positive(self):
        return False
    
    async def tick(self):
        """Deals damage to the user equal to 1% of their max health per stack."""
        damage = int(self.user.max_health * 0.01 * self.stacks)
        await self.user.inflict_damage(damage, 'poison ')
        await super().tick()
    



@dataclass
class NegateAttributeDisadvantage(BaseStatus):
    """
    Status that negates the user's attribute disadvantage.
    This status does not actively do anything, but damage calculation checks for its presence.
    """
    name: str = field(default='Immune to Attribute Disadvantage', init=False)

    def is_positive(self):
        return True

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
class BuffStatus(BaseStatus):
    """Class type for stat buffing effects."""
    multiplier: float

    def is_positive(self):
        return True if self.multiplier > 0 else False
    
    def add_multiplier(self, value: float):
        return value + self.multiplier
    
    async def on_apply(self):
        self.user.owner.battle.log(f"> *{self.user.name}*'s **{self.name.lower()}** was {'increased' if self.multiplier > 0 else 'decreased'} by {self.multiplier * -100 if self.multiplier < 0 else self.multiplier * 100}%{f' for {self.duration} {self.duration_type}' if self.duration < 99 else ''}.")

@dataclass
class DamageInflictedBuff(BuffStatus):
    """Basic damage buff.
    
    Args:
        multiplier (float): Bonus percentage to damage inflicted.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns' or 'cards'.
    """
    multiplier: float
    name: str = field(default='damage dealt', init=False)
    display_emoji: str = field(default='💪', init=False)

    def display(self):
        if self.multiplier > 0:
            return f"**+{int(self.multiplier * 100)}%** {self.name}"
        else:
            return f"**{int(self.multiplier * 100)}%** {self.name}"
        
    async def on_apply(self):
        self.user.owner.battle.log(f"> *{self.user.name}*'s **{self.name.lower()}** was {'increased' if self.multiplier > 0 else 'decreased'} by {self.multiplier * -100 if self.multiplier < 0 else self.multiplier * 100}%{f' for {self.duration} {self.duration_type}' if self.duration < 99 else ''}.")

    
@dataclass
class TagSpecificDamageInflicted(DamageInflictedBuff):
    """Conditional damage buff that only applies to cards with a specified tag.

    Args:
        multiplier (float): Bonus percentage to damage inflicted.
        condition_tag (str): List of tags that the buff applies to.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns' or 'cards'.
    """
    condition_tag: str

    async def applicable_to_card(self, card: "battles.BaseCard"):
        """Returns True if the card has the specified tag."""
        return self.condition_tag in card.tags
    
    async def on_apply(self):
        self.user.owner.battle.log(f"> *{self.user.name}*'s *{self.condition_tag.title()}* **{self.name.lower()}** was {'increased' if self.multiplier > 0 else 'decreased'} by {self.multiplier * -100 if self.multiplier < 0 else self.multiplier * 100}%{f' for {self.duration} {self.duration_type}' if self.duration < 99 else ''}.")
    
@dataclass
class RoundConditionalDamageInflicted(DamageInflictedBuff):
    """Conditional damage buff that only applies after a certain round.

    Args:
        multiplier (float): Bonus percentage to damage inflicted.
        round_min (int): Minimum round for the buff to apply.
        round_max (int): Maximum round for the buff to apply.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns' or 'cards'.
    """
    round_min: int = 0
    round_max: int = 999

    async def applicable_to_card(self, card: "battles.BaseCard"):
        """Returns True if the round is within the specified range."""
        return self.user.owner.battle.round >= self.round_min and self.user.owner.battle.round <= self.round_max

@dataclass
class DamageReceivedBuff(BuffStatus):
    """Basic damage received buff.
    
    Args:
        multiplier (float): Bonus percentage to damage received.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns' or 'cards'.
    """
    multiplier: float
    name: str = field(default='damage taken', init=False)
    display_emoji: str = field(default='🦾', init=False)

    def display(self):
        if self.multiplier > 0:
            return f"**+{int(self.multiplier * 100)}%** {self.name}"
        else:
            return f"**{int(self.multiplier * 100)}%** {self.name}"
        
    async def on_apply(self):
        self.user.owner.battle.log(f"> *{self.user.name}*'s **{self.name.lower()}** was {'increased' if self.multiplier > 0 else 'decreased'} by {self.multiplier * -100 if self.multiplier < 0 else self.multiplier * 100}%{f' for {self.duration} {self.duration_type}' if self.duration < 99 else ''}.")

    def add_multiplier(self, value: float):
        return value * self.multiplier

@dataclass
class SpeedBuff(BuffStatus):
    """Basic flat speed buff.
    
    Args:
        multiplier (float): Flat bonus to speed.
        duration (int): Duration of the buff.
        duration_type (str): Units of duration. Default is 'rounds', can also be 'turns' or 'cards'.
    """
    multiplier: float
    name: str = field(default='speed', init=False)
    display_emoji: str = field(default='🏃‍♂️', init=False)

    def display(self):
        return f"**{'+' if self.multiplier > 0 else ''}{int(self.multiplier)}** {self.name}"
        
    async def on_apply(self):
        self.user.owner.battle.log(f"> *{self.user.name}*'s **{self.name.lower()}** was {'increased' if self.multiplier > 0 else 'decreased'} by {self.multiplier * -100 if self.multiplier < 0 else self.multiplier * 100}%{f' for {self.duration} {self.duration_type}' if self.duration < 99 else ''}.")


import battles.battles as battles