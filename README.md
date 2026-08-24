# Pilot Checklists (`pilot-checklists`)

Aviation-type checklist generator, runner, and card rendering engine based on commercial airline Quick Reference Handbooks (QRH / FCOM), NASA human factors engineering (Degani & Wiener), and strict Challenge-Response protocols.

Designed to eliminate cognitive overload, prevent task omission errors, combat ADHD working memory drop-off, and guarantee flawless execution under stress or fatigue.

---

## Why Standard To-Do Lists Fail

Standard to-do lists are passive, unstructured memory prompts. When humans are tired, distracted, or operating under time pressure, passive lists induce **habitual complacency**—items get checked off mentally without verifying the physical state.

Aviation checklists are **critical safety barriers** engineered around specific cognitive constraints:
1. **Challenge — Response:** Every item pairs an explicit cue with an observable target condition (`[CHALLENGE] ......... [RESPONSE]`). Vague items like "check" or "done" are banned.
2. **Operational Modes:**
   - **Do-Confirm (Do-Verify):** Operator executes a physical/tactile sweep from memory first, then opens the checklist card at a designated pause trigger to verify critical points.
   - **Read-and-Do:** For high-consequence, irreversible, or emergency workflows. Each step is read, executed, and confirmed before advancing.
3. **Killer Item Isolation (`[!]`):** Failure-critical points (e.g. fire hazards, locked doors, uncommitted secrets, battery limits) are isolated. Any interruption requires restarting from the last Killer Item.
4. **Miller's Law Chunking (5–9 Rule):** Checklists are chunked into chronological phases containing at most 5 to 7 items to prevent working memory drop-off.
5. **Defined Pause Points ("Hold Short" Lines):** Explicit physical or temporal triggers commanding when the checklist must be executed.
6. **Tactile Flow Patterns:** Spatial sweep instructions combined with point-and-call physical verification to overcome habit blindness.
7. **Standard Aviation Typography Rules:**
   - **Size:** Minimum 10 pt to 12 pt for paper checklists (character height ~0.14″ to 0.20″) to maintain readability under red night-lighting, vibration, or low-light conditions.
   - **Case:** Mixed case (Sentence or Title Case) for challenges and steps. ALL CAPS is strictly reserved for critical warnings, section headers, or emergency memory items.
   - **Weight Hierarchy:** Regular weight for the Challenge (the item being checked) and Bold for the Response (the required switch/lever state) to visually separate the two actions.

---

## Example Checklist Cards

### Leaving Home & Pre-Departure (`CHK-HOME`)

```text
+--------------------------------------------------------------------+
| LEAVING HOME & PRE-DEPARTURE                            [CHK-HOME] |
| MODE: DO-VERIFY  |  PAUSE TRIGGER: Hand on front door knob         |
+--------------------------------------------------------------------+
| TACTILE FLOW: Clockwise room sweep (Kitchen / Bed / Office / Hall) |
+--------------------------------------------------------------------+
| >> PHASE 1: FIRE & UTILITIES HAZARD SWEEP                          |
| [!] Stove & Oven ................... ZERO FLAME / KNOBS OFF / COLD |
| [ ] Coffee Maker & Kettle .................. UNPLUGGED / BASE COLD |
| [ ] Iron & Hair Tools ........................... UNPLUGGED & SAFE |
| [ ] Windows & Balcony ........................... CLOSED & LATCHED |
| [!] Faucets & Running Water ................ ZERO DRIP / FULLY OFF |
+--------------------------------------------------------------------+
| >> PHASE 2: DIGITAL & POWER SECURITY                               |
| [ ] Workstation Monitors ............................ LOCKED / OFF |
| [ ] Tailscale Remote Access .............. CONNECTED (PING PVE OK) |
| [ ] Phone Battery .................... MIN 50% OR POWERBANK PACKED |
+--------------------------------------------------------------------+
| >> PHASE 3: BODY & POCKET CROSS-CHECK (POINT & TOUCH)              |
| [!] Physical Keys (Home + Bike/Car) ...... TOUCHED IN RIGHT POCKET |
| [!] Wallet & ID / Payment Cards ........... TOUCHED IN LEFT POCKET |
| [!] Smartphone .................................. IN HAND / POCKET |
| [!] Front Door Lock .................... DEADBOLT ENGAGED / TESTED |
+--------------------------------------------------------------------+
| AVIATION SAFETY STANDARD  |  POINT & VERIFY  |  DO NOT GUESS       |
+--------------------------------------------------------------------+
```

