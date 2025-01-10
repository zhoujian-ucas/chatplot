# Development Guide

## Development Environment Setup

### Prerequisites

1. Install development tools:
   - Python 3.10+
   - Node.js 20+
   - Git
   - Visual Studio Code (recommended)
   - Docker (optional)

2. Clone the repository:
```bash
git clone https://github.com/yourusername/chatplot.git
cd chatplot
```

3. Set up the development environment:
```bash
# Create and activate Conda environment
conda env create -f environment.yml
conda activate chatplot

# Install pre-commit hooks
pre-commit install

# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Project Structure

### Backend

```
backend/
├── models/             # Database models
│   ├── __init__.py
│   └── database.py
├── services/          # Business logic
│   ├── __init__.py
│   ├── data_service.py
│   ├── ollama_service.py
│   └── visualization_service.py
├── utils/            # Utility functions
│   ├── __init__.py
│   ├── helpers.py
│   └── health_check.py
├── tests/           # Test files
│   ├── __init__.py
│   ├── test_data_service.py
│   └── test_visualization_service.py
└── main.py         # FastAPI application
```

### Frontend

```
frontend/
├── src/
│   ├── components/   # React components
│   ├── services/     # API services
│   ├── hooks/        # Custom hooks
│   ├── utils/        # Utility functions
│   ├── types/        # TypeScript types
│   └── App.tsx
├── public/          # Static files
└── package.json
```

## Development Workflow

### Code Style

We use the following tools to maintain code quality:

1. Python:
```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy .

# Linting
flake8

# Run all checks
pre-commit run --all-files
```

2. TypeScript/JavaScript:
```bash
# Format code
npm run format

# Lint
npm run lint

# Type check
npm run type-check
```

### Testing

1. Backend tests:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_data_service.py
```

2. Frontend tests:
```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Git Workflow

1. Create a new branch:
```bash
git checkout -b feature/your-feature
```

2. Make changes and commit:
```bash
git add .
git commit -m "Add your feature"
```

3. Push changes:
```bash
git push origin feature/your-feature
```

4. Create a Pull Request

### Database Migrations

Using SQLAlchemy migrations:

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Development

### Adding New Endpoints

1. Create route in `main.py`:
```python
@app.post("/api/new-endpoint")
async def new_endpoint(data: NewEndpointSchema):
    result = await service.process(data)
    return result
```

2. Add schema in `models`:
```python
class NewEndpointSchema(BaseModel):
    field1: str
    field2: Optional[int]
```

3. Implement service logic
4. Add tests
5. Update API documentation

### WebSocket Development

1. Create new WebSocket endpoint:
```python
@app.websocket("/ws/new-socket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            response = await process_ws_message(data)
            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass
```

2. Implement message handling
3. Add error handling
4. Add tests

## Frontend Development

### Adding New Components

1. Create component file:
```tsx
// src/components/NewComponent.tsx
import React from 'react';

interface Props {
    data: any;
}

export const NewComponent: React.FC<Props> = ({ data }) => {
    return (
        <div>
            {/* Component content */}
        </div>
    );
};
```

2. Add styles:
```css
/* src/components/NewComponent.css */
.new-component {
    /* styles */
}
```

3. Add tests:
```tsx
// src/components/__tests__/NewComponent.test.tsx
import { render } from '@testing-library/react';
import { NewComponent } from '../NewComponent';

describe('NewComponent', () => {
    it('renders correctly', () => {
        const { container } = render(<NewComponent data={mockData} />);
        expect(container).toMatchSnapshot();
    });
});
```

### State Management

Using React Context and Hooks:

```tsx
// src/context/DataContext.tsx
export const DataContext = createContext<DataContextType | undefined>(undefined);

export const DataProvider: React.FC = ({ children }) => {
    const [data, setData] = useState<Data | null>(null);

    return (
        <DataContext.Provider value={{ data, setData }}>
            {children}
        </DataContext.Provider>
    );
};
```

## Building and Deployment

### Development Build

1. Backend:
```bash
uvicorn main:app --reload --port 8000
```

2. Frontend:
```bash
npm run dev
```

### Production Build

1. Backend:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Frontend:
```bash
npm run build
```

### Docker Build

```bash
# Build images
docker-compose build

# Run services
docker-compose up -d
```

## Monitoring and Debugging

### Health Checks

```bash
# Run health check
python backend/utils/health_check.py

# View logs
tail -f logs/app.log
```

### Performance Monitoring

1. Backend:
- Use FastAPI's built-in performance metrics
- Monitor database query performance
- Track memory usage

2. Frontend:
- Use React DevTools
- Monitor bundle size
- Track component re-renders

## Documentation

### Updating Documentation

1. API documentation:
- Update OpenAPI specs
- Update API examples
- Test all endpoints

2. User documentation:
- Update user guide
- Add new features
- Update screenshots

3. Development documentation:
- Update setup instructions
- Document new tools/processes
- Update troubleshooting guide 