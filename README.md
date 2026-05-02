# Textile Sales Analytics Dashboard

A full-stack web application for analyzing textile sales data, tracking trends, and forecasting future sales. Built with React, FastAPI, and Docker.

![React](https://img.shields.io/badge/React-18.2-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Node.js](https://img.shields.io/badge/Node.js-18-green)
##Screenshots
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6a5a2504-e9a9-4b24-88d8-0c2c958e3381" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2bf68f77-930d-4427-9bb7-2da9d0f3398d" />


## Features

- 📊 **Sales Analytics Dashboard** - View key performance indicators (KPIs) and metrics at a glance
- 📈 **Trend Analysis** - Track monthly sales trends with interactive charts
- 🎯 **Top Products** - Identify best-performing products
- 🧵 **Fabric Breakdown** - Analyze sales by fabric type
- ⚠️ **Inventory Alerts** - Monitor low stock and slow-moving inventory
- 🔮 **Sales Forecasting** - Predict future sales with time-series forecasting
- 📤 **CSV Upload** - Upload sales data in CSV format for analysis
- 📱 **Responsive UI** - Works seamlessly on desktop and mobile devices
- 🎨 **Interactive Charts** - Built with Recharts for beautiful visualizations

## Tech Stack

### Frontend
- **React 18.2** - UI library
- **Vite** - Build tool and dev server
- **Recharts** - Chart library
- **Lucide React** - Icon library
- **CSS** - Custom styling

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11** - Runtime
- **Uvicorn** - ASGI server
- **Pandas** - Data manipulation
- **NumPy** - Numerical computations
- **Scikit-learn** - Machine learning for forecasting

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
.
├── frontend/                    # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx             # Main app component
│   │   ├── App.css             # Global styles
│   │   ├── main.jsx            # Entry point
│   │   └── components/         # React components
│   ├── index.html              # HTML template
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
│
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI app & static file serving
│   │   ├── models.py          # Pydantic models
│   │   ├── routes/            # API route handlers
│   │   │   ├── upload.py      # CSV upload endpoint
│   │   │   ├── analytics.py   # Analytics endpoints
│   │   │   └── forecast.py    # Forecasting endpoint
│   │   ├── services/          # Business logic
│   │   │   ├── data_processor.py
│   │   │   └── forecaster.py
│   │   └── utils/             # Utility functions
│   │       └── validators.py
│   ├── requirements.txt        # Python dependencies
│   └── sample_data.csv        # Sample data for testing
│
├── Dockerfile                 # Multi-stage build for frontend & backend
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose** (for containerized deployment)
- OR
- **Node.js 18+** and **Python 3.11+** (for local development)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GAI
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Open your browser and navigate to `http://localhost:8000`
   - The app will be served with the built frontend

### Option 2: Local Development

#### Backend Setup

1. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server**
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```
   Server runs at `http://localhost:8000`

#### Frontend Setup

1. **Install Node dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```
   Frontend runs at `http://localhost:5173` (with API proxy to `http://localhost:8000`)

## API Endpoints

### Health & Status
- `GET /health` - Health check endpoint

### Upload
- `POST /api/upload` - Upload CSV file for analysis

### Analytics
- `GET /api/analytics/summary` - Get sales summary (total revenue, units sold, etc.)
- `GET /api/analytics/trends` - Get monthly sales trends
- `GET /api/analytics/top-products` - Get top selling products (limit: 10)
- `GET /api/analytics/fabric-breakdown` - Get sales breakdown by fabric type
- `GET /api/analytics/alerts` - Get inventory alerts (days_threshold: 10)

### Forecasting
- `GET /api/forecast` - Get sales forecast data

## CSV Format

Upload your sales data in the following CSV format:

```csv
Date,ProductName,FabricType,Quantity,Price,Revenue
2024-01-01,Product A,Cotton,100,50,5000
2024-01-02,Product B,Silk,50,100,5000
```

**Required columns:**
- `Date` - Date of sale (YYYY-MM-DD format)
- `ProductName` - Name of the product
- `FabricType` - Type of fabric
- `Quantity` - Units sold
- `Price` - Price per unit
- `Revenue` - Total revenue (Quantity × Price)

## Usage

1. **Upload Data**: Click the "Upload CSV" button and select your CSV file
2. **View Analytics**: After upload, the dashboard displays:
   - Total revenue, units sold, and average order value
   - Monthly sales trends chart
   - Top-selling products
   - Fabric type breakdown
   - Inventory alerts for slow-moving items
3. **Forecasting**: View predicted sales trends for future periods

## Building for Production

### Build Frontend
```bash
cd frontend
npm run build
```
Built files will be in `frontend/dist/`

### Build Docker Image
```bash
docker build -t textile-analytics:latest .
```

### Run Production Container
```bash
docker run -p 8000:8000 textile-analytics:latest
```

## Deployment on Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set the build command: `npm --prefix frontend run build`
5. Set the start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1`
6. Deploy

The application uses a multi-stage Docker build that:
- Builds the frontend with Node.js
- Copies the built files to the Python backend
- Serves the frontend as static files from the FastAPI app

## Performance Considerations

- Data is processed in-memory; for large datasets (100K+ rows), consider implementing database storage
- Forecasting uses exponential smoothing; for more advanced predictions, consider time-series models like ARIMA or Prophet
- Consider implementing caching for frequently accessed endpoints

## Troubleshooting

### White Screen on Load
Ensure `StaticFiles` is properly mounted at `/` in FastAPI and the frontend build is in the `static/` directory.

### API Errors
1. Check that the backend is running (`GET /health` should return `{"status": "healthy"}`)
2. Verify CORS is enabled in `backend/app/main.py`
3. Ensure the upload endpoint has the correct CSV format

### Upload Fails
- Verify CSV file uses UTF-8 encoding
- Check that required columns are present: `Date`, `ProductName`, `FabricType`, `Quantity`, `Price`, `Revenue`
- Date format should be YYYY-MM-DD

## Future Enhancements

- [ ] Database integration (PostgreSQL)
- [ ] User authentication
- [ ] Export reports to PDF
- [ ] Advanced forecasting models
- [ ] Real-time data streaming
- [ ] Mobile app
- [ ] Multi-language support

## License

This project is created by **TheSkynet**.

## Support

For issues or questions, please create an issue in the repository.

---

**Happy analyzing! 📊**
