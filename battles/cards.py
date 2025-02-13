import copy
import random
import config
import math
from enum import Enum, member
from dataclasses import dataclass, field

@dataclass
class BaseCard():
    """Provides empty functions for all card mechanics.
    Subclass card types only need to define the mechanics they use; other events will call the pass functions in this class.
    This class is not a functional card, and is only used to provide an interface for card types.
    """
    
    name: str
    rarity: str
    cost: int
    requirements: dict = field(default_factory=dict, kw_only=True)  #kw only fields go at the end of dataclass __init()__ to avoid compilation errors
    keywords: list[str] = field(default_factory=list, kw_only=True) 
    priority: int = field(default=0, kw_only=True)
    tags: tuple = field(default=tuple(), kw_only=True)
    filename: str = field(default=None, kw_only=True)

    revealed: int = field(default=0, kw_only=True)
    owner: "battles.Player" = field(default=None, init=False)  # not included in constructor because only assigned to copies used in battles
    location: str = field(default=None, init=False)
    negated: bool = field(default=False, init=False)
    energy_spent: int = field(default=0, init=False)
    


    def copy(self):
        return copy.deepcopy(self)
    
    def set_owner(self, player):
        self.owner = player

    def set_location(self, location: str):
        self.location = location

    def display(self):
        return f"**[{self.name}]** ({self.cost})"

    async def info_text(self) -> str:
        """Generates the description text displayed when viewing the card information."""
        text = f"**{'. '.join(self.keywords).title()}.**" if self.keywords else ''
        text += f"\n*Priority*: {'+' + str(self.priority) if self.priority > 0 else self.priority}" if self.priority != 0 else ''

        for key, value in self.requirements.items():
            match key:
                case 'user_tag':
                    text += f"\nCan only be used by *Tag: {value}* characters."
                case 'user_name':
                    text += f"\nCan only be used by *Character: {value}*."

        return text

    async def move_to(self, destination: str):
        success = await self.owner.zones.move(self, destination)
        if success:
            self.negated = False
            if self.revealed == 1:
                self.revealed = 0
            
        
    async def discard(self, run_on_discard = True):
        if ('ephemeral' in self.keywords and self.location == 'selection') or 'fleeting' in self.keywords:
            await self.owner.zones.erase(self)
        else:
            await self.owner.zones.discard(self, run_on_discard)

    async def negate(self):
        if not self.negated:
            self.negated = True
            await self._on_negation()

    async def reveal(self, permanent: bool = False):
        reveal_type = 2 if permanent else 1
        if reveal_type > self.revealed:
            self.revealed = reveal_type
            await self._on_reveal()

        
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
    
    async def _on_negation(self):
        """Runs when the card is negated."""
        pass
    
    async def _on_reveal(self):
        """Runs when the card is revealed."""
        pass

@dataclass
class BaseAttack(BaseCard):
    """Generic attack type card.
    Takes inputs for attack and defense stat, damage type, and attack and defense ratios used.
    Simply calculates damage and inflicts it to the opponent on use.
    """
    atk_stat: str
    def_stat: str
    dmg_type: str
    atk_multiplier: float
    def_multiplier: float

    
    async def resolve(self):
        """Inflicts damage to the opposing active character equal to:
        damage = atk_stat * atk_multiplier * 100 / (100 + def_stat * def_multiplier)
        """

        user: battles.Character = self.owner.active_character

        if not user or not self.owner.opponent.active_character:
            return
        
        target: battles.Character = self.owner.opponent.active_character

        await target.targeted_by_attack()

        dmg_inflicted = 1 + sum([status.multiplier for status in user.get_statuses(statuses.DamageInflictedBuff) if await status.applicable_to_card(self)])
        dmg_received = math.prod([(1 + status.multiplier) for status in target.get_statuses(statuses.DamageReceivedBuff) if await status.applicable_to_card(self)])

        atk_stat = user.get_stat(self.atk_stat)
        def_stat = target.get_stat(self.def_stat)
        damage = atk_stat * self.atk_multiplier * random.randint(80, 120) * dmg_inflicted * dmg_received/ (100 + def_stat * self.def_multiplier)

        inflicted = await target.inflict_attack_damage(int(damage), user)
        return inflicted

    
    async def info_text(self):
        # Basic text
        text = "Deals **{power}%** {dmg_type} damage to the opponent.".format(power = int(self.atk_multiplier * 100), dmg_type = self.dmg_type)

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
class RecoilAttack(BaseAttack):
    """Attack type card.
    Inflicts recoil damage to the user equal to a specified percentage of the damage dealt.
    Args:
        recoil (float): Percentage of the damage dealt that is inflicted to the user.
    """
    recoil: float

    async def resolve(self):
        damage_dealt = await super().resolve()
        damage = int(damage_dealt * self.recoil)
        await self.owner.active_character.inflict_damage(damage, 'recoil ')

    async def info_text(self):
        text = await super().info_text()
        text += f"\nThe user takes **{int(self.recoil * 100)}%** recoil damage."
        return text
    
