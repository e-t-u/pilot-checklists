---
name: pilot-checklists
description: "Aviation-grade checklist generator and runner based on airline Quick Reference Handbooks (QRH), NASA human factors engineering, and Challenge-Response protocols. Creates perfectly chunked, killer-item-isolated checklist cards for ADHD memory support, pre-flight travel, code deployment, homelab maintenance, leaving home, and morning/evening routines."
---

# Aviation-Grade Checklist Skill (`pilot-checklists`)

## Overview

The `pilot-checklists` skill transforms standard to-do lists and procedural instructions into **aviation-grade checklist cards**. Based on human factors research from NASA (Degani & Wiener), commercial airline Quick Reference Handbooks (QRH / FCOM), and *The Checklist Manifesto*, this skill eliminates cognitive overload, combats ADHD task omission / working memory drop-off, and guarantees flawless execution under fatigue or stress.

---

## 1. Core Aviation Principles

When generating or auditing any checklist, apply these six non-negotiable aviation rules:

### A. The Challenge — Response Standard
Every single line item must have a distinct **Challenge** (cue / object) and **Response** (exact verifiable state) separated by dot leaders:
```text
[ CHALLENGE / CUE ] .............................. [ RESPONSE / TARGET STATE ]
```
- **Banned responses**: `"Check"`, `"Verify"`, `"Done"`, `"OK"`, `"Look at"`.
- **Mandated verifiable states**: Binary, sensory, or measurable conditions (e.g., `OFF / ZERO FLAME`, `TOUCHED IN RIGHT POCKET`, `LOCKED & KEY IN HAND`, `CONNECTED (PING OK)`, `0 TEST FAILURES`).

### B. Operational Mode Selection
1. **Do-Confirm (Do-Verify)**: For routine, high-cadence tasks. The operator performs an established tactile/spatial sweep from memory, then pulls up the checklist card at a designated pause point to verify critical items.
2. **Read-and-Do (Challenge-Response)**: For high-risk, irreversible, or infrequent procedures (e.g. international border transit, server re-flashing, git release). Read step $\rightarrow$ take action $\rightarrow$ confirm state before reading next.

### C. "Killer Item" Isolation
A **Killer Item** is a critical failure point where omission leads to severe consequences (e.g., leaving the stove on, locking keys inside, pushing uncommitted secrets to Git, packing powerbanks in checked baggage).
- Flagged with `[!] ⚠️` on cards and highlighted in bold red/yellow.
- If interrupted during execution, the operator **must restart from the last Killer Item**.

### D. Miller's Law Chunking (5–9 Rule)
- Never exceed 5 to 7 items (hard limit 9) per operational phase.
- Multi-step tasks must be broken down into temporal phases (e.g., *Phase 1: Pre-Departure*, *Phase 2: In-Transit*, *Phase 3: Arrival & Shutdown*).

### E. Defined Pause Points ("Hold Short" Line)
Every checklist card must declare an unambiguous physical or temporal trigger that commands running the checklist (e.g., *"Hand on front door knob"*, *"Sitting down with morning tea"*, *"Prior to git push origin main"*).

### F. Tactile Flow Patterns (Anti-Complacency Sweeps)
Require a spatial sweep pattern (e.g., *Clockwise room perimeter*, *Top-to-bottom luggage layer*, *Cockpit left-to-right*) combined with physical touch / pointing ("Japanese Shisa Kanko") to eliminate blind habitual assumptions.

### G. Standard Aviation Typography Rules
1. **Size:** Minimum 10 pt to 12 pt for paper checklists (character height ~0.14″ to 0.20″) to maintain readability under red night-lighting, vibration, or low-light conditions.
2. **Case:** Mixed case (Sentence or Title Case) for challenges and steps. ALL CAPS is strictly reserved for critical warnings, section headers, or emergency memory items.
3. **Weight Hierarchy:** Regular weight for the Challenge (the item being checked) and Bold for the Response (the required switch/lever state) to visually separate the two actions.

---

## 2. CLI Tool & Interactive Runner

The skill includes a dedicated terminal engine and card renderer:

