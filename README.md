# 🔬 Light Calculator Dashboard

An interactive web-based calculator for analyzing camera sensor performance, from scene illumination to final signal-to-noise ratio. Features a clean, code-free interface perfect for photographers, engineers, and researchers.

## ✨ Features

- **🎛️ Interactive Dashboard**: Real-time sliders for all camera parameters
- **📊 Complete Analysis**: Light collection + comprehensive noise analysis  
- **🔍 SNR Calculation**: Signal-to-noise ratio with EMVA1288 compliant dB conversion
- **🎯 Smart Presets**: Scenarios for different camera types (DSLR, smartphone, astro)
- **📈 Advanced Visualizations**: 4-panel charts showing light path and noise breakdown
- **⚙️ Noise Regime Detection**: Automatic identification of limiting noise source
- **🌐 Web-Based**: No installation needed - runs in any browser

## 🚀 Quick Start

1. **Setup Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Launch Dashboard:**
   ```bash
   python start_dashboard.py
   ```

3. **Open Browser:** Go to `http://localhost:8866` for the clean dashboard interface

## 📊 What You Can Analyze

### 🔬 **Complete Light Path:**
1. **Scene Illumination** → Scene Luminance  
2. **Through Lens** → Sensor Illuminance
3. **Photon Conversion** → Electron Count  
4. **Noise Analysis** → Final SNR

### 🔊 **Comprehensive Noise Model:**
- **Shot Noise**: √(signal electrons) - quantum limit
- **Read Noise**: Electronics noise floor  
- **Dark Current Noise**: Thermal electron generation
- **Total Noise**: Root-sum-of-squares combination
- **SNR**: 20×log₁₀(Signal/Noise) per EMVA1288

### 🎛️ **Interactive Parameters:**
- Scene Illuminance (1-100,000 lux)
- Scene Reflectance (1-90%)
- Lens f-number (f/1.0-f/22)
- Lens Transmittance (60-95%)
- Pixel Size (1-15 μm)
- Exposure Time (0.1-1000 ms)
- Wavelength (400-700 nm)
- Quantum Efficiency (20-95%)
- **Read Noise (0.1-20 e⁻)**
- **Dark Current (0.001-10 e⁻/px/s)**

## 🎯 Preset Scenarios

| Scenario | Description | Typical SNR |
|----------|-------------|-------------|
| **☀️ Bright Daylight** | DSLR, f/8, fast shutter | >100 (40+ dB) |
| **🏠 Indoor Portrait** | Full-frame, f/2.8, flash | 20-50 (26-34 dB) |
| **🌙 Low Light** | Fast lens, high ISO equivalent | 5-20 (14-26 dB) |
| **🔭 Astro Camera** | Cooled sensor, long exposure | 10-100+ (20-40+ dB) |
| **📱 Smartphone** | Small pixels, computational photography | 10-30 (20-30 dB) |

## 📁 Project Structure

```
light_calculator/
├── start_dashboard.py              # 🚀 Main launcher (run this!)
├── light_calculator_dashboard.ipynb # 📊 Interactive dashboard
├── light_calculator.py            # 🔬 Core calculation engine
├── custom.css                     # 🎨 Dashboard styling
├── requirements.txt               # 📦 Dependencies
├── README.md                      # 📖 This file
├── CLAUDE.md                      # 🤖 AI development guidance
└── .gitignore                     # 🚫 Git exclusions
```

## 🌐 Online Deployment

### **🚀 Option 1: Binder (Free, One-Click Launch)**
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ximea-gmbh/light_calculator/main?urlpath=voila%2Frender%2Flight_calculator_dashboard.ipynb)

**How to use:**
1. Click the Binder badge above
2. Wait 1-2 minutes for environment setup
3. Dashboard opens automatically - no installation needed!

**⚠️ Binder Notes:**
- Free service with usage limits
- Sessions timeout after ~10 minutes of inactivity  
- May take time to start if repository was recently updated
- Perfect for demos, education, and quick calculations

### **🏠 Option 2: Local Installation (Best Performance)**
```bash
git clone https://github.com/ximea-gmbh/light_calculator.git
cd light_calculator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python start_dashboard.py
```

### **☁️ Option 3: Self-Hosted Deployment**
Deploy to cloud platforms for permanent hosting:
- **Heroku**: Use provided `Procfile` 
- **Render**: Automatic deployment from GitHub
- **Railway**: Simple Docker-based deployment
- **Google Cloud Run**: Containerized deployment

**Repository includes deployment configs for all major platforms.**

## 🛠️ Troubleshooting

### **Binder Issues:**
- **Slow to start?** Binder builds environment on first use - be patient!
- **Session expired?** Refresh and launch again
- **Widgets not working?** Try refreshing the page
- **Still having issues?** Use local installation instead

### **Local Installation Issues:**
- **Python version**: Requires Python 3.8+
- **Widget display**: Ensure Jupyter widgets are enabled
- **Port conflicts**: Dashboard uses port 8866 by default

## 🧮 The Physics

### **Core Calculations:**
```
Scene Luminance = (Illuminance × Reflectance) / π
Sensor Illuminance = (Luminance × Transmittance × π) / (4 × f²)
Photon Count = (Irradiance × Pixel_Area × Exposure) / Photon_Energy  
Signal Electrons = Photons × Quantum_Efficiency
Total Noise = √(Signal + Dark + Read²)
SNR = Signal / Total_Noise
```

### **Noise Regimes:**
- **🟢 Shot Limited**: Quantum-limited performance (best case)
- **🟡 Read Limited**: Electronics-limited (low light)  
- **🔴 Dark Limited**: Thermally-limited (long exposures)
- **🔵 Mixed Regime**: Multiple noise sources significant

## 💡 Use Cases

- **📸 Photography**: Optimize camera settings for different lighting
- **🔬 Scientific Imaging**: Calculate detection limits and SNR requirements
- **🎓 Education**: Understand fundamental limits of digital imaging
- **🔧 Engineering**: Design and specify camera systems
- **🌌 Astronomy**: Plan observations and exposure times

## 🤝 Contributing

This calculator demonstrates the fundamental physics of digital photography and sensor design. Contributions welcome for:
- Additional camera presets
- Enhanced visualizations  
- Deployment improvements
- Educational content

## 📄 License

Open source project for educational and research purposes.

---

*Built with ❤️ using Python, Jupyter, Voilà, and ipywidgets*