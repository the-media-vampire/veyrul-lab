---
# FULL-EXAMPLE FORM
# Reflects the full example as written in the documentation page
# (art_01M6Q91BRD43K87VBTF37G6ASA r1, lines 94, 95, 97, 107, 110)
# Curator observation: prose and example differ; this is shown, not explained.
---

```mermaid
kanban
  [To Do]
    [Write tests]
  col2[In Progress]
    id3[Fix bug @{ assigned: bob, ticket: PROJ-2, priority: Very High }]
  [Done]
    id3[Deploy to staging]
```

# Notes:
# - Line 94: column written as [Title] with no identifier
# - Line 95: task written as [Description] with no identifier
# - Line 97: another column with no identifier
# - Lines 107 and 110: identifier id3 appears twice in the original example
#   (curator observation; the page calls identifiers unique at lines 29, 36, 44)
# - This form is shown as written; no claim is made that it renders correctly.