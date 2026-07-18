# Requirements

- Create a @dataclass for a game character
- define the attributes of the character (name, level, Inventory list)
- Write a Save & Load function to and from a JSON file.
- Test the exercise by creating, saving and then loading the character.

## What variables are needed?

- a place to store the character and its information
- a place to store/save the newly created JSON file containing the character data

# Data Structures

- Dictionary: stores the character data values (key:value) and orders them while making them unique (no duplicates)
- JSON: Storing data for exchanging between commands that cannot directly interact with eachother.
- File I/O: File creation, saving, loading, character information.

# Patterns Identified

- Output
- File I/O
- CRUD
- Transformation
- Variables / State
- Input
- Error Handling

# Decisions I made and why

- I decided to go with this exercise because I felt that I needed to work on [File I/O] and also become more familiar with [@decorators], the primary reason for this was because I wanted to see how far I could go when it came to expanding a class and its associated attributes while also working with data exchanging. That is also why I added [JSON] functionality to this exercise. A sort of interesting challenge to use all three simultaneously, and adding some quality of life additives in the exercise/project to enhance the overall look and flow of the program.

# Future features

- Potentially expanding the idea inside of a larger project.
