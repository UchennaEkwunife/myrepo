from argparse import ArgumentParser
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Player:
    """A class representing the player character in a story.
    
    Attributes:
        name (str): the player's name.
        inventory (list): a list containing all of the items 
            a player will pick up.
        health (int): the amount of health points a player has.
    """
    def __init__(self, name, health = 100):
        """ Primary Author:
            
            Initializes a Player object.
        
        Args:
            name (str): the player's name.
            health (int): the amount of health points a player has.
                
        Side Effects:
            Initializes name, inventory, and health.
        """
        self.name = name
        self.inventory =set()
        self.health = 100
    

    def add_item(self, item):
        """Primary Author: Conrad Dzikunu,
            Technique: set operation
            Appends an item to an inventory list.
        
        Args:
            item (str): the item that will go into a player's inventory.
        """
        self.inventory =set()
        self.inventory.add(item)

    def display_inventory(self):
        """ Primary Author: Conrad Dzikunu
            Technique: f-strings
            Prints the player's current inventory.
        
        Side Effects:
            Prints result as an f-string.
        """
        inventory_str = ''.join(self.inventory)
        print(f"Inventory: {inventory_str}")
        
    def is_alive(self):
        """ Primary Author:
            Techniques: conditional expressions
            Checks player's current health to see if they are alive.
        
        Returns:
            True: if health is greater than 0.
            False: if health is less than 0.
        """
        return True if self.health > 0 else False
    
    def __add__(self, operator):
        """ Primary Author:
            Techniques: magic method
            
            Returns a new Player object with the player's health 
            increased by the given operator.
            
            Args:
                operator (int): the amount that will be added to
                    the player's health.
            
            Returns:
                new_player (Player): the new player object 
                    and their health.
        """
        new_player = Player(self.name, self.health + operator)
        return new_player
        
    def __sub__(self, operator):
        """ Primary Author:
            Techniques: magic method
            
            Returns a new Player object with the player's health 
            decreased by the given operator.
            
            Args:
                operator (int): the amount that will be added to
                    the player's health.
            
            Returns:
                new_player (Player): the new player onject and their 
                    health.
        """
        new_player = Player(self.name, self.health - operator)
        return new_player
    
class Story:
    """A class representing the story for the game.
    
    Attributes:
        story_id (str): a unique key for each possible story path.
        story_text (str): the text in the story.
        choices (dict): the available choices the player can pick as
            their story path.
    """
    def __init__(self, story_id, story_text, choices, items):
        """ Primary Author:
        
            Initializes a Story object.
        
        Args:
            story_id (str): a unique key for each possible story path.
            story_text (str): the text in the story.
            choices (dict): the available choices the player can pick as 
                their story path.
            items (dict): the available items to be added to a player's inventory
                
        Side Effects:
            Initializes story_id, story_text, choices, and items.
        """
        self.story_id = story_id
        self.story_text = story_text
        self.choices = choices
        self.items = items
    
    def display_story(self):
        """ Primary Author:
            Returns the story's current text.
        
        Returns:
            self.story_text: the current text in the story.
        """
        return self.story_text
    
    def get_choices(self):
        """ Primary Author:
        
            Returns the avaible choices for the given point in the story.
        
        Returns:
            self.choices: the available choices for the current path.
        """
        return self.choices
    
    def get_items(self):
        return self.items

    def update_story(self, choice):
        """ Primary Author:
            
            Updates the story based on the player's choice and 
            returns the next part. Returns None if there is no 
            next part.
        
        Args:
            choice (str):
                the story path the player selected.
        
        Returns:
            None: if there is no next choice.
            next_story: the next part of the story based on 
                the selected choice.
        """
        if not choice:
            return None

        if isinstance(choice, str):
            choice_id = choice.strip()
        next_story = self.choices.get(choice_id)
        
        return next_story

class Game():
    """ A class representing the game.
    
    Attributes:
        filepath (str): the path leading to a file containing 
            the story.
        name (str): the player's name.
        health (int): the amount of health points a player has.
    """
    def __init__(self, filepath):
        """ Primary Author:
            Techniques: sequence unpacking, with
            Initializes a Game object.
        
        Args:
            filepath (str): the path leading to a file containing 
                the story.
            name (str): the player's name.
            health (int): the amount of health points a player has.
                
        Side Effects:
            Initializes name and health.
        """
        

        self.story_map = {}
        with open(filepath, "r") as f:
            data = json.load(f)
            for story_id, story_data in data.items():
                story_text = story_data.get("story_text")
                choices = story_data.get("Choice")
                items = story_data.get("items")
                self.story_map[story_id] = Story(story_id, story_text, choices,items)
    
    
    def load_frequency(self):
        """ Primary Author: Uchenna Ekwunife
            Techniques: Pandas, pyplot, seaborn
            
            Loads data from a JSON file containing a story and displays a bar plot of the frequency of each choice made by readers.
            Side Effects:
                Creates a graph showing frequent answers by users.
        """
        with open('story1.json') as f:
            story = json.load(f)
            counts = {}
            
            for key in story:
                if 'Choice' in story[key]:
                    for choice in story[key]['Choice']:
                        counts[choice] = counts.get(choice, 0) + 1

            data = [(choice, count) for choice, count in counts.items()]
            df = pd.DataFrame(data, columns=['choice', 'count'])
               
            sns.barplot(x='count', y='choice', data=df)
            plt.xlabel('Count')
            plt.ylabel('Choice')
            plt.show()
            
    def play(self):
        """ Primary Author: Uchenna Ekwunife
            Techniques: Composition
        
            Displays the story,inventory and choices made as the game is played,
            story is updated based on the player's choices.
        
        Side Effects:
            Prints the current story, inventory, choices, a game over message, 
                and an invalid choice error.
        """
        player = Player(self)
        current_story_id = "start"
        
        while True:
            if current_story_id.__contains__("game_over"):
                story_is_over = self.story_map[current_story_id]
                print(story_is_over.display_story())
                print("Game Over")
                player.display_inventory()
                print()
                break
            story = self.story_map[current_story_id]
            print()
            print(story.display_story())
            choices = story.get_choices()
            items= story.get_items()
            print()
            if not choices:
                break
            items = story.get_items()
            if items:
                for item_id in items:
                    player.add_item(item_id)
                    print(f"{item_id} added to inventory")
                    player.display_inventory()
                    print()
                    

            while True:
                for choice_id in choices:
                    print(f"{choice_id}:")
                choice = input("Enter your choice: ")
                    
                current_story_id = story.update_story(choice)
                if current_story_id:
                    break
                print("Invalid choice. Please try again") 
            
        
def main(filepath, name, health):
    """Primary Author: 
        Technique: ArgumentParser
        
        A function that runs the program. It allows users to enter
        their name, and reads a story file and the amount of health
        they have to create an instance of a Game object.
    
    Args:
        filepath (str): the path leading to a file containing 
            the story.
        name (str): the player's name.
        health (int): the amount of health points a player has.
    
    """
    name = input("Enter your name: ")
    game = Game(filepath)
    game.play()
    df = game.load_frequency()
    print(df)
    

if __name__ == "__main__":
    """This is executed when the script is run directly 
        (not imported as a module). It creates an argument 
        parser and defines the arguments, then calls the
        main() function.
    """
    parser = ArgumentParser()
    parser.add_argument("filepath", help="path to story file")
    parser.add_argument("--name", help="player name (default: Player)", default="Player")
    parser.add_argument("--health", help="player health (default: 100)", type=int, default=100)
    args = parser.parse_args()
    main(args.filepath, args.name, args.health)