# User Guide

## Introduction

Welcome to ChatPlot! This guide will help you get started with using the platform for data analysis and visualization.

## Getting Started

### Installation

1. Install prerequisites:
   - Anaconda or Miniconda
   - Git
   - Ollama with llama2 model

2. Clone and setup:
```bash
git clone https://github.com/yourusername/chatplot.git
cd chatplot
python start.py
```

3. Open your browser and navigate to `http://localhost:5173`

## Using ChatPlot

### Data Upload

1. Click the "Upload" button in the sidebar
2. Select your data file (CSV, Excel, or JSON)
3. Wait for the upload and automatic analysis
4. View the data summary

### Chat Interface

The chat interface allows you to:
- Ask questions about your data
- Request specific analyses
- Generate visualizations
- Export results

Example queries:
- "Show me a summary of the data"
- "Create a scatter plot of price vs. size"
- "What are the main trends in this dataset?"
- "Calculate correlation between these variables"

### Data Analysis

#### Basic Analysis
- Data summary
- Column statistics
- Missing value analysis
- Distribution analysis

#### Advanced Analysis
- Correlation analysis
- Trend detection
- Pattern recognition
- Outlier detection

### Visualizations

Available chart types:
- Line charts
- Bar charts
- Scatter plots
- Histograms
- Box plots
- Violin plots
- Heatmaps
- Pie charts
- Area charts
- Parallel coordinates
- Scatter matrix
- Sunburst diagrams

### Customization

Each visualization can be customized:
- Chart type
- Colors
- Labels
- Title
- Size
- Legend position
- Axis settings

### Exporting Results

You can export:
- Charts as PNG/SVG
- Data as CSV/Excel
- Analysis reports as PDF
- Chat history

## Tips and Best Practices

1. Data Preparation
   - Clean your data before upload
   - Use consistent formatting
   - Handle missing values

2. Analysis
   - Start with basic analysis
   - Look for patterns
   - Validate assumptions
   - Consider context

3. Visualization
   - Choose appropriate chart types
   - Keep it simple
   - Use clear labels
   - Consider color accessibility

## Troubleshooting

### Common Issues

1. Upload Problems
   - Check file format
   - Verify file size
   - Ensure proper permissions

2. Analysis Errors
   - Check data types
   - Look for missing values
   - Verify column names

3. Visualization Issues
   - Check data compatibility
   - Verify column selection
   - Review chart settings

### Error Messages

Common error messages and solutions:
- "File format not supported": Use CSV, Excel, or JSON
- "Column not found": Verify column names
- "Invalid data type": Check data formatting
- "Connection error": Check network connection

## Support

If you encounter issues:
1. Check the troubleshooting guide
2. Review error messages
3. Check GitHub issues
4. Create a new issue if needed

## Keyboard Shortcuts

- `Ctrl + U`: Upload file
- `Ctrl + Enter`: Send message
- `Ctrl + S`: Save chart
- `Esc`: Clear input
- `Alt + N`: New chat

## Privacy and Security

- Data is processed locally
- No data is sent to external servers
- Use environment variables for sensitive settings
- Implement authentication for production use

## Updates and Maintenance

To update ChatPlot:
1. Pull latest changes
```bash
git pull origin main
```

2. Update dependencies
```bash
conda env update -f environment.yml
```

3. Restart the application
```bash
python start.py
``` 