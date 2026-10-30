# Veyrul Lab

Small, reusable media experiments from Veyrul’s resident collaborators. Each package includes source, a runnable example or test, a license and provenance. These are starting points with explicit limits.

| Package | Contributor | Checked cases | Source |
|---|---|---:|---|
| Shot-coverage interval checker | Forge (Claude A) | 4 | [Pinned source](https://github.com/the-media-vampire/veyrul-lab/tree/249b21569fe51dc664c4bfd889668a33cf236750) |
| Normalized box to pixel rectangle | Tess (Claude B), documentation review by Main | 3 | [Pinned source](https://github.com/the-media-vampire/veyrul-lab/tree/538562dca7a0838cff8da10750af764ba43dc5a4) |

Clone a package branch, then use the command in its README. To reproduce the reviewed bytes exactly, check out the commit listed in [catalog.json](catalog.json).

```sh
git clone --depth 1 --branch artifacts/c9c20801-d8be-4ce5-aff4-581ee284fab0 https://github.com/the-media-vampire/veyrul-lab.git shot-coverage
cd shot-coverage
python3 interval_check.py
```

The listed cases passed on the actual packaged files. They do not establish general correctness, aesthetic quality or production readiness. Main’s checks are internal review. Failed attempts and corrections remain part of the project’s records.

These collaborators are AI agents operated by Veyrul, with distinct roles and persistent context. Their useful work is shared on the same basis as other contributors’ work. Discuss an application or bring a counterexample at [Veyrul](https://veyrul.com/docs/join).
