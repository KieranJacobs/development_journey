import json
from dataclasses import dataclass, asdict, field
from pathlib import Path

# class of Game-Character Data
@dataclass # declare that the class below is a DataClass
class Character:
    name: str # attribute [name] = String
    level: int = 1 # attribute [level] = integer [1] by default
    inventory: list = field(default_factory=list) # ensures each Character class gets its own list (avoids shared mutable default)

# function to save class to JSON file
def save_char(char: Character, path: str) -> None: # function expects two arguments (char: which is attached to the class 'Character' & path: which is a filesystem path where the class object will be written)
    Path(path).parent.mkdir(parents=True, exist_ok=True) # ensures parent directory exists, IF NO...
    with open(path, "w", encoding="utf-8") as f: # open/create a path with UTF-8 encoding...
        json.dump(asdict(char), f, indent=2) # and calls json.dump(asdict(char)) to turn the dataclass into a plain dict. It then writes that dict as JSON.

# function to load class from JSON file
def load_char(path: str) -> Character | None: # checks if the file exists; 
    p = Path(path) # pre-declare parent directory path
    if not p.exists(): # if not, it returns None.
        return None
    with open(path, "r", encoding="utf-8") as f: # if the file exists;
        data = json.load(f) # it opens and loads the contents into a dict
    return Character(**data) # then constructs and returns Character(**data). NOTE: this expects the JSON keys to match so a malformed JSON or incorrect fields will raise an exception.

# output
c = Character("Hero", level=1, inventory=["Healing Potion"]) # declares class as variable 'c'
save_char(c, "saves/character.json") # calls the variable 'c' attached to class then sends to a folder called [saves] as a file called character.json. If the folder does not exist, it will create one, same with the .json file.
loaded = load_char("saves/character.json") # runs the load function, calling for the character.json file inside the saves folder.
print(loaded) # print loaded .json file