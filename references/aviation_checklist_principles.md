# Aviation Checklist Principles & Human Factors Reference

Checklists in aviation are not memory aids or generic "to-do" lists; they are **critical safety barriers designed to prevent catastrophic omission errors under stress, distraction, and cognitive fatigue**.

This reference outlines the foundational human factors principles established by NASA (Degani & Wiener, 1990; NASA TM-101440), the FAA, and commercial airline Quick Reference Handbooks (QRH / FCOM).

---

## 1. The Two Core Operational Modes

Every checklist must be explicitly classified into one of two operational philosophies:

### A. Do-Confirm (Do-Verify) — Routine Normal Operations
- **When to use**: High-frequency, routine tasks where an established physical/cognitive "flow" already exists (e.g. morning setup, leaving home, daily coding commits, packing bags).
- **Execution Flow**:
  1. The operator executes actions smoothly from muscle memory in a structured spatial pattern (e.g., clockwise room sweep, cockpit left-to-right sweep).
  2. At a defined **Pause Point** (e.g., hand on doorknob, before `git push`), the operator opens the checklist card.
  3. The card is read to **verify** that every critical configuration is set.
- **Advantage**: Fast, maintains natural cadence, does not disrupt flow.

### B. Read-and-Do (Challenge-Response) — High Risk, Infrequent, or Abnormal
- **When to use**: Complex multi-step operations, irreversible actions, high consequence tasks, or emergency/abnormal situations (e.g. production database migrations, international travel border transit, server re-flashing, panic/overwhelm recovery).
- **Execution Flow**:
  1. Read the **Challenge** (item name/cue).
  2. Visually/physically locate the control/item and take the action.
  3. Vocalize or verify the exact **Response** (target state).
  4. Advance to the next line only after verification is confirmed.
- **Advantage**: Zero reliance on working memory; eliminates skipped steps.

---

## 2. Anatomy of an Aviation Checklist Line Item

A valid aviation checklist item consists of two distinct components separated by dot leaders (`...`):

```text
[ CHALLENGE / CUE ] .............................. [ RESPONSE / TARGET STATE ]
```

### The Challenge (What to look at)
- Concise, unequivocal noun phrase identifying the component, system, or object.
- Example: `PASSPORT & BOARDING PASS`, `PROXMOX BACKUP STATUS`, `MAIN WATER VALVE`.

### The Response (Exact verifiable state)
- Must state the **observable condition**, not a vague action verb.
- **Banned responses**: `"Check"`, `"Verify"`, `"Done"`, `"OK"`, `"Look at"`.
- **Approved standard responses**:
  - `SET [VALUE]` (e.g., `SET 2.4 BAR`)
  - `ON / OFF`
  - `ARMED / SAFE / DISARMED`
  - `LOCKED & KEY IN POCKET`
  - `OFFLINE CACHED (AIRPLANE MODE TESTED)`
  - `PASSING (0 FAILURES / 0 REGRESSIONS)`
  - `CLOSED & LATCHED`

---

## 3. "Killer Items" & Boldface Memory Actions

### Killer Items (Safety-Critical Points)
- A *Killer Item* is a step whose omission results in catastrophic failure, immediate lockout, financial damage, or irreversible data loss.
- In checklist cards, Killer Items are highlighted with high-contrast boxed borders or warning markers (`⚠️ KILLER ITEM`).
- **Rule of Operation**: If interrupted during a checklist, the operator must restart from the last Killer Item or the top of the phase.

### Boldface / Memory Items
- Actions required immediately when time is critical before opening the physical checklist (e.g., immediate stove fire, sudden server breach, panic freeze).
- Stored on the card with heavy border boxes: `[ IMMEDIATE MEMORY ACTIONS ]`.

---

## 4. Chunking and the Rule of 5–9 (Miller's Law)

- Human working memory degrades under fatigue, ADHD, sensory overload, and urgency.
- **Maximum items per chunk**: 5 to 7 items (hard limit 9).
- Structure longer processes across distinct **Phases of Operation** (e.g., Phase 1: Planning $\rightarrow$ Phase 2: Pre-Launch $\rightarrow$ Phase 3: In-Transit $\rightarrow$ Phase 4: Arrival & Shutdown).
- Each phase gets its own dedicated card or bordered section.

---

## 5. Defined Pause Points ("Hold Short" Lines)

- A checklist must have an unambiguous, concrete trigger condition:
  - *“Hold short of runway”* $\rightarrow$ *“Hand on front door handle”*
  - *“Top of descent”* $\rightarrow$ *“15 minutes before departure alert”*
  - *“Before gear retraction”* $\rightarrow$ *“Before issuing PR merge”*
- If the trigger is reached, all other multitasking ceases until the checklist card is completed.

---

## 6. Physical Flow Patterns & Anti-Complacency Sweeps

Before reading a Do-Verify checklist, enforce a tactile/spatial flow:
- **Spatial Order**: Left -> Right, Top -> Bottom, or Clockwise perimeter.
- **Point-and-Call (Japanese Shisa Kanko / Cockpit Cross-Check)**: Physically touching or pointing at the verified item while confirming the response eliminates blind habitual blindness.

---

## 7. Standard Aviation Typography Rules

Checklist cards must adhere to cockpit human factors legibility standards (NASA / FAA FCOM):

1. **Size**: Minimum 10 pt to 12 pt for paper checklists (character height ~0.14″ to 0.20″) to maintain instant readability under red night-lighting, motion vibration, or low-light conditions.
2. **Case**: Mixed case (Sentence or Title Case) for challenges and routine steps. ALL CAPS is strictly reserved for critical warnings, section headers, or emergency memory items.
3. **Weight Hierarchy**: Regular weight for the Challenge (the item being checked) and Bold for the Response (the required switch/lever state) to visually separate the two actions and guide the pilot's eye instantly to the target state.

