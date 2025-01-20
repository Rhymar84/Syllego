import discord
import sqlite3
import random
import bot
import gacha
import math
import copy
from character_database import BaseChar
from typing import Union
from PIL import Image
from io import BytesIO
from collections import defaultdict
import aiosqlite
from discord.utils import get
from discord.ui import Select, View
from config import COLOUR_EMOJI_KEY, BUFF_STAT_KEY

class CardZones():

    def __init__(self):
        self.deck: list[BaseCard] = []
        self.hand: list[BaseCard] = []
        self.discard_pile: list[BaseCard] = []
        self.selection: list[BaseCard] = []

    def initialise_deck(self, deck: list["BaseCard"]):
        for card in deck:
            self.deck.append(card)
            card.set_location('deck')

    async def shuffle_deck(self):
        random.shuffle(self.deck)

    async def move(self, card: "BaseCard", destination: str):
        """
        Moves a card to the specified destination.
        Destination can be 'deck', 'hand', or 'discard_pile'.
        """

        if destination not in ['deck', 'hand', 'discard_pile'] or destination == card.location:
            return
        
        match card.location:
            case 'deck':
                current_location = self.deck
            case 'hand':
                current_location = self.hand
            case 'discard_pile':
                current_location = self.discard_pile
            case 'selection':
                current_location = self.selection
        match destination:
            case 'deck':
                destination_location = self.deck
            case 'hand':
                destination_location = self.hand
            case 'discard_pile':
                destination_location = self.discard_pile

        current_location.remove(card)
        destination_location.append(card)
        card.set_location(destination)

    async def discard(self, card: "BaseCard"):
        await self.move(card, 'discard_pile')
        await card.on_discard()

    async def erase(self, card: "BaseCard"):
        if card.location not in ['deck', 'hand', 'discard_pile', 'selection']:
            return

        match card.location:
            case 'deck':
                self.deck.remove(card)
            case 'hand':
                self.hand.remove(card)
            case 'discard_pile':
                self.discard_pile.remove(card)
            case 'selection':
                self.selection.remove(card)

        card.set_location('erased')

    async def replenish_deck(self):
        for card in self.discard_pile:
            self.deck.append(card)
            card.set_location('deck')

        self.discard_pile.clear()
        await self.shuffle_deck()

    async def discard_hand(self):
        for card in self.hand:
            await card.discard()

    async def choose_card(self, card: "BaseCard"):
        """Moves a card to the selection zone. Does nothing if selection already contains a card."""
        if self.selection:
            return

        match card.location:
            case 'deck':
                current_location = self.deck
            case 'hand':
                current_location = self.hand
            case 'discard_pile':
                current_location = self.discard_pile
            case 'selection':
                return
            
        current_location.remove(card)
        self.selection.append(card)
        card.set_location('selection')


    async def draw(self):
        """
        Moves the first card in the deck to the hand. Does nothing if the hand is full (5 cards).
        If the deck is empty, call replenish_deck(). If it is still empty, a card cannot be drawn.
        """
        if len(self.hand) > 4:
            return
        if not self.deck:
            await self.replenish_deck()
            if not self.deck:
                return
            
        card = self.deck[0]
        await self.move(card, 'hand')
        await card.on_draw()


    async def create_card(self, card: "BaseCard", location: str):
        if (location == 'selection' and self.selection) or (location == 'hand' and len(self.hand) > 4):
            return

        match location:
            case 'deck':
                destination = self.deck
            case 'hand':
                destination = self.hand
            case 'discard_pile':
                destination = self.discard_pile
            case 'selection':
                destination = self.selection
        
        clone = card.copy()
        destination.append(clone)
        clone.set_location(location)
        
        
        
        

        

class Character():

    def __init__(self, base: BaseChar, attribute: str, health: int, attack: int, defense: int, magic_attack: int, magic_defense: int, speed: int, 
                 passive_ability: "passives.BasePassive", active_ability, growth_style: str, tags: list[str] = []):
        
        self.name = base.short_name
        self.tags = tuple([base.series] + tags)
        self.attribute = attribute
        self.growth_style = growth_style

        self.owner: Player | None = None

        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.magic_attack = magic_attack
        self.magic_defense = magic_defense
        self.speed = speed
        
        self.passive_ability: passives.BasePassive = passive_ability()
        self.passive_ability.set_user(self)
        self.active_ability = active_ability

        self.shield = 0
        self.statuses: list[statuses.BaseStatus] = []
        self.buffs: list[dict] = []

    def __repr__(self):
        if self.owner.active_character is not self:
            return f"{COLOUR_EMOJI_KEY[self.attribute]} {self.name} - {self.health}❤️ {self.shield}🛡️" if self.shield else f"{self.name} - {self.health}❤️"

    def set_owner(self, player: "Player"):
        self.owner = player

    def get_stat(self, stat: str):
        KEY = {
            'atk': self.attack,
            'def': self.defense,
            'm.a': self.magic_attack,
            'm.d': self.magic_defense,
            'spd': self.speed
        }
        return KEY[stat]
    
    def get_statuses(self) -> list["statuses.BaseStatus"]:
        return self.statuses + self.passive_ability.passive_statuses

    async def inflict_damage(self, amount: int):
        
        self.shield -= amount
        if self.shield < 0:
            self.health += self.shield # Shield will now be a negative value equal to excess damage, so add that amount to health to subtract the excess from HP.
            self.shield = 0

    async def calculate_damage(self, damage_value: int):
        return int(damage_value)
    
    async def add_shield(self, amount: int):
        self.shield += amount
    
    async def heal(self, amount: int):
        self.health = min(self.health + amount, self.max_health)

    async def apply_status(self, status: "statuses.BaseStatus"):
        if isinstance(status, statuses.BaseStatus):

            if await self.can_apply_status(status):
                # Apply the status effect.
                self.statuses.append(status)
                await status.on_apply()
            else:
                # If the status is negated, trigger the negation function.
                await status.on_negation()

    async def remove_status(self, status_name: str):
        to_remove = [status for status in self.statuses if status.name == status_name]

        if to_remove:
            self.statuses = [status for status in self.statuses if status not in to_remove]

    async def can_apply_status(self, status: "statuses.BaseStatus"):
        if any(isinstance(status, immunity) for immunity in [x.immune_to for x in self.get_statuses() if isinstance(x, statuses.StatusImmunity)]):
            return False

        return True

    ## Event trigger functions: simply calls the associated function in the ability object.
    async def targeted_by_attack(self):
        await self.passive_ability.targeted_by_attack()
    async def on_hit_attack(self, damage: int):
        await self.passive_ability.on_hit_attack(damage)
    async def hit_by_attack(self):
        await self.passive_ability.hit_by_attack()


class Player():
    def __init__(self, member: discord.Member, channel: discord.Thread):
        self.member = member
        self.channel = channel

        self.opponent: Player | None = None

        self.active_character: Character | None = None
        self.zones = CardZones()

        self.party: tuple[Character] = ()
        self.characters: list[Character] = []

    def set_party(self, party: list[Character]):
        self.party = party
        self.characters = list(party)

    def set_opponent(self, opponent: "Player"):
        self.opponent = opponent
    
    def selected_card(self):
        if self.zones.selection:
            return self.zones.selection[0]
        
    async def draw(self, amount: int):
        for _ in range(amount):
            await self.zones.draw()


from battles.cards import BaseCard
import battles.statuses as statuses
import battles.passives as passives