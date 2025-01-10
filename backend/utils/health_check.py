import psutil
import requests
import logging
from typing import Dict, Any, Optional
import os
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class HealthCheck:
    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.thresholds = {
            "cpu_percent": 90,
            "memory_percent": 85,
            "disk_percent": 90
        }

    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        try:
            self.metrics["cpu_percent"] = psutil.cpu_percent(interval=1)
            self.metrics["memory_percent"] = psutil.virtual_memory().percent
            self.metrics["disk_percent"] = psutil.disk_usage("/").percent
            
            return {
                "status": "healthy" if self._is_healthy() else "warning",
                "metrics": self.metrics,
                "warnings": self._get_warnings()
            }
        except Exception as e:
            logger.error(f"Error checking system resources: {str(e)}")
            return {"status": "error", "error": str(e)}

    def check_ollama_service(self) -> Dict[str, Any]:
        """Check Ollama service status"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "models": response.json()
                }
            return {"status": "error", "error": "Ollama service not responding"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking Ollama service: {str(e)}")
            return {"status": "error", "error": str(e)}

    def check_data_directories(self) -> Dict[str, Any]:
        """Check data directories and permissions"""
        try:
            data_dir = Path("data")
            uploads_dir = data_dir / "uploads"
            sample_dir = data_dir / "sample"
            
            status = {
                "data_dir": self._check_directory(data_dir),
                "uploads_dir": self._check_directory(uploads_dir),
                "sample_dir": self._check_directory(sample_dir)
            }
            
            return {
                "status": "healthy" if all(s["exists"] and s["writable"] for s in status.values()) else "warning",
                "directories": status
            }
        except Exception as e:
            logger.error(f"Error checking directories: {str(e)}")
            return {"status": "error", "error": str(e)}

    def check_database(self) -> Dict[str, Any]:
        """Check database connection and status"""
        try:
            from sqlalchemy import create_engine
            from config import settings
            
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as conn:
                return {
                    "status": "healthy",
                    "connection": "active"
                }
        except Exception as e:
            logger.error(f"Error checking database: {str(e)}")
            return {"status": "error", "error": str(e)}

    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        return {
            "system": self.check_system_resources(),
            "ollama": self.check_ollama_service(),
            "directories": self.check_data_directories(),
            "database": self.check_database()
        }

    def _is_healthy(self) -> bool:
        """Check if system metrics are within healthy thresholds"""
        return all(
            self.metrics.get(metric, 0) < threshold
            for metric, threshold in self.thresholds.items()
        )

    def _get_warnings(self) -> list[str]:
        """Get list of warning messages for metrics exceeding thresholds"""
        warnings = []
        for metric, threshold in self.thresholds.items():
            value = self.metrics.get(metric, 0)
            if value >= threshold:
                warnings.append(f"{metric} usage ({value}%) exceeds threshold ({threshold}%)")
        return warnings

    def _check_directory(self, path: Path) -> Dict[str, bool]:
        """Check if directory exists and is writable"""
        return {
            "exists": path.exists(),
            "writable": os.access(path, os.W_OK) if path.exists() else False
        }

    def save_report(self, report: Dict[str, Any], path: Optional[str] = None) -> str:
        """Save health check report to file"""
        try:
            if path is None:
                path = "health_report.json"
            
            with open(path, "w") as f:
                json.dump(report, f, indent=2)
            
            return path
        except Exception as e:
            logger.error(f"Error saving health report: {str(e)}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    health_check = HealthCheck()
    report = health_check.run_all_checks()
    print(json.dumps(report, indent=2)) 