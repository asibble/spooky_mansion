import json, time, os, random

#LEFT TODO: 

def main():
    # TODO: allow them to choose from multiple JSON files?
    print("Which game would you like to play?")
    games=[]
    for file in os.listdir():
        if "json" in file:
            games.append(file)
    for i in range(len(games)):
        print("  ", str(i+1)+".", games[i])
    targetgame=games[int(input("> "))-1]
    with open(targetgame) as fp:
        game = json.load(fp)
    print_instructions()
    #print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    clothing = []
    start_time=time.time()
    cat_location= rooms['__metadata__']['catstart']
    #Exit Checker: No Dead Ends
    for i in rooms:
        for j in rooms[i]["exits"]:
            if j["destination"] not in rooms:
                print ("ERROR: There is an exit without a destination. This game is broken.")
                return
    
    while True:
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        cat_place=rooms[cat_location]
        if cat_place==here:
            print ("\nThere is a cat hanging around. Meow.\n")
        # TODO: print any available items in the room... 
        # e.g., There is a Mansion Key.
                    
        if len(here["items"]) > 0:
            print("In this room:")
            for i in here["items"]:
                print("")
                print (i)
            print("")
        
        # Is this a game-over?
        if here.get("ends_game", False):
            print("You finished the game in", int(time.time()-start_time), "seconds")
            break
        if "x-ray glasses" in clothing:
            for exit in here['exits']:
                if "invisible" in exit:
                    exit.pop("invisible", True)
                    print ("You see something with the glasses!")
        
        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))
        
        cat_exits = find_usable_exits(rooms[cat_location], stuff)
        # See what they typed:
        action = input("> ").lower().strip()
    
        # If they type any variant of quit; exit the game.
        
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        # TODO: if they type "stuff", print any items they have (check the stuff list!) 4 pts
        elif action=="help":
            if "x-ray glasses" in stuff or "x-ray glasses" in clothing:
                print_instructions_2()
            else:
                print_instructions()
            continue
        elif action == "stuff":
            if len(stuff)>0:
                print("You have:")
                for i in stuff:
                    print("   -"+i)
                    print("")
            else:
                print("You have nothing.")
                print("")
            continue
        # TODO: if they type "take", grab any items in the room. 4 pts
        elif action =="take":
            if len(here["items"]) == 0:
                print ("There is nothing to take.")
            elif here["items"] not in stuff:
                for i in here["items"]:
                    stuff.append(i)
                    if i == "x-ray glasses":
                        print(" - Type 'glasses' to wear the x-ray glasses.")
                print ("You took the items you were able to find.")
                here["items"].clear()
            print("")
            continue
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        elif action == "search":
            print("You search the room for secrets")
            for exit in here['exits']:
                if "hidden" in exit:
                    exit.pop("hidden", True)
                    print ("Found something!")
            print("")
            continue
        elif action == "glasses":
            if "x-ray glasses" in clothing:
                print("You took off the glasses and put them with your stuff.")
                clothing.remove("x-ray glasses")
                stuff.append("x-ray glasses")
            elif "x-ray glasses" in stuff:
                print("You put on the glasses! You might be able to find a secret.")
                clothing.append("x-ray glasses")
                stuff.remove("x-ray glasses")            
            continue
            
        elif action == "drop":
            if len(stuff)>0:
                print("Which item would you like to drop?")
                for i in stuff:
                    print ("1.", i)
                drop_num=int(input("> "))-1
                if drop_num <= (len(stuff)+1):
                    thing=stuff[drop_num]
                    here["items"].append(thing)
                    stuff.remove(thing)
                else:
                    print("That is not an option, try again")
                    drop_num=input("> ")
            continue
        # Try to turn their action into an exit, by number.
        
            
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
            cat_location=cat_exits[random.randint(0,len(cat_exits)-1)]['destination']
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("invisible", False):
            continue
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

def print_instructions_2():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'glasses' to wear the x-ray glasses.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()