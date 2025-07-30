#!/usr/bin/env python3
"""
Setup script for Shipping Agent Streamlit Frontend
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("📝 Creating .env file from template...")
            with open('.env.example', 'r') as template:
                content = template.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created! Please edit it with your AWS credentials.")
        else:
            print("⚠️  .env.example not found. Please create .env manually.")
    else:
        print("✅ .env file already exists.")

def main():
    print("🚀 Setting up Shipping Agent Streamlit Frontend...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation.")
        return
    
    # Create env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit the .env file with your AWS credentials")
    print("2. Run: streamlit run app.py")
    print("3. Configure your AWS Bedrock Agent in the sidebar")
    print("\n📚 Need help? Check the README.md file!")

if __name__ == "__main__":
    main()