@dataclass
class HurtSelfAttack(BaseAttack):
    """Attack type card.
    Inflicts damage to the user equal to a specified value.
    Args:
        value (float): Amount of damage inflicted to the user.
        type (str): Type of damage value. Can be 'flat' or 'max_health'.
    """
    value: float
    type: str

    async def resolve(self):
        await super().resolve()
        user: battles.Character = self.owner.active_character
        if not user or user.is_defeated():
            return

        match self.type:
            case 'flat':
                damage = self.value
            case 'max_health':
                damage = int(self.owner.active_character.max_health * self.value)
            case _:
                damage = 0
        await user.inflict_damage(damage, 'self-inflicted' )

    async def info_text(self):
        text = await super().info_text()
        text += f"\nDeals {f'**{self.value}**' if self.type == 'flat' else f'**{int(self.value * 100)}%** Max Health'} damage to the user."
        return text



@dataclass
class StatusApplyingAttack(BaseAttack):
    """Attack type card.
    Has the additional effect of applying the specified status to the target when they are hit.
    """
    status: "statuses.BaseStatus"
    kwargs: dict

    async def info_text(self):
        text = await super().info_text()
        status: statuses.BaseStatus = self.status(**self.kwargs)

        text += '\n' + StatusEffect.status_info_text(status, 'opponent')

        return text
    
    async def resolve(self):
        damage = await super().resolve()
        target: battles.Character = self.owner.opponent.active_character
        if target and damage is not None:
            await target.apply_status(self.status(**self.kwargs))

        

@dataclass
class HitAllAttack(BaseAttack):
    """Attack type card.
    Hits all opposing characters instead of just one.
    If bench_multiplier is specified, bench characters will receive a different ratio of damage.
    """
    bench_multiplier: float = field(default=1, kw_only=True)

    async def resolve(self):

        user: battles.Character = self.owner.active_character
        if not user or not self.owner.opponent.active_character:
            return

        await super().resolve()

        variance = random.randint(80, 120)
        dmg_inflicted = 1 + sum([status.multiplier for status in user.get_statuses(statuses.DamageInflictedBuff) if await status.applicable_to_card(self)])

        for target in [char for char in self.owner.opponent.characters if char is not self.owner.opponent.active_character]:
            atk_stat = user.get_stat(self.atk_stat)
            def_stat = target.get_stat(self.def_stat)
            damage = atk_stat * self.atk_multiplier * self.bench_multiplier * variance * dmg_inflicted / (100 + def_stat * self.def_multiplier)

            await target.inflict_damage(damage)


    async def info_text(self):
        text = await super().info_text()
        text += "\nHits all enemy characters."
        return text


@dataclass
class EnergyRestoreAttack(BaseAttack):
    """Attack type card.
    Restores a specified amount of energy to the user after hitting the target.
    Args:
        energy (int): Amount of energy restored.
    """
    energy: int

    async def resolve(self):
        attack_success = await super().resolve()
        if attack_success is not None:
            await self.owner.gain_energy(self.energy)

    async def info_text(self):
        text = await super().info_text()
        text += f"\nReplenishes **{self.energy}** energy upon landing this attack."
        return text


@dataclass
class BlackFlash(EnergyRestoreAttack):
    """Attack type card.
    Black Flash adaptively changes attack stat and damage type to the user's highest stat.
    Args:
        energy (int): Amount of energy restored.
    """

    async def resolve(self):
        user: battles.Character = self.owner.active_character

        if user.get_stat('atk') > user.get_stat('m.a'):
            self.atk_stat = 'atk'
            self.def_stat = 'def'
            self.dmg_type = 'physical'
        else:
            self.atk_stat = 'm.a'
            self.def_stat = 'm.d'
            self.dmg_type = 'magic'

        await super().resolve()

    async def info_text(self):
        text = await super().info_text()
        return text.replace('physical', 'adaptive')
    