```bash
# List all installed checklist cards in the library
python3 ~/.agents/skills/pilot-checklists/scripts/checklist_cli.py list

# Run interactive Challenge-Response checklist in terminal
python3 ~/.agents/skills/pilot-checklists/scripts/checklist_cli.py run leaving_home

# Print ASCII formatted pocket card to terminal / markdown
python3 ~/.agents/skills/pilot-checklists/scripts/checklist_cli.py card software_release

# Generate print-ready A5 vector PDF card (148 x 210 mm)
python3 ~/.agents/skills/pilot-checklists/scripts/checklist_cli.py pdf leaving_home -o ~/leaving_home_A5.pdf

# Generate all 7 cards into a directory as A5 PDFs
python3 ~/.agents/skills/pilot-checklists/scripts/checklist_cli.py pdf-all -d ./pdf/ --theme print
```

---

## 3. Installed Checklist Library

Templates live in `~/.agents/skills/pilot-checklists/templates/`:

1. **`leaving_home`** (`CHK-HOME`): Stove/appliances, faucets, windows, workstation lock, Tailscale remote check, 3-pocket tactile pat-down (keys, wallet, phone, deadbolt).
2. **`flight_travel`** (`CHK-FLIGHT`): Passport >6mo validity, offline boarding passes, carry-on meds, lithium powerbanks $\le 100\text{Wh}$ in cabin, Flatpak timezone, NordVPN profiles.
3. **`software_release`** (`CHK-RELEASE`): Git clean status, 0 checked-in secrets, test suite green, version bump, documentation & PDF rebuilds, rollback SHA recorded.
4. **`morning_launch`** (`CHK-LAUNCH`): ADHD sensory baseline, meds, hydration, calendar scan, 1-minute friction-free micro-step, distraction shielding.
5. **`evening_shutdown`** (`CHK-SHUTDOWN`): Task logging to [`~/LOG.md`](file:///home/etu/LOG.md), tab purge, unpushed WIP commit, device charging, wake-up alarms armed.
6. **`homelab_maintenance`** (`CHK-HOMELAB`): PBS backup verified, container snapshots, ping baseline, config diff backup, service unit verification.
7. **`panic_freeze_qrh`** (`QRH-OVERWHELM`): Emergency Quick Reference Handbook for acute overwhelm, sensory reset, 5-4-3-2-1 grounding, radical scope reduction.

---

## 4. How to Generate a Perfect Checklist Card

When the user asks to create a checklist for any workflow or routine:

1. **Identify the Trigger**: Define the exact physical pause point where this card is executed.
2. **Determine the Mode**: Choose `DO-VERIFY` (routine flow) or `READ-AND-DO` (safety-critical).
3. **Establish the Flow Pattern**: Define the physical/spatial sweep preceding verification.
4. **Segment into Phases**: Group into chronological phases of $\le 7$ items each.
5. **Convert every item into Challenge — Response**: Ensure binary verifiable states with dot leaders.
6. **Flag Killer Items**: Mark failure-critical points with `killer: true` / `[!] ⚠️`.
7. **Output in Standard Card Format**: Present the card in ASCII/Markdown box format and offer to save it as a template or render as HTML/PDF.

### JSON Template Specification
```json
{
  "title": "Descriptive Card Title",
  "code": "CHK-CODE",
  "mode": "DO-VERIFY | READ-AND-DO | EMERGENCY",
  "trigger": "Exact physical pause point",
  "flow_pattern": "Physical sweep description",
  "immediate_memory_actions": [
    {"challenge": "ITEM", "response": "TARGET STATE"}
  ],
  "phases": [
    {
      "name": "Phase 1: Phase Title",
      "items": [
        {"challenge": "NOUN / SYSTEM", "response": "VERIFIABLE STATE", "killer": true}
      ]
    }
  ]
}
```

---

## 5. Thermal Label & Dymo Sticker Integration

For sticky micro-checklists placed on door frames, monitor bezels, server racks, or flight bags, format checklist items into 1-to-2 column thermal label text suitable for printing with the `dymbo` skill:

```text
[DO-VERIFY: LEAVE HOME]
* STOVE/OVEN ...... OFF/COLD
* WATER/TAPS ...... OFF
* KEYS ............ IN POCKET
* PHONE/WALLET .... WITH YOU
* DEADBOLT ........ LOCKED
```
