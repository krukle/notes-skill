# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/sticky-note.svg" card_color="#FEE255" width="50" height="50" style="vertical-align:bottom"/> Notes

Takes notes and adds them to the MMM-Notes MagicMirror module.

## Dependencies

```bash
mycroft-pip install sqlite3
git clone git@github.com:krukle/MMM-Notes.git ~/MagicMirror/modules/MMM-Notes
```

> **Note**
>
> Change git clone destination according to your setup.

## Installation

```bash
git clone git@github.com:krukle/notes-skill.git ~/mycroft-core/skills/notes-skill
```

## Messages

### Emitted

| Message | Data | About |
| ------- | ---- | ----- |
| NEW-POST | `{"post": (int:id, str:title, str:content)}` | Emitted when a post is created. |
| ALL-POSTS | `{"posts": list((int:id, str:title, str:content))}` | Emitted to send all posts to MagicMirror. |
| DELETE-POSTS | `{}` | Emitted when all posts are deleted. |
| DELETE-POST | `{"id": int:id}` | Emitted when a post with id; `id`, is deleted.

### Subscribed

| Message | About |
| ------- | ----- |
| notes-skill:get_all_posts | Received when all posts should be sent. |

## Commands

### Create note

| English | Swedish |
| ------- | ------- |
| "Create note" | "Skapa anteckning" |
| "Jot down that `note`" | "Skriv ned att `note`" |

If `note` is left blank, Mycroft will ask the user for the notes content.

### Delete note

| English | Swedish |
| ------- | ------- |
| "Delete note" | "Radera anteckning" |
| "Remove note `id`" | "Ta bort anteckning `id`" |

If `id` is left blank, Mycroft will ask the user for the notes `id`.

### Clear notepad

| English | Swedish |
| ------- | ------- |
| "Clear notepad" | "Rensa anteckningsblock" |
| "Erase all notes" | "Ta bort all anteckningar" |

## Database

The notes are hosted in a local sqlite database which is created in `~/mycroft-core/database/notes-skill/`.
