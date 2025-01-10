import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path
import time
import logging
from typing import Optional
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChatPlotManager:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.backend_dir = self.root_dir / "backend"
        self.frontend_dir = self.root_dir / "frontend"
        self.data_dir = self.root_dir / "data"
        self.env_file = self.root_dir / ".env"
        self.is_windows = platform.system().lower() == "windows"
        self.conda_env_name = "chatplot"

    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        try:
            # Check Python version
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
                logger.error("Python 3.10 or higher is required")
                return False

            # Check if conda is installed
            conda_result = subprocess.run(["conda", "--version"], capture_output=True, text=True)
            if conda_result.returncode != 0:
                logger.error("Conda is not installed or not in PATH")
                return False

            # Check if Node.js is installed
            node_result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if node_result.returncode != 0:
                logger.error("Node.js is not installed or not in PATH")
                return False

            # Check if Ollama is installed
            ollama_cmd = "ollama.exe" if self.is_windows else "ollama"
            ollama_result = subprocess.run([ollama_cmd, "list"], capture_output=True, text=True)
            if ollama_result.returncode != 0:
                logger.error("Ollama is not installed or not running")
                return False

            return True
        except Exception as e:
            logger.error(f"Error checking prerequisites: {str(e)}")
            return False

    def setup_environment(self) -> bool:
        """Set up the Conda environment and project structure"""
        try:
            # Create Conda environment if it doesn't exist
            env_list = subprocess.run(["conda", "env", "list"], capture_output=True, text=True)
            if self.conda_env_name not in env_list.stdout:
                logger.info("Creating Conda environment...")
                subprocess.run(["conda", "env", "create", "-f", "environment.yml"], check=True)

            # Create necessary directories
            for dir_path in [self.data_dir / "uploads", self.data_dir / "sample"]:
                dir_path.mkdir(parents=True, exist_ok=True)

            # Copy .env.example to .env if it doesn't exist
            if not self.env_file.exists():
                shutil.copy2(".env.example", ".env")
                logger.info("Created .env file from template")

            return True
        except Exception as e:
            logger.error(f"Error setting up environment: {str(e)}")
            return False

    def start_backend(self) -> Optional[subprocess.Popen]:
        """Start the backend server"""
        try:
            logger.info("Starting backend server...")
            activate_cmd = "activate" if self.is_windows else "source activate"
            cmd = f"{activate_cmd} {self.conda_env_name} && cd backend && uvicorn main:app --reload"
            
            if self.is_windows:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    preexec_fn=os.setsid
                )
            
            # Wait for backend to start
            time.sleep(3)
            return process
        except Exception as e:
            logger.error(f"Error starting backend: {str(e)}")
            return None

    def start_frontend(self) -> Optional[subprocess.Popen]:
        """Start the frontend development server"""
        try:
            logger.info("Starting frontend server...")
            os.chdir(self.frontend_dir)
            
            # Install dependencies if node_modules doesn't exist
            if not (self.frontend_dir / "node_modules").exists():
                subprocess.run(["npm", "install"], check=True)
            
            cmd = "npm run dev"
            if self.is_windows:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    preexec_fn=os.setsid
                )
            
            # Wait for frontend to start
            time.sleep(3)
            return process
        except Exception as e:
            logger.error(f"Error starting frontend: {str(e)}")
            return None
        finally:
            os.chdir(self.root_dir)

    def run(self):
        """Run the ChatPlot application"""
        try:
            logger.info("Starting ChatPlot...")
            
            # Check prerequisites
            if not self.check_prerequisites():
                logger.error("Prerequisites check failed")
                return
            
            # Setup environment
            if not self.setup_environment():
                logger.error("Environment setup failed")
                return
            
            # Start backend
            backend_process = self.start_backend()
            if not backend_process:
                logger.error("Failed to start backend")
                return
            
            # Start frontend
            frontend_process = self.start_frontend()
            if not frontend_process:
                logger.error("Failed to start frontend")
                backend_process.terminate()
                return
            
            # Open browser
            webbrowser.open("http://localhost:5173")
            
            logger.info("ChatPlot is running!")
            logger.info("Press Ctrl+C to stop the application")
            
            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Shutting down ChatPlot...")
                frontend_process.terminate()
                backend_process.terminate()
                logger.info("ChatPlot stopped")
        
        except Exception as e:
            logger.error(f"Error running ChatPlot: {str(e)}")

if __name__ == "__main__":
    manager = ChatPlotManager()
    manager.run() 