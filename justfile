# list available recipes
default:
    @just --list

# show the current version
version:
    @sed -n 's/^VERSION = "\(.*\)"$/\1/p' src/version.py

# release, commit and tag a new version (YEAR.MONTH.RELEASE); without argument the next one is computed
release version="":
    #!/usr/bin/env python3
    import re
    import subprocess
    import sys
    from datetime import datetime, timezone
    from pathlib import Path

    VERSION_FILE = Path('src/version.py')
    PYPROJECT = Path('pyproject.toml')
    CHANGELOG = Path('changelog.md')

    def fail(message):
        sys.exit(f'error: {message}')

    def git(*args):
        return subprocess.run(['git', *args], check=True, capture_output=True, text=True).stdout

    def parse(version):
        if not re.fullmatch(r'\d{4}\.\d{1,2}\.\d+', version):
            fail(f'version "{version}" is not in the form YEAR.MONTH.RELEASE')
        return tuple(int(part) for part in version.split('.'))

    # nothing else may end up in the release commit
    if git('status', '--porcelain', '--untracked-files=no'):
        fail('working tree has uncommitted changes; commit or stash them first')

    # current version
    source = VERSION_FILE.read_text()
    current = re.search(r'^VERSION = "(.+)"$', source, re.M).group(1)
    current_tuple = parse(current)

    # new version
    now = datetime.now(timezone.utc)
    new = '{{ version }}'
    if not new:
        year, month, release = current_tuple
        release = release + 1 if (year, month) == (now.year, now.month) else 1
        new = f'{now.year}.{now.month}.{release}'
    new_tuple = parse(new)
    if new_tuple <= current_tuple:
        fail(f'new version {new} must be greater than the current version {current}')
    if git('tag', '--list', new):
        fail(f'tag {new} already exists')

    # changelog must contain unreleased changes
    changelog = CHANGELOG.read_text()
    unreleased = re.search(r'^## \[Unreleased\]\n(.*?)(?=^## \[|^\[Unreleased\]:)', changelog, re.M | re.S)
    if unreleased is None:
        fail(f'section "## [Unreleased]" not found in {CHANGELOG}')
    if not re.search(r'^- ', unreleased.group(1), re.M):
        fail(f'section "## [Unreleased]" in {CHANGELOG} is empty, nothing to release')
    notes = unreleased.group(1).strip()

    # changelog: move unreleased changes under the new version and update links
    changelog = changelog.replace(
        '## [Unreleased]\n',
        f'## [Unreleased]\n\n\n## [{new}] - {now:%Y-%m-%d}\n',
        1,
    )
    link = re.search(r'^\[Unreleased\]: (.+)/compare/(.+)\.\.\.HEAD$', changelog, re.M)
    if link is None:
        fail(f'link "[Unreleased]: .../compare/<version>...HEAD" not found in {CHANGELOG}')
    repo, previous = link.groups()
    changelog = changelog.replace(
        link.group(0),
        f'[Unreleased]: {repo}/compare/{new}...HEAD\n'
        f'[{new}]: {repo}/compare/{previous}...{new}',
    )
    CHANGELOG.write_text(changelog)

    # src/version.py
    source = re.sub(r'^VERSION = ".*"$', f'VERSION = "{new}"', source, flags=re.M)
    source = re.sub(r'^VERSION_TUPLE = .*$', f'VERSION_TUPLE = {new_tuple}', source, flags=re.M)
    source = re.sub(r'^BUILD_DATE = ".*"$', f'BUILD_DATE = "{now:%Y-%m-%dT%H:%M:%SZ}"', source, flags=re.M)
    VERSION_FILE.write_text(source)

    # pyproject.toml
    pyproject = PYPROJECT.read_text()
    pyproject = re.sub(r'^version = ".*"$', f'version = "{new}"', pyproject, count=1, flags=re.M)
    PYPROJECT.write_text(pyproject)

    # uv.lock
    subprocess.run(['uv', 'lock', '--quiet'], check=True)

    # commit only the release files and tag the commit
    files = [str(CHANGELOG), str(PYPROJECT), str(VERSION_FILE)]
    if git('ls-files', 'uv.lock'):
        files.append('uv.lock')
    git('add', *files)
    git('commit', '--quiet', '-m', f'release {new}')
    git('tag', '--annotate', '--cleanup=verbatim', new, '-m', f'Release {new}\n\n{notes}')

    print(f'Released {current} -> {new} (commit and tag {new} created)')
    print('Publish it with:')
    print('  git push --follow-tags')
