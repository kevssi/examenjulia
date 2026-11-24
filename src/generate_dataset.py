"""
Script para generar el dataset canónico de The Legend of Zelda: Hyrule Compendium.
Contiene más de 650 registros clasificados en armas, arcos, escudos, armaduras, materiales, monstruos y consumibles.
Incluye intencionalmente imperfecciones controladas (duplicados, valores nulos y pequeñas inconsistencias de formato)
para cumplir con los requerimientos de la Parte 2 y Parte 3 del proyecto integrador.
"""

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

# Listas maestras basadas en el universo canónico de The Legend of Zelda (BotW & TotK)

REGIONS = [
    "Central Hyrule", "Death Mountain", "Gerudo Desert", "Hebra Mountains",
    "Faron Woods", "Lanayru", "Akkala", "Great Plateau", "Hyrule Castle", "Depths"
]

EFFECT_TYPES = [
    "None", "Attack Up", "Defense Up", "Speed Up", "Stealth Up",
    "Heat Resistance", "Cold Resistance", "Shock Resistance",
    "Fire Elemental", "Ice Elemental", "Electric Elemental", "Extra Hearts"
]

# 1. ARMAS (Weapons: 1-handed, 2-handed, spears)
weapon_bases = [
    ("Master Sword", "One-handed Sword", 30, 0, 40, 0, 5, "Hyrule Castle", "None", 0),
    ("Master Sword (Awakened)", "One-handed Sword", 60, 0, 188, 0, 5, "Hyrule Castle", "None", 0),
    ("Royal Broadsword", "One-handed Sword", 36, 0, 36, 280, 4, "Hyrule Castle", "Attack Up", 1),
    ("Knight's Broadsword", "One-handed Sword", 26, 0, 27, 140, 3, "Central Hyrule", "None", 0),
    ("Soldier's Broadsword", "One-handed Sword", 14, 0, 20, 60, 2, "Central Hyrule", "None", 0),
    ("Traveler's Sword", "One-handed Sword", 5, 0, 20, 20, 1, "Great Plateau", "None", 0),
    ("Rusty Broadsword", "One-handed Sword", 6, 0, 8, 12, 1, "Central Hyrule", "None", 0),
    ("Scimitar of the Seven", "One-handed Sword", 32, 0, 60, 1200, 5, "Gerudo Desert", "Attack Up", 2),
    ("Gerudo Scimitar", "One-handed Sword", 16, 0, 23, 75, 2, "Gerudo Desert", "None", 0),
    ("Moonlight Scimitar", "One-handed Sword", 25, 0, 32, 180, 3, "Gerudo Desert", "None", 0),
    ("Zora Sword", "One-handed Sword", 15, 0, 27, 85, 2, "Lanayru", "Speed Up", 1),
    ("Silver Longsword", "One-handed Sword", 22, 0, 30, 150, 3, "Lanayru", "None", 0),
    ("Feathered Edge", "One-handed Sword", 15, 0, 27, 90, 2, "Hebra Mountains", "Speed Up", 1),
    ("Forest Dweller's Sword", "One-handed Sword", 22, 0, 27, 130, 3, "Faron Woods", "None", 0),
    ("Demon Carver", "One-handed Sword", 40, 0, 25, 350, 4, "Gerudo Desert", "Attack Up", 2),
    ("Ancient Short Sword", "One-handed Sword", 40, 0, 54, 1000, 4, "Akkala", "None", 0),
    ("Guardian Sword", "One-handed Sword", 20, 0, 17, 120, 2, "Central Hyrule", "None", 0),
    ("Guardian Sword+", "One-handed Sword", 30, 0, 26, 250, 3, "Central Hyrule", "None", 0),
    ("Guardian Sword++", "One-handed Sword", 40, 0, 32, 450, 4, "Central Hyrule", "Attack Up", 2),
    ("Flameblade", "One-handed Sword", 24, 0, 36, 300, 4, "Death Mountain", "Fire Elemental", 2),
    ("Frostblade", "One-handed Sword", 20, 0, 30, 300, 4, "Hebra Mountains", "Ice Elemental", 2),
    ("Thunderblade", "One-handed Sword", 22, 0, 36, 300, 4, "Faron Woods", "Electric Elemental", 2),
    ("Boomerang", "One-handed Sword", 8, 0, 18, 30, 1, "Faron Woods", "None", 0),
    ("Lizal Boomerang", "One-handed Sword", 14, 0, 17, 50, 2, "Lanayru", "None", 0),
    ("Lizal Forked Boomerang", "One-handed Sword", 24, 0, 25, 120, 3, "Lanayru", "None", 0),
    ("Lizal Tri-Boomerang", "One-handed Sword", 36, 0, 27, 240, 4, "Akkala", "Attack Up", 1),
    ("Tree Branch", "One-handed Sword", 2, 0, 4, 2, 1, "Great Plateau", "None", 0),
    ("Torch", "One-handed Sword", 2, 0, 8, 5, 1, "Great Plateau", "Fire Elemental", 1),
    ("Soup Ladle", "One-handed Sword", 1, 0, 5, 3, 1, "Central Hyrule", "None", 0),
    ("Spring-Loaded Hammer", "One-handed Sword", 1, 0, 80, 300, 3, "Akkala", "None", 0),
    ("Bokoblin Arm", "One-handed Sword", 5, 0, 5, 4, 1, "Central Hyrule", "None", 0),
    ("Lizalfos Arm", "One-handed Sword", 12, 0, 8, 8, 1, "Central Hyrule", "None", 0),
    ("Moblin Arm", "Two-handed Claymore", 15, 0, 5, 10, 1, "Central Hyrule", "None", 0),
    ("Royal Claymore", "Two-handed Claymore", 52, 0, 40, 420, 4, "Hyrule Castle", "Attack Up", 2),
    ("Knight's Claymore", "Two-handed Claymore", 38, 0, 30, 210, 3, "Central Hyrule", "None", 0),
    ("Soldier's Claymore", "Two-handed Claymore", 20, 0, 25, 90, 2, "Central Hyrule", "None", 0),
    ("Traveler's Claymore", "Two-handed Claymore", 10, 0, 20, 30, 1, "Great Plateau", "None", 0),
    ("Rusty Claymore", "Two-handed Claymore", 12, 0, 10, 18, 1, "Central Hyrule", "None", 0),
    ("Boulder Breaker", "Two-handed Claymore", 60, 0, 60, 1500, 5, "Death Mountain", "Attack Up", 2),
    ("Cobble Crusher", "Two-handed Claymore", 15, 0, 30, 70, 2, "Death Mountain", "None", 0),
    ("Stone Smasher", "Two-handed Claymore", 42, 0, 40, 260, 3, "Death Mountain", "Attack Up", 1),
    ("Golden Claymore", "Two-handed Claymore", 28, 0, 30, 180, 3, "Gerudo Desert", "None", 0),
    ("Edge of Duality", "Two-handed Claymore", 50, 0, 35, 380, 4, "Hyrule Castle", "Attack Up", 2),
    ("Eightfold Longblade", "Two-handed Claymore", 32, 0, 25, 220, 3, "Lanayru", "Speed Up", 1),
    ("Ancient Bladesaw", "Two-handed Claymore", 55, 0, 50, 1100, 4, "Akkala", "Attack Up", 2),
    ("Great Flameblade", "Two-handed Claymore", 34, 0, 50, 450, 4, "Death Mountain", "Fire Elemental", 3),
    ("Great Frostblade", "Two-handed Claymore", 30, 0, 40, 450, 4, "Hebra Mountains", "Ice Elemental", 3),
    ("Great Thunderblade", "Two-handed Claymore", 32, 0, 50, 450, 4, "Faron Woods", "Electric Elemental", 3),
    ("Fierce Deity Sword", "Two-handed Claymore", 60, 0, 35, 1600, 5, "Hyrule Castle", "Attack Up", 3),
    ("Biggoron's Sword", "Two-handed Claymore", 50, 0, 60, 1400, 5, "Death Mountain", "None", 0),
    ("Savage Lynel Crusher", "Two-handed Claymore", 78, 0, 35, 850, 5, "Central Hyrule", "Attack Up", 3),
    ("Mighty Lynel Crusher", "Two-handed Claymore", 54, 0, 30, 500, 4, "Lanayru", "Attack Up", 2),
    ("Lynel Crusher", "Two-handed Claymore", 36, 0, 24, 300, 3, "Lanayru", "Attack Up", 1),
    ("Iron Sledgehammer", "Two-handed Claymore", 12, 0, 40, 40, 1, "Great Plateau", "None", 0),
    ("Giant Boomerang", "Two-handed Claymore", 25, 0, 40, 160, 3, "Faron Woods", "None", 0),
    ("Royal Halberd", "Spear", 26, 0, 50, 320, 4, "Hyrule Castle", "Speed Up", 2),
    ("Knight's Halberd", "Spear", 13, 0, 40, 150, 3, "Central Hyrule", "Speed Up", 1),
    ("Soldier's Spear", "Spear", 7, 0, 35, 65, 2, "Central Hyrule", "None", 0),
    ("Traveler's Spear", "Spear", 3, 0, 30, 22, 1, "Great Plateau", "None", 0),
    ("Rusty Halberd", "Spear", 5, 0, 15, 14, 1, "Central Hyrule", "None", 0),
    ("Lightscale Trident", "Spear", 22, 0, 70, 1300, 5, "Lanayru", "Speed Up", 2),
    ("Ceremonial Trident", "Spear", 14, 0, 40, 300, 3, "Lanayru", "Speed Up", 1),
    ("Silverscale Spear", "Spear", 12, 0, 40, 110, 2, "Lanayru", "None", 0),
    ("Feathered Spear", "Spear", 10, 0, 35, 95, 2, "Hebra Mountains", "Speed Up", 1),
    ("Gerudo Spear", "Spear", 16, 0, 35, 120, 2, "Gerudo Desert", "None", 0),
    ("Drillshaft", "Spear", 14, 0, 50, 180, 3, "Death Mountain", "None", 0),
    ("Ancient Spear", "Spear", 30, 0, 50, 1000, 4, "Akkala", "Attack Up", 2),
    ("Guardian Spear", "Spear", 10, 0, 20, 90, 2, "Central Hyrule", "None", 0),
    ("Guardian Spear+", "Spear", 15, 0, 25, 180, 3, "Central Hyrule", "None", 0),
    ("Guardian Spear++", "Spear", 20, 0, 35, 350, 4, "Central Hyrule", "Speed Up", 2),
    ("Flamespear", "Spear", 24, 0, 50, 380, 4, "Death Mountain", "Fire Elemental", 2),
    ("Frostspear", "Spear", 20, 0, 40, 380, 4, "Hebra Mountains", "Ice Elemental", 2),
    ("Thunderspear", "Spear", 22, 0, 50, 380, 4, "Faron Woods", "Electric Elemental", 2),
    ("Savage Lynel Spear", "Spear", 30, 0, 45, 600, 5, "Central Hyrule", "Attack Up", 2),
    ("Mighty Lynel Spear", "Spear", 20, 0, 35, 380, 4, "Lanayru", "Attack Up", 1),
    ("Lynel Spear", "Spear", 14, 0, 25, 220, 3, "Lanayru", "None", 0),
]

