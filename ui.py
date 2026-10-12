import time

import pyfiglet
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


console = Console()


def show_banner(title):
    banner = pyfiglet.figlet_format(title)
    if max((len(line) for line in banner.splitlines()), default=0) > console.width:
        console.print(title)
        return
    console.print(Text(banner, style="bold #D99032"))
    console.rule(style="dim")


def show_scene(title, body, typewriter=False):
    if not typewriter:
        console.print(Panel(body, title=title, border_style="dim", width=80))
        return

    typed_body = ""
    with Live(
        Panel(typed_body, title=title, border_style="dim", width=80),
        console=console,
        refresh_per_second=60,
    ) as live:
        for character in body:
            typed_body += character
            live.update(Panel(typed_body, title=title, border_style="dim", width=80))
            time.sleep(0.012)
        live.update(
            Panel(Text(typed_body, style="cyan"), title=title, border_style="dim", width=80)
        )


def show_choices(choices):
    for index, choice in enumerate(choices, start=1):
        line = Text()
        line.append(f"{index}.", style="bold")
        line.append(f" {choice}")
        console.print(line)


def say(text):
    console.print(f"│ {text}", style="italic dim")


def storm(frames=3):
    frame_count = max(0, frames)
    delay = min(0.18, 1.5 / frame_count) if frame_count else 0
    lightning = (
        "        .     .",
        "   .      \\  /      .",
        "      ----<*",
        "             \\__",
        "        .          .",
    )

    for frame in range(frame_count):
        console.clear()
        style = "bold bright_yellow" if frame % 2 == 0 else "bold yellow"
        for line in lightning:
            console.print(line, style=style)
        time.sleep(delay)

    console.clear()


def lamp(pulse=True):
    widths = (1, 3, 5, 3, 1) if pulse else (3,)
    for width in widths:
        console.clear()
        console.print("      /\\")
        console.print("     /  \\")
        console.print("    | [] |")
        console.print("    |    |")
        console.print("    |____|")
        console.print("       ||")
        console.print("       ||")
        console.print(" " * 6 + "=" * width + ">")
        if pulse:
            time.sleep(0.12)


def bell():
    console.print("   .-.")
    console.print("  (   )")
    console.print("   | |")
    console.print("  _| |_")
    console.print("  '---'")
    console.print("[bold]Ding![/bold]")