### Software Release & Deployment Gate (`CHK-RELEASE`)

```text
+--------------------------------------------------------------------+
| SOFTWARE RELEASE & DEPLOYMENT VERIFICATION           [CHK-RELEASE] |
| MODE: DO-VERIFY  |  PAUSE TRIGGER: Prior to git push origin main / |
+--------------------------------------------------------------------+
| TACTILE FLOW: Source tree clean / Build / Test / Scan / Package    |
+--------------------------------------------------------------------+
| >> PHASE 1: WORKING TREE & CLEANLINESS                             |
| [!] GIT Working Tree .................... CLEAN (NO UNTRACKED/PYC) |
| [!] Secrets & API Keys ................. 0 IN CODE (.GITIGNORE OK) |
| [ ] Version & Changelog ....................... BUMPED IN MANIFEST |
+--------------------------------------------------------------------+
| >> PHASE 2: AUTOMATED QUALITY GATE                                 |
| [!] Test Suite (Cargo/Pytest) .......... PASS (0 FAILS / 0 ERRORS) |
| [ ] Linter & Typecheck ........................ CLEAN (0 WARNINGS) |
| [ ] Docs & Compiled Pdfs ....................... REBUILT & CURRENT |
+--------------------------------------------------------------------+
| >> PHASE 3: ROLLBACK PLAN & RELEASE HANDOFF                        |
| [!] Schema / Migrations ...................... TESTED & COMPATIBLE |
| [!] Rollback Commit SHA ...................... RECORDED & VERIFIED |
| [ ] TODO.MD / LOG.MD Sync .............. LOGGED UNDER TODAY'S DATE |
+--------------------------------------------------------------------+
| AVIATION SAFETY STANDARD  |  POINT & VERIFY  |  DO NOT GUESS       |
+--------------------------------------------------------------------+
```

---

## Installation & Quickstart

### 1. Direct Python Execution (Zero Dependencies)

The engine requires only Python 3.8+ with standard library modules:

```bash
# List all available checklist cards
python3 scripts/checklist_cli.py list

# Run interactive Challenge-Response terminal verification
python3 scripts/checklist_cli.py run leaving_home

# Print ASCII formatted card
python3 scripts/checklist_cli.py card software_release

# Generate print-ready A5 vector PDF card (148 x 210 mm)
python3 scripts/checklist_cli.py pdf leaving_home -o ~/leaving_home_A5.pdf

# Generate all 7 checklist cards to A5 PDFs in one command
python3 scripts/checklist_cli.py pdf-all -d ./pdf/ --theme print
```

### 2. Pip Installation

```bash
pip install -e .
pilot-checklist list
pilot-checklist pdf morning_launch -o morning.pdf
```

### 3. Agent Skill Integration (Google Antigravity / Claude Code / Cursor)

This repository includes [`SKILL.md`](./SKILL.md), allowing AI coding assistants to automatically generate, validate, and execute aviation-type checklist cards according to NASA human factors standards.

```bash
mkdir -p ~/.agents/skills/pilot-checklists
cp -r * ~/.agents/skills/pilot-checklists/
```

---

## Built-In Checklist Library

Templates are located in [`templates/`](./templates/). All checklist cards are pre-compiled and available in print-ready vector PDF format under [`pdf/`](./pdf/):
- **A5 Landscape Knee-board Format ($210 \times 148\text{ mm}$):** [`pdf/*.pdf`](./pdf/)
- **A6 Landscape Pocket Card Format ($148 \times 105\text{ mm}$):** [`pdf/a6_landscape/*.pdf`](./pdf/a6_landscape/)

