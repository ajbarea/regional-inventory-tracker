# Regional Supermarket Inventory Tracking System

[![codecov](https://codecov.io/gh/ajbarea/regional-inventory-tracker/graph/badge.svg?token=O6Y8NTQYSq)](https://codecov.io/gh/ajbarea/regional-inventory-tracker) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ajbarea_regional-inventory-tracker&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ajbarea_regional-inventory-tracker)

This system tracks the inventory in a chain of regional supermarkets and determines the product that will be shipped to each store from a central distribution center.

## Team

- [**Kemoy**](https://github.com/kemoycampbell)
- [**Devaj**](https://github.com/DevajMody)
- [**AJ**](https://github.com/ajbarea)

## Quickstart

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --reload-exclude logs/
```

## API Endpoints

- **GET /** - Health check
- **Docs**: <http://localhost:8000/docs>

## Test

```bash
python -m unittest discover
```
