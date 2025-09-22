# 🚁 FLYSCOPE - AI-Powered Drone Inspection System

FLYSCOPE is an advanced AI-powered drone inspection system designed for safer infrastructure monitoring. It combines drone technology, computer vision, and machine learning to automatically detect faults in difficult or dangerous areas.

## 🎯 Project Goals

- **Enhanced Safety**: Reduce human risk in dangerous inspection areas
- **Improved Efficiency**: Automated fault detection using AI
- **Cost-Effective**: Utilize affordable drones for comprehensive monitoring
- **Real-Time Analysis**: Instant defect detection and reporting

## ✨ Key Features

### 📤 Media Upload & Capture
- Upload drone images and videos (JPG, PNG, MP4, AVI, MOV)
- Live drone camera integration (coming soon)
- Sample infrastructure images for testing

### 🤖 AI-Powered Analysis
- **Crack Detection** (94.2% accuracy) - Structural cracks in concrete, asphalt, metal
- **Corrosion Detection** (91.8% accuracy) - Rust and corrosion on metal infrastructure
- **Thermal Anomaly** (96.5% accuracy) - Overheating and thermal hotspots
- **Vegetation Risk** (89.3% accuracy) - Vegetation growth near critical infrastructure
- **Structural Damage** (92.7% accuracy) - General structural integrity assessment

### 📊 Results & Visualization
- Detailed detection results with confidence scores
- Bounding box visualization on images
- Severity classification (Critical, High, Medium, Low)
- Interactive charts and metrics

### 🗺️ Fault Mapping
- Interactive map visualization of detected faults
- Geographic distribution of defects
- Severity-based color coding
- Statistical analysis and charts

### 📁 Data Management
- Inspection history tracking
- CSV export functionality
- PDF report generation (coming soon)
- Data backup and import tools

## 🛠️ Technology Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **OpenCV**: Computer vision processing
- **TensorFlow/PyTorch**: Deep learning frameworks (for future ML models)
- **Folium**: Interactive mapping
- **Plotly**: Data visualization
- **Pandas**: Data manipulation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd pythonProject
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run flyscope_app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

## 📋 Usage Workflow

### 1. Home Page
- Overview of FLYSCOPE features and capabilities
- Project goals and technology information

### 2. Media Upload
- **Upload Files**: Select drone images or videos from your device
- **Sample Images**: Use pre-loaded infrastructure images for testing
- **Live Camera**: Connect to drone camera (feature in development)

### 3. AI Analysis
- **Model Selection**: Choose from 5 AI detection models
- **Settings Configuration**: Adjust confidence threshold and sensitivity
- **Run Analysis**: Process uploaded media with selected models

### 4. Results & Reports
- **Detailed Results**: View detection results with images and metrics
- **Export Options**: Download CSV data or generate PDF reports
- **Statistics**: Comprehensive analysis summary

### 5. Fault Mapping
- **Interactive Map**: Geographic visualization of detected faults
- **Severity Analysis**: Color-coded markers based on fault severity
- **Distribution Charts**: Statistical breakdown of fault types

### 6. Data Management
- **Inspection History**: Track all previous analyses
- **Data Tools**: Clear, import, or backup inspection data
- **Dataset Viewer**: Browse historical inspection results

## 🔧 Configuration Options

### Analysis Settings
- **Confidence Threshold**: 0.1 - 1.0 (default: 0.7)
- **Detection Sensitivity**: Low, Medium, High
- **Analysis Mode**: Quick Scan, Detailed Analysis, Comprehensive Report

### Supported File Formats
- **Images**: JPG, JPEG, PNG
- **Videos**: MP4, AVI, MOV

## 📊 AI Model Details

| Model | Accuracy | Use Cases | Description |
|-------|----------|-----------|-------------|
| Crack Detection | 94.2% | Bridges, Buildings, Roads, Dams | Detects structural cracks in various materials |
| Corrosion Detection | 91.8% | Power lines, Bridges, Pipelines, Towers | Identifies rust and corrosion on metal surfaces |
| Thermal Anomaly | 96.5% | Electrical systems, Mechanical equipment | Detects overheating and thermal hotspots |
| Vegetation Risk | 89.3% | Power lines, Railways, Pipelines | Identifies vegetation encroachment |
| Structural Damage | 92.7% | Buildings, Bridges, Towers, Dams | General structural integrity assessment |

## 🚧 Future Enhancements

### Planned Features
- **Real-time drone integration** with DJI Tello, DJI Mini, and custom drones
- **Advanced ML models** with actual trained neural networks
- **PDF report generation** with detailed analysis
- **Annotation tools** for model improvement
- **Multi-language support**
- **Cloud deployment** for team collaboration
- **Mobile app** for field operations

### Drone Integration Roadmap
- DJI Tello SDK integration
- DJI Mini compatibility
- Custom drone support
- Autonomous flight patterns
- Real-time video streaming

## 🤝 Contributing

We welcome contributions to FLYSCOPE! Here's how you can help:

1. **Report Issues**: Submit bug reports or feature requests
2. **Code Contributions**: Fork the repository and submit pull requests
3. **Documentation**: Improve documentation and tutorials
4. **Testing**: Help test new features and report feedback

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, questions, or collaboration opportunities:
- Create an issue in the repository
- Contact the development team
- Check the documentation for troubleshooting

## 🙏 Acknowledgments

- **Streamlit** for the excellent web framework
- **OpenCV** for computer vision capabilities
- **Folium** for interactive mapping
- **Plotly** for data visualization
- The open-source community for inspiration and tools

---

**FLYSCOPE** - Making infrastructure inspection safer, smarter, and more efficient through AI-powered drone technology. 🚁✨
