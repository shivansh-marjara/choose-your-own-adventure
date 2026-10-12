import argparse
import json
from pathlib import Path

from rich.prompt import Prompt

import story
import ui
import weather


SAVE_FILE = "keeper_save.json"
ITEM_FLAGS = {"has_lantern", "has_key", "has_logbook", "has_photo"}
STORY_FLAGS = {
    "obeyed",
    "defied",
    "has_lantern",
    "has_key",
    "has_logbook",
    "has_photo",
    "knows_truth",
    "ship_seen",
}


def load_save():
    fresh_save = {
        "name": "",
        "nights": 0,
        "last_ending": None,
        "endings_seen": [],
    }
    try:
        loaded = json.loads(Path(SAVE_FILE).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return fresh_save
    except (OSError, json.JSONDecodeError) as error:
        ui.console.print(f"[yellow]Could not load save file: {error}[/yellow]")
        return fresh_save

    if not isinstance(loaded, dict):
        ui.console.print("[yellow]Save file was not an object; starting a fresh game.[/yellow]")
        return fresh_save

    meta = {**fresh_save, **loaded}
    if not isinstance(meta["name"], str):
        meta["name"] = ""
    if not isinstance(meta["nights"], int) or isinstance(meta["nights"], bool):
        meta["nights"] = 0
    if meta["last_ending"] is not None and not isinstance(meta["last_ending"], str):
        meta["last_ending"] = None
    if not isinstance(meta["endings_seen"], list):
        meta["endings_seen"] = []
    else:
        meta["endings_seen"] = [
            ending for ending in meta["endings_seen"] if isinstance(ending, str)
        ]
    return meta


def save_game(meta):
    Path(SAVE_FILE).write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def decide_ending(state) -> str:
    flags = state["flags"]
    if "dark_used" in flags and "knows_truth" in flags:
        return "end_true_shore"
    if "dark_used" in flags:
        return "end_extinguished"
    if state["remember_count"] >= 3 and "obeyed" in flags:
        return "end_two_lights"
    if "has_photo" in flags and "defied" not in flags:
        return "end_remembered"
    return "end_faithful"


def _apply_flags(state, flags):
    for flag in flags:
        state["flags"].add(flag)
        if flag in ITEM_FLAGS:
            state["inventory"].add(flag)


def _show_entry_effects(scene_id, state, animations=True, skip_storm=False):
    effects = {
        "storm": lambda: ui.storm(),
        "lamp": lambda: ui.lamp(),
        "bell": lambda: ui.bell(),
    }
    for effect in story.SCENES[scene_id]["on_enter"]:
        if effect in effects:
            if effect == "storm" and skip_storm:
                continue
            if not animations:
                continue
            if effect not in {"bell"} and ui.console.width < 40:
                continue
            effects[effect]()
        elif effect in STORY_FLAGS:
            _apply_flags(state, [effect])
        else:
            raise ValueError(f"Unknown on_enter effect: {effect}")


def _visible_choices(scene, state):
    return [
        choice
        for choice in scene["choices"]
        if choice["requires"] is None
        or choice["requires"] in state["flags"]
        or choice["requires"] in state["inventory"]
    ]


def _ending_narration(ending_id):
    messages = {
        "end_faithful": "You chose the light before. It led them to the rocks.",
        "end_true_shore": "You chose the true shore before. The sea remembers.",
        "end_extinguished": "You chose the dark before. It did not free you.",
        "end_remembered": "You remembered the keeper before. The tower remembers too.",
        "end_two_lights": "You carried two lights before. One is still burning.",
    }
    return messages.get(ending_id, "You have been here before. The tower remembers.")


def play(debug=False, typewriter=False):
    meta = load_save()
    if not meta["name"]:
        while not meta["name"]:
            meta["name"] = Prompt.ask("What is your name").strip()
            if not meta["name"]:
                ui.console.print("[yellow]Please enter a name to begin.[/yellow]")
        save_game(meta)
        ui.say(f"You are awake, {meta['name']}. Keep the light burning.")
    else:
        meta["nights"] += 1
        save_game(meta)
        ui.say(f"It has been {meta['nights']} nights. You came back, {meta['name']}.")
        ui.say(_ending_narration(meta["last_ending"]))

    try:
        place = Prompt.ask(
            "Which coast should the light watch? (a city, or Enter to skip)",
            default="",
        ).strip()
        sky = (
            weather.sky_for(place)
            if place
            else {"mood": "calm", "line": None, "place": None, "raw": None}
        )
    except Exception:
        sky = {"mood": "calm", "line": None, "place": None, "raw": None}

    ui.show_banner("KEEPER")

    while True:
        state = {
            "flags": set(),
            "inventory": set(),
            "current": "start",
            "remember_count": 0,
            "weather": sky,
        }
        if sky["mood"] == "storm":
            state["flags"].add("real_storm")
        entering_scene = True

        while True:
            current = state["current"]
            if current.startswith("end_"):
                ending = story.ENDINGS[current]
                if debug:
                    ui.console.print(f"Ending: {current}")
                    ui.console.print(f"Final flags: {', '.join(sorted(state['flags'])) or '(none)'}")
                else:
                    ui.show_scene(ending["title"], ending["body"], typewriter=typewriter)
                meta["last_ending"] = current
                meta["endings_seen"].append(current)
                save_game(meta)
                break

            scene = story.SCENES[current]
            if entering_scene:
                is_weather_storm = current == "start" and sky["mood"] == "storm"
                if current == "start" and sky["line"] is not None:
                    if is_weather_storm:
                        ui.storm()
                    ui.say(sky["line"])
                _show_entry_effects(
                    current,
                    state,
                    animations=not debug,
                    skip_storm=is_weather_storm,
                )
                entering_scene = False

            body = scene["body"].replace("{name}", meta["name"])
            ui.show_scene(scene["title"], body, typewriter=typewriter)
            choices = _visible_choices(scene, state)
            ui.show_choices([choice["label"] for choice in choices])
            answer = Prompt.ask("Your choice").strip()

            try:
                choice_number = int(answer)
            except ValueError:
                choice_number = 0

            if 1 <= choice_number <= len(choices):
                choice = choices[choice_number - 1]
                _apply_flags(state, choice["sets"])
                destination = choice["next"]
                if destination.startswith("end_"):
                    state["current"] = decide_ending(state)
                else:
                    state["current"] = destination
                entering_scene = True
                continue

            verb_name = answer.lower()
            if verb_name in story.VERBS:
                verb = story.VERBS[verb_name]
                _apply_flags(state, verb["sets"])
                if verb_name == "dark":
                    # Keep the typed action distinct from other ways to defy the Narrator.
                    state["flags"].add("dark_used")
                elif verb_name == "remember":
                    state["remember_count"] += 1
                ui.console.print(verb["message"])
                continue

            ui.console.print("[yellow]That isn't a choice. Try a number or a secret word.[/yellow]")

        if Prompt.ask("Play again?", choices=["y", "n"], default="n") == "n":
            return
        ui.say(f"The storm draws you back, {meta['name']}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play KEEPER, a lighthouse story.")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="show ending ids and final flags instead of ending text",
    )
    parser.add_argument(
        "--typewriter",
        action="store_true",
        help="reveal scene text with a typewriter effect",
    )
    arguments = parser.parse_args()
    play(debug=arguments.debug, typewriter=arguments.typewriter)
