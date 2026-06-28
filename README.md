# VLC-Camera-Manager

**A Tkinter-based GUI application for managing IP camera playlists and streaming via VLC.**

---

## 📌 **Features**

✅ **Camera Management**

- Add, edit, and delete IP cameras with dynamic RTSP URL generation
- Support for **50+ manufacturers** (Hikvision, Dahua, Axis, Reolink, EZVIZ, etc.)
- Custom URL support for unsupported manufacturers

✅ **RTSP Stream Testing**

- Test camera connectivity and RTSP stream validity using `ffprobe`
- Visual status indicators (✅ OK / ❌ Failed / ⏱️ Timeout)

✅ **VLC Integration**

- Play camera streams directly in VLC with one click
- Dynamic URL generation before sending to VLC

✅ **Playlist Management**

- Save and load camera playlists in JSON format
- Organize cameras into custom playlists

✅ **User-Friendly Interface**

- Clean Tkinter GUI with intuitive controls
- Real-time status updates
- Responsive design

---

## 📦 **Installation**

### **Prerequisites**

#### **1. Python 3.8+**

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Windows
# Download from https://www.python.org/downloads/
```

#### **2. FFmpeg (for stream testing)**

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

#### **3. VLC Media Player**

```bash
# Ubuntu/Debian
sudo apt install vlc

# macOS
brew install --cask vlc

# Windows
# Download from https://www.videolan.org/vlc/
```

---

### **Install CSPM**

#### **Option 1: Clone from GitHub**

```bash
git clone https://github.com/your-username/CSPM.git
cd CSPM
pip install -r requirements.txt
python main.py
```

#### **Option 2: Manual Download**

1. Download `main.py`, `manufacturers.json`, and `requirements.txt`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

---

## 🚀 **Usage**

### **1. Add a Camera**

1. Click **"Ajouter"**
2. Fill in the details:
  - **Name**: Camera identifier (e.g., "Front Door")
  - **Manufacturer**: Select from dropdown (50+ options)
  - **IP**: Camera IP address (e.g., `192.168.1.100`)
  - **Port**: Default is `554`
  - **Username/Password**: Camera credentials
  - **Dynamic Fields**: Appear based on manufacturer (e.g., `channel` for Hikvision)
3. Click **"Ajouter"** to save

### **2. Test a Camera**

- Select a camera from the list
- Click **"Tester"**
- Status will update to ✅ (OK), ❌ (Failed), or ⏱️ (Timeout)

### **3. Play in VLC**

- Select a camera
- Click **"Lire dans VLC"**
- VLC will open with the RTSP stream

### **4. Save/Load Playlists**

- **Save**: Click **"Sauvegarder"** to save the current camera list as a JSON file
- **Load**: Click **"Charger"** to load a previously saved playlist

---

## 📂 **Project Structure**

```
CSPM/
├── main.py              # Main application (Tkinter GUI)
├── manufacturers.json    # Manufacturer RTSP URL templates
├── requirements.txt      # Python dependencies
├── playlists/            # Saved playlists (auto-created)
│   └── default.json      # Example playlist
└── README.md             # This file
```

---

## 🎯 **Supported Manufacturers**


| **Manufacturer** | **Example URL**                                               | **Dynamic Fields**   |
| ---------------- | ------------------------------------------------------------- | -------------------- |
| Hikvision        | `rtsp://user:pass@ip:554/Streaming/Channels/101`              | `channel`            |
| Dahua            | `rtsp://user:pass@ip:554/cam/realmonitor?channel=1&subtype=0` | `channel`, `subtype` |
| Axis             | `rtsp://user:pass@ip:554/axis-media/media.amp`                | -                    |
| Reolink          | `rtsp://user:pass@ip:554/h264Preview_01_main`                 | `channel`            |
| EZVIZ            | `rtsp://user:pass@ip:554/h264`                                | -                    |
| UniFi            | `rtsp://user:pass@ip:7447/camera_id`                          | `camera_id`          |
| Tapo             | `rtsp://user:pass@ip:554/stream1`                             | `stream_number`      |
| ...              | ...                                                           | ...                  |
| **Custom**       | User-defined                                                  | -                    |


> **Full list**: See `manufacturers.json` for all 50+ supported manufacturers.

---

## 🔧 **RTSP URL Examples**

### **Hikvision**

```
Main Stream:   rtsp://admin:12345@192.168.1.100:554/Streaming/Channels/101
Sub Stream:    rtsp://admin:12345@192.168.1.100:554/Streaming/Channels/102
```

### **Dahua**

```
Main Stream:   rtsp://admin:12345@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0
Sub Stream:    rtsp://admin:12345@192.168.1.100:554/cam/realmonitor?channel=1&subtype=1
```

### **UniFi**

```
rtsp://admin:12345@192.168.1.100:7447/000000000000
```

*(Camera ID found in UniFi Protect interface)*

### **Axis**

```
rtsp://admin:12345@192.168.1.100:554/axis-media/media.amp
```

---

## 🐛 **Troubleshooting**

### **1. VLC not opening streams**

- **Issue**: VLC opens but shows no video
- **Solution**: 
  - Verify camera credentials
  - Test the RTSP URL in VLC manually
  - Check firewall settings

### **2. "ffprobe not found" error**

- **Issue**: Stream testing fails with `ffprobe` error
- **Solution**: Install FFmpeg:
  ```bash
  # Ubuntu/Debian
  sudo apt install ffmpeg

  # macOS
  brew install ffmpeg
  ```

### **3. "VLC not found" error**

- **Issue**: VLC does not launch
- **Solution**: Install VLC:
  ```bash
  # Ubuntu/Debian
  sudo apt install vlc

  # macOS
  brew install --cask vlc
  ```

### **4. Invalid IP format**

- **Issue**: IP address validation fails
- **Solution**: Use a valid IPv4 address (e.g., `192.168.1.100`)

---

## 📜 **License**

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🤝 **Contributing**

Contributions are welcome! Feel free to:

- Report bugs or suggest features via **Issues**
- Submit **Pull Requests** for improvements

---

## 📞 **Support**

For questions or issues:

- Open an issue on GitHub
- Check the [Troubleshooting](#-troubleshooting) section

---

**Made with ❤️ and Python | © 2026 Camera Stream Playlist Manager**
