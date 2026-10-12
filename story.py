from typing import TypedDict


class Choice(TypedDict):
    label: str
    next: str
    requires: str | None
    sets: list[str]


class Scene(TypedDict):
    title: str
    body: str
    choices: list[Choice]
    on_enter: list[str]


class Verb(TypedDict):
    hint: str | None
    sets: list[str]
    message: str


class Ending(TypedDict):
    title: str
    body: str


SCENES: dict[str, Scene] = {
    "start": {
        "title": "The Keeper Wakes",
        "body": (
            "You wake on the cold iron floor of the lighthouse lamp room, with rain "
            "rattling the glass above you. The Narrator greets you by name—“Welcome, "
            "{name}”—and tells you to keep the light burning so the ships can find "
            "safe passage. Beyond the lantern, the sea folds itself around the rocks."
        ),
        "weather_lines": {
            "calm": "The sea is quiet tonight; keep the light steady, and every ship will find its way home.",
            "grey": "A low sky gathers over the coast; the light will guide every ship safely through it.",
            "storm": "The wind is rising against the windows; hold the light true, and the ships will find safe passage.",
        },
        "choices": [
            {
                "label": "Tend the lamp and obey the Narrator",
                "next": "lamp",
                "requires": None,
                "sets": ["obeyed"],
            },
            {
                "label": "Search the windows for ships",
                "next": "window",
                "requires": None,
                "sets": [],
            },
        ],
        "on_enter": ["storm"],
    },
    "lamp": {
        "title": "The Lantern",
        "body": (
            "You turn the tarnished lens, and its amber beam crawls across the "
            "black water. The Narrator urges you to make it brighter, though a "
            "faint bell rings whenever the beam touches the rocks. Beneath the "
            "lamp, you find a small hand lantern crusted with salt."
        ),
        "choices": [
            {
                "label": "Take the hand lantern",
                "next": "gallery",
                "requires": None,
                "sets": ["has_lantern"],
            },
            {
                "label": "Look toward the flashing water",
                "next": "window",
                "requires": None,
                "sets": [],
            },
            {
                "label": "Keep the great lamp burning",
                "next": "bell",
                "requires": None,
                "sets": ["obeyed"],
            },
        ],
        "on_enter": ["lamp"],
    },
    "window": {
        "title": "The Storm Window",
        "body": (
            "You press your face to the salt-clouded glass and glimpse a ship "
            "struggling against the tide. The beam draws it closer, not toward "
            "the harbor but toward a jagged line of rocks. A pale shape beneath "
            "the waves raises one hand as if it knows you."
        ),
        "choices": [
            {
                "label": "Mark the ship's position",
                "next": "gallery",
                "requires": None,
                "sets": ["ship_seen"],
            },
            {
                "label": "Follow the wet footprints into the gallery",
                "next": "gallery",
                "requires": None,
                "sets": ["ship_seen"],
            },
            {
                "label": "Answer the bell below",
                "next": "bell",
                "requires": None,
                "sets": ["ship_seen"],
            },
        ],
        "on_enter": ["storm", "ship_seen"],
    },
    "gallery": {
        "title": "The Portrait Gallery",
        "body": (
            "You enter a narrow gallery where every portrait has been turned "
            "toward the wall. One frame shows a keeper with your own familiar "
            "eyes, while a locked cabinet trembles in the storm. A faded "
            "photograph lies half-hidden beneath its warped door."
        ),
        "choices": [
            {
                "label": "Study the photograph",
                "next": "log_room",
                "requires": "has_lantern",
                "sets": ["has_photo"],
            },
            {
                "label": "Search the cabinet for a key",
                "next": "cellar",
                "requires": None,
                "sets": ["has_key"],
            },
            {
                "label": "Carry your lantern into the log room",
                "next": "log_room",
                "requires": "has_lantern",
                "sets": [],
            },
            {
                "label": "Return to the lamp room for a lantern",
                "next": "lamp",
                "requires": None,
                "sets": [],
            },
        ],
        "on_enter": [],
    },
    "log_room": {
        "title": "The Keeper's Log",
        "body": (
            "You enter the log room, where damp pages cling together beneath "
            "a film of sea salt. In the last entry, you read that the lighthouse "
            "beam lured ships onto the rocks, and that the previous keeper "
            "drowned before the Narrator began speaking in your ear. The ink "
            "runs in the same hand as the name on your photograph."
        ),
        "choices": [
            {
                "label": "Take the logbook and accept what it says",
                "next": "cellar",
                "requires": None,
                "sets": ["has_logbook", "knows_truth"],
            },
            {
                "label": "Carry the truth to the bell",
                "next": "bell",
                "requires": None,
                "sets": ["knows_truth"],
            },
            {
                "label": "Return to the gallery",
                "next": "gallery",
                "requires": None,
                "sets": [],
            },
        ],
        "on_enter": [],
    },
    "cellar": {
        "title": "The Flooded Cellar",
        "body": (
            "You descend into the cellar, where black water laps at the lowest "
            "stair. A chain runs from the lighthouse mechanism into the flooded "
            "dark, and a drowned keeper's coat turns slowly in the current. You "
            "recognize the voice that tells you to leave the light alone."
        ),
        "choices": [
            {
                "label": "Follow the chain toward the bell",
                "next": "bell",
                "requires": None,
                "sets": ["knows_truth"],
            },
            {
                "label": "Break the chain and go to the lamp",
                "next": "lamp",
                "requires": "has_key",
                "sets": ["defied"],
            },
            {
                "label": "Return to the log room",
                "next": "log_room",
                "requires": "has_lantern",
                "sets": [],
            },
        ],
        "on_enter": [],
    },
    "bell": {
        "title": "The Bell Tower",
        "body": (
            "You reach the bell tower as the storm leans against the stone. "
            "Below, the ship edges toward the reefs while the Narrator begs you "
            "to keep the light bright. The drowned keeper's voice rises from "
            "the sea, and you must choose which signal the living will see."
        ),
        "choices": [
            {
                "label": "Keep faith with the Narrator and the light",
                "next": "end_faithful",
                "requires": "obeyed",
                "sets": [],
            },
            {
                "label": "Turn the beam toward the true shore",
                "next": "end_true_shore",
                "requires": "knows_truth",
                "sets": ["defied"],
            },
            {
                "label": "Extinguish the lighthouse",
                "next": "end_extinguished",
                "requires": "defied",
                "sets": [],
            },
            {
                "label": "Speak the keeper's name into the storm",
                "next": "end_remembered",
                "requires": "has_photo",
                "sets": [],
            },
            {
                "label": "Raise a second light beside the first",
                "next": "end_two_lights",
                "requires": "has_lantern",
                "sets": [],
            },
        ],
        "on_enter": ["bell", "lamp"],
    },
}


