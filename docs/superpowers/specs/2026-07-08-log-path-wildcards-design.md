# Design: wildcard-aware `log_path`

**Date:** 2026-07-08
**File:** `ab_utils/smk.py`

## Problem

Snakemake requires a rule's `log:` path to contain the same `{wildcard}`
placeholders as its outputs. `log_path` currently returns a fixed path, so it
cannot be used on rules with wildcards.

## Design

Change the signature to accept explicit wildcard names as varargs:

```python
def log_path(script: str, snakefile: str, *wildcards: str) -> str
```

Each wildcard name is appended after the script stem as a literal brace
placeholder for Snakemake to fill in, joined with underscores, in the order
given:

```
log/{dot_path}.{timestamp}.{script_stem}_{sample}_{chrom}.log
```

Usage from a Snakefile:

```python
rule align:
    output: "results/{sample}/{chrom}.bam"
    log: log_path("scripts/align.py", workflow.snakefile, "sample", "chrom")
```

## Behaviour

- With no wildcards passed, the output is identical to today (fully backward
  compatible).
- No validation of wildcard names beyond what Snakemake itself performs; it
  errors clearly on placeholders that do not match the rule's wildcards.

## Testing

No existing tests cover `log_path` and there are no in-repo callers. Verify
with an inline check that the returned string contains the expected
`{sample}`-style placeholders and that the zero-wildcard form is unchanged.
