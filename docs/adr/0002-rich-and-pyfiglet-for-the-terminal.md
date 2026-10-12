# rich and pyfiglet for the terminal layer

All terminal output goes through `rich` and `pyfiglet` rather than hand-rolled ANSI escape codes. `rich` provides panels, colour, and terminal-width handling for free, and `pyfiglet` produces the title banner.

We accepted the dependency because the visual layer is the most visible part of the submission, and hand-built ANSI styling was producing fragile, repetitive code (the original prototype colourised a string and then typed its escape codes one character at a time). The trade-off is one setup step: the game now requires `pip install -r requirements.txt` before it runs.