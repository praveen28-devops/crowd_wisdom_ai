# Quick Start Guide

## 🚀 Running the Demo

### Option 1: Comprehensive Demo (Recommended)
```bash
python demo_comprehensive.py
```

This runs a full demonstration of all system capabilities:
- ✅ Environment validation
- ✅ Live SEC data fetching
- ✅ Chart generation
- ✅ Sentiment analysis
- ✅ Optional CrewAI analysis
- ✅ Output review

### Option 2: Main Production Analysis
```bash
python main.py
```

This runs the full production analysis with all agents.

### Option 3: CrewAI Flow (Advanced)
```bash
python flows/insider_trading_flow.py
```

This runs the complete CrewAI flow orchestration.

## 📚 Documentation

- **[APPROACH_DOCUMENTATION.md](APPROACH_DOCUMENTATION.md)** - Complete technical architecture and approach
- **[VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)** - Detailed video recording script for demonstrations
- **[README.md](README.md)** - Full project documentation

## 🔧 Environment Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   # Create .env file with:
   GROQ_API_KEY=gsk_your_api_key_here
   CONTACT_EMAIL=your-email@company.com
   ```

4. **Get free Groq API key:**
   - Visit: https://console.groq.com/
   - Sign up and generate API key
   - Copy key starting with 'gsk_' to .env file

## 📊 Expected Outputs

After running the demo, check the `reports/` directory for:

- **final_report.txt** - Executive analysis report
- **insider_trading_chart.png** - Trading volume visualization
- **raw_sec_data.json** - Raw SEC filing data
- **demo_results.json** - Demo execution results
- **Various log files** - Detailed execution logs

## 🎬 Video Recording

Use the **VIDEO_SCRIPT.md** to create a professional demonstration video:

1. Follow the pre-recording checklist
2. Use the provided timeline and script
3. Highlight key features and outputs
4. Show real-time execution

## 🔍 Key Features Demonstrated

### Real-time SEC Data
- Fetches live insider trading filings from SEC EDGAR
- Validates and normalizes data
- Handles API rate limiting and errors

### Multi-Agent AI System
- Specialized agents for different tasks
- CrewAI orchestration and coordination
- Fallback strategies for robustness

### Professional Reporting
- Executive-level insights and analysis
- Interactive and static visualizations
- Comprehensive audit trails

### Production Ready
- Error handling and logging
- Environment validation
- Performance optimization

## 🤝 Next Steps

1. **Customize for your needs:**
   - Modify agents for specific analysis requirements
   - Add additional data sources
   - Customize reporting formats

2. **Production deployment:**
   - Set up automated scheduling
   - Configure monitoring and alerting
   - Integrate with existing systems

3. **Advanced features:**
   - Add machine learning models
   - Implement real-time alerts
   - Build web dashboard interface

---

*Built with ❤️ using CrewAI, Groq LLM, and the SEC EDGAR API*
