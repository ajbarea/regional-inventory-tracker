# Regional Supermarket Inventory Tracking System

[![codecov](https://codecov.io/gh/ajbarea/regional-inventory-tracker/graph/badge.svg?token=O6Y8NTQYSq)](https://codecov.io/gh/ajbarea/regional-inventory-tracker) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ajbarea_regional-inventory-tracker&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ajbarea_regional-inventory-tracker)

This system tracks the inventory in a chain of regional supermarkets and determines the product that will be shipped to each store from a central distribution center.

## Team

- [**Kemoy**](https://github.com/kemoycampbell)
- [**Devaj**](https://github.com/DevajMody)
- [**AJ**](https://github.com/ajbarea)

## Software Architecure Views
### Module View

```mermaid

---
config:
  theme: 'base'
  themeVariables:
    primaryColor: '#E8F4FD'
    primaryBorderColor: '#2196F3'
    primaryTextColor: '#1565C0'
    secondaryColor: '#F3E5F5'
    secondaryBorderColor: '#9C27B0'
    secondaryTextColor: '#6A1B9A'
    tertiaryColor: '#E8F5E8'
    tertiaryBorderColor: '#4CAF50'
    tertiaryTextColor: '#2E7D32'
    lineColor: '#424242'
    background: '#FAFAFA'
    textColor: '#212121'
    nodeTextColor: '#1565C0'
    edgeLabelBackground: '#FFFFFF'
    clusterBkg: '#F5F5F5'
    clusterBorder: '#BDBDBD'
    fillType0: '#E3F2FD'
    fillType1: '#F3E5F5'
    fillType2: '#E8F5E8'
    fillType3: '#FFF3E0'
    fillType4: '#FCE4EC'
    fillType5: '#F1F8E9'
    fillType6: '#E0F2F1'
    fillType7: '#FFF8E1'
---
graph LR
  subgraph Store Frontend
    SF["Store Frontend (Web Application)"]
  end

  subgraph Backend Services
    CDC["Central Distribution Center (REST API)"]
    DS["PostgreSQL / SQLite"]
    CL["Redis Cache"]
    MS["Apache Kafka"]
  end

  subgraph Deployment
    CI["Docker Containerization"]
  end

  SF -->|HTTPS| CDC
  CDC -->|REST| DS
  CDC -->|Redis| CL
  CDC -->|Kafka| MS
  SF -.-> CI
  CDC -.-> CI

```

### Components & Connectors View

```mermaid

---
config:
  theme: 'base'
  themeVariables:
    primaryColor: '#E8F4FD'
    primaryBorderColor: '#2196F3'
    primaryTextColor: '#1565C0'
    secondaryColor: '#F3E5F5'
    secondaryBorderColor: '#9C27B0'
    secondaryTextColor: '#6A1B9A'
    tertiaryColor: '#E8F5E8'
    tertiaryBorderColor: '#4CAF50'
    tertiaryTextColor: '#2E7D32'
    lineColor: '#424242'
    background: '#FAFAFA'
    textColor: '#212121'
    nodeTextColor: '#1565C0'
    edgeLabelBackground: '#FFFFFF'
    clusterBkg: '#F5F5F5'
    clusterBorder: '#BDBDBD'
    fillType0: '#E3F2FD'
    fillType1: '#F3E5F5'
    fillType2: '#E8F5E8'
    fillType3: '#FFF3E0'
    fillType4: '#FCE4EC'
    fillType5: '#F1F8E9'
    fillType6: '#E0F2F1'
    fillType7: '#FFF8E1'
---
graph LR
  subgraph Store Frontend
    SF["Store Frontend (Web Application)"]
    SF -->|HTTPS| CDC["Central Distribution Center (REST API)"]
  end

  subgraph Backend Services
    CDC -->|REST| DS["PostgreSQL / SQLite"]
    CDC -->|Redis| CL["Redis Cache"]
    CDC -->|Kafka| MS["Apache Kafka"]
  end

  subgraph Deployment
    CI["Docker Containerization"]
    SF -.-> CI
    CDC -.-> CI
  end

```
### Allocation View

```mermaid
---
config:
  theme: 'base'
  themeVariables:
    primaryColor: '#E8F4FD'
    primaryBorderColor: '#2196F3'
    primaryTextColor: '#1565C0'
    secondaryColor: '#F3E5F5'
    secondaryBorderColor: '#9C27B0'
    secondaryTextColor: '#6A1B9A'
    tertiaryColor: '#E8F5E8'
    tertiaryBorderColor: '#4CAF50'
    tertiaryTextColor: '#2E7D32'
    lineColor: '#424242'
    background: '#FAFAFA'
    textColor: '#212121'
    nodeTextColor: '#1565C0'
    edgeLabelBackground: '#FFFFFF'
    clusterBkg: '#F5F5F5'
    clusterBorder: '#BDBDBD'
    fillType0: '#E3F2FD'
    fillType1: '#F3E5F5'
    fillType2: '#E8F5E8'
    fillType3: '#FFF3E0'
    fillType4: '#FCE4EC'
    fillType5: '#F1F8E9'
    fillType6: '#E0F2F1'
    fillType7: '#FFF8E1'
---
graph TB
  subgraph VPC
    subgraph Public Subnet
      ALB[(Application Load Balancer)]
    end

    subgraph Private Subnet A
      ECS_CDC[(ECS: Central Distribution Center Container)]
      RDS[(RDS: PostgreSQL / SQLite)]
    end

    subgraph Private Subnet B
      ECS_SF[(ECS: Store Frontend Container)]
      MSK[(MSK Cluster: Apache Kafka)]
      REDIS[(ElastiCache Redis)]
    end

    ALB -->|HTTPS| ECS_SF
    ALB -->|HTTPS| ECS_CDC
    ECS_CDC -->|connects to| RDS
    ECS_CDC -->|connects to| MSK
    ECS_CDC -->|connects to| REDIS
    ECS_SF -->|connects to| MSK
  end

```

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
pytest
```
