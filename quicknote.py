#!/usr/bin/env python3
"""Append a quick note to the most recent dated Markdown note in a folder."""

from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys


SETTINGS_FILE = Path(__file__).with_name("settings.json")
DATE_FORMATS = {
    "31-08-26": "%d-%m-%y",
    "2026-08-31": "%Y-%m-%d",
    "31-08-2026": "%d-%m-%Y",
}
EMPTY_SETTINGS = {"notes_path": "", "date_format": ""}


def run_menu(command):
    """Run an Omarchy or Zenity menu and return its selected text."""
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def load_settings():
    """Return saved settings, treating a missing or invalid file as empty."""
    if not SETTINGS_FILE.exists():
        return EMPTY_SETTINGS.copy()

    try:
        with SETTINGS_FILE.open(encoding="utf-8") as file:
            settings = json.load(file)
    except (json.JSONDecodeError, OSError):
        return EMPTY_SETTINGS.copy()

    if not isinstance(settings, dict):
        return EMPTY_SETTINGS.copy()

    return {**EMPTY_SETTINGS, **settings}


def save_settings(settings):
    """Write settings as readable JSON."""
    with SETTINGS_FILE.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)
        file.write("\n")


def settings_are_complete(settings):
    return bool(settings["notes_path"]) and settings["date_format"] in DATE_FORMATS.values()


def configure_settings(settings):
    """Let the user choose a notes folder and a filename date format."""
    save_settings(settings)

    while True:
        choice = run_menu([
            "omarchy", "menu", "select", "Quicknote instellingen",
            "Notitiemap kiezen",
            "Datumformaat kiezen",
            "Opslaan en sluiten",
        ])

        if choice is None or choice == "Opslaan en sluiten":
            return settings

        if choice == "Notitiemap kiezen":
            folder = run_menu([
                "zenity", "--file-selection", "--directory",
                "--title=Kies Quicknote-map",
            ])
            if folder:
                settings["notes_path"] = folder
                save_settings(settings)

        if choice == "Datumformaat kiezen":
            label = run_menu([
                "omarchy", "menu", "select", "Datumformaat",
                *DATE_FORMATS.keys(),
            ])
            if label:
                settings["date_format"] = DATE_FORMATS[label]
                save_settings(settings)


def find_or_create_latest_note(notes_folder, date_format):
    """Find the newest dated Markdown file or create one for today."""
    dated_files = []

    for file in notes_folder.glob("*.md"):
        try:
            datetime.strptime(file.stem, date_format)
            dated_files.append(file)
        except ValueError:
            continue

    if dated_files:
        return max(
            dated_files,
            key=lambda file: datetime.strptime(file.stem, date_format),
        )

    return notes_folder / datetime.now().strftime(date_format + ".md")


def main():
    settings = load_settings()

    if "--settings" in sys.argv or not settings_are_complete(settings):
        settings = configure_settings(settings)

    if not settings_are_complete(settings):
        print("Quicknote is nog niet ingesteld.")
        return

    notes_folder = Path(settings["notes_path"]).expanduser()
    if not notes_folder.is_dir():
        print("De gekozen notitiemap bestaat niet.")
        return

    latest_file = find_or_create_latest_note(notes_folder, settings["date_format"])
    latest_file.touch(exist_ok=True)

    quicknote = run_menu(["omarchy", "menu", "input", "Quicknote"])
    if not quicknote:
        return

    time = datetime.now().strftime("%H:%M")
    with latest_file.open("a", encoding="utf-8") as file:
        file.write(f"\n- {time} — {quicknote}\n")


if __name__ == "__main__":
    main()
