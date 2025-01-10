import React, { useState } from 'react';
import { Upload, Button, Card, Space, message } from 'antd';
import { UploadOutlined, BarChartOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import type { UploadFile } from 'antd/es/upload/interface';
import './DataAnalysis.css';

interface AnalysisResult {
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

const DataAnalysis: React.FC = () => {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = async () => {
    if (fileList.length === 0) {
      message.warning('Please select a file first');
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    fileList.forEach(file => {
      if (file.originFileObj) {
        formData.append('file', file.originFileObj);
      }
    });

    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze data');
      }

      const result = await response.json();
      setAnalysisResult(result);
    } catch (error) {
      console.error('Error:', error);
      message.error('Failed to analyze data');
    } finally {
      setIsLoading(false);
    }
  };

  const getChartOption = () => {
    if (!analysisResult) return {};

    // Basic chart option template
    return {
      title: {
        text: `${analysisResult.metadata.viz_type} Chart`,
      },
      tooltip: {
        trigger: 'axis',
      },
      xAxis: {
        type: 'category',
        name: analysisResult.metadata.x_column,
      },
      yAxis: {
        type: 'value',
        name: analysisResult.metadata.y_column,
      },
      series: [
        {
          type: analysisResult.metadata.viz_type.toLowerCase(),
          data: [], // This would be populated with actual data
        },
      ],
    };
  };

  return (
    <div className="analysis-container">
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <Card title="Data Upload">
          <Upload
            fileList={fileList}
            onChange={({ fileList }) => setFileList(fileList)}
            beforeUpload={() => false}
          >
            <Button icon={<UploadOutlined />}>Select File</Button>
          </Upload>
          <Button
            type="primary"
            onClick={handleUpload}
            loading={isLoading}
            style={{ marginTop: 16 }}
            icon={<BarChartOutlined />}
          >
            Analyze Data
          </Button>
        </Card>

        {analysisResult && (
          <>
            <Card title="Visualization">
              <ReactECharts option={getChartOption()} style={{ height: 400 }} />
            </Card>

            <Card title="Analysis Insights">
              <h4>Insights:</h4>
              <ul>
                {analysisResult.analysis.insights.map((insight, index) => (
                  <li key={index}>{insight}</li>
                ))}
              </ul>

              <h4>Recommendations:</h4>
              <ul>
                {analysisResult.analysis.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </Card>
          </>
        )}
      </Space>
    </div>
  );
};

export default DataAnalysis; 