# 2. ARCOS (Bows)
bow_bases = [
    ("Bow of Light", "Legendary Bow", 100, 0, 999, 5000, 5, "Hyrule Castle", "Attack Up", 3),
    ("Savage Lynel Bow (5x)", "Multi-shot Bow", 64, 0, 45, 900, 5, "Central Hyrule", "Attack Up", 3),
    ("Savage Lynel Bow (3x)", "Multi-shot Bow", 48, 0, 45, 750, 5, "Central Hyrule", "Attack Up", 2),
    ("Mighty Lynel Bow", "Multi-shot Bow", 30, 0, 35, 450, 4, "Lanayru", "Attack Up", 1),
    ("Lynel Bow", "Multi-shot Bow", 20, 0, 30, 280, 3, "Lanayru", "None", 0),
    ("Great Eagle Bow", "Multi-shot Bow", 28, 0, 60, 1400, 5, "Hebra Mountains", "Speed Up", 2),
    ("Royal Bow", "Longbow", 38, 0, 60, 360, 4, "Hyrule Castle", "Attack Up", 1),
    ("Knight's Bow", "Longbow", 26, 0, 48, 180, 3, "Central Hyrule", "None", 0),
    ("Soldier's Bow", "Light Bow", 14, 0, 36, 75, 2, "Central Hyrule", "None", 0),
    ("Traveler's Bow", "Light Bow", 5, 0, 22, 25, 1, "Great Plateau", "None", 0),
    ("Ancient Bow", "Sniper Bow", 44, 0, 120, 1200, 5, "Akkala", "Attack Up", 2),
    ("Falcon Bow", "Rapid Bow", 20, 0, 50, 220, 3, "Hebra Mountains", "Speed Up", 2),
    ("Swallow Bow", "Rapid Bow", 9, 0, 30, 60, 2, "Hebra Mountains", "Speed Up", 1),
    ("Golden Bow", "Sniper Bow", 14, 0, 60, 200, 3, "Gerudo Desert", "None", 0),
    ("Phrenic Bow", "Sniper Bow", 10, 0, 45, 120, 2, "Lanayru", "None", 0),
    ("Duplex Bow", "Multi-shot Bow", 28, 0, 18, 190, 3, "Gerudo Desert", "Speed Up", 1),
    ("Forest Dweller's Bow", "Multi-shot Bow", 20, 0, 35, 230, 3, "Faron Woods", "None", 0),
    ("Spiked Boko Bow", "Light Bow", 12, 0, 20, 35, 2, "Central Hyrule", "None", 0),
    ("Dragonbone Boko Bow", "Light Bow", 24, 0, 30, 95, 3, "Death Mountain", "None", 0),
    ("Lizal Bow", "Light Bow", 14, 0, 25, 45, 2, "Lanayru", "None", 0),
    ("Enhanced Lizal Bow", "Light Bow", 25, 0, 35, 110, 3, "Lanayru", "None", 0),
    ("Steel Lizal Bow", "Light Bow", 36, 0, 50, 240, 4, "Akkala", "Attack Up", 1),
    ("Wooden Bow", "Light Bow", 4, 0, 20, 15, 1, "Great Plateau", "None", 0),
]

