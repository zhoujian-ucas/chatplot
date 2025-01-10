# ChatPlot

<div align="center">

![ChatPlot Logo](docs/images/logo.png)

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

ChatPlot is an intelligent data analysis and visualization platform that combines natural language chat interface with powerful data processing capabilities. It enables users to analyze and visualize data through intuitive conversations, powered by Ollama's local LLM technology.

## ✨ Features

### 🤖 Intelligent Chat Interface
- Natural language data analysis queries
- Context-aware conversations
- Automated insights generation
- Smart visualization suggestions

### 📊 Advanced Data Analysis
- Support for multiple data formats (CSV, Excel, JSON)
- Automated data cleaning and preprocessing
- Statistical analysis and pattern detection
- Correlation analysis and trend identification

### 📈 Interactive Visualizations
- Real-time interactive charts
- Multiple visualization types
- Customizable chart options
- Export capabilities

### 🛠 Technical Features
- Local LLM integration with Ollama
- Real-time data processing
- Automated health monitoring
- Cross-platform compatibility

## 🚀 Quick Start

### Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Git](https://git-scm.com/downloads)
- [Ollama](https://ollama.ai/download) with llama2 model

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chatplot.git
cd chatplot
```

2. One-click setup and run:
```bash
python start.py
```

Or follow the manual setup:

1. Create and activate the Conda environment:
```bash
conda env create -f environment.yml
conda activate chatplot
```

2. Configure environment:
```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

3. Start the application:
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm install
npm run dev
```

## 🏗 Project Structure

```
chatplot/
├── backend/                 # Backend server
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   │   ├── data_service.py     # Data processing
│   │   ├── ollama_service.py   # LLM integration
│   │   └── visualization_service.py  # Chart generation
│   ├── utils/              # Utility functions
│   └── main.py            # FastAPI application
├── frontend/               # Frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   └── App.tsx       # Main application
│   └── package.json
├── data/                   # Data storage
│   ├── uploads/           # User uploads
│   └── sample/            # Sample datasets
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── docs/                   # Documentation
├── environment.yml         # Conda environment
├── requirements.txt        # Python dependencies
├── start.py               # Startup script
└── README.md
```

## 💻 Development

### Backend Development

The backend is built with FastAPI and provides:
- RESTful API endpoints
- WebSocket connections for real-time updates
- Data processing and analysis services
- Visualization generation
- Health monitoring

### Frontend Development

The frontend is built with React and TypeScript:
- Modern UI with Ant Design
- Interactive data visualization with Plotly
- Real-time WebSocket communication
- Responsive design

### Quality Assurance

```bash
# Run tests
pytest

# Code formatting
black .
isort .

# Type checking
mypy .

# Linting
flake8

# Run all checks
pre-commit run --all-files
```

### Health Monitoring

```bash
# Check system health
python backend/utils/health_check.py

# View health report
cat health_report.json
```

## 📊 Supported Visualizations

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

## 🔧 Configuration

Key configuration options in `.env`:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Data Storage
UPLOAD_DIR=./data/uploads
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pre-commit install`)
4. Make your changes
5. Run tests and checks (`pytest && pre-commit run --all-files`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://reactjs.org/) - Frontend framework
- [Ollama](https://ollama.ai/) - Local LLM technology
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Ant Design](https://ant.design/) - UI components
- [Pandas](https://pandas.pydata.org/) - Data processing
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM

## 📚 Documentation

For detailed documentation, please visit:
- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## 🚀 Roadmap

- [ ] Support for more data sources
- [ ] Advanced ML/AI analysis features
- [ ] Custom visualization templates
- [ ] Collaborative features
- [ ] Export to various formats
- [ ] Plugin system

## 📧 Contact

- Project Link: [https://github.com/yourusername/chatplot](https://github.com/yourusername/chatplot)
- Report Bugs: [Issues](https://github.com/yourusername/chatplot/issues) 