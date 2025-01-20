from battles.battles import Character
import battles.passives as passives

FIGHTERS = {

    # Dragon Ball Z

    # Re: Zero

    # Attack on Titan
    "AOT-11": {
        "passive_ability": passives.SashaPassive, "active_ability": None, "attribute": "green", 
        "health": 270, "attack": 80, "defense": 100, "magic_attack": 50, "magic_defense": 90, "speed": 105, "growth_style": "technical"
    },
    "AOT-14": {
        "passive_ability": passives.ConniePassive, "active_ability": None, "attribute": "orange",
        "health": 290, "attack": 110, "defense": 80, "magic_attack": 10, "magic_defense": 70, "speed": 124, "growth_style": "balanced"
    }
    # Jujutsu Kaisen

    # One Punch Man

    # My Hero Academia

    # Demon Slayer

}