# 3. ESCUDOS (Shields)
shield_bases = [
    ("Hylian Shield", "Legendary Shield", 0, 90, 800, 3000, 5, "Hyrule Castle", "Defense Up", 3),
    ("Royal Guard's Shield", "Heavy Shield", 0, 70, 14, 500, 4, "Hyrule Castle", "Defense Up", 3),
    ("Royal Shield", "Heavy Shield", 0, 55, 60, 400, 4, "Hyrule Castle", "Defense Up", 2),
    ("Knight's Shield", "Metal Shield", 0, 40, 48, 210, 3, "Central Hyrule", "Defense Up", 1),
    ("Soldier's Shield", "Metal Shield", 0, 16, 26, 80, 2, "Central Hyrule", "None", 0),
    ("Traveler's Shield", "Wood Shield", 0, 4, 12, 20, 1, "Great Plateau", "None", 0),
    ("Daybreaker", "Legendary Shield", 0, 48, 60, 1200, 5, "Gerudo Desert", "Defense Up", 2),
    ("Gerudo Shield", "Metal Shield", 0, 20, 20, 100, 2, "Gerudo Desert", "None", 0),
    ("Radiant Shield", "Parry Shield", 0, 35, 26, 260, 3, "Gerudo Desert", "Speed Up", 2),
    ("Ancient Shield", "Guardian Tech Shield", 0, 70, 32, 1300, 5, "Akkala", "Defense Up", 2),
    ("Guardian Shield", "Guardian Tech Shield", 0, 18, 10, 90, 2, "Central Hyrule", "None", 0),
    ("Guardian Shield+", "Guardian Tech Shield", 0, 30, 13, 200, 3, "Central Hyrule", "None", 0),
    ("Guardian Shield++", "Guardian Tech Shield", 0, 42, 20, 380, 4, "Central Hyrule", "Defense Up", 1),
    ("Savage Lynel Shield", "Spiked Shield", 21, 62, 20, 700, 5, "Central Hyrule", "Attack Up", 2),
    ("Mighty Lynel Shield", "Spiked Shield", 15, 44, 15, 420, 4, "Lanayru", "Attack Up", 1),
    ("Lynel Shield", "Spiked Shield", 10, 30, 12, 250, 3, "Lanayru", "Attack Up", 1),
    ("Steel Lizal Shield", "Metal Shield", 0, 35, 15, 170, 3, "Akkala", "None", 0),
    ("Reinforced Lizal Shield", "Metal Shield", 0, 22, 12, 90, 2, "Lanayru", "None", 0),
    ("Lizal Shield", "Metal Shield", 0, 9, 8, 35, 1, "Lanayru", "None", 0),
    ("Dragonbone Boko Shield", "Bone Shield", 0, 25, 15, 80, 2, "Death Mountain", "None", 0),
    ("Spiked Boko Shield", "Bone Shield", 0, 10, 12, 35, 1, "Central Hyrule", "None", 0),
    ("Boko Shield", "Bone Shield", 0, 3, 5, 12, 1, "Great Plateau", "None", 0),
    ("Pot Lid", "Improvised Shield", 0, 1, 10, 5, 1, "Central Hyrule", "None", 0),
    ("Wooden Shield", "Wood Shield", 0, 2, 12, 15, 1, "Great Plateau", "None", 0),
    ("Emblazoned Shield", "Wood Shield", 0, 3, 12, 20, 1, "Faron Woods", "None", 0),
    ("Hunter's Shield", "Wood Shield", 0, 3, 12, 20, 1, "Faron Woods", "None", 0),
    ("Fisherman's Shield", "Wood Shield", 0, 3, 12, 20, 1, "Lanayru", "None", 0),
    ("Kite Shield", "Wood Shield", 0, 14, 16, 120, 3, "Hebra Mountains", "Speed Up", 1),
    ("Shield of the Mind's Eye", "Parry Shield", 0, 16, 16, 150, 3, "Lanayru", "Speed Up", 2),
]

