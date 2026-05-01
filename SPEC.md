# Sales Analytics Dashboard for Textile Business - Specification

## 1. Project Overview

**Project Name:** TextileSales Analytics Dashboard  
**Type:** Full-stack Web Application (Data Analytics Dashboard)  
**Core Functionality:** Upload CSV sales data, process textile-specific metrics, visualize trends, and forecast future sales using ML  
**Target Users:** Textile business owners, sales managers, inventory planners

---

## 2. UI/UX Specification

### Layout Structure

**Page Sections:**
- **Header:** Logo, app title, upload button
- **Hero Metrics:** 4 KPI cards in a row (Total Revenue, Total Orders, Top Product, Avg Order Value)
- **Main Content:** Two-column grid
  - Left: Sales Trend Chart (line chart)
  - Right: Top Products Chart (bar chart)
- **Forecast Section:** Full-width chart with historical + predicted data
- **Inventory Alerts:** Table showing low-stock products

**Responsive Breakpoints:**
- Desktop: 1200px+ (full layout)
- Tablet: 768px-1199px (2-column becomes 1-column)
- Mobile: <768px (stacked cards)

### Visual Design

**Color Palette:**
- Primary: `#1E3A5F` (Deep Navy Blue - trust, professionalism)
- Secondary: `#F4A261` (Warm Amber - textile warmth)
- Accent: `#2A9D8F` (Teal - success/growth)
- Background: `#F8FAFC` (Light gray-blue)
- Card Background: `#FFFFFF`
- Text Primary: `#1F2937`
- Text Secondary: `#6B7280`
- Error/Alert: `#E63946`
- Success: `#10B981`

**Typography:**
- Font Family: `'DM Sans', sans-serif` (headings), `'IBM Plex Sans', sans-serif` (body)
- H1: 28px, font-weight 700
- H2: 22px, font-weight 600
- H3: 18px, font-weight 600
- Body: 14px, font-weight 400
- Small: 12px

**Spacing System:**
- Base unit: 4px
- Card padding: 24px
- Section gap: 32px
- Component gap: 16px

**Visual Effects:**
- Card shadows: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`
- Border radius: 12px (cards), 8px (buttons), 6px (inputs)
- Hover transitions: 200ms ease-in-out

### Components

**Upload Button:**
- States: default (outlined), hover (filled), loading (spinner), success (checkmark)
- Accepts: .csv files only

**KPI Cards:**
- Icon + Label + Value + Trend indicator (up/down arrow with percentage)
- Hover: slight lift effect

**Charts:**
- Line chart: smooth curves, gradient fill under line
- Bar chart: rounded corners, hover tooltip
- Forecast chart: solid line for historical, dotted for predicted

**Alert Table:**
- Sortable columns
- Row highlight on hover
- Status badges (Critical: red, Warning: amber)

---

## 3. Functionality Specification

### Core Features

#### 3.1 CSV Upload & Data Ingestion
- **Endpoint:** `POST /api/upload`
- Accept CSV file with textile-specific columns
- Validate required columns
- Handle missing values (fill with 0 or forward-fill)
- Store processed data in memory (or SQLite for persistence)

**Required CSV Columns:**
| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Order date |
| product_name | string | Product/SKU name |
| fabric_type | string | Silk, Cotton, Polyester, etc. |
| quantity | int | Units sold |
| unit_price | float | Price per unit |
| category | string | Product category |

#### 3.2 Analytics Endpoints

**GET /api/analytics/summary**
- Returns: total_revenue, total_orders, top_product, avg_order_value

**GET /api/analytics/trends**
- Returns: monthly sales data (month, revenue, quantity)

**GET /api/analytics/top-products**
- Returns: top 10 products by revenue with fabric type breakdown

**GET /api/analytics/fabric-breakdown**
- Returns: revenue and quantity by fabric type

#### 3.3 Forecasting
- **Endpoint:** `GET /api/forecast`
- Uses Random Forest Regressor (better for seasonal data than Linear Regression)
- Predicts next 30 days of sales
- Returns: date, predicted_revenue, confidence_interval

#### 3.4 Inventory Alerts
- **Endpoint:** `GET /api/alerts`
- Calculate sales velocity (avg daily sales last 30 days)
- Flag products where velocity suggests stockout in <10 days

### User Interactions

1. User clicks "Upload CSV" button
2. File picker opens, user selects CSV
3. Loading spinner shows during processing
4. Success: Dashboard populates with data
5. Error: Toast notification with specific error message

### Edge Cases

- Empty CSV: Show "No data found" message
- Missing columns: Return specific error "Missing required column: {column_name}"
- Invalid dates: Skip row, log warning
- Negative values: Treat as 0
- Large files (>10MB): Show warning, process in chunks

---

## 4. Technical Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry
│   ├── models.py            # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py        # CSV upload endpoint
│   │   ├── analytics.py     # Analytics endpoints
│   │   └── forecast.py      # Forecast endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_processor.py # Pandas processing
│   │   └── forecaster.py    # ML forecasting
│   └── utils/
│       ├── __init__.py
│       └── validators.py    # CSV validation
├── requirements.txt
└── sample_data.csv          # Sample textile sales data
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── KPICard.jsx
│   │   ├── SalesTrendChart.jsx
│   │   ├── TopProductsChart.jsx
│   │   ├── ForecastChart.jsx
│   │   └── InventoryAlerts.jsx
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── index.html
├── package.json
└── vite.config.js
```

---

## 5. Acceptance Criteria

### Visual Checkpoints
- [ ] Header displays app title and upload button
- [ ] 4 KPI cards show with icons and trend indicators
- [ ] Sales trend line chart renders with smooth curves
- [ ] Top products bar chart shows top 10 products
- [ ] Forecast chart shows historical (solid) + predicted (dotted) lines
- [ ] Inventory alerts table shows critical items in red

### Functional Checkpoints
- [ ] CSV upload works and shows success/error feedback
- [ ] Analytics data populates all charts
- [ ] Forecast generates 30-day predictions
- [ ] Responsive layout works on tablet/mobile
- [ ] Error handling shows user-friendly messages

### Performance
- [ ] Page loads in <3 seconds
- [ ] CSV processing completes in <5 seconds for files up to 10MB