# Barangay Data Import Commands

This document explains how to use the management commands to import barangay data from the Philippine Standard Geographic Code (PSGC) API.

## Available Commands

### 1. Import Barangays (General Command)

This command can import barangays from any region, province, or municipality in the Philippines. By default, it imports barangays from Dumingag, Zamboanga del Sur.

```bash
python manage.py import_barangays
```

#### Options:

- `--region`: Filter by region code (e.g., 01, 02, NCR)
- `--province`: Filter by province name (default: Zamboanga del Sur)
- `--municipality`: Filter by municipality name (default: Dumingag)
- `--limit`: Limit the number of barangays to import
- `--clear`: Clear existing barangay data before importing

#### Examples:

Import all barangays from Dumingag, Zamboanga del Sur (default):
```bash
python manage.py import_barangays
```

Import all barangays from a specific province:
```bash
python manage.py import_barangays --province="Cebu"
```

Import all barangays from a specific municipality:
```bash
python manage.py import_barangays --province="Cebu" --municipality="Cebu City"
```

Import all barangays from a specific region:
```bash
python manage.py import_barangays --region="09"
```

Clear existing data and import new data:
```bash
python manage.py import_barangays --clear
```

### 2. Import Dumingag Barangays (Specific Command)

This command specifically imports barangays from Dumingag, Zamboanga del Sur.

```bash
python manage.py import_dumingag_barangays
```

#### Options:

- `--clear`: Clear existing barangay data before importing

#### Examples:

Import all barangays from Dumingag:
```bash
python manage.py import_dumingag_barangays
```

Clear existing data and import Dumingag barangays:
```bash
python manage.py import_dumingag_barangays --clear
```

## Data Source

The data is sourced from the Philippine Standard Geographic Code (PSGC) API:
https://psgc.gitlab.io/api/

## Notes

- The commands use the `tqdm` package to display progress bars during import.
- For Dumingag, Zamboanga del Sur, the zip code is set to "7028".
- For other locations, a generic zip code is generated based on the location code.
- The import process adds a small delay between API requests to avoid overwhelming the server.
