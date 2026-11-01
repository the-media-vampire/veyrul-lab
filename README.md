# C2PA attach-and-verify stage

Companion to **art_01M6AJ76STE4ZBNCDZFA84G2NK r1**.
Pinned refs: c2patool 767cc549, c2pa-rs 7eea357d, c2pa-python 5897963a, c2pa-js db335ea6.

## Interface

**Inputs:** `asset_path`, `manifest_def` (JSON), `signer_config` (JSON, no embedded keys), `output_path`, optional `trust_anchor`.

**Outputs:** `signed_asset` at `output_path` (exit 0 only); `manifest_report` JSON to stdout; non-zero exit blocks the asset.

## Key assumptions (from source docs)

1. **Keys**: never embed a private key in `signer_config` in production; use KMS/HSM (c2pa-python docs, same source).
2. **Format routing**: SDK resolves type from file extension; pass the correct extension (c2pa-rs docs).
3. **Fragmented MP4**: file-based Rust library only, not via c2patool subprocess.
4. **API stability**: c2pa-rs is 0.x; pin to a commit hash in your lock file.
5. **Node binding**: use `@contentauth/c2pa-node` from c2pa-js monorepo (Node >= 22); c2pa-node-v2 is archived.
6. **Trust list**: fetched over HTTP; its current membership was not verified in the source article.

## Failure codes

| Code | Cause | Action |
|---|---|---|
| `SIGN_FAIL` | Signer non-zero exit | Block; alert ops |
| `FORMAT_UNSUPPORTED` | Extension not in SDK table | Reject at intake |
| `TRUST_FAIL` | Cert not in trust list | Quarantine; reviewer |
| `NET_FAIL` | Trust list HTTP unreachable | Retry; fail-open with warning |
| `KEY_CONFIG_ERR` | Embedded key in prod config | Hard stop |

## Composability

This is a pure `asset → signed_asset` transform. Insert after any generation step that produces a supported file type. If a browser viewer (c2pa-web/Wasm) is also in the pipeline, its binary hosting is a separate interface point not covered here.

## Not executed

No code here has been installed or run. This is a documentary contract.