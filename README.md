# 📦 AWS Bedrock Agent Streamlit Frontend

A minimalistic and user-friendly Streamlit frontend that connects to AWS Bedrock Agents for intelligent assistance. Perfect for shipping, customer service, or any AI agent use case.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- 🎨 **Minimalistic Design** - Clean, modern interface
- 💬 **Real-time Chat** - Interactive conversation with your AI agent
- 🔗 **AWS Integration** - Direct connection to AWS Bedrock Agents
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- 🚀 **Quick Actions** - Pre-built buttons for common tasks
- 🔐 **Secure** - Credentials stored safely, never in code

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/aws-bedrock-streamlit-frontend.git
cd aws-bedrock-streamlit-frontend
```

### 2. Install Dependencies
```bash
# Option 1: Use the setup script (recommended)
python3 setup.py

# Option 2: Manual installation
pip install -r requirements.txt
```

### 3. Configure Your AWS Credentials
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual credentials
nano .env  # or use any text editor
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔧 AWS Setup Required

**⚠️ Important:** This frontend requires your own AWS setup. You need:

### 1. AWS Account & Credentials
- AWS Account with billing enabled
- IAM user with programmatic access
- Access Key ID and Secret Access Key

### 2. AWS Bedrock Agent
- A deployed Bedrock Agent in your AWS account
- Agent ID and Alias ID
- Proper IAM permissions for Bedrock

### 3. Required IAM Permissions
Your AWS user needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent",
                "bedrock:GetAgent",
                "bedrock:ListAgents"
            ],
            "Resource": "*"
        }
    ]
}
```

## 📋 Step-by-Step AWS Setup

### Step 1: Create AWS Bedrock Agent
1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Agents" in the left sidebar
3. Click "Create Agent"
4. Follow the setup wizard to create your agent
5. Note down your **Agent ID** and **Alias ID**

### Step 2: Get AWS Credentials
1. Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
2. Create a new user or use existing user
3. Attach the Bedrock permissions policy (see above)
4. Generate Access Key ID and Secret Access Key
5. **Keep these secure!**

### Step 3: Configure the Frontend
1. Copy `.env.example` to `.env`
2. Fill in your credentials:
```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
BEDROCK_AGENT_ID=your_agent_id_here
BEDROCK_AGENT_ALIAS_ID=TSTALIASID
```

## 🎯 How to Use

1. **Start the app**: `streamlit run app.py`
2. **Configure connection**: Use the sidebar to enter your AWS credentials
3. **Test connection**: Click "Connect to Agent"
4. **Start chatting**: Type messages in the chat interface
5. **Use quick actions**: Try the pre-built buttons for common tasks

## 🛠️ Customization

### Change the UI Theme
Edit the CSS in `app.py`:
```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #your-color 0%, #your-color2 100%);
    }
</style>
""", unsafe_allow_html=True)
```

### Add New Quick Actions
Add buttons in the "Quick Actions" section:
```python
if st.button("🆕 Your New Action", use_container_width=True):
    # Your custom logic here
    pass
```

### Modify Agent Prompts
Update the quick action messages to match your agent's capabilities.

## 📁 Project Structure

```
aws-bedrock-streamlit-frontend/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── .env.example          # Environment variables template
├── .env                  # Your actual credentials (not in repo)
├── .gitignore            # Files to ignore in Git
└── README.md             # This file
```

## 🔐 Security Best Practices

- ✅ **Never commit `.env`** - It's in `.gitignore` for safety
- ✅ **Use IAM roles** when possible instead of access keys
- ✅ **Rotate credentials** regularly
- ✅ **Use least privilege** - Only grant necessary permissions
- ✅ **Monitor usage** - Check AWS CloudTrail logs

## 🚨 Troubleshooting

### "Connection failed" Error
- ✅ Check AWS credentials are correct
- ✅ Verify IAM permissions
- ✅ Ensure agent ID and alias ID are correct
- ✅ Check AWS region matches your agent's region

### "Agent not responding" Error
- ✅ Verify your Bedrock agent is deployed and active
- ✅ Check agent alias is published
- ✅ Test agent in AWS console first

### Import Errors
```bash
# Update pip and reinstall
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## 💰 AWS Costs

**Be aware of costs:**
- Bedrock Agent invocations are charged per request
- Costs vary by model and usage
- Monitor your usage in AWS Billing Dashboard
- Consider setting up billing alerts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- 📖 [Streamlit Documentation](https://docs.streamlit.io/)
- 🐛 [Report Issues](https://github.com/yourusername/aws-bedrock-streamlit-frontend/issues)
- 💬 [Discussions](https://github.com/yourusername/aws-bedrock-streamlit-frontend/discussions)

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

---

**Made with ❤️ and ☕ for the AWS community**
