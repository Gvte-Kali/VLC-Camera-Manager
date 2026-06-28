#!/usr/bin/env python3
"""
Camera Stream Playlist Manager (CSPM)
===================================

A Tkinter-based GUI application for managing IP camera playlists and streaming via VLC.

Features:
- Add, edit, and delete cameras with dynamic RTSP URL generation based on manufacturer.
- Test camera connectivity and RTSP stream validity.
- Play streams directly in VLC.
- Save and load camera playlists in JSON format.
- Support for 50+ manufacturers with custom URL templates.

Dependencies:
- python-vlc (optional, for advanced VLC control)
- ffmpeg (for stream testing via ffprobe)

Usage:
    python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import json
import os
import re
import webbrowser


class CameraManagerApp:
    """Main application class for Camera Stream Playlist Manager."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Camera Stream Playlist Manager")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)
        
        # Load manufacturers data
        self.manufacturers = self.load_manufacturers()
        
        # Initialize camera list and current playlist
        self.cameras = []
        self.current_playlist = "default.json"
        
        # Setup UI
        self.setup_ui()
        
        # Load default playlist if exists
        if os.path.exists(f"playlists/{self.current_playlist}"):
            self.load_playlist(f"playlists/{self.current_playlist}")
    
    def load_manufacturers(self):
        """Load manufacturer data from JSON file."""
        try:
            with open("manufacturers.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to embedded data if file not found
            return {
                "Hikvision": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/Streaming/Channels/{channel}",
                    "fields": ["channel"],
                    "default_port": 554,
                    "help": "Channel: 101 (main), 102 (sub)"
                },
                "Dahua": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/cam/realmonitor?channel={channel}&subtype={subtype}",
                    "fields": ["channel", "subtype"],
                    "default_port": 554,
                    "help": "channel: 1-4, subtype: 0 (main), 1 (sub)"
                },
                "Axis": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/axis-media/media.amp",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Reolink": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/h264Preview_{channel}_main",
                    "fields": ["channel"],
                    "default_port": 554,
                    "help": "Channel: 01, 02, etc."
                },
                "EZVIZ": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/h264",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Annke": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/Streaming/Channels/{channel}",
                    "fields": ["channel"],
                    "default_port": 554,
                    "help": "Channel: 101, 102, etc."
                },
                "UniFi": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:7447/{camera_id}",
                    "fields": ["camera_id"],
                    "default_port": 7447,
                    "help": "Camera ID: Check UniFi Protect interface"
                },
                "Tapo": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/stream{stream_number}",
                    "fields": ["stream_number"],
                    "default_port": 554,
                    "help": "Stream number: 1 or 2"
                },
                "Foscam": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/videoMain",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Amcrest": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/cam/realmonitor?channel=1&subtype=0",
                    "fields": ["channel", "subtype"],
                    "default_port": 554,
                    "help": "channel: 1-4, subtype: 0 (main), 1 (sub)"
                },
                "Swann": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/channel{channel}",
                    "fields": ["channel"],
                    "default_port": 554,
                    "help": "Channel: 1, 2, etc."
                },
                "Lorex": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/stream1",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Night Owl": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/h264",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Arlo": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Nest": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/stream",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Ring": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/media.smp",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Blink": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/live0",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Wyze": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/live",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "360 Xiaomi": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/ch0",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "YI Technology": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/ch0",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Kasa": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/stream1",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "LaView": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/{channel}",
                    "fields": ["channel"],
                    "default_port": 554,
                    "help": "Channel: 101, 102, etc."
                },
                "LTS": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/{channel}",
                    "fields": ["channel"],
                    "default_port": 554,
                    "help": "Channel: 101, 102, etc."
                },
                "ZOSI": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/{channel}",
                    "fields": ["channel"],
                    "default_port": 554,
                    "help": "Channel: 101, 102, etc."
                },
                "SV3C": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/live/ch0",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "GoolRC": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/live/ch0",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "V380": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/av0_0",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "ICSee": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/ch0",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "ZMODo": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "SANNCE": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "AOSU": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "JIDE": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "JOOAN": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "SECO": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "VSTARCAM": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Wansview": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Hiseeu": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "ieGeek": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "APEMAN": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "ALPTOP": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "CTRING": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/Streaming/Channels/101",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "ONVIF": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:554/onvif1",
                    "fields": [],
                    "default_port": 554,
                    "help": ""
                },
                "Generic RTSP": {
                    "url_template": "rtsp://{user}:{pass}@{ip}:{port}/{custom_path}",
                    "fields": ["custom_path"],
                    "default_port": 554,
                    "help": "Example: live.sdp"
                },
                "Custom": {
                    "url_template": "{custom_url}",
                    "fields": [],
                    "default_port": 554,
                    "help": "Enter full RTSP URL"
                }
            }
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Camera table
        self.camera_table = ttk.Treeview(main_frame, columns=("name", "manufacturer", "ip_port", "url", "status"), show="headings")
        self.camera_table.heading("name", text="Nom")
        self.camera_table.heading("manufacturer", text="Constructeur")
        self.camera_table.heading("ip_port", text="IP:Port")
        self.camera_table.heading("url", text="URL RTSP")
        self.camera_table.heading("status", text="Statut")
        
        # Configure column widths
        self.camera_table.column("name", width=150)
        self.camera_table.column("manufacturer", width=120)
        self.camera_table.column("ip_port", width=100)
        self.camera_table.column("url", width=300)
        self.camera_table.column("status", width=80)
        
        self.camera_table.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        ttk.Button(button_frame, text="Ajouter", command=self.add_camera).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Éditer", command=self.edit_camera).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Supprimer", command=self.delete_camera).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tester", command=self.test_camera).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Lire dans VLC", command=self.play_in_vlc).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sauvegarder", command=self.save_playlist).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Charger", command=self.load_playlist).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)
        
        # Double-click to play
        self.camera_table.bind("<Double-1>", lambda event: self.play_in_vlc())
    
    def generate_rtsp_url(self, manufacturer, **kwargs):
        """Generate RTSP URL dynamically based on manufacturer template."""
        if manufacturer not in self.manufacturers:
            return None
        
        template = self.manufacturers[manufacturer]["url_template"]
        try:
            return template.format(**kwargs)
        except KeyError as e:
            messagebox.showerror("Erreur", f"Champ manquant: {e}")
            return None
    
    def add_camera(self):
        """Open a window to add a new camera."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter une caméra")
        add_window.geometry("600x500")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Common fields
        ttk.Label(add_window, text="Nom:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(add_window, width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Constructeur:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        manufacturer_var = tk.StringVar()
        manufacturer_combobox = ttk.Combobox(add_window, textvariable=manufacturer_var,
                                           values=list(self.manufacturers.keys()), width=37)
        manufacturer_combobox.grid(row=1, column=1, padx=5, pady=5)
        manufacturer_combobox.set("Hikvision")
        
        ttk.Label(add_window, text="IP:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ip_entry = ttk.Entry(add_window, width=40)
        ip_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Port:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        port_entry = ttk.Entry(add_window, width=40)
        port_entry.grid(row=3, column=1, padx=5, pady=5)
        port_entry.insert(0, "554")
        
        ttk.Label(add_window, text="Utilisateur:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        user_entry = ttk.Entry(add_window, width=40)
        user_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(add_window, text="Mot de passe:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        pass_entry = ttk.Entry(add_window, width=40, show="*")
        pass_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Dynamic fields frame
        dynamic_frame = ttk.Frame(add_window)
        dynamic_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Store dynamic entries
        dynamic_entries = {}
        
        def update_dynamic_fields(*args):
            """Update dynamic fields based on selected manufacturer."""
            # Clear previous dynamic fields
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
            dynamic_entries.clear()
            
            manufacturer = manufacturer_var.get()
            if manufacturer not in self.manufacturers:
                return
            
            fields = self.manufacturers[manufacturer].get("fields", [])
            for i, field in enumerate(fields):
                ttk.Label(dynamic_frame, text=f"{field}:").grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
                entry = ttk.Entry(dynamic_frame, width=30)
                entry.grid(row=i, column=1, padx=5, pady=2)
                dynamic_entries[field] = entry
            
            # Help text
            help_text = self.manufacturers[manufacturer].get("help", "")
            if help_text:
                ttk.Label(dynamic_frame, text=f"Aide: {help_text}", foreground="blue").grid(
                    row=len(fields), column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        manufacturer_var.trace_add("write", update_dynamic_fields)
        update_dynamic_fields()  # Initial call
        
        # Custom URL field (for Custom manufacturer)
        custom_url_frame = ttk.Frame(add_window)
        custom_url_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(custom_url_frame, text="URL RTSP personnalisée:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        custom_url_entry = ttk.Entry(custom_url_frame, width=40)
        custom_url_entry.grid(row=0, column=1, padx=5, pady=2)
        
        def update_custom_url_visibility(*args):
            """Show/hide custom URL field based on manufacturer."""
            if manufacturer_var.get() == "Custom":
                custom_url_frame.grid()
            else:
                custom_url_frame.grid_remove()
        
        manufacturer_var.trace_add("write", update_custom_url_visibility)
        update_custom_url_visibility()
        
        # Buttons
        button_frame = ttk.Frame(add_window)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Ajouter", command=lambda: self.save_new_camera(
            name_entry.get(), manufacturer_var.get(), ip_entry.get(), port_entry.get(),
            user_entry.get(), pass_entry.get(), dynamic_entries, custom_url_entry.get()
        )).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Annuler", command=add_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_new_camera(self, name, manufacturer, ip, port, user, password, dynamic_entries, custom_url):
        """Save a new camera to the list."""
        if not name or not manufacturer or not ip:
            messagebox.showerror("Erreur", "Les champs Nom, Constructeur et IP sont obligatoires.")
            return
        
        # Validate IP format
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            messagebox.showerror("Erreur", "Format d'IP invalide.")
            return
        
        # Prepare kwargs for URL generation
        kwargs = {
            "user": user,
            "pass": password,
            "ip": ip,
            "port": port
        }
        
        # Add dynamic fields
        for field, entry in dynamic_entries.items():
            kwargs[field] = entry.get()
        
        # Generate URL
        if manufacturer == "Custom":
            url = custom_url if custom_url else None
        else:
            url = self.generate_rtsp_url(manufacturer, **kwargs)
        
        if not url:
            return
        
        # Add to list
        self.cameras.append({
            "name": name,
            "manufacturer": manufacturer,
            "ip": ip,
            "port": port,
            "user": user,
            "password": password,
            "url": url,
            "dynamic_fields": {field: dynamic_entries[field].get() for field in dynamic_entries},
            "custom_url": custom_url if manufacturer == "Custom" else None
        })
        
        # Update table
        self.update_camera_table()
        self.status_var.set(f"Caméra ajoutée: {name}")
    
    def update_camera_table(self):
        """Update the camera table with current data."""
        for item in self.camera_table.get_children():
            self.camera_table.delete(item)
        
        for camera in self.cameras:
            self.camera_table.insert("", tk.END, values=(
                camera["name"],
                camera["manufacturer"],
                f"{camera['ip']}:{camera['port']}",
                camera["url"],
                ""
            ))
    
    def edit_camera(self):
        """Edit the selected camera."""
        selected = self.camera_table.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Aucune caméra sélectionnée.")
            return
        
        index = self.camera_table.index(selected[0])
        camera = self.cameras[index]
        
        # Create edit window (similar to add_camera but pre-filled)
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Éditer: {camera['name']}")
        edit_window.geometry("600x500")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        # Common fields
        ttk.Label(edit_window, text="Nom:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(edit_window, width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, camera["name"])
        
        ttk.Label(edit_window, text="Constructeur:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        manufacturer_var = tk.StringVar()
        manufacturer_combobox = ttk.Combobox(edit_window, textvariable=manufacturer_var,
                                           values=list(self.manufacturers.keys()), width=37)
        manufacturer_combobox.grid(row=1, column=1, padx=5, pady=5)
        manufacturer_combobox.set(camera["manufacturer"])
        
        ttk.Label(edit_window, text="IP:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ip_entry = ttk.Entry(edit_window, width=40)
        ip_entry.grid(row=2, column=1, padx=5, pady=5)
        ip_entry.insert(0, camera["ip"])
        
        ttk.Label(edit_window, text="Port:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        port_entry = ttk.Entry(edit_window, width=40)
        port_entry.grid(row=3, column=1, padx=5, pady=5)
        port_entry.insert(0, camera["port"])
        
        ttk.Label(edit_window, text="Utilisateur:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        user_entry = ttk.Entry(edit_window, width=40)
        user_entry.grid(row=4, column=1, padx=5, pady=5)
        user_entry.insert(0, camera["user"])
        
        ttk.Label(edit_window, text="Mot de passe:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        pass_entry = ttk.Entry(edit_window, width=40, show="*")
        pass_entry.grid(row=5, column=1, padx=5, pady=5)
        pass_entry.insert(0, camera["password"])
        
        # Dynamic fields frame
        dynamic_frame = ttk.Frame(edit_window)
        dynamic_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        # Store dynamic entries
        dynamic_entries = {}
        
        def update_dynamic_fields(*args):
            """Update dynamic fields based on selected manufacturer."""
            # Clear previous dynamic fields
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
            dynamic_entries.clear()
            
            manufacturer = manufacturer_var.get()
            if manufacturer not in self.manufacturers:
                return
            
            fields = self.manufacturers[manufacturer].get("fields", [])
            for i, field in enumerate(fields):
                ttk.Label(dynamic_frame, text=f"{field}:").grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
                entry = ttk.Entry(dynamic_frame, width=30)
                entry.grid(row=i, column=1, padx=5, pady=2)
                # Pre-fill with saved value if exists
                if camera.get("dynamic_fields") and field in camera["dynamic_fields"]:
                    entry.insert(0, camera["dynamic_fields"][field])
                dynamic_entries[field] = entry
            
            # Help text
            help_text = self.manufacturers[manufacturer].get("help", "")
            if help_text:
                ttk.Label(dynamic_frame, text=f"Aide: {help_text}", foreground="blue").grid(
                    row=len(fields), column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        manufacturer_var.trace_add("write", update_dynamic_fields)
        update_dynamic_fields()  # Initial call
        
        # Custom URL field
        custom_url_frame = ttk.Frame(edit_window)
        custom_url_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(custom_url_frame, text="URL RTSP personnalisée:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        custom_url_entry = ttk.Entry(custom_url_frame, width=40)
        custom_url_entry.grid(row=0, column=1, padx=5, pady=2)
        if camera.get("custom_url"):
            custom_url_entry.insert(0, camera["custom_url"])
        
        def update_custom_url_visibility(*args):
            """Show/hide custom URL field based on manufacturer."""
            if manufacturer_var.get() == "Custom":
                custom_url_frame.grid()
            else:
                custom_url_frame.grid_remove()
        
        manufacturer_var.trace_add("write", update_custom_url_visibility)
        update_custom_url_visibility()
        
        # Buttons
        button_frame = ttk.Frame(edit_window)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Sauvegarder", command=lambda: self.save_edited_camera(
            index, name_entry.get(), manufacturer_var.get(), ip_entry.get(), port_entry.get(),
            user_entry.get(), pass_entry.get(), dynamic_entries, custom_url_entry.get()
        )).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Annuler", command=edit_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_edited_camera(self, index, name, manufacturer, ip, port, user, password, dynamic_entries, custom_url):
        """Save edited camera data."""
        if not name or not manufacturer or not ip:
            messagebox.showerror("Erreur", "Les champs Nom, Constructeur et IP sont obligatoires.")
            return
        
        # Validate IP format
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            messagebox.showerror("Erreur", "Format d'IP invalide.")
            return
        
        # Prepare kwargs for URL generation
        kwargs = {
            "user": user,
            "pass": password,
            "ip": ip,
            "port": port
        }
        
        # Add dynamic fields
        for field, entry in dynamic_entries.items():
            kwargs[field] = entry.get()
        
        # Generate URL
        if manufacturer == "Custom":
            url = custom_url if custom_url else None
        else:
            url = self.generate_rtsp_url(manufacturer, **kwargs)
        
        if not url:
            return
        
        # Update camera data
        self.cameras[index] = {
            "name": name,
            "manufacturer": manufacturer,
            "ip": ip,
            "port": port,
            "user": user,
            "password": password,
            "url": url,
            "dynamic_fields": {field: dynamic_entries[field].get() for field in dynamic_entries},
            "custom_url": custom_url if manufacturer == "Custom" else None
        }
        
        # Update table
        self.update_camera_table()
        self.status_var.set(f"Caméra mise à jour: {name}")
    
    def delete_camera(self):
        """Delete the selected camera."""
        selected = self.camera_table.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Aucune caméra sélectionnée.")
            return
        
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette caméra ?"):
            index = self.camera_table.index(selected[0])
            del self.cameras[index]
            self.update_camera_table()
            self.status_var.set("Caméra supprimée")
    
    def test_camera(self):
        """Test if the selected camera is reachable and returns a valid RTSP stream."""
        selected = self.camera_table.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Aucune caméra sélectionnée.")
            return
        
        index = self.camera_table.index(selected[0])
        camera = self.cameras[index]
        
        self.status_var.set(f"Test en cours: {camera['name']}...")
        self.root.update()
        
        # Re-generate URL in case fields changed
        kwargs = {
            "user": camera["user"],
            "pass": camera["password"],
            "ip": camera["ip"],
            "port": camera["port"]
        }
        if camera.get("dynamic_fields"):
            kwargs.update(camera["dynamic_fields"])
        
        if camera["manufacturer"] == "Custom":
            url = camera.get("custom_url", "")
        else:
            url = self.generate_rtsp_url(camera["manufacturer"], **kwargs)
        
        try:
            # Check if ffprobe is available
            subprocess.run(["ffprobe", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            messagebox.showerror("Erreur", "ffprobe (FFmpeg) est requis pour tester les flux.\n\nInstallez-le avec:\n\nUbuntu/Debian: sudo apt install ffmpeg\n\nWindows: Téléchargez FFmpeg depuis https://ffmpeg.org")
            self.status_var.set("❌ ffprobe non installé")
            return
        
        try:
            # Test with ffprobe
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", 
                 "-of", "default=noprint_wrappers=1:nokey=1", url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )
            
            if result.returncode == 0 and b"video" in result.stdout:
                # Update status in table
                self.camera_table.item(selected[0], values=(
                    camera["name"],
                    camera["manufacturer"],
                    f"{camera['ip']}:{camera['port']}",
                    camera["url"],
                    "✅ OK"
                ))
                self.status_var.set(f"✅ {camera['name']}: Flux RTSP valide")
                messagebox.showinfo("Succès", f"Caméra joignable: {camera['name']}\nURL: {url}")
            else:
                self.camera_table.item(selected[0], values=(
                    camera["name"],
                    camera["manufacturer"],
                    f"{camera['ip']}:{camera['port']}",
                    camera["url"],
                    "❌ Échec"
                ))
                self.status_var.set(f"❌ {camera['name']}: Flux RTSP invalide")
                messagebox.showerror("Échec", f"Caméra non joignable: {camera['name']}\nURL: {url}")
        except subprocess.TimeoutExpired:
            self.camera_table.item(selected[0], values=(
                camera["name"],
                camera["manufacturer"],
                f"{camera['ip']}:{camera['port']}",
                camera["url"],
                "⏱️ Timeout"
            ))
            self.status_var.set(f"⏱️ {camera['name']}: Timeout")
            messagebox.showerror("Échec", f"Timeout pour: {camera['name']}")
        except Exception as e:
            self.camera_table.item(selected[0], values=(
                camera["name"],
                camera["manufacturer"],
                f"{camera['ip']}:{camera['port']}",
                camera["url"],
                "❌ Erreur"
            ))
            self.status_var.set(f"❌ {camera['name']}: Erreur")
            messagebox.showerror("Erreur", f"Erreur lors du test: {str(e)}")
    
    def play_in_vlc(self):
        """Play the selected camera stream in VLC."""
        selected = self.camera_table.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Aucune caméra sélectionnée.")
            return
        
        index = self.camera_table.index(selected[0])
        camera = self.cameras[index]
        
        # Re-generate URL dynamically
        kwargs = {
            "user": camera["user"],
            "pass": camera["password"],
            "ip": camera["ip"],
            "port": camera["port"]
        }
        if camera.get("dynamic_fields"):
            kwargs.update(camera["dynamic_fields"])
        
        if camera["manufacturer"] == "Custom":
            url = camera.get("custom_url", "")
        else:
            url = self.generate_rtsp_url(camera["manufacturer"], **kwargs)
        
        try:
            # Try to open with VLC
            subprocess.Popen(["vlc", url])
            self.status_var.set(f"Lecture dans VLC: {camera['name']}")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "VLC n'est pas installé ou n'est pas dans le PATH.\n\nInstallez VLC:\n\nUbuntu/Debian: sudo apt install vlc\n\nWindows: Téléchargez depuis https://www.videolan.org")
            self.status_var.set("❌ VLC non trouvé")
        except Exception as e:
            self.status_var.set(f"❌ Erreur VLC: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de lancer VLC: {str(e)}")
    
    def save_playlist(self):
        """Save the current playlist to a JSON file."""
        if not self.cameras:
            messagebox.showwarning("Avertissement", "Aucune caméra à sauvegarder.")
            return
        
        # Create playlists directory if it doesn't exist
        if not os.path.exists("playlists"):
            os.makedirs("playlists")
        
        # Ask for filename
        file_path = filedialog.asksaveasfilename(
            title="Sauvegarder la playlist",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialdir="playlists",
            initialfile=self.current_playlist
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.cameras, f, indent=4, ensure_ascii=False)
            self.current_playlist = os.path.basename(file_path)
            self.status_var.set(f"Playlist sauvegardée: {self.current_playlist}")
        except Exception as e:
            self.status_var.set(f"❌ Erreur sauvegarde: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de sauvegarder: {str(e)}")
    
    def load_playlist(self):
        """Load a playlist from a JSON file."""
        file_path = filedialog.askopenfilename(
            title="Charger une playlist",
            filetypes=[("JSON Files", "*.json")],
            initialdir="playlists"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.cameras = json.load(f)
            self.current_playlist = os.path.basename(file_path)
            self.update_camera_table()
            self.status_var.set(f"Playlist chargée: {self.current_playlist}")
        except Exception as e:
            self.status_var.set(f"❌ Erreur chargement: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de charger: {str(e)}")


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraManagerApp(root)
    root.mainloop()
