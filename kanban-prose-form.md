---
# PROSE FORM
# Follows the rules stated in prose (art_01M6Q91BRD43K87VBTF37G6ASA r1, lines 15, 21, 29, 36, 44)
# Every column and task has a unique identifier.
# Identifiers are unique as the prose requires (lines 29, 36, 44).
---

```mermaid
kanban
  col1[To Do]
    task1[Write tests]
    task2[Review PR @{ assigned: alice, ticket: PROJ-1, priority: High }]
  col2[In Progress]
    task3[Fix bug @{ assigned: bob, ticket: PROJ-2, priority: Very High }]
  col3[Done]
    task4[Deploy to staging]
```

# Notes:
# - Each column: unique id + [Title] (lines 15, 21)
# - Each task: indented, unique id + [Description] (lines 36, 44, 45)
# - Metadata: @{ key: value } with keys assigned, ticket, priority (lines 55, 59-61)
# - Four priority values: Very High, High, Low, Very Low (line 61)