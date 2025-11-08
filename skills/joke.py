import random

def tell_a_joke():
    jokes = [
        "I told my computer I needed a break… now it won't stop sending me Kit-Kat ads.",
        "Why did the scarecrow get promoted? Because he was outstanding in his field.",
        "I asked my dog what's two minus two. He said nothing.",
        "Parallel lines have so much in common… it's a shame they'll never meet.",
        "I told my Wi-Fi we should see other people — now it won't connect with me.",
        "My math teacher called me average. How mean!",
        "I tried to sue the airline for losing my luggage. I lost my case.",
        "I hate it when people use big words just to make themselves sound perspicacious.",
        "The last time I got caught stealing a calendar, I got twelve months.",
        "I asked my friend to help me round up my 37 sheep. He said '40'.",
        "My ex called me lazy. I almost replied.",
        "They say money talks, but mine just waves goodbye.",
        "My therapist says I have a preoccupation with vengeance. We'll see about that.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my boss three companies were after me, and I needed a raise to stay. It worked — he raised my pay. Those companies were the electric, gas, and water companies.",
        "My bed and I are in a committed relationship. We're just having a few sleep issues.",
        "I told my girlfriend she should embrace her mistakes. She hugged me.",
        "I'd tell you a time-travel joke, but you didn't like it.",
        "The problem with political jokes is they sometimes get elected.",
        "I asked Google for a joke about unemployment, it didn't work.",
        "I have a step ladder. I never knew my real ladder.",
        "I tried to start a career as a comedian, but my parents told me I wasn't allowed to joke about them anymore.",
    ]
    
    random_joke = random.choice(jokes)

    return random_joke