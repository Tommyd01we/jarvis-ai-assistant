#!/usr/bin/env python3
"""
Build script to create executable (.exe) for Jarvis AI Assistant
Uses PyInstaller to bundle Python code into standalone executable
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build Jarvis AI as standalone .exe executable"""
    
    print("=" * 60)
    print("JARVIS AI - Building Executable (.exe)")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("\n❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    build_cmd = [
        "pyinstaller",
        "--onefile",                          # Single executable file
        "--windowed",                         # No console window (comment out for console)
        "--icon=jarvis.ico",                  # Icon file (optional)
        "--name=Jarvis",                      # Executable name
        "--add-data=data:data",               # Include data directory
        "--add-data=models:models",           # Include models directory
        "--add-data=logs:logs",               # Include logs directory
        "--hidden-import=core",               # Hidden imports
        "--hidden-import=utils",
        "--distpath=./dist",                  # Output directory
        "--buildpath=./build",
        "--specpath=./",
        "main.py"                             # Entry point
    ]
    
    print("\n📦 Building executable...")
    print(f"Command: {' '.join(build_cmd)}\n")
    
    try:
        subprocess.run(build_cmd, check=True)
        
        print("\n✅ Build successful!")
        print("\n" + "=" * 60)
        print("📁 Output Location:")
        print("=" * 60)
        print(f"\n  Executable: ./dist/Jarvis.exe")
        print(f"  Size: ~{get_file_size('./dist/Jarvis.exe') if os.path.exists('./dist/Jarvis.exe') else 'TBD'}")
        
        print("\n" + "=" * 60)
        print("🚀 Next Steps:")
        print("=" * 60)
        print("\n1. Run the executable:")
        print("   ./dist/Jarvis.exe")
        print("\n2. Or copy to desired location and run from there")
        print("\n3. Create shortcuts for easy access")
        print("\n" + "=" * 60)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def get_file_size(filepath):
    """Get file size in MB"""
    if os.path.exists(filepath):
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        return f"{size_mb:.2f} MB"
    return "Unknown"

def create_installer_script():
    """Create optional NSIS installer script"""
    
    nsis_script = """
; NSIS Installer Script for Jarvis AI
; Download NSIS from https://nsis.sourceforge.io/

Name "Jarvis AI Assistant"
OutFile "Jarvis-Installer.exe"
InstallDir "$PROGRAMFILES\\Jarvis"

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\\Jarvis.exe"
  
  CreateDirectory "$SMPROGRAMS\\Jarvis"
  CreateShortcut "$SMPROGRAMS\\Jarvis\\Jarvis.lnk" "$INSTDIR\\Jarvis.exe"
  CreateShortcut "$DESKTOP\\Jarvis.lnk" "$INSTDIR\\Jarvis.exe"
SectionEnd
"""
    
    with open("jarvis_installer.nsi", "w") as f:
        f.write(nsis_script)
    
    print("✅ Installer script created: jarvis_installer.nsi")
    print("   (Optional: Use NSIS to create professional installer)")

def main():
    """Main build process"""
    
    # Step 1: Build executable
    success = build_executable()
    
    if success:
        # Step 2: Create installer script
        create_installer_script()
        
        print("\n" + "=" * 60)
        print("✨ BUILD COMPLETE!")
        print("=" * 60)
        print("\nJarvis AI is now available as:")
        print("  • Standalone executable: ./dist/Jarvis.exe")
        print("  • Portable - No installation required!")
        print("  • Self-contained with all dependencies")
        print("\n" + "=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ BUILD FAILED")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
