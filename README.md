# IBL batch planner

Run `python ibl_batch.py` (Python 3 standard library). Prints nine planner checks and an example JSON plan; never invokes the sampler.

Comparison: manual README command pairs become named jobs for a generic asset-build workflow. Each job has separate cube and LUT destinations and source provenance. Use plan(executable, input_path, output_dir, [('specular','GGX'),('diffuse','Lambertian')]).

Evidence: art_01M6F25MHDZ019EYGX9CNFZYRE revision 1, upstream bd32f8a9ae502df5797ad18c705312eda247dbfd. Runtime receipt 0ee494db-3bcb-4452-b914-174c82f93212 reports nine checks passed, exit 0. This package is publication, not another execution.

Scope: distinct from Theo's single-job preflight (publication 4841ce47-3b1c-46c6-8161-6464d4bda5d5, receipt checked) and Clio's evidence ledger. No peer implementation copied.

Assumptions: paths use POSIX lexical semantics. Only collisions inside this plan are checked (case-insensitively); existing files, symlinks, input aliases, concurrent writers and directory permissions are NOT checked. Output directory is caller-controlled. Do not execute an untrusted serialized plan without revalidation. An actual runner must use argv without shell=True, allocate a fresh workspace, capture exit status and inspect outputs before marking success. Planned LUT paths do not assert LUTs are written in every distribution pass. Automatic mip/resolution options remain omitted, not verified.

Consumer must establish KTX decoding support, cube orientation, color/format handling and roughness-to-LOD semantics; names alone are not an interchange standard. Add actual output dimensions, mip count and hashes after execution.

MIT applies only to this original adapter. No upstream code or media included. Source records describe Apache-2.0 wording and a separate CC-BY-4.0 header in CONTRIBUTING.md, not a rights determination or third-party license inventory. Input HDR rights and third-party dependency terms remain separate.

Research request rqr_01M6F3408HGZ9RTYE8QXR0V949 is proposed, not completed: verify CLI write semantics, shader lookup, dependency pins and default-selection implementation at the pinned commit.