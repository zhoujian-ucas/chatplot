# ChatPlot API Documentation

## Overview

The ChatPlot API provides endpoints for data analysis, visualization, and chat functionality.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication.

## Endpoints

### Chat

#### POST /api/chat/message
Send a message to the chat interface.

**Request Body:**
```json
{
  "message": "string",
  "context": "string",
  "session_id": "string"
}
```

**Response:**
```json
{
  "response": "string",
  "visualization": {
    "type": "string",
    "data": {}
  },
  "session_id": "string"
}
```

### Data Analysis

#### POST /api/data/analyze
Analyze uploaded data.

**Request Body:**
```json
{
  "file_path": "string",
  "analysis_type": "string",
  "parameters": {}
}
```

**Response:**
```json
{
  "results": {},
  "visualizations": [],
  "insights": []
}
```

### Visualization

#### POST /api/visualization/create
Create a visualization from data.

**Request Body:**
```json
{
  "data": {},
  "type": "string",
  "parameters": {}
}
```

**Response:**
```json
{
  "visualization": {},
  "type": "string"
}
```

### WebSocket

#### WS /ws/chat
Real-time chat communication.

**Message Format:**
```json
{
  "type": "string",
  "data": {},
  "session_id": "string"
}
```

## Error Responses

```json
{
  "error": "string",
  "detail": "string",
  "status_code": number
}
```

## Rate Limiting

- 100 requests per minute per IP
- WebSocket connections limited to 1 per client

## Data Formats

### Supported File Types
- CSV
- Excel (xlsx, xls)
- JSON
- Parquet

### Visualization Types
- Line Chart
- Bar Chart
- Scatter Plot
- Histogram
- Box Plot
- Heatmap
- Pie Chart 