# 4. ARMADURAS (Armor Pieces: Helms, Chestplates, Greaves)
armor_bases = [
    ("Champion's Tunic", "Armor Chest", 0, 32, 150, 2000, 5, "Central Hyrule", "Extra Hearts", 2),
    ("Ancient Helm", "Armor Head", 0, 28, 120, 1500, 5, "Akkala", "Defense Up", 2),
    ("Ancient Cuirass", "Armor Chest", 0, 28, 120, 1500, 5, "Akkala", "Defense Up", 2),
    ("Ancient Greaves", "Armor Legs", 0, 28, 120, 1500, 5, "Akkala", "Defense Up", 2),
    ("Barbarian Helm", "Armor Head", 0, 20, 100, 1200, 4, "Hebra Mountains", "Attack Up", 2),
    ("Barbarian Armor", "Armor Chest", 0, 20, 100, 1200, 4, "Faron Woods", "Attack Up", 2),
    ("Barbarian Leg Wraps", "Armor Legs", 0, 20, 100, 1200, 4, "Gerudo Desert", "Attack Up", 2),
    ("Flamebreaker Helm", "Armor Head", 0, 20, 100, 1000, 4, "Death Mountain", "Heat Resistance", 2),
    ("Flamebreaker Armor", "Armor Chest", 0, 20, 100, 1000, 4, "Death Mountain", "Heat Resistance", 2),
    ("Flamebreaker Boots", "Armor Legs", 0, 20, 100, 1000, 4, "Death Mountain", "Heat Resistance", 2),
    ("Snowquill Headdress", "Armor Head", 0, 20, 100, 800, 4, "Hebra Mountains", "Cold Resistance", 2),
    ("Snowquill Tunic", "Armor Chest", 0, 20, 100, 800, 4, "Hebra Mountains", "Cold Resistance", 2),
    ("Snowquill Trousers", "Armor Legs", 0, 20, 100, 800, 4, "Hebra Mountains", "Cold Resistance", 2),
    ("Desert Voe Headband", "Armor Head", 0, 20, 100, 750, 4, "Gerudo Desert", "Heat Resistance", 2),
    ("Desert Voe Spaulder", "Armor Chest", 0, 20, 100, 750, 4, "Gerudo Desert", "Heat Resistance", 2),
    ("Desert Voe Trousers", "Armor Legs", 0, 20, 100, 750, 4, "Gerudo Desert", "Heat Resistance", 2),
    ("Stealth Mask", "Armor Head", 0, 16, 90, 600, 3, "Lanayru", "Stealth Up", 2),
    ("Stealth Chest Guard", "Armor Chest", 0, 16, 90, 600, 3, "Lanayru", "Stealth Up", 2),
    ("Stealth Tights", "Armor Legs", 0, 16, 90, 600, 3, "Lanayru", "Stealth Up", 2),
    ("Climber's Bandanna", "Armor Head", 0, 20, 100, 900, 4, "Lanayru", "Speed Up", 2),
    ("Climbing Gear", "Armor Chest", 0, 20, 100, 900, 4, "Central Hyrule", "Speed Up", 2),
    ("Climbing Boots", "Armor Legs", 0, 20, 100, 900, 4, "Lanayru", "Speed Up", 2),
    ("Zora Helm", "Armor Head", 0, 20, 100, 850, 4, "Lanayru", "Speed Up", 2),
    ("Zora Armor", "Armor Chest", 0, 20, 100, 850, 4, "Lanayru", "Speed Up", 2),
    ("Zora Greaves", "Armor Legs", 0, 20, 100, 850, 4, "Lanayru", "Speed Up", 2),
    ("Rubber Helm", "Armor Head", 0, 20, 90, 700, 3, "Faron Woods", "Shock Resistance", 2),
    ("Rubber Armor", "Armor Chest", 0, 20, 90, 700, 3, "Faron Woods", "Shock Resistance", 2),
    ("Rubber Tights", "Armor Legs", 0, 20, 90, 700, 3, "Faron Woods", "Shock Resistance", 2),
    ("Hylian Hood", "Armor Head", 0, 20, 80, 250, 2, "Central Hyrule", "None", 0),
    ("Hylian Tunic", "Armor Chest", 0, 20, 80, 250, 2, "Central Hyrule", "None", 0),
    ("Hylian Trousers", "Armor Legs", 0, 20, 80, 250, 2, "Central Hyrule", "None", 0),
    ("Soldier's Helm", "Armor Head", 0, 28, 110, 400, 3, "Central Hyrule", "Defense Up", 1),
    ("Soldier's Armor", "Armor Chest", 0, 28, 110, 400, 3, "Central Hyrule", "Defense Up", 1),
    ("Soldier's Greaves", "Armor Legs", 0, 28, 110, 400, 3, "Central Hyrule", "Defense Up", 1),
    ("Fierce Deity Mask", "Armor Head", 0, 20, 120, 1800, 5, "Hyrule Castle", "Attack Up", 3),
    ("Fierce Deity Armor", "Armor Chest", 0, 20, 120, 1800, 5, "Hyrule Castle", "Attack Up", 3),
    ("Fierce Deity Boots", "Armor Legs", 0, 20, 120, 1800, 5, "Hyrule Castle", "Attack Up", 3),
    ("Dark Hood", "Armor Head", 0, 12, 70, 500, 3, "Akkala", "Speed Up", 1),
    ("Dark Tunic", "Armor Chest", 0, 12, 70, 500, 3, "Akkala", "Speed Up", 1),
    ("Dark Trousers", "Armor Legs", 0, 12, 70, 500, 3, "Akkala", "Speed Up", 1),
]

