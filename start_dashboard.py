#!/usr/bin/env python3
"""
Light Calculator - Dashboard Launcher

Launches a clean, code-free interface using Voilà that hides all code
and presents only the interactive widgets and results.
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import voila
        import ipywidgets
        import matplotlib
        import numpy
        print("✅ All dashboard dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_notebook():
    """Check if dashboard notebook exists"""
    dashboard_path = "light_calculator_dashboard.ipynb"
    if not os.path.exists(dashboard_path):
        print(f"❌ Dashboard notebook not found: {dashboard_path}")
        print("Please ensure you're in the correct directory.")
        return False
    return True

def launch_dashboard():
    """Launch Voilà dashboard"""
    dashboard_path = "light_calculator_dashboard.ipynb"
    
    print("🚀 Starting Light Calculator Dashboard...")
    print("📱 This will open a clean interface with no code visible")
    
    try:
        # Try different Voilà launch approaches
        launch_commands = [
            # Standard Voilà command
            [sys.executable, '-m', 'voila', dashboard_path, '--enable_nbextensions=True'],
            # Alternative approach
            ['voila', dashboard_path, '--enable_nbextensions=True'],
            # Fallback without nbextensions
            [sys.executable, '-m', 'voila', dashboard_path]
        ]
        
        success = False
        for cmd in launch_commands:
            try:
                print(f"🔄 Trying: {' '.join(cmd)}")
                # Start the dashboard
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Wait a moment to see if it starts successfully
                time.sleep(2)
                
                if process.poll() is None:  # Process is still running
                    success = True
                    print("✅ Dashboard server started successfully!")
                    break
                else:
                    # Process exited, try next command
                    continue
                    
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
        
        if success:
            print("")
            print("🎉 Dashboard is now running!")
            print("🌐 Open your browser and go to: http://localhost:8866")
            print("📱 You'll see a clean interface with sliders and results only")
            print("")
            print("💡 Features:")
            print("   • Interactive sliders for all parameters")
            print("   • Real-time calculation updates")
            print("   • Preset scenario buttons")
            print("   • No code visible - just the interface!")
            print("")
            print("🛑 To stop the dashboard, press Ctrl+C in this terminal")
            
            # Keep the launcher running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down dashboard...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except:
                    pass
                print("✅ Dashboard stopped")
            
            return True
        else:
            print("❌ Could not start Voilà dashboard with any method.")
            print("🔧 Please try manually:")
            print(f"   voila {dashboard_path}")
            print("   or")
            print(f"   python -m voila {dashboard_path}")
            return False
        
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        print("🔧 Please try manually:")
        print(f"   voila {dashboard_path}")
        return False

def main():
    print("🔬 Light Calculator - Clean Dashboard Launcher")
    print("=" * 55)
    print("This creates a code-free interface perfect for users")
    print("who just want to use the calculator without seeing code.")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("light_calculator.py"):
        print("❌ Please run this script from the light_calculator directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check notebook exists
    if not check_notebook():
        sys.exit(1)
    
    # Launch dashboard
    if not launch_dashboard():
        sys.exit(1)

if __name__ == "__main__":
    main()