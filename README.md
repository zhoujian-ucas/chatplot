# ChatPlot - Ollama-Powered Chat Data Analysis

An interactive data analysis tool that combines chat interface with data visualization, powered by Ollama local LLM.

## Features

- Natural language chat interface with Ollama LLM
- Automatic data analysis based on chat context
- Real-time data visualization with multiple chart types
- Local data storage and management
- Support for various file formats (CSV, Excel, JSON)
- Interactive data exploration and analysis
- Customizable visualization options
- Historical chat and analysis tracking

## Prerequisites

- Python 3.8+
- Ollama installed locally (with llama2 model)
- Node.js and npm (for frontend)
- Modern web browser

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatplot.git
   cd chatplot
   ```

2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Modify settings as needed

6. Generate sample data (optional):
   ```bash
   python backend/scripts/generate_sample_data.py
   ```

## Running the Application

1. Start the Ollama server:
   ```bash
   ollama run llama2
   ```

2. Start the backend server:
   ```bash
   cd backend
   python main.py
   ```

3. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
chatplot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database session management
│   ├── models/              # SQLAlchemy models
│   ├── services/            # Business logic services
│   ├── utils/               # Utility functions
│   ├── scripts/             # Utility scripts
│   └── data/                # Data storage
│       ├── sample/          # Sample datasets
│       └── uploads/         # User uploads
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   └── package.json
├── requirements.txt         # Python dependencies
└── README.md
```

## Usage

1. **Chat Interface**
   - Start a conversation with the AI assistant
   - Ask questions about your data
   - Request specific analyses or visualizations

2. **Data Analysis**
   - Upload your data files (CSV, Excel, JSON)
   - Get automatic analysis and insights
   - Explore different visualization options

3. **Visualization**
   - View generated charts and graphs
   - Customize visualization parameters
   - Export visualizations

## Supported Data Formats

- CSV files
- Excel files (XLSX, XLS)
- JSON files
- Text files with structured data

## Supported Chart Types

- Line charts
- Bar charts
- Scatter plots
- Pie charts
- Heatmaps
- Box plots
- Histograms

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ollama team for providing the local LLM capability
- FastAPI for the powerful Python web framework
- React and Ant Design for the frontend components
- ECharts for the visualization library 