# 5. MATERIALES Y BOTÍN (Materials: Gems, Monster Drops, Foraging)
material_bases = [
    ("Diamond", "Gemstone", 0, 0, 1, 500, 5, "Death Mountain", "Defense Up", 1),
    ("Star Fragment", "Celestial Gem", 0, 0, 1, 300, 5, "Central Hyrule", "Extra Hearts", 3),
    ("Ruby", "Gemstone", 0, 0, 1, 210, 4, "Death Mountain", "Heat Resistance", 2),
    ("Sapphire", "Gemstone", 0, 0, 1, 260, 4, "Hebra Mountains", "Cold Resistance", 2),
    ("Topaz", "Gemstone", 0, 0, 1, 180, 4, "Gerudo Desert", "Shock Resistance", 2),
    ("Opal", "Gemstone", 0, 0, 1, 60, 3, "Lanayru", "Speed Up", 1),
    ("Amber", "Gemstone", 0, 0, 1, 30, 2, "Central Hyrule", "Defense Up", 1),
    ("Luminous Stone", "Mineral", 0, 0, 1, 70, 3, "Lanayru", "Stealth Up", 1),
    ("Giant Ancient Core", "Ancient Tech Part", 0, 0, 1, 200, 5, "Hyrule Castle", "Defense Up", 3),
    ("Ancient Core", "Ancient Tech Part", 0, 0, 1, 80, 4, "Akkala", "Defense Up", 2),
    ("Ancient Gear", "Ancient Tech Part", 0, 0, 1, 30, 3, "Central Hyrule", "None", 0),
    ("Ancient Shaft", "Ancient Tech Part", 0, 0, 1, 40, 3, "Central Hyrule", "None", 0),
    ("Ancient Spring", "Ancient Tech Part", 0, 0, 1, 15, 2, "Central Hyrule", "None", 0),
    ("Ancient Screw", "Ancient Tech Part", 0, 0, 1, 12, 2, "Central Hyrule", "None", 0),
    ("Lynel Guts", "Monster Organ", 0, 0, 1, 200, 5, "Central Hyrule", "Attack Up", 3),
    ("Lynel Horn", "Monster Part", 0, 0, 1, 150, 4, "Central Hyrule", "Attack Up", 2),
    ("Lynel Hoof", "Monster Part", 0, 0, 1, 50, 4, "Central Hyrule", "Speed Up", 1),
    ("Hinox Guts", "Monster Organ", 0, 0, 1, 80, 4, "Faron Woods", "Attack Up", 2),
    ("Hinox Tooth", "Monster Part", 0, 0, 1, 35, 3, "Faron Woods", "None", 0),
    ("Hinox Toenail", "Monster Part", 0, 0, 1, 20, 2, "Faron Woods", "None", 0),
    ("Molduga Guts", "Monster Organ", 0, 0, 1, 110, 4, "Gerudo Desert", "Attack Up", 2),
    ("Molduga Fin", "Monster Part", 0, 0, 1, 30, 3, "Gerudo Desert", "Speed Up", 1),
    ("Dinraal's Horn", "Dragon Relic", 0, 0, 1, 300, 5, "Death Mountain", "Fire Elemental", 3),
    ("Dinraal's Scale", "Dragon Relic", 0, 0, 1, 150, 4, "Death Mountain", "Fire Elemental", 2),
    ("Dinraal's Claw", "Dragon Relic", 0, 0, 1, 180, 4, "Death Mountain", "Fire Elemental", 2),
    ("Dinraal's Fang", "Dragon Relic", 0, 0, 1, 250, 5, "Death Mountain", "Fire Elemental", 3),
    ("Naydra's Horn", "Dragon Relic", 0, 0, 1, 300, 5, "Lanayru", "Ice Elemental", 3),
    ("Naydra's Scale", "Dragon Relic", 0, 0, 1, 150, 4, "Lanayru", "Ice Elemental", 2),
    ("Naydra's Claw", "Dragon Relic", 0, 0, 1, 180, 4, "Lanayru", "Ice Elemental", 2),
    ("Naydra's Fang", "Dragon Relic", 0, 0, 1, 250, 5, "Lanayru", "Ice Elemental", 3),
    ("Farosh's Horn", "Dragon Relic", 0, 0, 1, 300, 5, "Faron Woods", "Electric Elemental", 3),
    ("Farosh's Scale", "Dragon Relic", 0, 0, 1, 150, 4, "Faron Woods", "Electric Elemental", 2),
    ("Farosh's Claw", "Dragon Relic", 0, 0, 1, 180, 4, "Faron Woods", "Electric Elemental", 2),
    ("Farosh's Fang", "Dragon Relic", 0, 0, 1, 250, 5, "Faron Woods", "Electric Elemental", 3),
    ("Keese Wing", "Monster Part", 0, 0, 1, 2, 1, "Central Hyrule", "Speed Up", 1),
    ("Fire Keese Wing", "Monster Part", 0, 0, 1, 6, 2, "Death Mountain", "Fire Elemental", 1),
    ("Ice Keese Wing", "Monster Part", 0, 0, 1, 6, 2, "Hebra Mountains", "Ice Elemental", 1),
    ("Electric Keese Wing", "Monster Part", 0, 0, 1, 6, 2, "Faron Woods", "Electric Elemental", 1),
    ("Chuchu Jelly", "Monster Part", 0, 0, 1, 5, 1, "Great Plateau", "None", 0),
    ("Red Chuchu Jelly", "Monster Part", 0, 0, 1, 10, 2, "Death Mountain", "Fire Elemental", 1),
    ("White Chuchu Jelly", "Monster Part", 0, 0, 1, 10, 2, "Hebra Mountains", "Ice Elemental", 1),
    ("Yellow Chuchu Jelly", "Monster Part", 0, 0, 1, 10, 2, "Faron Woods", "Electric Elemental", 1),
    ("Bokoblin Horn", "Monster Part", 0, 0, 1, 3, 1, "Central Hyrule", "None", 0),
    ("Bokoblin Fang", "Monster Part", 0, 0, 1, 8, 1, "Central Hyrule", "None", 0),
    ("Bokoblin Guts", "Monster Organ", 0, 0, 1, 20, 2, "Central Hyrule", "None", 0),
    ("Moblin Horn", "Monster Part", 0, 0, 1, 5, 1, "Central Hyrule", "None", 0),
    ("Moblin Fang", "Monster Part", 0, 0, 1, 12, 2, "Central Hyrule", "None", 0),
    ("Moblin Guts", "Monster Organ", 0, 0, 1, 25, 3, "Central Hyrule", "None", 0),
    ("Lizalfos Horn", "Monster Part", 0, 0, 1, 10, 2, "Lanayru", "None", 0),
    ("Lizalfos Talon", "Monster Part", 0, 0, 1, 15, 2, "Lanayru", "None", 0),
    ("Lizalfos Tail", "Monster Part", 0, 0, 1, 28, 3, "Lanayru", "None", 0),
    ("Red Lizalfos Tail", "Monster Part", 0, 0, 1, 35, 3, "Death Mountain", "Fire Elemental", 2),
    ("Icy Lizalfos Tail", "Monster Part", 0, 0, 1, 35, 3, "Hebra Mountains", "Ice Elemental", 2),
    ("Yellow Lizalfos Tail", "Monster Part", 0, 0, 1, 35, 3, "Gerudo Desert", "Electric Elemental", 2),
    ("Octorok Tentacle", "Monster Part", 0, 0, 1, 10, 1, "Lanayru", "None", 0),
    ("Octorok Eyeball", "Monster Part", 0, 0, 1, 25, 2, "Lanayru", "None", 0),
    ("Octo Balloon", "Monster Part", 0, 0, 1, 5, 1, "Lanayru", "None", 0),
    ("Silent Shroom", "Mushroom", 0, 0, 1, 10, 2, "Faron Woods", "Stealth Up", 2),
    ("Ironshroom", "Mushroom", 0, 0, 1, 12, 2, "Central Hyrule", "Defense Up", 1),
    ("Razorshroom", "Mushroom", 0, 0, 1, 12, 2, "Central Hyrule", "Attack Up", 1),
    ("Sunshroom", "Mushroom", 0, 0, 1, 10, 2, "Death Mountain", "Cold Resistance", 1),
    ("Chillshroom", "Mushroom", 0, 0, 1, 10, 2, "Hebra Mountains", "Heat Resistance", 1),
    ("Zapshroom", "Mushroom", 0, 0, 1, 10, 2, "Gerudo Desert", "Shock Resistance", 1),
    ("Hearty Truffle", "Mushroom", 0, 0, 1, 24, 3, "Central Hyrule", "Extra Hearts", 2),
    ("Big Hearty Truffle", "Mushroom", 0, 0, 1, 60, 4, "Faron Woods", "Extra Hearts", 3),
    ("Endura Carrot", "Root", 0, 0, 1, 30, 4, "Central Hyrule", "Speed Up", 3),
    ("Swift Carrot", "Root", 0, 0, 1, 10, 2, "Lanayru", "Speed Up", 1),
    ("Mighty Bananas", "Fruit", 0, 0, 1, 20, 3, "Faron Woods", "Attack Up", 2),
    ("Hearty Radish", "Root", 0, 0, 1, 32, 3, "Central Hyrule", "Extra Hearts", 2),
    ("Big Hearty Radish", "Root", 0, 0, 1, 75, 4, "Akkala", "Extra Hearts", 3),
    ("Fleet-Lotus Seeds", "Flower", 0, 0, 1, 18, 3, "Lanayru", "Speed Up", 2),
    ("Silent Princess", "Flower", 0, 0, 1, 100, 5, "Hyrule Castle", "Stealth Up", 3),
    ("Armoranth", "Flower", 0, 0, 1, 10, 2, "Central Hyrule", "Defense Up", 1),
    ("Mighty Thistle", "Flower", 0, 0, 1, 10, 2, "Faron Woods", "Attack Up", 1),
    ("Cool Safflina", "Flower", 0, 0, 1, 8, 2, "Hebra Mountains", "Heat Resistance", 1),
    ("Warm Safflina", "Flower", 0, 0, 1, 8, 2, "Death Mountain", "Cold Resistance", 1),
    ("Electric Safflina", "Flower", 0, 0, 1, 8, 2, "Gerudo Desert", "Shock Resistance", 1),
    ("Fairy", "Special", 0, 0, 1, 2, 5, "Faron Woods", "Extra Hearts", 3),
]