@dataclass
class ForceSwitchAttack(BaseAttack):
    """Attack type card.
    Forcibly switches the target out to a random ally if possible upon hit.
    """
    async def resolve(self):
        damage = await super().resolve()
        opponent: battles.Character = self.owner.opponent.active_character
        targets = [char for char in self.owner.opponent.characters if char is not opponent]

        if targets and not opponent.is_defeated() and damage is not None:
            target = random.choice(targets)
            opponent.owner.battle.log(f"- ***{target.name}* was dragged out.**")
            await opponent.owner.switch_character(target, bypass_cooldown=True)
            


    async def info_text(self):
        text = await super().info_text()
        text += "\nForces the target to switch out to a random ally upon hit."
        return text
    

@dataclass
class ShieldGenAttack(BaseAttack):
    """Attack type card that also grants the user shield.
    Args:
        shield_amount (int): Amount of shield granted.
    """
    shield_amount: int

    async def resolve(self):
        user: battles.Character = self.owner.active_character
        if user and not user.is_defeated():
            await user.add_shield(self.shield_amount)
            await super().resolve()

    async def info_text(self):
        text = await super().info_text()
        text += "\nGain **{shield}** Shield.".format(shield = self.shield_amount)
        return text

        
@dataclass
class ShieldCounterAttack(BaseAttack):
    """Attack type card.
    Multiplies its power if the target has shield.
    Args:
        multiplier (float): Power multiplier if the target has shield.
    """
    shield_multiplier: float

    async def resolve(self):
        target: battles.Character = self.owner.opponent.active_character
        if target.shield:
            original_power = self.atk_multiplier
            self.atk_multiplier *= self.shield_multiplier

        await super().resolve()
        self.atk_multiplier = original_power

    async def info_text(self):
        text = await super().info_text()
        text += f"\nIf the opponent has shield, deals **{int(self.shield_multiplier * self.atk_multiplier * 100)}%** {self.dmg_type} damage instead."
        return text
    
@dataclass
class GainPowerAttack(BaseAttack):
    """Attack type card.
    On hit, permanently increases the power of the card.
    Args:
        increase (float): Bonus to attack_multiplier permanently added on hit.
    """
    increase: float
    bonus_count: int = field(default=0, init=False)

    def display(self):
        if not self.bonus_count:
            return super().display()
        
        display = super().display()
        display = display.split(']')
        return f"{display[0]} +{self.bonus_count}]" + display[1]

    async def resolve(self):
        damage = await super().resolve()
        if damage is not None:
            self.atk_multiplier += self.increase
            self.bonus_count += 1

    async def info_text(self):
        return await super().info_text() + f"\nPermanently increases this card's damage by **+{int(self.increase * 100)}%** on hit."
    
@dataclass
class MultiHitAttack(BaseAttack):
    """Attack type card.
    Hits the target multiple times.
    Args:
        hits (int): Number of times the target is hit.
    """
    hits: int | str

    async def resolve(self):
        hits = self.energy_spent if self.hits == 'X' else self.hits

        for _ in range(hits):
            if not self.owner.opponent.active_character or self.owner.opponent.active_character.is_defeated():
                break
            await super().resolve()

    async def info_text(self):
        text = await super().info_text()
        lines = text.split('\n')
        damage_index = lines.index([line for line in lines if 'Deals' in line][0])
        lines[damage_index] = f"Deals **{int(self.atk_multiplier * 100)}%** {self.dmg_type} damage to the opponent {'**twice**' if self.hits == 2 else '**' + self.hits + '** times'}."
        return '\n'.join(lines)


