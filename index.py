import subprocess
import sys
import os

def run_bot():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "src", "main.py")
    
    if not os.path.exists(main_script):
        sys.exit(1)

    try:
        subprocess.run([sys.executable, "-m", "src.main"], check=True)
    except KeyboardInterrupt:
        pass
    except subprocess.CalledProcessError:
        pass

if __name__ == "__main__":
    run_bot()
