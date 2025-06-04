import battles.battles as battles
import battles.statuses as statuses
import battles.cards as cards
import copy
import random
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
    permissions: dict[str, bool] = field(default_factory=dict, init=False)

    def copy(self):
        return copy.deepcopy(self)
    
    def set_user(self, user):
        self.user = user

    def log_activation(self):
        self.user.owner.battle.log(f"- **{self.user.name}: *{self.name}***")

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
    
    # Passive effect mirrors
    async def round_start_global(self):
        """Triggers at the start of the round. Mainly useful for active abilities that grant passive effects."""
        pass
    async def turn_start_global(self):
        """Triggers at the start of the turn. Mainly useful for active abilities that grant passive effects."""
        pass

### AOT

@dataclass
class SashaActive(BaseActive):
    """- All allies recover 30% Max Health.
    Requirements: Round 3+
    """
    name: str = "Potato Girl's Treat"
    requirements: dict = field(default_factory=lambda: {"round_min": 3}, init=False)

    async def resolve(self):
        for character in self.user.owner.characters:
            await character.heal(character.max_health * 0.3)

@dataclass
class LethalBlow(BaseActive):
    """- This character's next attack deals +100% damage.
    Requirements: Round 5+
    """
    name: str = "Lethal Blow"
    requirements: dict = field(default_factory=lambda: {"round_min": 5}, init=False)

    async def resolve(self):
        await self.user.apply_status(statuses.DamageInflictedBuff(1, duration=1, duration_type='cards'))

@dataclass
class JeanActive(BaseActive):
    """- This character takes -40% damage for the rest of the round.
    Requirements: Round 3+
    """
    name: str = "Scout's Vitality"
    requirements: dict = field(default_factory=lambda: {"round_min": 3}, init=False)

    async def resolve(self):
        await self.user.apply_status(statuses.DamageReceivedBuff(-0.4, duration=1, duration_type='rounds'))



### JJK

@dataclass
class NobaraActive(BaseActive):
    """- Create 3 **[Iron Nail]** in your discard pile.
    Requirements: Round 6+
    """
    name: str = "Straw Doll: Hairpin"
    requirements: dict = field(default_factory=lambda: {"round_min": 6}, init=False)

    async def resolve(self):
        raise NotImplementedError("This ability has not been implemented yet.")

@dataclass
class InumakiActive(BaseActive):
    """- Discard all your held cards. 
    - Create five *Cursed Commands* in hand.
    Requirements: Round 4+
    """
    name: str = "Cursed Speech"
    requirements: dict = field(default_factory=lambda: {"round_min": 4}, init=False)

    async def resolve(self):
        raise NotImplementedError("This ability has not been implemented yet.")

@dataclass
class MakiActive(BaseActive):
    """- This character deals +50% damage for 1 round.
    This character takes -30% damage for 1 round.
    Requirements: Round 7+
    """
    name: str = "Destroy Everything, Big Sis"
    requirements: dict = field(default_factory=lambda: {"round_min": 7}, init=False)

    async def resolve(self):
        await self.user.apply_status(statuses.DamageInflictedBuff(0.5, duration=1, duration_type='rounds'))
        await self.user.apply_status(statuses.DamageReceivedBuff(-0.3, duration=1, duration_type='rounds'))
    

@dataclass
class NanamiActive(BaseActive):
    """- Opposing character takes +50% damage for the rest of the round.
    Requirements: Round 5+
    """
    name: str = "Ratio Technique"
    requirements: dict = field(default_factory=lambda: {"round_min": 5}, init=False)

    async def resolve(self):
        opponent = self.user.owner.opponent.active_character
        if opponent:
            await opponent.apply_status(statuses.DamageReceivedBuff(0.5, duration=0, duration_type='rounds'))



### HxH
@dataclass
class GonActive(BaseActive):
    """- Discard down to 2 cards in hand.
    - Create a **[Jajanken: Rock]**, **[Jajanken: Paper]**, and **[Jajanken: Scissors]** in hand.
    - This character recovers 40% Missing Health
    Requirements: Round 8+
    """
    name: str = "Here Comes Rock..."
    requirements: dict = field(default_factory=lambda: {"round_min": 8}, init=False)

    async def resolve(self):
        # Discard cards
        to_discard = max(0, len(self.user.owner.zones.hand) - 2)
        if to_discard:
            await self.user.owner.discard_random(to_discard)
        
        # Create cards
        await self.user.owner.create_card(cards.Cards.JAJANKEN_ROCK, 'hand')
        await self.user.owner.create_card(cards.Cards.JAJANKEN_PAPER, 'hand')
        await self.user.owner.create_card(cards.Cards.JAJANKEN_SCISSORS, 'hand')

        # Heal
        await self.user.heal((self.user.max_health - self.user.health) * 0.4)
        
@dataclass
class DoctorBlythe(BaseActive):
    """- Toggle the effects of *Doctor Blythe* on/off. Upon toggling on, you must select an ally to target.
    - *Doctor Blythe* cannot be toggled again for 1 round.

    **__Doctor Blythe: On__**
    **▼Base Effects**
    - This character deals -50% damage.
    - This character takes +50% damage.
    **▼Turn Start (Global)**
    - Targeted ally recovers 10% Max Health. If they are already at full health, *Doctor Blythe* is toggled off.
    This effect still activates when the user is on standby.
    **▼Round Start**
    If user is on standby:
    - Expend 1 Energy to maintain *Doctor Blythe*.
    Requirements: Round 2+
    """
    name: str = "Doctor Blythe"
    requirements: dict = field(default_factory=lambda: {"round_min": 2, "active_cooldown": 0}, init=False)
    target: battles.Character = field(default=None, init=False)
    cooldown: int = field(default=0, init=False)
    active: bool = field(default=False, init=False)

    async def resolve(self):
        import battles.buttons as buttons
        self.has_been_used = False # Toggleable abilities can be used indefinitely

        if self.active:
            await self.toggle_off()
        else:
            view = buttons.CharacterSelectView(self.user.owner, 'Select a target for *Doctor Blythe*')
            await self.user.owner.battle.wait_for_input([view])
            await self.toggle_on(view.selection)

    async def turn_start_global(self):
        if self.active:
            if self.target.health == self.target.max_health or self.target.is_defeated():
                await self.toggle_off()
                return
            self.log_activation()
            await self.target.heal(self.target.max_health * 0.1)

    async def round_start_global(self):
        if self.active:
            if self.user.owner.energy == 0:
                await self.toggle_off()
                return
            await self.user.owner.spend_energy(1)

    async def toggle_on(self, target: battles.Character):
        self.active = True
        self.cooldown = 1
        self.target = target
        self.user.passive_ability.passive_statuses.append(statuses.DamageInflictedBuff(-0.5, unique_id='doctor_blythe'))
        self.user.passive_ability.passive_statuses.append(statuses.DamageReceivedBuff(0.5, unique_id='doctor_blythe'))
        self.user.owner.battle.log(f"> **Doctor Blythe** is now healing *{target.name}*.")

    async def toggle_off(self):
        self.active = False
        self.cooldown = 1
        self.target = None
        self.user.passive_ability.passive_statuses = [status for status in self.user.passive_ability.passive_statuses if status.unique_id != 'doctor_blythe']
        self.user.owner.battle.log(f"> **Doctor Blythe** was deactivated.")