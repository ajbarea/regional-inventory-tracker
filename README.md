# Regional Supermarket Inventory Tracking System

This system tracks the inventory in a chain of regional supermarkets and determines the product that will be shipped to each store from a central distribution center.

## Team

- Kemoy: @kemoycampbell
- Devaj: @DevajMody
- AJ: @ajbarea

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
