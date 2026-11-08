# TextGen GGUF — Contributor Brief

Source: art_01M6WM52ZBRBMS22NHSN9JW7YA revision 1 (documentary, not run).
TextGen commit c93f8871, README read 2026-11-07.

---

## What the gap actually is

Every step in the article is *expected*, not observed. No one has run
the install. The clearest single contribution is a first run report.

---

## Three entry points, ranked by resource cost

### 1. Portable build — lowest cost (~15 min, no Python needed)

**Who this suits:** anyone with Windows, macOS or Linux and a GPU or CPU.

1. Download the portable build for your hardware from the TextGen releases page.
   Hardware options: CUDA (NVIDIA), Vulkan (AMD/Intel), ROCm (AMD Linux), CPU-only.
2. Unzip. Double-click `textgen`.
3. Drop a GGUF model file into `user_data/models/`.
4. Report back:
   - OS and hardware option chosen
   - Whether the UI opened
   - Whether the GGUF file appeared in the model list without extra config
   - Any error, verbatim

That four-point report upgrades the evidence status from `not_run` to observed.

### 2. Manual venv install — medium cost (~30 min, Python 3.9+ and git required)

Commands from the article (untested):

```
git clone <repository address from the README>
cd textgen
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements/portable/requirements.txt --upgrade
python server.py --portable --api --auto-launch
```

After launch, test the CMD_FLAGS.txt startup:

```
--model my-model.gguf
--cache-type q8_0
```

Report: did `--auto-launch` open a browser tab? Did `--api` enable an
API endpoint? The article does not state the port; note whatever you observe.

### 3. API compatibility check — requires a working install first

With `--api` set, TextGen advertises OpenAI/Anthropic-style endpoints.
A contributor with an existing local client (e.g. a script already
calling the OpenAI SDK) can point it at the local server and report
whether requests succeed without code changes.

---

## Attribution obligations before you use this

TextGen is AGPL v3 (LICENSE file confirmed at commit c93f8871).
AGPL v3 key obligation: if you *distribute* a modified version or run
it as a network service others access, you must make your source
available. Running it locally for yourself does not trigger that.
The article flags this but does not assess it further; check the
licence before deploying to a team server.

---

## Known limits of the article (do not re-derive these)

- No memory or speed figures were read; size-fit guidance is absent.
- Multi-file model folders need the full install, not the portable build.
- The flag reference, Conda, Docker, extensions and wiki were not read.
- API port and address are not stated in the article.
- Model licences are not assessed.

---

## Sharpest open research question

**Does the portable build handle GGUF files above ~8 GB on systems
with less VRAM than the model requires?** The README gave no memory
figures in the sections read. A contributor with a mid-range GPU
(e.g. 8 GB VRAM) and a 13B Q4 model (~7 GB) could answer this in one
session. Stopping condition: model loads, errors out, or the UI gives
a clear message. Report the GPU, VRAM, model size and quant level.