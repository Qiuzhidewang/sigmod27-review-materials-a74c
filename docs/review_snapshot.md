# Anonymous review snapshot

This snapshot contains the implementation, frozen data, saved model outputs,
case-level results, and reproduction tools used for the reported experiments.

The export replaces historical workstation paths with a neutral path and
anonymizes the author name in this project's MIT notice. The license terms are
unchanged. Third-party names and citations are retained.

File and protocol digests that depend on the redacted provenance were recomputed
for this snapshot. These are review-snapshot checksums, not a claim that the
redacted files have the byte hashes of the original development records.
Source code, numeric data, candidate packets, model outputs, predictions, and
metric definitions are unchanged. The historical source archive is unchanged.

The root README describes offline verification and fresh deterministic refitting
with exact saved LLM-response replay. No new LLM requests are made by these
commands. Download all repository files before running the commands locally.

Large records are distributed as gzip files because the review host limits file
size. `restore_artifact_files.py` reconstructs their exact bytes and validates
both compressed and uncompressed checksums. Run it before the reproduction
commands. `MANIFEST.sha256` describes the downloadable files; `PACKED_FILES.json`
also records the hashes of the restored records.