VERBS: dict[str, Verb] = {
    "listen": {
        "hint": "The sea keeps what the tower forgets.",
        "sets": ["knows_truth"],
        "message": "You hear the drowned keeper beneath the Narrator's borrowed voice.",
    },
    "remember": {
        "hint": "Some names return when you let the silence settle.",
        "sets": [],
        "message": "You hold a lost name in your thoughts, and the tower remembers you.",
    },
    "shine": {
        "hint": None,
        "sets": ["obeyed"],
        "message": "You turn the beam outward, and its hungry glow reaches across the sea.",
    },
    "dark": {
        "hint": None,
        "sets": ["defied"],
        "message": "You deny the light its command, and the sea answers in darkness.",
    },
    "open": {
        "hint": None,
        "sets": ["has_key"],
        "message": "You force the swollen cabinet open and find a small brass key.",
    },
    "look": {
        "hint": None,
        "sets": ["ship_seen"],
        "message": "You spot a ship beyond the rain, already turning toward the rocks.",
    },
    "climb": {
        "hint": None,
        "sets": [],
        "message": "You climb the wet stairs as the bell tolls somewhere above you.",
    },
    "wait": {
        "hint": None,
        "sets": [],
        "message": "You wait, and the storm fills the silence with a drowned voice.",
    },
}


ENDINGS: dict[str, Ending] = {
    "end_faithful": {
        "title": "Faithful Keeper",
        "body": (
            "You keep the lamp burning as the Narrator commanded, and its bright "
            "beam draws the ship onto the waiting rocks. You hear the drowned "
            "keeper thank you from beneath the waves, while the tower claims "
            "another faithful voice."
        ),
    },
    "end_true_shore": {
        "title": "The True Shore",
        "body": (
            "You turn the beam away from the reefs and sweep it across the safe "
            "harbor mouth. The ship follows your signal through the storm, and "
            "you hear the Narrator fall silent beneath the surf. You have given "
            "the living a shore the dead could not find."
        ),
    },
    "end_extinguished": {
        "title": "Extinguished",
        "body": (
            "You snuff the lighthouse flame, and the false voice vanishes into "
            "the dark. The ship slips past the reefs by starlight, but the tower "
            "goes blind around you. You stand alone with the sea and its "
            "unanswered bell."
        ),
    },
    "end_remembered": {
        "title": "Remembered",
        "body": (
            "You speak the keeper's name, and the drowned face in the photograph "
            "finally looks back at you. The Narrator remembers the life it lost "
            "and releases its hold on the tower. You carry that name beyond the "
            "shore, where the sea can no longer erase it."
        ),
    },
    "end_two_lights": {
        "title": "Two Lights",
        "body": (
            "You lift the hand lantern beside the great lamp, sending two "
            "distinct signals into the storm. The ship reads the smaller flame "
            "as a warning and steers clear of the rocks. You keep one light for "
            "the living and leave one burning for the dead."
        ),
    },
}
