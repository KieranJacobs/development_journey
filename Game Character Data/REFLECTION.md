# Research

- Field from dataclasses module
- pathlib/path module
- File Handling/File I/O
- Function Arguments

# Development

- What went well?:
  Using examples that I had created from studying about Python syntax, I was able to build the foundation for my functions utilizing file handling and the dataclass I made for the object. I was able to intuitively understand the function of each line, stopping only to research any particular syntax that I was unsure about its function, or to take a look at what I had built and repeat the functionality in my head to enhance my comprehension of what the function wanted to achieve and if that aligned with my goals.

- What was difficult?:
  specific syntax within the dataclasses module was difficult to understand at first glance, but after exploring the problem and referring to syntax manuals and schooling resources available online, I started to make sense of what each syntax wanted to achieve, but the examples they provided were either too generalized or didnt translate well to my current issue.

- What did I learn?:
  The usage of Path, and the usage of Field, I learnt the usage of Field and how it stops the shared-mutable-default bug when referring to an attribute that might share the same mutable such as; string[str]. And the usage of Path in file handling, I learnt that utilizing it provides object-oriented representation rather than relying on raw-strings for File input/output.

- What would I improve?:
  To start with I would want to improve error handling that I have seemingly forgotten to add. Add atomic saves to write a temporary file and use os.replace to avoid an error that might cause half-written files when outputting the result. I would also expand the exercise to be included into its own project and possibly consider multiple classes that interact with eachother as experimentation.

- Which programming patterns did I use?:
  Dictionaries, File I/O, CRUD, Variables/State, Output, Functions.

# Result vs Review

- I managed to achieve the result of printing the character information correctly, however there was some sections of my code that required some tweaks to make it more robust and improve it. For the sake of completing the exercise I chose not apply those changes for the sake of future review.

# Closing Reflection

- Overall, I have learned new concepts and module functionality and module collaboration, I also noticed while testing that I had mistakenly mis-typed the incorrect syntax in the dataclass and the output sections of the exercise program. So I traced back through my code to find me incorrectly searching the wrong file in the load_char() function in the output section of the code, and that I had mistakenly input '=' instead of a semi-colon ':' when defining the [inventory] attribute causing that specific section to fail as well.

- These mistakes allowed me to utilize Python's accurate error declarations and help me find where I had went wrong. I have a new-found interest in debugging as I compare it to a jigsaw puzzle, and this fills me with enthusiasm to keep writing more code with more mistakes and inefficiency to learn from.
