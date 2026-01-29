# idb Command Reference

Complete reference for all idb commands and options.

## Table of Contents

1. [Target Management](#target-management)
2. [App Lifecycle](#app-lifecycle)
3. [File System](#file-system)
4. [Testing](#testing)
5. [UI Automation](#ui-automation)
6. [Media Capture](#media-capture)
7. [Logs and Diagnostics](#logs-and-diagnostics)
8. [System Configuration](#system-configuration)
9. [Companion Management](#companion-management)
10. [Troubleshooting](#troubleshooting)

---

## Target Management

### list-targets

List available simulators and devices.

```bash
idb list-targets [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--state <STATE>` | Filter by state: `booted`, `shutdown`, `creating`, `unknown` |
| `--json` | Output as JSON |

### boot

Boot a simulator.

```bash
idb boot <UDID> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--headless` | Boot without UI window |
| `--direct-companion-launch` | Launch companion alongside boot |

### shutdown

Shutdown a booted simulator.

```bash
idb shutdown <UDID>
```

### erase

Erase all content and settings from a simulator.

```bash
idb erase <UDID>
```

### create

Create a new simulator.

```bash
idb create <NAME> <DEVICE_TYPE> <OS_VERSION>
```

**Device Types** (examples):
- `com.apple.CoreSimulator.SimDeviceType.iPhone-15`
- `com.apple.CoreSimulator.SimDeviceType.iPhone-15-Pro-Max`
- `com.apple.CoreSimulator.SimDeviceType.iPad-Pro-12-9-inch-6th-generation`

**OS Versions** (examples):
- `com.apple.CoreSimulator.SimRuntime.iOS-17-0`
- `com.apple.CoreSimulator.SimRuntime.iOS-16-4`

### delete

Delete a simulator.

```bash
idb delete <UDID>
# or delete all unavailable simulators
idb delete-all unavailable
```

### clone

Clone an existing simulator.

```bash
idb clone <UDID> --new-name "Cloned Simulator"
```

### focus

Bring simulator window to front.

```bash
idb focus [--udid <UDID>]
```

---

## App Lifecycle

### install

Install an application.

```bash
idb install <PATH> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--make-debuggable` | Enable debugging for release builds |
| `--skip-signing` | Skip code signing check |

Supports: `.app` bundles, `.ipa` files, `.xctest` bundles

### uninstall

Remove an installed application.

```bash
idb uninstall <BUNDLE_ID>
```

### list-apps

List installed applications.

```bash
idb list-apps [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |

Output includes: bundle ID, name, architecture, install type, process state, debuggable status.

### launch

Launch an application.

```bash
idb launch <BUNDLE_ID> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--args <ARGS>...` | Pass arguments to app |
| `--env <KEY=VALUE>...` | Set environment variables |
| `--foreground-if-running` | Bring to front if already running |
| `--wait-for` | Wait for app to launch before returning |
| `--wait-for-debugger` | Launch paused, waiting for debugger |

### terminate

Terminate a running application.

```bash
idb terminate <BUNDLE_ID>
```

---

## File System

### file push

Copy files to device/simulator.

```bash
idb file push <LOCAL_PATH> <BUNDLE_ID>/<CONTAINER_PATH> [OPTIONS]
```

**Container paths**:
- `<BUNDLE_ID>/Documents/` - App Documents directory
- `<BUNDLE_ID>/Library/` - App Library directory
- `<BUNDLE_ID>/tmp/` - App tmp directory
- `<BUNDLE_ID>/` - App bundle root (read-only)

| Option | Description |
|--------|-------------|
| `--bundle-id <ID>` | Alternative bundle ID specification |

### file pull

Copy files from device/simulator.

```bash
idb file pull <BUNDLE_ID>/<CONTAINER_PATH> <LOCAL_PATH>
```

### file ls

List directory contents.

```bash
idb file ls <BUNDLE_ID>/<CONTAINER_PATH>
```

### file rm

Remove files or directories.

```bash
idb file rm <BUNDLE_ID>/<CONTAINER_PATH>
```

### file mkdir

Create a directory.

```bash
idb file mkdir <BUNDLE_ID>/<CONTAINER_PATH>
```

### file move

Move/rename files within container.

```bash
idb file move <BUNDLE_ID>/<SRC_PATH> <BUNDLE_ID>/<DST_PATH>
```

---

## Testing

### xctest install

Install a test bundle.

```bash
idb xctest install <PATH>
```

Supports: `.xctestrun` files, `.xctest` bundles

### xctest list

List installed test bundles.

```bash
idb xctest list [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |

### xctest list-tests

List test methods in a bundle.

```bash
idb xctest list-tests <TEST_BUNDLE_ID>
```

### xctest run

Execute tests.

```bash
idb xctest run <MODE> <TEST_BUNDLE_ID> [OPTIONS]
```

**Modes**:
- `logic` - Unit tests without app
- `app` - Tests with host app
- `ui` - UI tests

| Option | Description |
|--------|-------------|
| `--app-bundle-id <ID>` | Host application bundle ID |
| `--tests <TEST>...` | Run specific tests (Class or Class/method) |
| `--tests-to-skip <TEST>...` | Skip specific tests |
| `--test-arguments <ARG>...` | Pass arguments to test process |
| `--env <KEY=VALUE>...` | Environment variables for tests |
| `--timeout <SECONDS>` | Test timeout |
| `--report-activities` | Include activity reporting |
| `--report-attachments` | Include test attachments |
| `--coverage` | Enable code coverage |
| `--json` | Output results as JSON |

**Examples**:

```bash
# Run all tests
idb xctest run logic MyTests

# Run specific test class
idb xctest run logic MyTests --tests LoginTests

# Run specific test method
idb xctest run logic MyTests --tests LoginTests/testValidCredentials

# UI tests with app
idb xctest run ui MyUITests --app-bundle-id com.example.app

# With code coverage
idb xctest run logic MyTests --coverage --json > results.json
```

### xctest uninstall

Remove a test bundle.

```bash
idb xctest uninstall <TEST_BUNDLE_ID>
```

---

## UI Automation

### ui describe-all

Get full UI accessibility tree with element coordinates.

```bash
idb ui describe-all [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--nested` | Nested output format |
| `--json` | Output as JSON |

**Key fields in output**:
- `AXFrame`: `{{x, y}, {width, height}}` - element position/size
- `AXLabel`: Text label
- `AXUniqueId`: testID if set
- `type`: Element type (Button, StaticText, etc.)
- `enabled`: Whether interactive

### ui describe-point

Describe element at coordinates.

```bash
idb ui describe-point <X> <Y>
```

### ui tap

Simulate tap at coordinates.

```bash
idb ui tap <X> <Y> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--duration <SECONDS>` | Hold duration for long press |

### ui swipe

Simulate swipe gesture.

```bash
idb ui swipe <X_START> <Y_START> <X_END> <Y_END> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--duration <SECONDS>` | Swipe duration |
| `--delta <PIXELS>` | Intermediate steps delta |

### ui text

Type text string.

```bash
idb ui text "<TEXT>"
```

### ui button

Press hardware button.

```bash
idb ui button <BUTTON>
```

**Buttons**: `HOME`, `LOCK`, `SIDE_BUTTON`, `SIRI`, `APPLE_PAY`

### ui key

Send key event.

```bash
idb ui key <KEY_CODE>
```

### ui key-sequence

Send multiple key events.

```bash
idb ui key-sequence <KEY_CODE>...
```

---

## Media Capture

### screenshot

Capture screen image.

```bash
idb screenshot <OUTPUT_PATH> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--type <FORMAT>` | Output format: `png`, `tiff`, `bmp`, `gif`, `jpeg` |

### record-video

Record screen video.

```bash
idb record-video <OUTPUT_PATH> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--codec <CODEC>` | Video codec: `h264`, `hevc`, `minih264` |
| `--fps <FPS>` | Frames per second |

Press `Ctrl+C` to stop recording.

### add-media

Add photos/videos to media library.

```bash
idb add-media <FILE_PATH>...
```

Supports: JPEG, PNG, GIF, MOV, MP4

---

## Logs and Diagnostics

### log

Stream device/simulator logs.

```bash
idb log [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--predicate <PREDICATE>` | NSPredicate filter string |
| `--level <LEVEL>` | Minimum log level |
| `--source` | Include source info |

**Predicate Examples**:
```bash
idb log --predicate 'subsystem == "com.example.app"'
idb log --predicate 'process == "MyApp"'
idb log --predicate 'eventMessage contains "error"'
```

### crash list

List crash logs.

```bash
idb crash list [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--before <TIMESTAMP>` | Only crashes before time |
| `--since <TIMESTAMP>` | Only crashes after time |
| `--bundle-id <ID>` | Filter by bundle ID |
| `--json` | Output as JSON |

### crash show

Display crash log contents.

```bash
idb crash show <CRASH_NAME>
```

### crash delete

Delete crash logs.

```bash
idb crash delete <CRASH_NAME>
idb crash delete --all
idb crash delete --before <TIMESTAMP>
```

### instruments run

Run Instruments trace.

```bash
idb instruments run <TEMPLATE> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--output <PATH>` | Output trace file path |
| `--post-args <ARGS>...` | Arguments after template |

---

## System Configuration

### set-location

Set device location.

```bash
idb set-location <LATITUDE> <LONGITUDE>
```

### clear-keychain

Clear all keychain data.

```bash
idb clear-keychain
```

### open

Open URL.

```bash
idb open <URL>
```

Supports `http://`, `https://`, custom URL schemes.

### approve

Grant app permissions.

```bash
idb approve <BUNDLE_ID> <PERMISSIONS>...
```

**Permissions**: `photos`, `camera`, `contacts`, `url`, `location`, `notification`, `microphone`

### revoke

Revoke app permissions.

```bash
idb revoke <BUNDLE_ID> <PERMISSIONS>...
```

### contacts update

Update contacts database.

```bash
idb contacts update <DB_PATH>
```

---

## Companion Management

### connect

Connect to a companion.

```bash
idb connect <HOST>:<PORT>
idb connect <UDID>
```

### disconnect

Disconnect from a companion.

```bash
idb disconnect <UDID>
```

### daemon

Run idb as background daemon.

```bash
idb daemon [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--port <PORT>` | Listen port |
| `--grpc-port <PORT>` | gRPC port |
| `--notifier-path <PATH>` | Path to notifier binary |

### kill

Kill the companion for a target.

```bash
idb kill
```

---

## Global Options

These options work with most commands:

| Option | Description |
|--------|-------------|
| `--udid <UDID>` | Target device/simulator UDID |
| `--log <LEVEL>` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `--json` | Output as JSON (where supported) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `IDB_UDID` | Default target UDID |
| `IDB_COMPANION` | Companion address (host:port) |
| `IDB_LOG_LEVEL` | Default log level |

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Connection failed |
| 3 | Target not found |

---

## Troubleshooting

### Python 3.14+ Compatibility

idb uses deprecated `get_event_loop()` which fails on Python 3.14+. Workaround:

```bash
# Run idb through Python with manual event loop setup
/path/to/pipx/venvs/fb-idb/bin/python -c "
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
import sys
sys.argv = ['idb', 'ui', 'describe-all', '--udid', 'YOUR_UDID']
from idb.cli.main import main
main()
"
```

Find your pipx venv path: `pipx environment` or check `~/.local/pipx/venvs/fb-idb/bin/python`

### Must Connect Before UI Commands

UI commands require explicit connection:

```bash
# This fails without prior connect
idb ui describe-all --udid <UDID>  # Error!

# Connect first
idb connect <UDID>
idb ui describe-all --udid <UDID>  # Works
```

### Finding Simulator UDIDs

```bash
# List all available simulators
xcrun simctl list devices available | grep -E "(iPhone|iPad)"

# List booted simulators only
xcrun simctl list devices | grep Booted

# Or use idb
idb list-targets --state booted
```
