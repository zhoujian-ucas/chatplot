import requests
import logging
import json
from typing import Dict, Any, Optional, List
from config import settings

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, base_url: str = settings.OLLAMA_BASE_URL):
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        self.context: Dict[str, List[Dict[str, str]]] = {}

    async def generate_response(
        self,
        prompt: str,
        client_id: str,
        model: str = settings.OLLAMA_MODEL,
        system_prompt: Optional[str] = None,
        keep_context: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a response from Ollama model with context management
        """
        try:
            # Initialize context for new clients
            if client_id not in self.context:
                self.context[client_id] = []

            # Build conversation history
            conversation = self.context[client_id][-5:] if keep_context else []  # Keep last 5 messages
            
            # Prepare the prompt with context
            full_prompt = self._build_prompt(prompt, conversation, system_prompt)
            
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_ctx": 2048,
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt

            response = requests.post(self.generate_url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Update conversation history
            if keep_context:
                self.context[client_id].append({"role": "user", "content": prompt})
                self.context[client_id].append({"role": "assistant", "content": result["response"]})

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            raise Exception(f"Failed to get response from Ollama: {str(e)}")

    async def analyze_data(
        self,
        prompt: str,
        data_context: Dict[str, Any],
        client_id: str,
        model: str = settings.OLLAMA_MODEL
    ) -> Dict[str, Any]:
        """
        Analyze data using Ollama model with enhanced context
        """
        system_prompt = """You are an expert data analyst assistant. Your task is to:
1. Analyze the provided data summary and context
2. Identify key patterns, trends, and insights
3. Suggest appropriate visualizations
4. Provide actionable recommendations

Format your response as JSON with the following structure:
{
    "analysis_type": "string (basic|correlation|trend|distribution)",
    "visualization_type": "string (line|bar|scatter|pie|heatmap|boxplot|histogram)",
    "insights": [
        {
            "type": "string (pattern|trend|anomaly|correlation)",
            "description": "string",
            "importance": "number (1-5)",
            "confidence": "number (0-1)"
        }
    ],
    "recommendations": [
        {
            "action": "string",
            "reason": "string",
            "priority": "number (1-5)"
        }
    ],
    "suggested_visualizations": [
        {
            "type": "string",
            "title": "string",
            "description": "string",
            "columns": ["string"]
        }
    ]
}"""

        # Prepare detailed data context
        context_prompt = f"""
Data Summary:
{json.dumps(data_context['summary'], indent=2)}

Column Information:
- Numeric columns: {', '.join(data_context['summary']['numeric_columns'])}
- Categorical columns: {', '.join(data_context['summary']['categorical_columns'])}

Data Quality:
- Missing values: {json.dumps(data_context['summary']['missing_values'])}
- Sample size: {data_context['summary']['shape'][0]} rows, {data_context['summary']['shape'][1]} columns

User Request:
{prompt}

Please provide a comprehensive analysis focusing on the most relevant insights and appropriate visualizations.
"""

        try:
            response = await self.generate_response(
                prompt=context_prompt,
                client_id=client_id,
                model=model,
                system_prompt=system_prompt,
                keep_context=False  # Don't keep analysis context in chat history
            )

            # Parse and validate the response
            try:
                analysis = json.loads(response["response"])
                return self._validate_analysis_response(analysis)
            except json.JSONDecodeError:
                logger.error("Failed to parse Ollama response as JSON")
                return self._generate_fallback_analysis()

        except Exception as e:
            logger.error(f"Error in data analysis: {str(e)}")
            raise

    def _build_prompt(
        self,
        prompt: str,
        conversation: List[Dict[str, str]],
        system_prompt: Optional[str]
    ) -> str:
        """
        Build a prompt with conversation history
        """
        if not conversation:
            return prompt

        context_str = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in conversation
        ])
        
        return f"""Previous conversation:
{context_str}

Current request:
{prompt}"""

    def _validate_analysis_response(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean up the analysis response
        """
        required_fields = [
            "analysis_type",
            "visualization_type",
            "insights",
            "recommendations"
        ]

        for field in required_fields:
            if field not in analysis:
                analysis[field] = []

        return analysis

    def _generate_fallback_analysis(self) -> Dict[str, Any]:
        """
        Generate a fallback analysis when the model response is invalid
        """
        return {
            "analysis_type": "basic",
            "visualization_type": "bar",
            "insights": [
                {
                    "type": "error",
                    "description": "Failed to generate detailed analysis",
                    "importance": 5,
                    "confidence": 1.0
                }
            ],
            "recommendations": [
                {
                    "action": "Please try again with a more specific request",
                    "reason": "The analysis engine encountered an error",
                    "priority": 5
                }
            ],
            "suggested_visualizations": [
                {
                    "type": "bar",
                    "title": "Basic Overview",
                    "description": "Basic data overview",
                    "columns": []
                }
            ]
        }

    def clear_context(self, client_id: str) -> None:
        """
        Clear conversation history for a client
        """
        if client_id in self.context:
            self.context[client_id] = [] 