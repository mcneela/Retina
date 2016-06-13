import matplotlib as mpl

class Controller:
    def __init__(self, artist):
        self.artist = artist
        if not isinstance(artist, mpl.backend_bases.Artist):
            raise TypeError("artist must be a Matplotlib artist")
        self.bindings = {}
        event = None
        binding = None
        while True: 
            print(
            "Welcome to the Fovea controller interface!\n"
            "This dynamic, interactive class allows you to bind\n"
            "events of your choice to behavior in the Matplotlib window.\n"
            "To start, enter the key or word to which you would like to bind\n"
            "to Matplotlib/Fovea behavior. For mouse buttons enter one of\n"
            "    1. <LeftClick>\n"
            "    2. <RightClick>\n"
            "To exit the controller interface while saving all current bindings,\n"
            "type 'exit'.\n"
            )
            event = input()
            if event == "exit":
                break
            print("Please enter the Matplotlib function call to be bound.")
            binding = input()
            if binding == "exit":
                break
            self.bindings[event] = binding
        
