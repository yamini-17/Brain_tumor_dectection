#!/usr/bin/env python3
"""
Setup and Installation Script for Brain Tumor Detection System
Automates environment setup, dependency installation, and initial configuration.
"""

import os
import sys
import subprocess
from pathlib import Path
import platform

class SetupManager:
    """Manages setup and installation process."""
    
    def __init__(self):
        self.os_type = platform.system()
        self.backend_dir = Path(__file__).parent
        self.venv_dir = self.backend_dir / "venv"
        self.python_exec = self._get_python_executable()
    
    def _get_python_executable(self):
        """Get appropriate Python executable."""
        if self.os_type == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def print_header(self, title):
        """Print formatted header."""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70)
    
    def print_step(self, step_num, title):
        """Print step title."""
        print(f"\n[{step_num}] {title}...")
    
    def print_success(self, message):
        """Print success message."""
        print(f"✓ {message}")
    
    def print_error(self, message):
        """Print error message."""
        print(f"❌ {message}")
    
    def print_warning(self, message):
        """Print warning message."""
        print(f"⚠️  {message}")
    
    def run_command(self, command, shell=False, check=True):
        """Run shell command."""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                check=check,
                capture_output=True,
                text=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def check_python_version(self):
        """Check if Python version is 3.10+."""
        self.print_step(1, "Checking Python Version")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 10):
            self.print_error(f"Python 3.10+ required (found: {version.major}.{version.minor})")
            return False
        
        self.print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def create_virtual_environment(self):
        """Create Python virtual environment."""
        self.print_step(2, "Creating Virtual Environment")
        
        if self.venv_dir.exists():
            self.print_warning("Virtual environment already exists")
            return True
        
        success, output = self.run_command([sys.executable, "-m", "venv", str(self.venv_dir)])
        
        if success:
            self.print_success(f"Virtual environment created at {self.venv_dir}")
            return True
        else:
            self.print_error(f"Failed to create virtual environment: {output}")
            return False
    
    def upgrade_pip(self):
        """Upgrade pip, setuptools, and wheel."""
        self.print_step(3, "Upgrading pip")
        
        success, output = self.run_command(
            [str(self.python_exec), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"]
        )
        
        if success:
            self.print_success("pip upgraded successfully")
            return True
        else:
            self.print_error(f"Failed to upgrade pip: {output}")
            return False
    
    def install_dependencies(self):
        """Install project dependencies."""
        self.print_step(4, "Installing Dependencies")
        
        requirements_file = self.backend_dir / "requirements.txt"
        
        if not requirements_file.exists():
            self.print_error("requirements.txt not found")
            return False
        
        self.print_warning("This may take several minutes (especially PyTorch)...")
        
        success, output = self.run_command(
            [str(self.python_exec), "-m", "pip", "install", "-r", str(requirements_file)]
        )
        
        if success:
            self.print_success("All dependencies installed successfully")
            return True
        else:
            self.print_error(f"Failed to install dependencies")
            print(f"Output:\n{output}")
            return False
    
    def verify_installation(self):
        """Verify that all dependencies are installed."""
        self.print_step(5, "Verifying Installation")
        
        required_packages = [
            "flask",
            "flask_cors",
            "cv2",  # opencv-python
            "numpy",
            "torch",
            "ultralytics"
        ]
        
        verify_code = f"""
import importlib
packages = {required_packages}
missing = []
for pkg in packages:
    try:
        importlib.import_module(pkg)
    except ImportError:
        missing.append(pkg)
if missing:
    print("MISSING:" + ",".join(missing))
else:
    print("ALL_OK")
"""
        
        success, output = self.run_command(
            [str(self.python_exec), "-c", verify_code]
        )
        
        if "ALL_OK" in output:
            self.print_success("All dependencies verified")
            return True
        elif "MISSING:" in output:
            missing = output.split("MISSING:")[1].strip().split(",")
            self.print_error(f"Missing packages: {', '.join(missing)}")
            return False
        else:
            self.print_error("Could not verify installation")
            return False
    
    def check_model_file(self):
        """Check if model file exists."""
        self.print_step(6, "Checking Model File")
        
        model_dir = self.backend_dir / "model"
        model_dir.mkdir(exist_ok=True)
        
        model_file = model_dir / "yolov9.pt"
        
        if model_file.exists():
            size_mb = model_file.stat().st_size / (1024 * 1024)
            self.print_success(f"Model found: {model_file} ({size_mb:.1f}MB)")
            return True
        else:
            self.print_warning("YOLOv9 model not found")
            print("\n   The model will be auto-downloaded on first inference.")
            print("   Alternatively, download manually from:")
            print("   https://github.com/ultralytics/yolov9/releases")
            print(f"\n   Place the file at: {model_file}")
            return False
    
    def create_directories(self):
        """Create necessary directories."""
        self.print_step(7, "Creating Directories")
        
        directories = [
            self.backend_dir / "logs",
            self.backend_dir / "model",
            self.backend_dir / "uploads"
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            self.print_success(f"Directory ensured: {directory.name}/")
    
    def display_next_steps(self):
        """Display next steps for user."""
        self.print_header("SETUP COMPLETE ✓")
        
        print("\nNext Steps:\n")
        
        if self.os_type == "Windows":
            activate_cmd = f"{self.venv_dir}\\Scripts\\activate"
        else:
            activate_cmd = f"source {self.venv_dir}/bin/activate"
        
        print(f"1. Activate virtual environment:")
        print(f"   {activate_cmd}\n")
        
        print("2. Run the server:")
        print("   python app.py\n")
        
        print("3. In another terminal, test the API:")
        print("   python test_api.py\n")
        
        print("Documentation:")
        print("  - Full docs: README.md")
        print("  - Quick start: QUICKSTART.md")
        print("\n" + "="*70 + "\n")
    
    def run_setup(self):
        """Execute complete setup process."""
        self.print_header("BRAIN TUMOR DETECTION SYSTEM - SETUP")
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Creating virtual environment", self.create_virtual_environment),
            ("Upgrading pip", self.upgrade_pip),
            ("Installing dependencies", self.install_dependencies),
            ("Verifying installation", self.verify_installation),
            ("Creating directories", self.create_directories),
            ("Checking model file", self.check_model_file),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                if "Checking model" in step_name:
                    # Model file check is non-blocking
                    continue
                else:
                    self.print_error(f"Setup failed at: {step_name}")
                    return False
        
        self.display_next_steps()
        return True


def main():
    """Main entry point."""
    try:
        manager = SetupManager()
        success = manager.run_setup()
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
