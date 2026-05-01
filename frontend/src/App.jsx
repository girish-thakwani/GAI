// filepath: frontend/src/App.jsx
import { useState, useEffect, useRef } from 'react'
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, Area, AreaChart, Legend 
} from 'recharts'
import { 
  Upload, DollarSign, ShoppingCart, TrendingUp, Package, 
  AlertTriangle, CheckCircle, XCircle, Loader2 
} from 'lucide-react'

// API Base URL
const API_BASE = '/api'

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [toast, setToast] = useState(null)
  const fileInputRef = useRef(null)

  // Show toast notification
  const showToast = (message, type = 'success') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 4000)
  }

  // Handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    if (!file.name.endsWith('.csv')) {
      showToast('Only CSV files are accepted', 'error')
      return
    }

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData
      })

      const result = await response.json()

      if (result.success) {
        showToast(`Successfully loaded ${result.records_processed} records`, 'success')
        await fetchAnalytics()
      } else {
        showToast(result.detail || 'Failed to upload file', 'error')
      }
    } catch (error) {
      showToast('Error uploading file: ' + error.message, 'error')
    } finally {
      setUploading(false)
      event.target.value = ''
    }
  }

  // Fetch analytics data
  const fetchAnalytics = async () => {
    setLoading(true)
    try {
      const [summary, trends, topProducts, fabric, alerts, forecast] = await Promise.all([
        fetch(`${API_BASE}/analytics/summary`).then(r => r.json()).catch(() => null),
        fetch(`${API_BASE}/analytics/trends`).then(r => r.json()).catch(() => []),
        fetch(`${API_BASE}/analytics/top-products`).then(r => r.json()).catch(() => []),
        fetch(`${API_BASE}/analytics/fabric-breakdown`).then(r => r.json()).catch(() => []),
        fetch(`${API_BASE}/analytics/alerts`).then(r => r.json()).catch(() => []),
        fetch(`${API_BASE}/forecast`).then(r => r.json()).catch(() => null)
      ])

      setData({
        summary,
        trends,
        topProducts,
        fabric,
        alerts,
        forecast
      })
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  // Format currency
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(value)
  }

  // Custom tooltip for charts
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="label">{label}</p>
          <p className="value" style={{ color: payload[0].color }}>
            {formatCurrency(payload[0].value)}
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="logo">
            <TrendingUp size={24} />
          </div>
          <div>
            <h1>Textile Sales Analytics</h1>
            <p className="header-subtitle">By TheSkynet</p>
          </div>
        </div>
        <div>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept=".csv"
            className="file-input"
          />
          <button 
            className={`upload-btn ${uploading ? 'loading' : ''}`}
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
          >
            {uploading ? (
              <>
                <Loader2 size={18} className="spinner" />
                Processing...
              </>
            ) : (
              <>
                <Upload size={18} />
                Upload CSV
              </>
            )}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-container">
        {!data && !loading && (
          <div className="empty-state">
            <div className="empty-state-icon">
              <Upload size={40} />
            </div>
            <h2>Welcome to Textile Sales Analytics</h2>
            <p>Upload your CSV file to get started with sales analytics, trends, and forecasting.</p>
            <button 
              className="upload-btn"
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload size={18} />
              Upload CSV File
            </button>
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
              Loading analytics...
            </p>
          </div>
        )}

        {data && !loading && (
          <>
            {/* KPI Cards */}
            <div className="kpi-grid">
              <div className="kpi-card">
                <div className="kpi-header">
                  <div className="kpi-icon revenue">
                    <DollarSign size={24} />
                  </div>
                  <div className="kpi-trend up">
                    <TrendingUp size={14} />
                    +12.5%
                  </div>
                </div>
                <p className="kpi-label">Total Revenue</p>
                <p className="kpi-value">{formatCurrency(data.summary?.total_revenue || 0)}</p>
              </div>

              <div className="kpi-card">
                <div className="kpi-header">
                  <div className="kpi-icon orders">
                    <ShoppingCart size={24} />
                  </div>
                  <div className="kpi-trend up">
                    <TrendingUp size={14} />
                    +8.3%
                  </div>
                </div>
                <p className="kpi-label">Total Orders</p>
                <p className="kpi-value">{data.summary?.total_orders?.toLocaleString() || 0}</p>
              </div>

              <div className="kpi-card">
                <div className="kpi-header">
                  <div className="kpi-icon product">
                    <Package size={24} />
                  </div>
                </div>
                <p className="kpi-label">Top Product</p>
                <p className="kpi-value" style={{ fontSize: '1.25rem' }}>
                  {data.summary?.top_product || 'N/A'}
                </p>
              </div>

              <div className="kpi-card">
                <div className="kpi-header">
                  <div className="kpi-icon avg">
                    <TrendingUp size={24} />
                  </div>
                  <div className="kpi-trend down">
                    <TrendingUp size={14} style={{ transform: 'rotate(180deg)' }} />
                    -2.1%
                  </div>
                </div>
                <p className="kpi-label">Avg Order Value</p>
                <p className="kpi-value">{formatCurrency(data.summary?.avg_order_value || 0)}</p>
              </div>
            </div>

            {/* Charts Grid */}
            <div className="charts-grid">
              {/* Sales Trends */}
              <div className="chart-card">
                <div className="chart-header">
                  <div>
                    <h3 className="chart-title">Monthly Sales Trends</h3>
                    <p className="chart-subtitle">Revenue over time</p>
                  </div>
                </div>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={data.trends}>
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#2A9D8F" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#2A9D8F" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} />
                    <Tooltip content={<CustomTooltip />} />
                    <Area 
                      type="monotone" 
                      dataKey="revenue" 
                      stroke="#2A9D8F" 
                      fillOpacity={1} 
                      fill="url(#colorRevenue)" 
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              {/* Top Products */}
              <div className="chart-card">
                <div className="chart-header">
                  <div>
                    <h3 className="chart-title">Top Products</h3>
                    <p className="chart-subtitle">By revenue</p>
                  </div>
                </div>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={data.topProducts} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" tick={{ fontSize: 12 }} tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} />
                    <YAxis type="category" dataKey="product_name" width={120} tick={{ fontSize: 11 }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="revenue" fill="#F4A261" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Forecast Chart */}
            <div className="forecast-section">
              <div className="chart-header">
                <div>
                  <h3 className="chart-title">Sales Forecast</h3>
                  <p className="chart-subtitle">
                    Historical data + 30-day prediction ({data.forecast?.model_used || 'N/A'})
                  </p>
                </div>
              </div>
              <ResponsiveContainer width="100%" height={350}>
                <LineChart data={[...(data.forecast?.historical || []), ...(data.forecast?.forecast || [])]}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tick={{ fontSize: 11 }} 
                    tickFormatter={(v) => {
                      const date = new Date(v)
                      return `${date.getMonth() + 1}/${date.getDate()}`
                    }}
                  />
                  <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `₹${(v/1000).toFixed(0)}k`} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="predicted_revenue" 
                    stroke="#1E3A5F" 
                    strokeWidth={2}
                    dot={false}
                    strokeDasharray="5 5"
                    name="Forecast"
                  />
                  <Line 
                    type="monotone" 
                    dataKey={(d) => d.is_historical ? d.predicted_revenue : null} 
                    stroke="#2A9D8F" 
                    strokeWidth={2}
                    dot={false}
                    name="Historical"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Inventory Alerts */}
            {data.alerts && data.alerts.length > 0 && (
              <div className="alerts-section">
                <div className="chart-header">
                  <div>
                    <h3 className="chart-title">Inventory Alerts</h3>
                    <p className="chart-subtitle">Products requiring attention</p>
                  </div>
                </div>
                <table className="alerts-table">
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Fabric Type</th>
                      <th>Daily Velocity</th>
                      <th>Days Until Stockout</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.alerts.map((alert, idx) => (
                      <tr key={idx}>
                        <td>{alert.product_name}</td>
                        <td>{alert.fabric_type}</td>
                        <td>{alert.current_velocity} units/day</td>
                        <td>{alert.days_until_stockout} days</td>
                        <td>
                          <span className={`status-badge ${alert.status}`}>
                            {alert.status === 'critical' && <AlertTriangle size={12} style={{ marginRight: 4 }} />}
                            {alert.status === 'warning' && <AlertTriangle size={12} style={{ marginRight: 4 }} />}
                            {alert.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </main>

      {/* Toast Notification */}
      {toast && (
        <div className={`toast ${toast.type}`}>
          {toast.type === 'success' ? <CheckCircle size={20} /> : <XCircle size={20} />}
          {toast.message}
        </div>
      )}
    </div>
  )
}

export default App