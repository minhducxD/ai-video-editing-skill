---
name: video-editing-starter
description: Prepare and edit local narrated or talking-head videos with source-backed cuts, readable supporting visuals, faithful captions and an inspectable MP4 handoff. Use for footage-to-edit work and targeted revisions, not synthetic presenter creation or automatic publishing.
---

# Video editing starter

Work from the owner's actual recordings and goal. This is a reusable editing framework, not a bundled production engine. Inspect the tools available in the current environment; do not claim that an agent, renderer, transcript service or asset library is installed because this skill mentions it.

## Enter at the current stage

Read the current plan, edit decisions and handoff before changing an existing edit. Preserve authored changes and corrected captions. For new footage, identify the intended viewer, language, useful outcome and destination. Infer routine choices from the material; ask only about an unknown that could change the edit substantially.

Keep original recordings immutable. Work in a separate project and record source hashes or verified copies. Snapshot the current edit and its important notes before a consequential revision. Do not restart an automated pipeline over manual work without checking what it replaces.

Use [the small episode plan](templates/episode-plan.md) when a shared record would help. Keep it brief; do not fill a workbook for a simple cut. The [inventory helper](scripts/media_inventory.py) can record local metadata and hashes without modifying the source files.

## Check the speech before committing

Inspect the full supplied source and relevant screen evidence where possible. A transcript is a search aid, not proof of every word or visible action. Prefer one suitable transcription pass; revisit only uncertain material passages rather than automatically running several models on everything. Disclose missing audio, unreadable details and sampling limits. External audio transfer requires the owner's authorisation.

Compare the actual spoken explanation with its title, opening promise, example and ending. Distinguish a genuine contradiction, an unsupported claim, an absent demonstration and ordinary conversational grammar. Do not invent an error merely to justify a revision.

If a truthful, understandable cut resolves the issue, use it. If an essential problem needs a new take, stop the dependent edit and identify the exact file/range, what is wrong and a short proposed pickup. Continue useful independent preparation. A promised download or link is a before-publication dependency until it exists; never fabricate it.

The recorded wording governs the edit. Do not force an older script onto a changed recording, or replace spoken facts with different words in subtitles. A clearly labelled on-screen qualification is separate from the captions.

## Make a coherent first cut

Choose the smallest structure that fulfils the promise. Keep useful examples, qualifications and time to look at the screen. Do not treat every pause, repetition or filler as disposable. Cut complete thoughts at sensible boundaries and keep a source-to-edit record.

Use the available editing tools to make an actual preview. Review a representative integrated sequence before scaling a new layout or rendering a complicated full episode. Give the owner a concrete result to react to; instructions alone are not an edited video.

## Give the visuals a job

Choose the visual identity from the current subject, footage and any supplied references. Check suitable templates before inventing a new layout when a template would help. Inspect the actual preview, not just its name, and record an inaccessible preview honestly. Adapt a coherent template; custom graphics fill a real explanatory gap.

Use authentic screen evidence for app or result claims. Label diagrams and illustrative examples so they are not mistaken for real app progress, historical prompts or newly executed runs. Keep the presenter readable and use full camera, inset or full-screen material according to what the viewer needs at that moment.

Public creator references can inform pacing, composition or explanation. Build an original treatment using permitted assets; do not reuse someone else's footage, logos, artwork or audio merely because it was a reference. Keep source and licence information with any third-party material selected for the edit.

## Bind the edit to the voice

Attach each meaningful reveal to a recorded phrase, including its entrance time, first readable state and useful hold. Exact edited timings belong in one [cue map](templates/cue-map.csv), linked to the current edit revision. Recheck affected cues after changing cuts. Script estimates and broad ASR segments are not final sync evidence.

Captions follow the retained recording. Check names, numbers and technical terms using source context; do not silently rewrite grammar or invent speech. For a portrait derivative, reframe deliberately, check moving head/hand positions and keep important text away from likely interface overlays. Do not stretch a landscape frame into portrait.

Keep narration independently adjustable. Music and sound effects are optional; select them only when they help and their use is permitted. Do not infer what a sound is, or that a mix is good, from a filename, waveform or transcript.

## Render, inspect and hand off

Export the requested dimensions/frame rate and preserve editable sources, edit decisions and assets. Inspect the actual export, including cuts, meaningful visual changes, reading holds and audio transitions. Repair observed defects and recheck the affected regions.

The [export helper](scripts/check_export.py) can check decoding, requested dimensions/fps and SRT timing bounds. Those checks do not establish natural speech, correct captions, good design or intelligible audio. Record technical, visual, linguistic and listening coverage separately. Never claim a full watch-through or listening pass from sampled frames or machine QC.

Use [the handoff template](templates/handoff.md) to name the current MP4/captions, editable sources, source-to-edit map, actual review scope and remaining issues. For revisions, change the relevant part without undoing unrelated accepted work. Publishing, installing tools, spending money or sharing media is outside this skill unless the owner separately authorises it.
