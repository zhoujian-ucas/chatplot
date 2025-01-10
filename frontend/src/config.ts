const config = {
  api: {
    baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:8000',
  },
  upload: {
    maxSize: 10 * 1024 * 1024, // 10MB
    acceptedFormats: ['.csv', '.xlsx', '.xls', '.json'],
  },
  charts: {
    defaultHeight: 400,
    colors: [
      '#1890ff',
      '#2fc25b',
      '#facc14',
      '#223273',
      '#8543e0',
      '#13c2c2',
      '#3436c7',
      '#f04864',
    ],
    types: {
      line: 'Line Chart',
      bar: 'Bar Chart',
      scatter: 'Scatter Plot',
      pie: 'Pie Chart',
      heatmap: 'Heat Map',
      boxplot: 'Box Plot',
      histogram: 'Histogram',
    },
  },
  chat: {
    maxMessages: 100,
    messageTypes: {
      user: 'user',
      assistant: 'assistant',
      system: 'system',
      error: 'error',
    },
  },
} as const;

export default config; 