from generate import generate_images

traits = [
    {
        "Background": "Leaf",
        "Spots": "Zero",
        "Color": "Red",
        "Accessory": None,
        "Eyes": "White",
    },
    {
        "Background": "Stick",
        "Spots": "Two Black",
        "Color": "Red",
        "Accessory": None,
        "Eyes": "White",
    },
    {
        "Background": "Trees",
        "Spots": "Three Black Stripes",
        "Color": "Red",
        "Accessory": None,
        "Eyes": "White",
    },
    {
        "Background": "Road",
        "Spots": "Seven Black",
        "Color": "Red",
        "Accessory": None,
        "Eyes": "White",
    },
    {
        "Background": "City",
        "Spots": "Thirteen Black",
        "Color": "Red",
        "Accessory": None,
        "Eyes": "White",
    },
    {
        "Background": "Night Sky",
        "Spots": "Thirteen Black",
        "Color": "Red",
        "Accessory": None,
        "Eyes": "White",
    },
]

traits = generate_images(traits)
