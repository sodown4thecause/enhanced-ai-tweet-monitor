import subprocess
import sys

def check_monitor_status():
    """Check if the AI abilities monitor is running using Windows tasklist."""
    print("🔍 Checking AI abilities Monitor Status...")
    
    try:
        # Use tasklist to find Python processes
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and 'python.exe' in result.stdout:
            print("✅ Python processes found running")
            print("🤖 AI abilities Monitor appears to be active")
            
            # Try to get more details with wmic
            try:
                wmic_result = subprocess.run(['wmic', 'process', 'where', 'name="python.exe"', 
                                            'get', 'processid,commandline'], 
                                           capture_output=True, text=True)
                if wmic_result.returncode == 0:
                    lines = wmic_result.stdout.split('\n')
                    for line in lines:
                        if 'run_monitor.py' in line:
                            print(f"   📋 Found monitor process: {line.strip()}")
                            return True
            except:
                pass
                
            print("   ℹ️  Use Ctrl+C in the terminal where you started the monitor to stop it")
            return True
        else:
            print("❌ No Python processes found running")
            print("   You can start the monitor with: python run_monitor.py")
            return False
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        print("   Manual check: Look for 'python.exe run_monitor.py' in Task Manager")
        return False

if __name__ == "__main__":
    check_monitor_status()