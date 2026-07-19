# Time Table Generator

An automated, web based scheduling application designed to generate optimized, collision free academic timetables. The application utilizes a Python driven backtracking constraint layout engine, leverages a MySQL backend to keep track of configuration boundaries, and exports processed tables to local CSV frameworks.

  
## Publication

If you use this software or find the methodology useful, please cite my published paper:

* **Title:** A Constraint-Based Automated Timetable Generator For Educational Institutions
* **Authors:** Bryan Joe
* **Journal/Conference:** i-manager's Journal on Software Engineering
* **Links:** [Read Paper Here](https://imanagerpublications.com/article/22527) - https://imanagerpublications.com/article/22527

### Citation (BibTeX)

```bibtex
@article{joe2025constraint,
  author    = {Joe, Bryan},
  title     = {A Constraint-Based Automated Timetable Generator For Educational Institutions},
  journal   = {i-manager's Journal on Software Engineering},
  volume    = {20},
  number    = {1},
  year      = {2025},
  month     = {November}
}
```

> Bryan Joe. "A Constraint-Based Automated Timetable Generator For Educational Institutions." i-manager's Journal on Software Engineering, Vol. 20, Issue 1 (November 18, 2025).



## Features

- **Constraint-Based Scheduling Engine:** Automatically maps out weekly timetables while dynamically managing overlapping restrictions (e.g., teacher availability, consecutive practical lab sessions, and shared ground access).
- **Database-Driven Configuration:** Integrates with a MySQL backend to dynamically inherit variables like periods per day, active school days, and classroom thresholds.
- **Multi Format:** Writes structured output models directly back to a relational database instance and exports individual class distributions into neatly partitioned `.csv` spreadsheets.
- **Intuitive Web UI:** Uses a responsive web interface driven by backend application templates to view, configure, and generate administrative schedules dynamically.



## 🛠️ Architecture & Project Structure

The project separates core scheduling mechanics and file handling rules from the frontend visualization structure:

```Plaintext
├── Classes/                 # Directory for auto-generated CSV grade schedule
├── static/                  # Frontend user interface assets (CSS stylesheets and JS)
├── templates/               # UI layout view models (Rendered by the web application server).
├── Test/                    # Validation suite containing unit tests and engine layout test cases.
├── __pycache__/             # Compiled Python bytecode optimization caching.
├── ProjectDocuments/        # Specification data sheets, structural mockups, and wireframes.
│
├── app.py                   # UI Application Driver: Manages web routes, request handling, and template rendering.
├── data.py                  # Data Management Layer: Implements MySQL connectors and handles schemas.
├── timetable.py             # Core Engine: Contains the backtracking constraint-satisfaction layout algorithms.
├── main.py                  # System Entry Point: Manages the pipelines between components.
│
├── Rules.md / rules.md      # Configuration parameters and constraint logic documentation blueprints.
└── Reference.pur            # System structural planning blueprint
```



## Data Engine Design Principles

The application relies on a cascading execution model that strictly checks parameters before mapping structural elements into the array:

1. **Fixed Allocations First:** The system schedules practical split blocks (e.g., Physics/Chemistry dual labs running continuously for 2 periods) and high-priority physical education periods across standard structural layouts first.
2. **Teacher Coincidence Resolution:** Iterates through structural dictionaries to guarantee zero overlaps where a specific staff asset (`teacherDetails`) is scheduled across two separate sections simultaneously.
3. **Core Subjects Standard Distribution:** Backfills remaining open array bounds with traditional scholastic subjects (Math, English, Computer Science) according to a predefined maximum occurrences limit per day and target limits per week.



## Setup & Installation

### 1. Prerequisites

Ensure you have **Python 3.x** and **MySQL Server** installed on your host machine.

### 2. Database Initialization

Create a MySQL database named `timetable` and establish a configuration table containing the runtime boundaries:

```sql
CREATE DATABASE timetable;
USE timetable;

CREATE TABLE config (
    fieldName VARCHAR(255) PRIMARY KEY,
    fieldValue VARCHAR(255) NOT NULL
);

-- Seed initial constraints parameters
INSERT INTO config (fieldName, fieldValue) VALUES 
('noOfDays', '5'),
('periodsPerDay', '8'),
('maxClassesInGround', '2');
```

> **Note:** Update the connection parameters inside the initialization function of the `MySqlConnector` class (`host`, `user`, `password`) to match your local database authentication credentials.

### 3. Install Requirements

Install the required standard connector dependency:

```bash
pip install mysql-connector-python
```

### 4. Running the Application

Launch the web interface application driver directly:

```bash
python app.py
```

> (Replace `app.py` with the exact name of your main UI server file if named differently)

## Output Generation

When a complete layout passes all verification conditions:

- **Database Update:** The engine flushes existing structures, calls `updateOutput()`, and writes the compiled timeline data straight to a `ClassSchedule` table.
- **CSV Compilation:** The routine invokes `saveAsCSV()`, creating a segmented folder tree categorized by grade level (e.g., `Classes/11Grade/11A.csv`) mapping out day-by-day and period-by-period class distributions.
