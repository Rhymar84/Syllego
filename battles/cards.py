import copy
import asyncio
import random
import battles.battles as battles
from enum import Enum
from dataclasses import dataclass, field

@dataclass
class BaseCard():
    """Provides empty functions for all card mechanics.
    Subclass card types only need to define the mechanics they use; other events will call the pass functions in this class.
    This class is not a functional card, and is only used to provide an interface for card types.
    """
    name: str
    cost: int
    restrictions: dict = field(default_factory=dict, kw_only=True)  #kw only fields go at the end of dataclass __init()__ to avoid compilation errors
    keywords: list[str] = field(default_factory=list, kw_only=True) 
    priority: int = field(default=0, kw_only=True)
    tags: tuple = field(default=tuple(), kw_only=True)
    owner: battles.Player = field(default=None, init=False)  # not included in constructor because only assigned to copies used in battles
    location: str = field(default=None, init=False)


    def copy(self):
        return copy.deepcopy(self)
    
    def set_owner(self, player):
        self.owner = player

    def set_location(self, location: str):
        self.location = location

    async def info_text(self) -> str:
        """Generates the description text displayed when viewing the card information."""
        text = f"**{'. '.join(self.keywords).title()}.**" if self.keywords else ''

        for key, value in self.restrictions.items():
            match key:
                case 'user_tag':
                    text += f"\nCan only be used by *Tag: {value}* characters."

        return text

    async def move_to(self, destination: str):
        await self.owner.zones.move(self, destination)
        
    async def discard(self):
        if 'ephemeral' in self.keywords and self.location == 'selection':
            await self.owner.zones.erase(self)
        else:
            await self.owner.zones.discard(self)
        
    async def on_activation(self):
        """Runs when the card is activated, before any effects resolve."""
        pass

    async def resolve(self):
        """Main effects of the card when it resolves."""
        pass

    async def on_discard(self):
        """Runs when the card leaves the hand and is sent to the discard pile."""
        pass

    async def on_draw(self):
        """Runs when the card is drawn from the deck into the hand."""
        pass


@dataclass
class BaseAttack(BaseCard):
    """
    Generic attack type card.
    Takes inputs for attack and defense stat, damage type, and attack and defense ratios used.
    Simply calculates damage and inflicts it to the opponent on use.
    """
    atk_stat: str
    def_stat: str
    dmg_type: str
    atk_multiplier: float
    def_multiplier: float

    
    async def resolve(self):
        """
        Inflicts damage to the opposing active character equal to:
        damage = atk_stat * atk_multiplier * 100 / (100 + def_stat * def_multiplier)
        """

        user: battles.Character = self.owner.active_character

        if not user or not self.owner.opponent.active_character:
            return
        
        target: battles.Character = self.owner.opponent.active_character

        await target.targeted_by_attack()

        atk_stat = user.get_stat(self.atk_stat)
        def_stat = target.get_stat(self.def_stat)
        damage = atk_stat * self.atk_multiplier * random.randint(80, 120) / (100 + def_stat * self.def_multiplier)

        await target.inflict_damage(damage)
        await user.on_hit_attack(damage)
        await target.hit_by_attack()

    
    async def info_text(self):
        # Basic text
        text = "Inflicts **{power}%** {dmg_type} damage to the opponent.".format(power = int(self.atk_multiplier * 100), dmg_type = self.dmg_type)

        # Add lines for if the attack/defense stats differ from the norm
        if (self.dmg_type == 'physical' and self.atk_stat != 'atk') or (self.dmg_type == 'magic' and self.atk_stat != 'm.a'):
            text += "\nThe user's *{atk_stat}* stat is used in damage calculation instead.".format(atk_stat = self.atk_stat)
        if (self.dmg_type == 'physical' and self.def_stat != 'def') or (self.dmg_type == 'magic' and self.def_stat != 'm.d'):
            text += "\nThe target's *{def_stat}* stat is used in damage calculation instead.".format(def_stat = self.def_stat)

        # Add line for if the defense multiplier is different from normal
        if self.def_multiplier != 1:
            if self.def_multiplier > 1:
                text += "\nThe target's defense is **{extra_def}%** more effective against this attack.".format(extra_def = int(100 * (self.def_multiplier - 1)))
            else:
                text += "\nIgnores {ignored_def}% of the target's defense.".format(ignored_def = int(100 * (1 - self.def_multiplier)))

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text
    

