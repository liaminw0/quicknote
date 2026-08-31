# Quicknote

A small Python utility for Omarchy that appends a quick note to the newest dated Markdown file in a chosen folder.

## Requirements

- Python 3
- Omarchy, for `omarchy menu input` and `omarchy menu select`
- Zenity, for the folder picker

## Use

Run `python quicknote.py` to add a note. On the first run, Quicknote creates `settings.json` and opens its settings menu. Choose a notes folder, choose the filename date format, and select **Save and close**.

Run `python quicknote.py --settings` at any time to change those settings.

## Suggested Omarchy bindings

Add these to `~/.config/hypr/bindings.lua`, adjusting the script path if necessary:

```lua
o.bind("SUPER + N", "Quicknote", "python /path/to/quicknote.py")
o.bind("SUPER + ALT + N", "Quicknote settings", "python /path/to/quicknote.py --settings")
```

After saving, run `hyprctl reload` and then `hyprctl configerrors`.

## Filename formats

Quicknote supports these dated filename formats:

- `31-08-26`
- `2026-08-31`
- `31-08-2026`

If no dated Markdown file exists in the selected folder, it creates today’s file using the selected format.
