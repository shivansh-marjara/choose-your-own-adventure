# KEEPER

A terminal choose-your-own-adventure set inside a haunted lighthouse, told by a narrator who is not telling the truth.

| **Sky** | The real-world weather fetched for the chosen place; drives the opening mood. |
| **Mood** | One of `calm` / `grey` / `storm`; derived from the Sky. |
| **Place** | The real city/coast the player names; the light "watches" it. |
| **Fallback** | What the game does when the network is unavailable: behave as plain offline KEEPER. |

## Language

**Keeper**:
The role the player occupies: the consciousness operating the lighthouse lamp.
_Avoid_: player, hero, character, avatar

**Narrator**:
The voice that addresses the player throughout the game, and the drowned previous keeper. A character in the story, not the game's interface.
_Avoid_: system, AI, guide, text box

**Scene**:
A single node of the story: one body of text plus zero or more choices.
_Avoid_: room, level, page, stage

**Choice**:
A numbered option that moves the player to another scene and may set flags.
_Avoid_: option, answer, path, branch

**Verb**:
A secret word typeable at any prompt; performs an action without moving the player to another scene.
_Avoid_: command, cheat, keyword, input

**Flag**:
A single recorded fact about the current run.
_Avoid_: variable, state, condition, boolean

**Run**:
One playthrough, from the opening scene to one ending.
_Avoid_: game, session, play, attempt

**Ending**:
A terminal scene. There are five; two are hidden.
_Avoid_: finish, outcome, result, death