# 6. MONSTRUOS / ENEMIGOS (Monsters: HP mapped to durability/combat-power)
monster_bases = [
    ("Calamity Ganon", "Calamity Boss", 100, 50, 800, 0, 5, "Hyrule Castle", "Fire Elemental", 3),
    ("Dark Beast Ganon", "Calamity Boss", 120, 60, 1000, 0, 5, "Central Hyrule", "None", 0),
    ("Silver Lynel", "Apex Predator", 85, 40, 500, 650, 5, "Central Hyrule", "Attack Up", 3),
    ("Golden Lynel", "Apex Predator", 95, 45, 750, 950, 5, "Central Hyrule", "Attack Up", 3),
    ("White-Maned Lynel", "Apex Predator", 70, 30, 400, 450, 4, "Lanayru", "Attack Up", 2),
    ("Blue-Maned Lynel", "Apex Predator", 55, 25, 300, 300, 4, "Lanayru", "Attack Up", 2),
    ("Red Lynel", "Apex Predator", 40, 20, 200, 200, 3, "Lanayru", "Attack Up", 1),
    ("Guardian Stalker", "Ancient Machine", 75, 45, 500, 450, 5, "Central Hyrule", "Attack Up", 3),
    ("Guardian Skywatcher", "Ancient Machine", 65, 40, 450, 400, 4, "Akkala", "Attack Up", 2),
    ("Guardian Turret", "Ancient Machine", 80, 50, 400, 350, 4, "Hyrule Castle", "Attack Up", 2),
    ("Guardian Scout IV", "Ancient Machine", 45, 30, 250, 250, 4, "Great Plateau", "Speed Up", 2),
    ("Guardian Scout III", "Ancient Machine", 30, 20, 180, 150, 3, "Central Hyrule", "Speed Up", 1),
    ("Guardian Scout II", "Ancient Machine", 18, 12, 100, 80, 2, "Central Hyrule", "None", 0),
    ("Black Hinox", "Field Boss", 60, 20, 600, 300, 4, "Faron Woods", "None", 0),
    ("Blue Hinox", "Field Boss", 45, 15, 450, 200, 3, "Faron Woods", "None", 0),
    ("Red Hinox", "Field Boss", 30, 10, 300, 120, 2, "Central Hyrule", "None", 0),
    ("Stalnox", "Field Boss", 50, 25, 400, 280, 4, "Central Hyrule", "None", 0),
    ("Molduga", "Field Boss", 65, 35, 500, 350, 4, "Gerudo Desert", "Attack Up", 2),
    ("Molduking", "Field Boss", 80, 40, 650, 550, 5, "Gerudo Desert", "Attack Up", 3),
    ("Rare Stone Talus", "Field Boss", 50, 50, 450, 400, 4, "Death Mountain", "Defense Up", 2),
    ("Igneo Talus", "Field Boss", 55, 45, 400, 350, 4, "Death Mountain", "Fire Elemental", 2),
    ("Frost Talus", "Field Boss", 55, 45, 400, 350, 4, "Hebra Mountains", "Ice Elemental", 2),
    ("Stone Talus", "Field Boss", 35, 35, 300, 180, 3, "Great Plateau", "Defense Up", 1),
    ("Silver Bokoblin", "Minion Elite", 35, 15, 240, 100, 4, "Central Hyrule", "None", 0),
    ("Black Bokoblin", "Minion", 24, 10, 160, 60, 3, "Central Hyrule", "None", 0),
    ("Blue Bokoblin", "Minion", 14, 6, 90, 30, 2, "Central Hyrule", "None", 0),
    ("Red Bokoblin", "Minion", 6, 2, 40, 10, 1, "Great Plateau", "None", 0),
    ("Silver Moblin", "Minion Elite", 45, 18, 300, 140, 4, "Central Hyrule", "Attack Up", 1),
    ("Black Moblin", "Minion", 30, 12, 200, 80, 3, "Central Hyrule", "None", 0),
    ("Blue Moblin", "Minion", 18, 8, 120, 40, 2, "Central Hyrule", "None", 0),
    ("Red Moblin", "Minion", 9, 3, 60, 15, 1, "Central Hyrule", "None", 0),
    ("Silver Lizalfos", "Minion Elite", 42, 16, 280, 130, 4, "Lanayru", "Speed Up", 2),
    ("Black Lizalfos", "Minion", 28, 11, 180, 70, 3, "Lanayru", "Speed Up", 1),
    ("Blue Lizalfos", "Minion", 16, 7, 100, 35, 2, "Lanayru", "Speed Up", 1),
    ("Green Lizalfos", "Minion", 8, 3, 50, 12, 1, "Lanayru", "None", 0),
    ("Fire-Breath Lizalfos", "Elemental Minion", 25, 10, 160, 85, 3, "Death Mountain", "Fire Elemental", 2),
    ("Ice-Breath Lizalfos", "Elemental Minion", 25, 10, 160, 85, 3, "Hebra Mountains", "Ice Elemental", 2),
    ("Electric Lizalfos", "Elemental Minion", 25, 10, 160, 85, 3, "Gerudo Desert", "Electric Elemental", 2),
    ("Yiga Blademaster", "Assassin", 40, 15, 200, 150, 4, "Gerudo Desert", "Attack Up", 2),
    ("Yiga Footsoldier", "Assassin", 20, 8, 100, 60, 2, "Gerudo Desert", "Speed Up", 1),
    ("Blizzrobe", "Mage", 35, 12, 150, 120, 3, "Hebra Mountains", "Ice Elemental", 2),
    ("Meteor Wizzrobe", "Mage", 35, 12, 150, 120, 3, "Death Mountain", "Fire Elemental", 2),
    ("Thunder Wizzrobe", "Mage", 35, 12, 150, 120, 3, "Faron Woods", "Electric Elemental", 2),
]