| Code | Name | Mode | Focus Area | Formats |
| :--- | :--- | :--- | :--- | :--- |
| `CHK-HOME` | **Leaving Home** | Do-Verify | Fire hazards, faucets, windows, workstation lock, 3-pocket tactile pat-down (keys, wallet, phone, deadbolt) | [A5 PDF](./pdf/leaving_home.pdf) / [A6 PDF](./pdf/a6_landscape/leaving_home.pdf) |
| `CHK-FLIGHT` | **International Flight** | Read-and-Do | Passport validity, offline boarding passes, carry-on meds, lithium powerbank limits, network handoff | [A5 PDF](./pdf/flight_travel.pdf) / [A6 PDF](./pdf/a6_landscape/flight_travel.pdf) |
| `CHK-RELEASE` | **Software Release** | Do-Verify | Clean git tree, zero committed secrets, green tests, version bumps, rollback commit SHA | [A5 PDF](./pdf/software_release.pdf) / [A6 PDF](./pdf/a6_landscape/software_release.pdf) |
| `CHK-LAUNCH` | **Morning Focus Launch** | Do-Verify | ADHD sensory baseline, hydration, meds, calendar scan, 1-minute friction-free micro-step | [A5 PDF](./pdf/morning_launch.pdf) / [A6 PDF](./pdf/a6_landscape/morning_launch.pdf) |
| `CHK-SHUTDOWN` | **Evening Shutdown** | Do-Verify | Task completion logging, tab purge, unpushed WIP commit, device charging, wake-up alarms | [A5 PDF](./pdf/evening_shutdown.pdf) / [A6 PDF](./pdf/a6_landscape/evening_shutdown.pdf) |
| `CHK-HOMELAB` | **Homelab Maintenance** | Read-and-Do | Proxmox/PBS backups, container snapshots, ping baseline, config diffs, service unit health | [A5 PDF](./pdf/homelab_maintenance.pdf) / [A6 PDF](./pdf/a6_landscape/homelab_maintenance.pdf) |
| `QRH-OVERWHELM` | **Overwhelm / Freeze QRH** | Emergency | Somatic regulation (box breathing, cold water), 5-4-3-2-1 grounding, radical scope reduction | [A5 PDF](./pdf/panic_freeze_qrh.pdf) / [A6 PDF](./pdf/a6_landscape/panic_freeze_qrh.pdf) |

---

## Creating Custom Checklist Cards

Create a JSON template file in `templates/<name>.json`:

```json
{
  "title": "Database Migration Pre-Flight",
  "code": "CHK-DB-MIGRATE",
  "mode": "READ-AND-DO",
  "trigger": "Before running alembic upgrade / migration script",
  "flow_pattern": "Backup -> Dry-run -> Lock check -> Execution",
  "immediate_memory_actions": [],
  "phases": [
    {
      "name": "Phase 1: Pre-Flight Safety Net",
      "items": [
        {"challenge": "FULL DATABASE BACKUP", "response": "COMPLETED & DUMP TESTED", "killer": true},
        {"challenge": "ACTIVE CONNECTION LOCKS", "response": "0 BLOCKING TRANSACTIONS", "killer": true}
      ]
    },
    {
      "name": "Phase 2: Execution & Verification",
      "items": [
        {"challenge": "DOWNGRADE / DOWN SCRIPT", "response": "TESTED IN STAGING", "killer": true},
        {"challenge": "MIGRATION SCRIPT", "response": "EXECUTED (EXIT CODE 0)", "killer": true}
      ]
    }
  ]
}
```

---

## Running Tests

```bash
python3 -m unittest discover -s tests
```

---

## References & Human Factors Research

- Degani, A., & Wiener, E. L. (1990). *Human Factors of Flight-Deck Checklists: The Normal Checklist* (NASA Contractor Report 177549 / TM-101440). NASA Ames Research Center.
- Gawande, A. (2009). *The Checklist Manifesto: How to Get Things Right*. Metropolitan Books.
- Federal Aviation Administration (FAA). *Aeronautical Information Manual & Flight Crew Operating Manuals (FCOM)*.
- See [`references/aviation_checklist_principles.md`](./references/aviation_checklist_principles.md) for full design guidelines.

---

## License

MIT License. See [LICENSE](./LICENSE) for details.
