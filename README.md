# AI video editing starter

A reusable skill for editing narrated videos with an AI agent. Give the agent your footage, a clear outcome and access to media tools. It inspects the speech, makes an edit, and helps you review specific changes.

This is the **framework I refer to in my video**. It contains the editing instructions, small project templates and two local checking helpers. My media, reference and sound libraries, portraits, private configuration and complete production pipeline are not included.

## What it does

The skill guides an agent through:

1. Checking the supplied recordings and what the speaker actually says.
2. Flagging real contradictions or missing explanations before committing to an edit.
3. Planning a coherent cut while preserving the original files.
4. Choosing a visual direction from suitable templates and references.
5. Timing useful graphics and captions to the retained speech.
6. Exporting and checking the actual video, with an honest handoff.

It also supports targeted feedback: “keep this explanation,” “change the layout here,” or “bring this graphic closer to this phrase.”

## What you need

- An AI agent that can read local files and run media tools, and a way for it to load skills.
- Your own recordings and any screen captures or other media needed to support your claims.
- FFmpeg and ffprobe for media work. Python 3.10+ is needed only for the included checking helpers.
- A transcription tool when the agent needs a transcript. None is bundled. Use a local option or authorise any external transcription and its cost yourself.
- A graphics tool if the edit needs it. [HyperFrames](https://github.com/heygen-com/hyperframes) is one option; it is not bundled or installed automatically.

**This skill is instructions, not a standalone video editor or a one-click installer.** It does not supply a renderer, agent subscription, model access, connectors or an asset library. Your agent must use the tools available in your environment. It should tell you when a required capability is missing rather than pretend it ran.

## Use the skill

The skill folder is [`skills/video-editing-starter`](skills/video-editing-starter). Install or copy that entire folder using your agent's normal skill-loading procedure. Keep its `SKILL.md`, templates and scripts together. The folder name and the skill name are both `video-editing-starter`.

If your agent has a skill installer, ask it:

> Install the video-editing-starter skill from the skills/video-editing-starter folder in this repository.

Then try a request such as:

> Use the video-editing-starter skill to edit the recordings in my footage folder. Make a clear overview of my workflow. Check the full spoken content first. If a genuine contradiction needs a new take, tell me the exact passage and proposed replacement; otherwise proceed with a faithful edit. Keep my originals and provide the MP4, captions, edit decisions and review notes.

Specify language, destination and format when they matter. For a portrait short, say which moment or takeaway should stand on its own. A short does not have to be a compressed copy of the whole long video.

## Start with a small example

Let the agent prepare an outline and a short representative sequence before rendering a complicated full edit. Once it works, use it as a reference for the rest. Keep the instructions and your own approved examples with the project so the next revision has something concrete to follow.

For visual direction, you can point to a suitable template, including the [HyperFrames catalog](https://www.hyperframes.dev/?view=catalog), or to a public creator example. Study the structure, pacing or explanation. Recreate the technique with your own words and permitted assets; a reference is not permission to reuse someone else's footage, artwork or sound.

## Included files

| File | Purpose |
| --- | --- |
| [`SKILL.md`](skills/video-editing-starter/SKILL.md) | Instructions loaded by the agent |
| [`episode-plan.md`](skills/video-editing-starter/templates/episode-plan.md) | Small shared plan and content gate |
| [`cue-map.csv`](skills/video-editing-starter/templates/cue-map.csv) | Source-to-edit and phrase-to-visual mapping |
| [`handoff.md`](skills/video-editing-starter/templates/handoff.md) | Deliverables, evidence, review coverage and open issues |
| [`media_inventory.py`](skills/video-editing-starter/scripts/media_inventory.py) | Read-only media metadata and source hashes |
| [`check_export.py`](skills/video-editing-starter/scripts/check_export.py) | Decode, optional dimension/fps and SRT timing checks |

Run the helpers from a local checkout, for example:

```text
python skills/video-editing-starter/scripts/media_inventory.py ./footage --out ./inventory.json
python skills/video-editing-starter/scripts/check_export.py ./final.mp4 --srt ./final.srt --width 1920 --height 1080
```

They inspect files; they do not choose cuts or render an edit. Technical checks do not establish accurate captions, good pacing, intelligible sound or factual correctness. The agent should keep technical, visual, language and listening review separate.

## Build your own library

Keep your own approved examples, source links and licence records in a separate local folder. Add material deliberately as you need it. You do not need my library, and this repository does not fetch or redistribute one.

Generated footage, transcripts and exports should stay outside this repository. The `.gitignore` excludes common media, project, cache and secret-file locations. Inspect what you stage before you publish your own changes.

## Scope and licence

The framework and original helper code are shared under the [MIT licence](LICENSE). That licence does not cover third-party tools, templates or media you choose to use. Nothing in the skill grants permission to upload recordings, spend money, publish videos or change accounts.

To run the small local helper checks, use `python -m unittest discover -s tests -v`. The tests need FFmpeg and ffprobe.
