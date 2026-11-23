# picolibc-bsd

A redistribution of [picolibc](https://github.com/picolibc/picolibc) with all copyleft-licensed
files removed.

See the [upstream README](README.upstream.md) for picolibc documentation.

## Why this fork exists

Picolibc is a lightweight C library for embedded systems. The core library sources are permissively
licensed (BSD-3-Clause and similar), but the upstream repository includes a small number of
copyleft-licensed files:

- `test/` directory - GPLv2+ test suite files
- `scripts/GeneratePicolibcCrossFile.sh` - AGPLv3+ build helper
- `COPYING.GPL2` - GPL license text

These files are not needed to build or use picolibc, but their presence in git history can
complicate license compliance for projects that vendor picolibc as a submodule or dependency.

This fork provides a clean tree containing only permissively-licensed files, suitable for embedding
without copyleft concerns.

## History structure

The first commit is the upstream picolibc source at the base version tag with copyleft files
excluded. The second commit adds fork tooling. Future upstream updates are cherry-picked one commit
at a time with copyleft files filtered, preserving individual commit granularity.

## Updating from upstream

Updates can be triggered manually via the
[Update from Upstream](.github/workflows/update-upstream.yml) GitHub Actions workflow, which takes
an upstream release tag (e.g., `1.9.0`), branch, or commit (e.g., `ff59ec82f`) as input. The
workflow:

1. Detects the current base version from the nearest `*-bsd` tag on `main`
2. Runs `scripts/import-upstream.sh` to cherry-pick upstream commits with copyleft files filtered
   out
3. Opens a PR for review
4. On merge, a `<version>-bsd` tag and GitHub release are created automatically

The importer preserves `.github/workflows/` from this fork; upstream workflow changes are listed in
`UPSTREAM_EXCLUSIONS` and are not imported.

### Snapshot versions

Upstream commits that are not tagged releases are named relative to the nearest earlier release
with `git describe`, e.g., `1.8.12-274-gff59ec82fce7` (274 commits after `1.8.12`, at upstream
commit `ff59ec82fce7`). The name is used for the update branch and the `-bsd` tag, and Git resolves
it back to the same upstream commit for the next import. To print the name for an upstream ref:

```bash
scripts/import-upstream.sh --describe <upstream-ref>
```

### Manual import

To import locally instead of using the workflow:

```bash
from=$(git describe --tags --abbrev=0 --match '*-bsd' HEAD)
to=$(scripts/import-upstream.sh --describe <upstream-ref>)
scripts/import-upstream.sh "${from%-bsd}" "$to"
```

After importing, tag the result and push:

```bash
git tag "${to}-bsd"
git push origin main "${to}-bsd"
```

## License scanning

This repository uses [scancode-toolkit](https://github.com/aboutcode-org/scancode-toolkit) in CI to
verify that no copyleft-licensed files are present. See `.github/workflows/license-check.yml`.

## License

All source code files in this repository are under permissive licenses (BSD-3-Clause, BSD-2-Clause,
MIT, ISC, and similar). The `COPYING.picolibc` file contains a license inventory that references
copyleft licenses for documentation purposes - those files have been removed from the tree. See
`COPYING.picolibc` for per-file license details.

## Attribution

picolibc is created and maintained by Keith Packard and contributors. See the
[upstream repository](https://github.com/picolibc/picolibc) for full contributor history.
