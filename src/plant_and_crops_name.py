crops_plant_name = [
        "Potato","Tomato","Apple","Corn","Grape","Pepper","Peach",
        "Cherry","Soybean","Strawberry","Wheat","Rice"
        ]

languages = [
        "English","Hindi","Hinglish","Odia","Bengali","Tamil","Telugu",
        ]

# Plant disease name.
# --> Potato
potato_class = ['Early blight', 'Late_blight', 'Healthy leaf']
# --> Tomato
tomato_class = [
    "Bacterial Spot","Early Blight","Healthy","Late Blight","Leaf Mold",
    "Septoria Leaf Spot","Two-Spotted Spider Mite","Target Spot","Tomato Yellow Leaf Curl Virus"
]
# --> Grape
grape_class = ["Black Rot Disease","Esca (Grapevine Trunk Disease)","Healthy Leaf","Leaf Blight Disease"]
# --> Apple
apple_class = ["Apple Scab Disease","Black Rot Disease","Cedar Apple Rust Disease","Healthy Apple Leaf"]
# --> Corn 
corn_class = ["Gray Leaf Spot","Common Rust","Northern Leaf Blight","Healthy"]
# --> Weath
wheat_class = ['Wheat Brown Rust', 'Healthy', 'Wheat Yellow Rust']
# --> Rice 
rice_class =  ['Rice Bacterial Leaf Blight','Rice Brown Spot','Healthy Rice Leaf','Rice Leaf Blast','Rice Leaf Scald',
    'Rice Narrow Brown Leaf Spot','Rice Hispa','Rice Sheath Blight']

prediction_class = {
            "Potato" : potato_class,
            "Tomato" : tomato_class,
            "Apple" : apple_class,
            "Corn" : corn_class,
            "Grape" : grape_class,
            "Wheat" : wheat_class,
            "Rice" : rice_class,
            "Pepper" : 3,
            "Peach" : 4,
            "Cherry" : 4,
            "Soybean" : 2,
            "Strawberry" : 3
}
