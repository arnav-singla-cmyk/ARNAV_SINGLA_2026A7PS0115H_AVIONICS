# SEDS BPHC — Avionics Round 1 Induction Task

## Overview

This repository contains my solutions for the **Avionics Round 1 Induction Task**, consisting of two parts:

1. Finding the Sea Floor — Depth Data Analysis
2. Keeping Watch Over Odysseus — Onboard Monitoring System

---

## Task 1: Finding the Sea Floor

The provided depth data was recorded every second. I extracted the data from the CSV file and plotted the depth against time.

### Approach

* Read the depth data from the CSV file.
* Identified and handled corrupted or suspicious sensor readings.
* Replaced invalid values using the previous valid reading.
* Plotted the depth-time graph using Matplotlib.
* Animated the graph by adding one data point every second.
* Applied a moving average to reduce random noise in the depth data.

### Files

* `Arnav_Singla_2026A7PS0115H_AVIONICS_T1.py`
* `Depth Data.csv`

### Graph

The final depth-time graph is included in the repository as a screenshot.

---

## Task 2: Keeping Watch Over Odysseus

For the onboard monitoring system, I built the required circuit in Tinkercad using the specified components.

### Components Used

* Arduino
* Ultrasonic distance sensor
* Light sensor
* LCD screen
* Push button
* LED
* Buzzer

### Approach

The system uses a state machine with the following states:

* **OPEN SEA** — Default state when the journey begins.
* **ANCHOR DROPPED** — Controlled using the push button.
* **STORM** — Triggered when the light sensor reading falls below half.
* **CHARYBDIS** — Triggered when an object is detected within 100 cm.
* **WRECKED** — Entered if the ship remains in STORM or CHARYBDIS continuously for five seconds.

The current state is displayed on the LCD. The LED blinks during STORM, while the buzzer sounds during CHARYBDIS.

### Tinkercad

The complete circuit and Arduino code were implemented and tested in Tinkercad.

**Tinkercad Link:**
(https://www.tinkercad.com/things/iAH91bsOtqY-arnavsingla2026a7ps0115havionicst2?sharecode=n4WYFquMLEmwfyXOmYJapX48RK-9nmg1lL67ZUTDQ7k)

### Screenshots

Screenshots of the completed Tinkercad wiring are included in the repository.

---

## Repository Structure

```text
├── Arnav_Singla_2026A7PS0115H_AVIONICS_T1.py
├── Depth Data.csv
├── Tinkercad/
│   └── screenshots
├── Task_1/
│   └── graph_screenshot
└── README.md
```

## Author

**Arnav Singla**
ID: **2026A7PS0115H**