@dataclass
class BuffApplyingAttack(BaseAttack):
    """
    Attack type card.
    Has the additional effect of applying the specified buff to the target when they are hit.
    """
    buff_stat: str
    buff_value: float
    buff_duration: int
    duration_units: str
    is_flat_buff: bool = field(default=False, kw_only=True)

    async def info_text(self):
        text = await super().info_text()

        text += "\nApplies the following effect to the target:\n- **{value}** {stat}{duration}.".format(
            value = f"{'' if self.buff_value < 0 else '+'}{int(self.buff_value * 100)}{'' if self.is_flat_buff else '%'}",
            stat = battles.BUFF_STAT_KEY[self.buff_stat],
            duration = f" for {self.buff_duration} {self.duration_units}" if self.buff_duration < 99 else ""
        )

        return text
        

@dataclass
class HitAllAttack(BaseAttack):
    """
    Attack type card.
    Hits all opposing characters instead of just one.
    If bench_multiplier is specified, bench characters will receive a different ratio of damage.
    """
    bench_multiplier: float = field(default=1, kw_only=True)

    async def resolve(self):

        user: battles.Character = self.owner.active_character
        if not user or not self.owner.opponent.active_character:
            return
        
        variance = random.randint(80, 120)

        for target in [char for char in self.owner.opponent.characters if char is not self.owner.opponent.active_character]:
            atk_stat = user.get_stat(self.atk_stat)
            def_stat = target.get_stat(self.def_stat)
            damage = atk_stat * self.atk_multiplier * self.bench_multiplier * variance / (100 + def_stat * self.def_multiplier)

            await target.inflict_damage(damage)

        await super().resolve()

    async def info_text(self):
        text = await super().info_text()
        text += "\nHits all enemy characters."


        
@dataclass
class BaseBlock(BaseCard):
    """
    Generic effect card that grants the user a specified amount of Shield.
    """
    shield_amount: int


    async def resolve(self):
        user: battles.Character = self.owner.active_character
        if user:
            await user.add_shield(self.shield_amount)

    async def info_text(self):
        text = "Gain **{shield}** Shield.".format(shield = self.shield_amount)

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text



@dataclass
class BaseDrawEffect(BaseCard):
    """
    Generic card draw effect card. Simply calls the draw() function of the card's owner with the specified
    number of cards passed as a parameter.
    """
    draw_number: int


    async def resolve(self):
        await self.owner.draw(self.draw_number)

    async def info_text(self):
        text = "Draw **{cards}** cards.".format(cards = self.draw_number)

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text


@dataclass
class TitanShift(BaseCard):
    """
    Unique card type unlocked by collecting all Attack on Titan characters.
    Transforms a *Tag: Titan Shifter* character into their Titan form.
    """

    async def resolve(self):
        user: battles.Character = self.owner.active_character
        if not user or 'Titan Shifter' not in user.tags:
            return
        
        match user.name:
            case 'Eren Jaeger':
                await user.transform('Attack Titan')


    async def info_text(self):
        extra = await super().info_text()
        return f"{extra}\nTransforms the user into their Titan form." if extra else "Transforms the user into their Titan form."
    






    
class Cards(Enum):
    
    STRIKE = BaseAttack('Strike', 1, 'atk', 'def', 'physical', 1, 1, tags=('contact',))
    BLAST = BaseAttack('Blast', 1, 'm.a', 'm.d', 'magic', 1, 1, tags=('projectile',))
    BLOCK = BaseBlock('Block', 1, 60)
    FOCUS = BaseDrawEffect('Focus', 1, 2)

    SLAM = BaseAttack('Slam', 2, 'atk', 'def', 'physical', 2.1, 1, tags=('contact',))
    PIERCE = BaseAttack('Pierce', 2, 'atk', 'def', 'physical', 1, 0.7, tags=('contact',))
    FORTIFY = BaseBlock('Fortify', 2, 140)
    BEAM = BuffApplyingAttack('Beam', 2, 'm.a', 'm.d', 'magic', 1.5, 1, 'dmg_received', 0.1, 99, 'rounds', is_flat_buff=False)
    EXPLOSION = HitAllAttack('Explosion', 3, 'm.a', 'm.d', 'magic', 1.5, 1, bench_multiplier=0.5)

    # Attack On Titan
    TITAN_SHIFT = TitanShift('Titan Shift', 3, restrictions={'user_tag': 'Titan Shifter'}, keywords=['ephemeral', 'adaptive'])








def get_card(name:str) -> BaseCard:
    card = [x for x in list(Cards) if x.name.lower() == name.lower()]
    if card:
        return card[0].value

def create_card(name:str) -> BaseCard:
    card = get_card(name)
    if card:
        return card.copy()