@dataclass
class BaseBlock(BaseCard):
    """Generic effect card that grants the user a specified amount of Shield.
    Args:
        shield_amount (int): Amount of Shield granted.
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
class MultiplyShield(BaseBlock):
    """Effect card that multiplies the user's current shield by a specified multiplier.
    Args:
        multiplier (float): Multiplier for the user's current shield.
    """
    shield_amount: int = field(default=0, init=False)
    multiplier: float

    async def resolve(self):
        self.shield_amount = int(self.owner.active_character.shield * self.multiplier)
        await super().resolve()
    
    async def info_text(self):
        text = f"**{'Double' if self.multiplier == 2 else 'Triple' if self.multiplier == 3 else str(self.multiplier) + 'x'}** the user's current shield."

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        extra = extra.replace(f"Gain **{self.shield_amount}** Shield.", text) if extra else text
        return extra

@dataclass
class BaseHeal(BaseCard):
    """Generic effect card that heals the user.
    Args:
        heal_value (float): The value of the heal.
        heal_type (str): The type of healing done by the value. Default is "max_health", can also be "flat" or "missing_health".
    """
    heal_value: float
    heal_type: str = 'max_health'

    async def resolve(self):
        user: battles.Character = self.owner.active_character
        if not user or user.is_defeated():
            return

        match self.heal_type:
            case 'max_health':
                amount = int(user.max_health * self.heal_value)
            case 'max_health':
                amount = int((user.max_health - user.health) * self.heal_value)
            case 'flat':
                amount = self.heal_value
            case _:
                amount = 0
        
        await user.heal(amount)

    async def info_text(self):
        match self.heal_type:
            case 'max_health':
                text = f"Restores **{(self.heal_value * 100)}%** Max Health."
            case 'max_health':
                text = f"Restores **{(self.heal_value * 100)}%** Missing Health."
            case 'flat':
                text = f"Restores **{self.heal_value}** Health."

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text


@dataclass
class BaseDrawEffect(BaseCard):
    """Generic card draw effect card. Simply calls the draw() function of the card's owner.
    Args:
        count (int): The number of cards to draw.
    """
    count: int


    async def resolve(self):
        await self.owner.draw(self.count)

    async def info_text(self):
        text = "Draw **{cards}** cards.".format(cards = self.count)

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text
    

@dataclass
class HandRevealEffect(BaseCard):
    """Effect type card that reveals the opponent's held cards.
    Args:
        count (int): The number of cards to reveal.
    """
    count: int

    async def resolve(self):
        opponent_hand = self.owner.opponent.zones.hand
        count = min(len(opponent_hand), self.count)
        revealed = random.sample(opponent_hand, count)
        for card in revealed:
            await card.reveal()

        self.owner.battle.log(f"The following cards were revealed: {', '.join([f'**[{card.name}]**' for card in revealed])}")

    async def info_text(self):
        text = "Reveal **{cards}** of your opponent's held cards.".format(cards = self.count if self.count < 5 else "all")

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text


@dataclass
class StatusEffect(BaseCard):
    """Generic status effect card.
    Applies the specified status effect to the target.
    Args:
        target (str): The target of the status effect. Can be 'user' or 'opponent'.
        status (BaseStatus): The status effect to apply.
        kwargs (dict): Keyword arguments for the status effect.
    """
    target: str
    status: "statuses.BaseStatus"
    kwargs: dict

    async def resolve(self):
        match self.target:
            case 'user':
                target: battles.Character = self.owner.active_character
            case 'opponent':
                target: battles.Character = self.owner.opponent.active_character
        if target and not target.is_defeated():
            await target.apply_status(self.status(**self.kwargs))

    async def info_text(self):
        status: statuses.BaseStatus = self.status(**self.kwargs)

        text = StatusEffect.status_info_text(status, self.target)

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text
    
    @staticmethod
    def status_info_text(status: "statuses.BaseStatus", target: str):
        duration = f" for the rest of the {status.duration_type[:-1]}" if status.duration == 0 and status.duration_type != 'cards' else f" for {status.duration} {status.duration_type}" if status.duration < 99 else ""

        if getattr(status, 'multiplier', None) is not None:
            text = "The {target} gains *{name}*{duration}.".format(
                target = target,
                name = status.display(),
                duration = duration
            )
        elif getattr(status, 'stacks', None) is not None:
            text = "Applies **{stacks}** stack{plural} of the *{name}* status effect to the {target}{duration}.".format(
                stacks = status.stacks,
                plural = '' if status.stacks == 1 else 's',
                name = status.display(),
                target = target,
                duration = duration
            )
        else:
            text = "Applies the *{name}* status effect to the {target}{duration}.".format(
                name = status.display(),
                target = target,
                duration = duration
            )
        return text


@dataclass
class Overcharge(BaseCard):
    """Gain energy, but have  less next turn.
    Args:
        energy (int): Amount of energy gained.
        penalty (int): Amount of energy lost next turn.
    """
    energy: int
    penalty: int

    async def resolve(self):
        user: battles.Character = self.owner.active_character
        await user.gain_energy(self.energy)
        await user.reduce_energy_delta(self.penalty)

    async def info_text(self):
        text = f"Gain **{self.energy}** energy, but start with **{self.penalty}** less next turn."

        # Add parent information if there is any (conditions, keywords etc.) then return the full string
        extra = await super().info_text()
        return f"{extra}\n{text}" if extra else text

@dataclass
class DiscoverEffectTemplate(BaseCard):
    """Template card for discover effects.
    This class does NOT do anything on its own, and is used to provide the selection of cards to choose from for subclasses.
    Args:
        pool_size (int): Number of cards to choose from.
        source (str): The location to choose from. Can be 'random', 'deck', 'discard', or 'hand'. 'Random' will select from random copies of all non-imaginary cards in the game.
        filters (dict): Filters to apply to the selection pool. Default is an empty dictionary.
    """
    pool_size: int
    source: str
    filters: dict = field(default_factory=dict, kw_only=True)

    async def resolve(self) -> BaseCard:
        import battles.buttons as buttons

        # Fetch base pool of cards
        if self.source == 'random':
            pool = [x.value for x in Cards if x.value.rarity != 'imaginary']
        else:
            pool = self.owner.zones.locations[self.source]
        pool = random.sample(pool, min(self.pool_size, len(pool)))

        # Apply filters to pool
        for key, value in self.filters.items():
            match key:
                case 'rarity':
                    pool = [card for card in pool if card.rarity == value]
                case 'tag':
                    pool = [card for card in pool if value in card.tags]
                case 'type':
                    pool = [card for card in pool if isinstance(card, value)]

        if not pool:
            return
        
        # Create view and wait for input
        view = buttons.CardSelectView(self.owner, pool, "Discover a card.")
        await self.owner.battle.wait_for_input([view])

        # Return selection
        return view.selection if view.selection is not None else random.choice(pool)

    async def info_text(self):
        text = await super().info_text()
        text += f"\nDiscover a random card{'' if self.source == 'random' else f' from your {self.source}'}."
        return text
    
@dataclass
class DiscoverEffect(DiscoverEffectTemplate):
    """Discover a card to add to your hand.
    Args:
        pool_size (int): Number of cards to choose from.
        location (str): The location to choose from. Can be 'random', 'deck', 'discard', or 'hand'. 'Random' will select from random copies of all non-imaginary cards in the game.
        filters (dict): Filters to apply to the selection pool. Default is an empty dictionary.
    """
    async def resolve(self):
        selection = await super().resolve()
        if selection:
            if selection.location is None:
                await self.owner.create_card(selection, 'hand')
            else:
                await selection.move_to('hand')
                self.owner.log(f"> **[{selection.name}]** was added to your hand.")
                self.owner.opponent.log(f"> {f'**[{selection.name}]**' if selection.revealed else 'A card'} was added to your opponent's hand.")

    async def info_text(self):
        text = await super().info_text()
        text += "\nAdd the discovered card to your hand."
        return text

@dataclass
class TitanShift(BaseCard):
    """Attack on Titan's signature card.
    Transforms a *Tag: Titan Shifter* character into their Titan form.
    """

    async def resolve(self):
        raise NotImplementedError("This card has not been implemented yet.")

        user: battles.Character = self.owner.active_character
        if not user or 'Titan Shifter' not in user.tags:
            return
        
        match user.name:
            case 'Eren Jaeger':
                await user.transform('Attack Titan')


    async def info_text(self):
        extra = await super().info_text()
        return f"{extra}\nTransforms the user into their Titan form." if extra else "Transforms the user into their Titan form."

@dataclass
class DomainExpansion(BaseCard):
    """Jujutsu Kaisen's signature card.
    The domain has a different effect depending on the user.
    """

    async def resolve(self):
        raise NotImplementedError("This card has not been implemented yet.")

    async def info_text(self):
        extra = await super().info_text()
        return f"{extra}\nChange the battlefield to the user's unique domain for 1 round. If the user switches out, the effect ends early." if extra \
        else "Change the battlefield to the user's unique domain for 1 round. If the user switches out, the effect ends early."
    



import battles.battles as battles
import battles.statuses as statuses


    
class Cards(Enum):
    
    STRIKE = BaseAttack('Strike', 'basic', 1, 'atk', 'def', 'physical', 1, 1, tags=('contact',), filename="strike.jpg")
    BLAST = BaseAttack('Blast', 'basic', 1, 'm.a', 'm.d', 'magic', 1, 1, tags=('projectile',), filename="blast.jpg")
    BLOCK = BaseBlock('Block', 'basic', 1, 40, filename='block.jpg')

    FOCUS = BaseDrawEffect('Focus', 'common', 1, 3, filename="focus.jpg")
    SLAM = BaseAttack('Slam', 'common', 2, 'atk', 'def', 'physical', 2, 1, tags=('contact',), filename="slam.jpg")
    CRUSH = BaseAttack('Crush', 'common', 3, 'atk', 'def', 'physical', 3, 1, tags=('contact',), filename="crush.jpg")
    SHOCKWAVE = BaseAttack('Shockwave', 'common', 2, 'm.a', 'm.d', 'magic', 2, 1, filename="shockwave.jpg")
    BEAM = BaseAttack('Beam', 'common', 3, 'm.a', 'm.d', 'magic', 3, 1, filename="beam.jpg")
    PIERCE = BaseAttack('Pierce', 'common', 2, 'atk', 'def', 'physical', 1, 0.6, tags=('contact',), filename="pierce.jpg")
    CRIPPLE = StatusApplyingAttack('Cripple', 'common', 2, 'atk', 'def', 'physical', 1.8, 1, statuses.SpeedBuff, {'multiplier': -10, 'duration': 0}, filename='cripple.jpg')
    HEX = StatusApplyingAttack('Hex', 'common', 2, 'm.a', 'm.d', 'magic', 1.8, 1, statuses.DamageReceivedBuff, {'multiplier': 0.1, 'duration': 999} ,filename="hex.jpg")
    FORTIFY = BaseBlock('Fortify', 'common', 2, 75, filename="fortify.jpg")
    EXPLOSION = HitAllAttack('Explosion', 'common', 3, 'm.a', 'm.d', 'magic', 2, 1, bench_multiplier=0.5, filename="explosion.jpg")
    RECKLESS_SWING = RecoilAttack('Reckless Swing', 'common', 3, 'atk', 'def', 'physical', 4, 1, 0.3, tags=('contact',), filename="recklessswing.jpg")
    SWIFT_STRIKE = BaseAttack('Swift Strike', 'common', 2, 'atk', 'def', 'physical', 1.3, 1, priority=3, tags=('contact',), filename="swiftstrike.jpg")
    SONIC_WAVE = BaseAttack('Sonic Wave', 'common', 2, 'm.a', 'm.d', 'magic', 1.3, 1, priority=3, filename="sonicwave.jpg")
    VITALITY = BaseHeal('Vitality', 'common', 1, 30, 'flat', filename="vitality.jpg")
    HEAVY_ATTACK = BaseAttack('Heavy Attack', 'common', 1, 'atk', 'def', 'physical', 1.3, 1, priority=-3, tags=('contact',), filename="heavyattack.jpg")
    CHARGE_BOMB = BaseAttack('Charge Bomb', 'common', 1, 'm.a', 'm.d', 'magic', 1.3, 1, priority=-3, tags=('projectile',), filename="chargebomb.jpg")
    BULLET = BaseAttack('Bullet', 'common', 1, 'atk', 'def', 'physical', 1, 1, tags=('projectile',), filename="bullet.jpg")
    MAGIC_PUNCH = BaseAttack('Magic Punch', 'common', 1, 'm.a', 'm.d', 'magic', 1, 1, tags=('contact',), filename="magicpunch.jpg")
    VICIOUS_POISON = StatusEffect('Vicious Poison', 'common', 1, 'opponent', statuses.Poison, {'stacks': 5, 'duration': 0}, filename="viciouspoison.jpg")

    THROW = ForceSwitchAttack('Throw', 'uncommon', 2, 'atk', 'def', 'physical', 1, 1, tags=('contact',), filename="throw.jpg")
    BARRIER_BREAKER = ShieldCounterAttack('Barrier Breaker', 'uncommon', 3, 'm.a', 'm.d', 'magic', 2, 1, 2, filename="barrierbreaker.jpg")
    RAGE = StatusEffect('Rage', 'uncommon', 1, 'user', statuses.DamageInflictedBuff, {'multiplier': 0.25, 'duration': 0}, filename="rage.jpg")
    SWORD_AND_SHIELD = ShieldGenAttack('Sword and Shield', 'uncommon', 1, 'atk', 'def', 'physical', 0.75, 1, 25, filename="swordandshield.jpg")
    COATED_BLADE = StatusApplyingAttack('Coated Blade', 'uncommon', 1, 'atk', 'def', 'physical', 0.9, 1, statuses.Poison, {'stacks': 1, 'duration': 5}, requirements={'user_tag': 'Assassin'}, filename="coatedblade.jpg")
    TWIN_SLASH = MultiHitAttack('Twin Slash', 'uncommon', 2, 'atk', 'def', 'physical', 1, 1, 2, filename="twinslash.jpg")
    HEMOMANCY = HurtSelfAttack('Hemomancy', 'uncommon', 1, 'm.a', 'm.d', 'magic', 1.75, 1, 0.15, 'max_health', filename="hemomancy.jpg")
    SCRYING_TOME = DiscoverEffect('Scrying Tome', 'uncommon', 1, 5, 'deck', filename="scryingtome.jpg")

    SNOWBALL_SPELL = GainPowerAttack('Snowball Spell', 'rare', 1, 'm.a', 'm.d', 'magic', 1, 1, 1, tags=('projectile',), filename="snowballspell.jpg")
    OVERCHARGE = Overcharge('Overcharge', 'rare', 0, 1, 2, revealed=2, keywords=['revealed'], filename="overcharge.jpg")
    DEADLY_FLURRY = MultiHitAttack('Deadly Flurry', 'rare', 'X', 'atk', 'def', 'physical', 0.9, 1, 'X', filename="deadlyflurry.jpg")
    ENCHANTED_GUARD = MultiplyShield('Enchanted Guard', 'rare', 1, 2, filename="enchantedguard.jpg")

    # Attack On Titan
    TITAN_SHIFT = TitanShift('Titan Shift', 'legendary', 3, requirements={'user_tag': 'Titan Shifter'}, keywords=['ephemeral'], filename="titanshift.gif")

    # Jujutsu Kaisen
    BLACK_FLASH = BlackFlash("Black Flash", 'uncommon', 0, 'atk', 'def', 'physical', 1, 1, 1, requirements={'user_tag': 'Jujutsu Kaisen'}, keywords= ['ephemeral'], tags=('contact',), filename="blackflash.jpg")
    DOMAIN_EXPANSION = DomainExpansion("Domain Expansion", 'legendary', 5, keywords=['ephemeral'], requirements={'user_tag': 'Domain User'}, filename="domainexpansion.gif")

    # Hunter x Hunter
    GYO = HandRevealEffect("Gyo", 'rare', 1, 5, requirements={'user_tag': 'Hunter x Hunter'}, filename="gyo.jpg")
    JAJANKEN_ROCK = BaseAttack("Jajanken: Rock", 'imaginary', 3, 'atk', 'def', 'physical', 4, 1, keywords=['fleeting'], requirements={'user_name': 'Gon Freecss'}, tags=('jajanken', 'contact'), filename="jajankenrock.jpg")
    JAJANKEN_PAPER = BaseAttack("Jajanken: Paper", 'imaginary', 3, 'atk', 'def', 'physical', 2.5, 1, priority=3, keywords=['fleeting'], requirements={'user_name': 'Gon Freecss'}, tags=('jajanken', 'projectile'), filename="jajankenpaper.jpg")
    JAJANKEN_SCISSORS = BaseAttack("Jajanken: Scissors", 'imaginary', 3, 'atk', 'def', 'physical', 1.6, 0, keywords=['fleeting'], requirements={'user_name': 'Gon Freecss'}, tags=('jajanken', 'contact'), filename="jajankenscissors.jpg")



def create_card(card: Enum) -> BaseCard:
    card: BaseCard = card.value
    if card:
        return card.copy()
