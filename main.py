from dataclasses import dataclass, field
from functools import cache
from typing import Literal, Self, no_type_check
from enum import Enum
import json
from typeguard import check_type

CraftingMachine = Literal[
    "Backpack_Printer",
    "Chemistry_Lab"
]

Resource = Literal[
    "Soil",
    "Organic",
    "Compound",
    "Resin",
    "Clay",
    "Quartz",
    "Ammonium",
    "Graphite",
    "Laterite",
    "Astronium",
    "Sphalerite",
    "Wolframite",
    "Malachite",
    "Lithium",
    "Hematite",
    "Titanite",
]

RefinedResource = Literal[
    "Carbon",
    "Ceramic",
    "Glass",
    "Aluminum",
    "Zinc",
    "Copper",
    "Tungsten",
    "Iron",
    "Titanium",
]

CompositeResource = Literal[
    "Rubber",
    "Plastic",
    "Aluminum_Alloy",
    "Tungsten_Carbide",
    "Graphene",
    "Diamond",
    "Hydrazine",
    "Silicone",
    "Explosive_Powder",
    "Steel",
    "Titanium_Alloy",
    "Nanocarbon_Alloy",
]

Gas = Literal[
    "Hydrogen",
    "Argon",
    "Methane",
    "Nitrogen",
    "Sulfur",
    "Helium"
]

Planet = Literal[
    "Sylva",
    "Desolo",
    "Calidor",
    "Vesania",
    "Novus",
    "Glacio",
    "Atrox"
]

PLANET_ATMOSPHERE: dict[Planet, dict[Gas, int]] = {
    "Sylva": {
        "Hydrogen": 75,
        "Nitrogen": 100,
    },
    "Calidor": {
        "Hydrogen": 50,
        "Sulfur": 100,
    },
    "Vesania": {
        "Hydrogen": 100,
        "Argon": 50,
        "Nitrogen": 75
    },
    "Novus": {
        "Hydrogen": 25,
        "Methane": 75,
    },
    "Glacio": {
        "Argon": 100,
    },
    "Atrox": {
        "Methane": 100,
        "Nitrogen": 50,
        "Sulfur": 75,
        "Helium": 25
    }
}
# PLANET_ATMOSPHERE[%planet%].get(%gas%, 0)

COMMON_RESOURCES: list[Resource] = [
    "Soil",
    "Organic",
    "Compound",
    "Resin",
    "Clay",
    "Quartz",
    "Ammonium",
    "Graphite",
    "Laterite",
    "Astronium",
]

PLANET_RESOURCES: dict[Planet, list[Resource]] = {
    "Sylva": ["Sphalerite", "Malachite"],
    "Desolo": ["Sphalerite", "Wolframite"],
    "Calidor": ["Wolframite", "Malachite"],
    "Vesania": ["Lithium", "Titanite"],
    "Novus": ["Lithium", "Hematite"],
    "Glacio": ["Hematite", "Titanite"]
}

REFINED_RESOURCES: dict[RefinedResource, Resource] = {
    "Carbon": "Organic",
    "Ceramic": "Clay",
    "Glass": "Quartz",
    "Aluminum": "Laterite",
    "Zinc": "Sphalerite",
    "Copper": "Malachite",
    "Tungsten": "Wolframite",
    "Iron": "Hematite",
    "Titanium": "Titanite",
}

AnyResource = Literal[Resource, RefinedResource, CompositeResource]

COMPOSITE_RESOURCES: dict[CompositeResource, tuple[AnyResource, AnyResource, Gas | None]] = {
    "Rubber": ("Organic", "Resin", None),
    "Plastic": ("Carbon", "Compound", None),
    "Aluminum_Alloy": ("Aluminum", "Copper", None),
    "Tungsten_Carbide": ("Tungsten", "Carbon", None),
    "Graphene": ("Graphite", "Hydrazine", None),
    "Diamond": ("Graphene", "Graphene", None),
    "Hydrazine": ("Ammonium", "Ammonium", "Hydrogen"),
    "Silicone": ("Resin", "Quartz", "Methane"),
    "Explosive_Powder": ("Carbon", "Carbon", "Sulfur"),
    "Steel": ("Iron", "Carbon", "Argon"),
    "Titanium_Alloy": ("Titanium", "Graphene", "Nitrogen"),
    "Nanocarbon_Alloy": ("Titanium_Alloy", "Steel", "Helium"),

}


# @dataclass(frozen=True)
# class Recipe:
#     product = str
#     machine = str


# @dataclass(frozen=True)
# class Resource:
#     name: str
#     recipe: Recipe = field(init=False)

#     @cache
#     def __new__(cls, name: str) -> Self:
#         return super().__new__(cls)

def parser():
    with open('recipes.txt') as file:
        recipes_txt = file.read()
    recipes: dict[str, tuple[str, list[tuple[int, str]]]] = {}
    for block in recipes_txt.split("\n\n"):
        print_size, *b_recipes = block.split("\n")
        for recipe in b_recipes:
            product, resources = recipe.split("- ")
            resources = resources.split(", ")
            product = product.strip(" ").lower().title().replace(" ", "_")
            recipes[product] = (print_size, [])
            for quantity_resource in resources:
                quantity, *resource = quantity_resource.strip(" ").split(" ")
                resource = " ".join(resource).strip(" ").lower().title().replace(" ", "_")
                try:
                    check_type(argname='resource', value=resource, expected_type=AnyResource)
                    recipes[product][1].append((int(quantity), resource))
                except Exception as e:
                    print(recipe)
                    raise e
    
    with open("output.json", "w") as file:
        json.dump(recipes, file, indent = 4)

parser()

from recipes import RECIPES

def get_raw_resources(r):
    RECIPES[r]
