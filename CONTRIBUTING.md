For setup and general usage, see [README.md](README.md).

## Standards and Guide
Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) as a guideline when making pull requests.

## Running tests

Run tests from the project root (so pytest finds `pytest.ini` and the `tests/` directory):

```bash
pytest
```

To skip integration tests (e.g. those that use the network):

```bash
pytest -m "not integration"
```

## Pull requests

- Open PRs against `main`. Ensure tests pass locally by running `pytest` before submitting.

## Reporting issues

Open an issue for bugs or feature ideas; check existing issues first to avoid duplicates.
