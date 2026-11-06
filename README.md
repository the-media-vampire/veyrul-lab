# Mermaid kanban syntax comparison snippets

Two labeled snippet files for testing Mermaid kanban diagram syntax:

| File | What it represents |
|---|---|
| `kanban-prose-form.md` | Follows the prose rules: unique identifier on every column and task |
| `kanban-example-form.md` | Follows the full example as written: some columns/tasks have no identifier; `id3` appears twice |

## How to use

1. Copy a snippet block into a live Mermaid renderer (e.g. https://mermaid.live, a VS Code Mermaid extension, or a Markdown preview that supports Mermaid).
2. Note which renderer version you used.
3. Record what renders and what does not — especially for the duplicate `id3` and the no-identifier forms.
4. Attribute any published result to `art_01M6Q91BRD43K87VBTF37G6ASA` r1 as the documentation baseline.

## What this does not do

- Makes no claim that either form renders correctly.
- Does not resolve the prose/example conflict — that is the open question.
- Does not cover configuration (`ticketBaseUrl`) or the grammar source.

## Source

art_01M6Q91BRD43K87VBTF37G6ASA revision 1 (Veyrul)
Mermaid kanban.md at commit c9b12739 (unpinned; fetched 2026-11-05 per article)
LICENSE line 1: The MIT License (MIT)