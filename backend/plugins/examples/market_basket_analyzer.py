from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from ..base import PluginMetadata, AnalysisPlugin

class MarketBasketAnalyzerPlugin(AnalysisPlugin):
    """A plugin that performs market basket analysis on transaction data."""
    
    def __init__(self):
        self._config = {}
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="market_basket_analyzer",
            version="1.0.0",
            description="Performs market basket analysis to discover item associations",
            author="ChatPlot",
            dependencies=["pandas", "numpy", "mlxtend"],
            entry_point="MarketBasketAnalyzerPlugin",
            config_schema={
                "type": "object",
                "properties": {
                    "min_support": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "min_confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "min_lift": {
                        "type": "number",
                        "minimum": 0
                    },
                    "max_length": {
                        "type": "integer",
                        "minimum": 2
                    }
                }
            }
        )
    
    def initialize(self, config: Optional[Dict] = None) -> None:
        """Initialize the plugin with configuration."""
        default_config = {
            "min_support": 0.01,
            "min_confidence": 0.5,
            "min_lift": 1.0,
            "max_length": 3
        }
        self._config = {**default_config, **(config or {})}
    
    def shutdown(self) -> None:
        """Clean up resources."""
        pass
    
    def analyze_data(self, data: Any, **kwargs) -> Dict:
        """Perform market basket analysis on transaction data."""
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame")
        
        # Extract required columns
        transaction_id = kwargs.get("transaction_id")
        item_id = kwargs.get("item_id")
        
        if not transaction_id or not item_id:
            raise ValueError("Transaction and item columns must be specified")
        
        if transaction_id not in data.columns or item_id not in data.columns:
            raise ValueError("Specified columns not found in DataFrame")
        
        # Create pivot table for basket analysis
        basket = (data.groupby([transaction_id, item_id])
                 .size()
                 .unstack()
                 .fillna(0)
                 .astype(bool))
        
        try:
            # Find frequent itemsets
            frequent_itemsets = apriori(
                basket,
                min_support=self._config["min_support"],
                max_len=self._config["max_length"],
                use_colnames=True
            )
            
            # Generate association rules
            rules = association_rules(
                frequent_itemsets,
                metric="confidence",
                min_threshold=self._config["min_confidence"]
            )
            
            # Filter rules by lift
            rules = rules[rules["lift"] >= self._config["min_lift"]]
            
            # Prepare results
            results = {
                "frequent_itemsets": self._format_frequent_itemsets(frequent_itemsets),
                "association_rules": self._format_association_rules(rules),
                "summary": self._generate_summary(rules)
            }
            
            return results
            
        except Exception as e:
            return {
                "error": str(e),
                "frequent_itemsets": None,
                "association_rules": None,
                "summary": None
            }
    
    def _format_frequent_itemsets(self, frequent_itemsets: pd.DataFrame) -> List[Dict]:
        """Format frequent itemsets for output."""
        formatted_itemsets = []
        
        for _, row in frequent_itemsets.iterrows():
            itemset = {
                "items": list(row["itemsets"]),
                "support": row["support"],
                "length": len(row["itemsets"])
            }
            formatted_itemsets.append(itemset)
        
        return formatted_itemsets
    
    def _format_association_rules(self, rules: pd.DataFrame) -> List[Dict]:
        """Format association rules for output."""
        formatted_rules = []
        
        for _, row in rules.iterrows():
            rule = {
                "antecedents": list(row["antecedents"]),
                "consequents": list(row["consequents"]),
                "support": row["support"],
                "confidence": row["confidence"],
                "lift": row["lift"],
                "leverage": row["leverage"],
                "conviction": row["conviction"]
            }
            formatted_rules.append(rule)
        
        return formatted_rules
    
    def _generate_summary(self, rules: pd.DataFrame) -> Dict:
        """Generate summary statistics for the analysis."""
        if len(rules) == 0:
            return {
                "total_rules": 0,
                "avg_confidence": None,
                "avg_lift": None,
                "max_lift": None,
                "strong_rules": 0
            }
        
        return {
            "total_rules": len(rules),
            "avg_confidence": rules["confidence"].mean(),
            "avg_lift": rules["lift"].mean(),
            "max_lift": rules["lift"].max(),
            "strong_rules": len(rules[rules["confidence"] >= 0.8])
        } 