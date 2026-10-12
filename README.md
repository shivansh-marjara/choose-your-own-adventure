# choose-your-own-adventure

# KEEPER

A terminal choose-your-own-adventure set inside a haunted lighthouse — narrated by a voice
that is not telling you the truth.

## The idea

You wake in the lamp room of a lighthouse. A Narrator greets you by your name and tells you
to keep the light burning so ships reach safe harbour. It sounds like a rescue story.

Play it more than once and things start to change.

## Features

- A scene graph driven by flags and a four-item inventory, so your choices have consequences
- **8 secret verbs** you can type instead of a number — only 2 are ever hinted
- **5 endings**, two of which are hidden
- A narrator who lies, and rewrites earlier text once you learn the truth
- The game **remembers you**: it saves your name and your last ending, and greets returning players differently
- A `rich` + `pyfiglet` terminal layer — banner, panels, an animated storm, a pulsing lamp, an ASCII bell

## Requirements

- Python 3.10+
- `pip install -r requirements.txt`

## Run

```bash

Useful flags:

```bash


## How to play

At each prompt, enter the **number** of a choice. You may also try **typing a word** — the
game understands a few. Two of them are `listen` and `remember`. The other six are yours to find.

## Files

| File | Purpose |
| --- | --- |
| `game.py` | The engine: loop, input handling, save/load, ending resolution |
| `story.py` | All story content as plain data (scenes, verbs, endings) |
| `ui.py` | The terminal presentation layer (`rich` + `pyfiglet`) |
| `requirements.txt` | Dependencies |
| `GLOSSARY.md` | The game's canonical vocabulary |
| `docs/adr/` | Two decision records |

## Built with

GitHub Copilot, for **Global Hack Week: Hacktoberfest** — the "Use GitHub Copilot to Build a
Simple Application" challenge.