# 7. CONSUMIBLES / RECETAS / ELIXIRES (Consumables)
consumable_bases = [
    ("Hearty Meat and Seafood Fry", "Hearty Meal", 0, 0, 1, 120, 4, "Central Hyrule", "Extra Hearts", 3),
    ("Endura Elixir (Full Stamina)", "Elixir", 0, 0, 1, 150, 4, "Central Hyrule", "Speed Up", 3),
    ("Mighty Fried Bananas", "Attack Food", 0, 0, 1, 90, 3, "Faron Woods", "Attack Up", 3),
    ("Tough Meat-Stuffed Pumpkin", "Defense Food", 0, 0, 1, 90, 3, "Lanayru", "Defense Up", 3),
    ("Sneaky Steamed Fish", "Stealth Food", 0, 0, 1, 80, 3, "Lanayru", "Stealth Up", 3),
    ("Spicy Meat and Seafood Fry", "Warm Food", 0, 0, 1, 70, 2, "Great Plateau", "Cold Resistance", 2),
    ("Chilly Fruit and Mushroom Mix", "Cooling Food", 0, 0, 1, 70, 2, "Gerudo Desert", "Heat Resistance", 2),
    ("Electro Elixir", "Elixir", 0, 0, 1, 100, 3, "Faron Woods", "Shock Resistance", 3),
    ("Hasty Apple Pie", "Speed Food", 0, 0, 1, 65, 2, "Central Hyrule", "Speed Up", 2),
    ("Fairy Tonic", "Potion", 0, 0, 1, 110, 4, "Faron Woods", "Extra Hearts", 2),
    ("Monster Stew", "Monster Cuisine", 0, 0, 1, 55, 3, "Akkala", "None", 0),
    ("Dubious Food", "Failed Cuisine", 0, 0, 1, 2, 1, "Great Plateau", "None", 0),
    ("Rock-Hard Food", "Failed Cuisine", 0, 0, 1, 2, 1, "Death Mountain", "Defense Up", 1),
    ("Energizing Mushroom Rice Balls", "Stamina Food", 0, 0, 1, 50, 2, "Central Hyrule", "Speed Up", 1),
]

# Ahora expandiremos las listas de base mediante variaciones canónicas realistas (Modifiers: Attack Up+, Durability Up+, Long Throw, Critical Hit, Guard Up+, Ancient Proficiencies, Rusty vs Refurbished, Fusion Variants)
# para generar un catálogo enriquecido y completo de al menos 680 ítems.

raw_records = []
item_counter = 1

# Helper function to append item
def add_item(name, cat, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot):
    global item_counter
    raw_records.append({
        "item_id": f"ZEL-{item_counter:04d}",
        "item_name": name,
        "category": cat,
        "subcategory": subcat,
        "attack_power": int(atk),
        "defense_power": int(df),
        "durability": int(dur),
        "sell_price": int(price),
        "rarity_tier": int(rarity),
        "origin_region": reg,
        "effect_type": eff,
        "effect_potency": int(eff_pot)
    })
    item_counter += 1

# Expand weapons with modifiers/fusions
for base in weapon_bases:
    name, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot = base
    # Versión base
    add_item(name, "Weapons", subcat, atk, df, dur, price, rarity, reg, eff, eff_pot)
    
    # Variaciones con modifiers (Attack Up+, Durability Up+, Fuse Horn)
    if rarity >= 2:
        # Attack Up+
        add_item(f"{name} (Attack Up +{int(atk*0.25)+2})", "Weapons", subcat, atk + int(atk*0.25)+2, df, dur, int(price*1.3)+10, min(5, rarity+1), reg, "Attack Up" if eff == "None" else eff, max(1, eff_pot))
        # Durability Up+
        add_item(f"{name} (Durability Up +{int(dur*0.4)+5})", "Weapons", subcat, atk, df, dur + int(dur*0.4)+5, int(price*1.2)+15, rarity, reg, eff, eff_pot)
    
    # Fuse horn variants for common swords
    if "Sword" in subcat or "Claymore" in subcat or "Spear" in subcat:
        add_item(f"{name} + Silver Lynel Blade Horn", "Weapons", subcat, atk + 55, df, dur + 25, price + 400, 5, "Depths" if reg != "Hyrule Castle" else reg, "Attack Up", 3)
        add_item(f"{name} + Fire Gleeok Horn", "Weapons", subcat, atk + 30, df, dur + 18, price + 250, 4, "Death Mountain", "Fire Elemental", 3)
        add_item(f"{name} + Frost Gleeok Horn", "Weapons", subcat, atk + 30, df, dur + 18, price + 250, 4, "Hebra Mountains", "Ice Elemental", 3)

# Expand bows
for base in bow_bases:
    name, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot = base
    add_item(name, "Bows", subcat, atk, df, dur, price, rarity, reg, eff, eff_pot)
    if rarity >= 2:
        add_item(f"{name} (Quick Shot)", "Bows", subcat, atk, df, dur + 5, int(price*1.25)+10, rarity, reg, "Speed Up", 2)
        add_item(f"{name} (Attack Up +{int(atk*0.3)+3})", "Bows", subcat, atk + int(atk*0.3)+3, df, dur, int(price*1.35)+20, min(5, rarity+1), reg, "Attack Up", max(1, eff_pot))

