# API Documentation

## Overview

ChatPlot provides a RESTful API and WebSocket endpoints for data analysis and visualization. This document describes the available endpoints and their usage.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication for local development. For production deployment, implement appropriate authentication mechanisms.

## API Endpoints

### Data Management

#### Upload Data

```http
POST /api/data/upload
Content-Type: multipart/form-data
```

Upload a data file for analysis.

**Parameters:**
- `file`: The data file (CSV, Excel, or JSON)
- `type`: File type (optional, auto-detected if not provided)

**Response:**
```json
{
    "status": "success",
    "file_id": "string",
    "summary": {
        "rows": "integer",
        "columns": "integer",
        "column_types": "object"
    }
}
```

#### Get Data Summary

```http
GET /api/data/{file_id}/summary
```

Get summary statistics for uploaded data.

**Response:**
```json
{
    "shape": [100, 5],
    "columns": ["col1", "col2"],
    "numeric_columns": ["col1"],
    "categorical_columns": ["col2"],
    "missing_values": {"col1": 0},
    "numeric_summary": {
        "col1": {
            "mean": 0.0,
            "std": 1.0
        }
    }
}
```

### Analysis

#### Generate Analysis

```http
POST /api/analysis/generate
Content-Type: application/json
```

Generate analysis for the data.

**Request Body:**
```json
{
    "file_id": "string",
    "query": "string",
    "analysis_type": "string"
}
```

**Response:**
```json
{
    "analysis_type": "string",
    "visualization_type": "string",
    "insights": [
        {
            "type": "string",
            "description": "string",
            "importance": 0,
            "confidence": 0.0
        }
    ]
}
```

### Visualization

#### Create Visualization

```http
POST /api/visualization/create
Content-Type: application/json
```

Create a visualization from data.

**Request Body:**
```json
{
    "file_id": "string",
    "viz_type": "string",
    "x_column": "string",
    "y_column": "string",
    "title": "string"
}
```

**Response:**
```json
{
    "chart": "string",
    "metadata": {
        "x_column": "string",
        "y_column": "string",
        "viz_type": "string"
    }
}
```

### Chat

#### WebSocket Connection

```
ws://localhost:8000/ws/chat
```

Establish WebSocket connection for real-time chat.

**Message Format:**
```json
{
    "type": "string",
    "content": "string",
    "file_id": "string"
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
    "status": "error",
    "message": "string",
    "details": "object"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented for local development. For production deployment, implement appropriate rate limiting. 