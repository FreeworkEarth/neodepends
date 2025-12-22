# TrainTicketSystem - PYTHON_FIRST (Poor Architecture)

**Language:** Python 3.11+
**Architecture:** Monolithic with severe design issues
**Purpose:** Ground truth for NeoDepends + Deicide + DV8 validation

---

## Architecture Issues (Same as Java FIRST)

### 1. God Class (Singleton)
**File:** `tts/ticket_booking_system.py`
- Manages ALL entities (stations, trains, routes, passengers, staff, tickets)
- Creates massive coupling hub
- Violates Single Responsibility Principle

### 2. 3-Way Cyclic Dependency
```python
route.py → train_station.py (origin, destination)
train_station.py → train.py (available_trains)
train.py → route.py (route)
```

### 3. Bidirectional Dependencies
- `ticket_agent.py` ↔ `train_station.py`
- `passenger.py` ↔ `ticket.py`

### 4. Poor Layer Separation
- `main.py` directly uses all 11 modules
- Business logic scattered in entity classes

---

## Files (11 modules)

```
TrainTicketSystem_PYTHON_FIRST/
├── tts/
│   ├── __init__.py
│   ├── person.py                    (base)
│   ├── staff.py                     (base)
│   ├── passenger.py                 (Passenger → Ticket)
│   ├── train_station.py             (TrainStation → Train, TicketAgent)
│   ├── route.py                     (Route → TrainStation - CYCLE!)
│   ├── train.py                     (Train → Route - CYCLE!)
│   ├── ticket.py                    (Ticket → Passenger, Route, Train)
│   ├── ticket_agent.py              (TicketAgent → TrainStation + 4 others)
│   ├── station_manager.py           (StationManager → TrainStation, Train)
│   └── ticket_booking_system.py     (GOD CLASS - manages everything!)
├── main.py                          (coupled to all 11 modules)
└── README.md
```

---

## Expected DV8/NeoDepends Results

Based on Java FIRST version (M-Score: 21.15%):

| Metric | Expected | Reason |
|--------|----------|--------|
| **M-Score** | ~20-25% | God class, cycles, high coupling |
| **Propagation Cost** | ~60-70% | Changes propagate widely |
| **Decoupling Level** | ~5-15% | Tight coupling everywhere |
| **Independence Level** | ~5-15% | Files heavily interdependent |

---

## Cyclic Dependencies

```
CYCLE 1 (3-way):
  route.py → train_station.py (uses TrainStation objects)
  train_station.py → train.py (stores Train objects)
  train.py → route.py (uses Route object)

BIDIRECTIONAL:
  ticket_agent.py ↔ train_station.py
  passenger.py ↔ ticket.py (via list)
```

---

## Running the System

### Prerequisites
```bash
python3 --version  # Should be 3.11+
```

### Run
```bash
cd TrainTicketSystem_PYTHON_FIRST
python3 main.py
```

### Expected Output
```
=== Train Ticket Booking System (FIRST - Poor Architecture) ===

--- Initial System State ---
Stations: 2
Routes: 1
Trains: 2
Passengers: 2
Staff: 2

--- Booking Tickets ---
✓ Booked: TKT-...
...
```

---

## Running NeoDepends + Deicide

### Analyze with deicide-tool
```bash
cd /path/to/deicide-tool

# Analyze main.py (entry point)
deicide-tool \
  --project /path/to/TrainTicketSystem_PYTHON_FIRST \
  --filename main.py \
  --output-dir results_py_first \
  --language python \
  --dv8
```

### Expected Output Files
- `results_py_first/dependencies.db` - NeoDepends database
- `results_py_first/deicide_clustering.json` - Deicide clustering
- `results_py_first/deicide_clustering.dv8-clustering.json` - DV8 clustering format
- `results_py_first/deicide_clustering.dv8-dependency.json` - DV8 dependency format

---

## Validation Goals

### 1. NeoDepends Detection
- ✅ Detect 11 Python modules
- ✅ Detect cyclic dependencies (route ↔ train_station ↔ train)
- ✅ Detect god class (ticket_booking_system imports all)
- ✅ Detect high coupling in main.py

### 2. Deicide Clustering
- Should identify ticket_booking_system as large/god class
- Should suggest splitting into repositories
- Should detect tight coupling clusters

### 3. DV8 Compatibility
- DV8 clustering format should match Java output structure
- Dependency matrix should show same architectural issues
- Metrics should be comparable to Java version (±10%)

---

## Comparison with Java FIRST

| Aspect | Java | Python |
|--------|------|--------|
| Files | 11 | 11 |
| God Class | TicketBookingSystem.java | ticket_booking_system.py |
| Cycles | Route → TrainStation → Train | route → train_station → train |
| Dependencies | Object references | Object references |
| M-Score (expected) | 21.15% | ~20-25% |

**Goal:** Prove NeoDepends + Deicide produce equivalent results across languages!

---

## Known Issues (Intentional)

1. **God Class** - ticket_booking_system.py manages everything
2. **Cyclic Dependencies** - 3-way cycle destroys modularity
3. **Bidirectional Coupling** - ticket_agent ↔ train_station
4. **Poor Layering** - main.py uses all 11 modules directly
5. **Business Logic in Entities** - ticket_agent.book_ticket()

These are **intentional anti-patterns** for testing DV8 detection!

---

## Use Cases

1. **Validate NeoDepends** - Does it detect Python dependencies correctly?
2. **Validate Deicide** - Does it identify god class and suggest modularization?
3. **Validate DV8 Output** - Can we compare Java vs Python metrics?
4. **Test Configuration** - Find correct config for Python + Deicide

---

## Next Steps

1. Run NeoDepends + Deicide on this Python version
2. Compare DV8 output with Java FIRST version
3. Validate metrics are similar (±10%)
4. Document any configuration needed for Python

**Status:** ✅ Complete and Ready for Analysis
