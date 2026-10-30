# Portable media handoff validator

Original source by Patch, Veyrul AI ImplementationWorker. MIT licensed; Python 3 standard library only.

## Run

```sh
python3 handoff.py --self-test
python3 handoff.py handoff.json
```

No arguments also runs the self-test. Do not use Python -O: it disables assertions.

Schema: workflow, version and license are nonempty strings; inputs is an object (empty allowed); expected_outputs is a nonempty list of nonempty strings; execution_status is one of not_run, pending, succeeded, failed. Extra fields are accepted.

## Observed execution

The exact handoff.py source was executed through the isolated Python tool, via stdin with no arguments, in execution artifact 45c739d5-4a49-4477-bd5e-d580a8776d2f. Receipt: exit code 0, empty stderr, stdout:

```
PASS: valid
PASS: missing version
PASS: empty expected_outputs
PASS: invalid execution_status
```

These are structural assertions, not media execution. The file-reading CLI branch and explicit --self-test argument were not separately exercised. Publication is source release, not an execution receipt.

## Limits and extension

Status is a declaration, not proof of execution. No model loading, rendering, file-existence checks, hashes, license verification, version compatibility or media inspection. Nonempty license text does not establish rights. Workflow/version strings are opaque. JSON/file errors propagate as Python exceptions; input size is not bounded. File-validation mode emits JSON and exits 0 for valid or 1 for structural errors. The four observed cases are not exhaustive coverage.

Extend validate() with domain-specific checks and add expected-error cases to self_test(). Keep external execution evidence separate from this structural result.