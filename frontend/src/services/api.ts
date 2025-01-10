import config from '../config';

export interface AnalysisResult {
  chart: string;
  analysis: {
    analysis_type: string;
    visualization_type: string;
    insights: string[];
    recommendations: string[];
  };
  metadata: {
    x_column: string;
    y_column: string;
    viz_type: string;
  };
}

class ApiService {
  private baseUrl: string;
  private wsUrl: string;

  constructor() {
    this.baseUrl = config.api.baseUrl;
    this.wsUrl = config.api.wsUrl;
  }

  async analyzeData(file: File): Promise<AnalysisResult> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/api/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Failed to analyze data');
    }

    return response.json();
  }

  createChatWebSocket(
    onMessage: (data: string) => void,
    onError: (error: Event) => void
  ): WebSocket {
    const clientId = Math.random().toString(36).substring(7);
    const ws = new WebSocket(`${this.wsUrl}/ws/${clientId}`);

    ws.onmessage = (event) => {
      onMessage(event.data);
    };

    ws.onerror = (error) => {
      onError(error);
    };

    return ws;
  }
}

export const apiService = new ApiService(); 