# Expand shields
for base in shield_bases:
    name, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot = base
    add_item(name, "Shields", subcat, atk, df, dur, price, rarity, reg, eff, eff_pot)
    if rarity >= 2:
        add_item(f"{name} (Shield Guard Up +{int(df*0.3)+4})", "Shields", subcat, atk, df + int(df*0.3)+4, dur, int(price*1.3)+15, min(5, rarity+1), reg, "Defense Up", max(1, eff_pot))
        add_item(f"{name} (Durability Up +{int(dur*0.5)+8})", "Shields", subcat, atk, df, dur + int(dur*0.5)+8, int(price*1.25)+10, rarity, reg, eff, eff_pot)
    # Fuse rocket or bomb
    add_item(f"{name} + Zonai Rocket", "Shields", subcat, atk, df, dur + 5, price + 60, min(5, rarity+1), "Depths", "Speed Up", 3)

# Expand armor
for base in armor_bases:
    name, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot = base
    # Nivel base (★0)
    add_item(f"{name} ★1", "Armor", subcat, atk, df, dur, price, rarity, reg, eff, eff_pot)
    # Mejorado Gran Hada ★2
    add_item(f"{name} ★2", "Armor", subcat, atk, int(df * 1.5) + 2, dur + 20, int(price * 1.4) + 100, min(5, rarity + 1), reg, eff, min(3, eff_pot + 1))
    # Mejorado Gran Hada ★4 (Máximo)
    add_item(f"{name} ★4 (Max)", "Armor", subcat, atk, int(df * 2.3) + 6, dur + 50, int(price * 2.2) + 350, min(5, rarity + 1), reg, eff, min(3, eff_pot + 1))

# Expand materials
for base in material_bases:
    name, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot = base
    add_item(name, "Materials", subcat, atk, df, dur, price, rarity, reg, eff, eff_pot)
    # Lotes o variantes de calidad
    if rarity >= 3:
        add_item(f"Pristine {name}", "Materials", subcat, atk, df, dur, int(price * 1.6), min(5, rarity + 1), "Depths", eff, eff_pot)

# Expand monsters
for base in monster_bases:
    name, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot = base
    add_item(name, "Monsters", subcat, atk, df, dur, price, rarity, reg, eff, eff_pot)
    if "Lynel" in name or "Talus" in name or "Hinox" in name or "Ganon" in name:
        add_item(f"Malice {name}", "Monsters", subcat, int(atk * 1.35), int(df * 1.25), int(dur * 1.4), int(price * 1.5), min(5, rarity + 1), "Hyrule Castle", "Attack Up", 3)
    elif "Bokoblin" in name or "Moblin" in name or "Lizalfos" in name:
        add_item(f"Depths Gloom {name}", "Monsters", subcat, int(atk * 1.3), int(df * 1.2), int(dur * 1.3), int(price * 1.4), min(5, rarity + 1), "Depths", "Attack Up", 2)

# Expand consumables
for base in consumable_bases:
    name, subcat, atk, df, dur, price, rarity, reg, eff, eff_pot = base
    add_item(name, "Consumables", subcat, atk, df, dur, price, rarity, reg, eff, eff_pot)
    # Versiones Potenciadas / Critical Cook
    add_item(f"Critical Cook {name}", "Consumables", subcat, atk, df, dur, int(price * 1.5) + 30, min(5, rarity + 1), reg, eff, min(3, eff_pot + 1))
    add_item(f"Large Batch {name} (x5)", "Consumables", subcat, atk, df, dur, int(price * 3.8) + 50, min(5, rarity + 1), reg, eff, eff_pot)

df_all = pd.DataFrame(raw_records)
print(f"Total de registros generados inicialmente: {len(df_all)}")

# AHORA INTRODUCIMOS IMPERFECCIONES CONTROLADAS PARA EL DATASET ORIGINAL
# (Para que en la Parte 2 y Parte 3 se realice un análisis riguroso de detección y limpieza)

# 1. Duplicados exactos intencionales (7 registros duplicados)
dup_indices = [5, 12, 45, 88, 120, 205, 310]
duplicates = df_all.iloc[dup_indices].copy()
df_with_dups = pd.concat([df_all, duplicates], ignore_index=True)

# 2. Inconsistencias de texto (espacios en blanco accidentales o mayúsculas)
# Por ejemplo en 'category' y 'origin_region'
categories_corrupted = df_with_dups["category"].copy()
# Introducir "  Weapons ", "bows", " Shields  ", "materials "
for idx in [10, 25, 40, 70, 95]:
    val = categories_corrupted.iloc[idx]
    if idx % 2 == 0:
        categories_corrupted.iloc[idx] = f"  {val}  "
    else:
        categories_corrupted.iloc[idx] = val.lower()
df_with_dups["category"] = categories_corrupted

# 3. Valores nulos controlados (en sell_price, durability y effect_type)
df_with_nulls = df_with_dups.copy()
# 8 nulos en sell_price (e.g. ítems especiales donde no se había tasado el valor)
null_price_idx = [15, 33, 77, 142, 215, 305, 412, 530]
for idx in null_price_idx:
    if idx < len(df_with_nulls):
        df_with_nulls.loc[idx, "sell_price"] = np.nan

# 6 nulos en durability
null_dur_idx = [48, 92, 160, 250, 360, 480]
for idx in null_dur_idx:
    if idx < len(df_with_nulls):
        df_with_nulls.loc[idx, "durability"] = np.nan

# 5 nulos en effect_type
null_eff_idx = [22, 105, 199, 320, 501]
for idx in null_eff_idx:
    if idx < len(df_with_nulls):
        df_with_nulls.loc[idx, "effect_type"] = np.nan

# 4. Outliers extremos o inconsistencias numéricas (ej. un precio negativo o error de captura)
# ZEL con precio negativo -50 (error humano de captura) y uno con 99999
if 60 < len(df_with_nulls):
    df_with_nulls.loc[60, "sell_price"] = -50
if 130 < len(df_with_nulls):
    df_with_nulls.loc[130, "durability"] = -5

# Guardar dataset original con imperfecciones
output_path = "data/zelda_hyrule_compendium_original.csv"
df_with_nulls.to_csv(output_path, index=False, encoding="utf-8")
print(f"Dataset original guardado en {output_path}")
print(f"Dimensiones finales del dataset original: {df_with_nulls.shape}")
print(f"Valores nulos por columna:\n{df_with_nulls.isna().sum()}")
print(f"Filas duplicadas: {df_with_nulls.duplicated().sum()}")
