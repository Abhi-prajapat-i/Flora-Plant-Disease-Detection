crops_plant_name = [
        "Potato","Tomato","Apple","Corn","Grape","Pepper","Peach",
        "Cherry","Soybean","Strawberry",
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

prediction_class = {
            "Potato" : potato_class,
            "Tomato" : tomato_class,
            "Apple" : apple_class,
            "Corn" : 2,
            "Grape" : grape_class,
            "Pepper" : 3,
            "Peach" : 4,
            "Cherry" : 4,
            "Soybean" : 2,
            "Strawberry" : 3
}
