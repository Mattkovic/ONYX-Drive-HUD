from __future__ import annotations

import csv
import os
import json
import math
import socket
import struct
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from queue import Queue, Empty

from PyQt6.QtCore import Qt, QTimer, QPoint, QRectF, QPointF
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QBrush, QAction, QShortcut, QKeySequence, QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFormLayout, QLabel, QPushButton, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox,
    QColorDialog, QTabWidget, QLineEdit, QMessageBox, QGroupBox, QFrame, QFileDialog
)

try:
    import win32gui, win32con
    WIN32_OK = True
except Exception:
    WIN32_OK = False

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
    OPENPYXL_OK = True
except Exception:
    OPENPYXL_OK = False


APP_NAME = "ONYX Drive HUD"
CONFIG_PATH = Path("onyx_drive_hud_config.json")
ICON_PATH = Path("onyx_icon.ico")


LANGUAGES = {
    "en": "English",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "pt": "Português",
    "pl": "Polski",
    "tr": "Türkçe",
    "ru": "Русский",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "中文"
}

TEXT = {
    "en": {
        "title": "ONYX Drive HUD v4.2 SafeExit",
        "subtitle": "DRIVE HUD CONTROL CENTER · ONE PROCESS · SAFE EXIT · DYNO CLEAN",
        "general": "General", "tiles": "Tiles", "peak": "Peak Measurements",
        "design": "Design", "language": "Language", "hotkeys": "Keybinds",
        "save": "Save", "show_overlay": "Show Overlay", "hide_overlay": "Hide Overlay",
        "reset": "Reset all", "exit_app": "Exit ONYX", "start_recording": "Start Recording", "stop": "Stop",
        "reset_peaks": "Reset Peaks", "export_csv": "Export CSV", "export_xlsx": "Export XLSX",
        "system": "System / Appearance", "udp_port": "UDP port", "opacity": "Overlay opacity",
        "scale": "Scale", "tile_bg": "Tile background", "edit_mode": "Edit mode",
        "clickthrough": "Click-through", "select_tile": "Select tile",
        "position": "Position / Size / Color", "visible": "Visible", "width": "Width",
        "height": "Height", "label": "Label", "color": "Color", "choose_color": "Choose color",
        "apply_tile": "Apply tile", "theme": "Theme", "lang_hint": "English is default. German is included. Other major languages are available with mostly translated UI labels.",
        "saved": "Saved", "saved_msg": "Configuration saved. Overlay updates immediately.",
        "one_exe_note": "Overlay, Manager and Peak Measurements now share one UDP receiver in the same EXE.",
    },
    "de": {
        "title": "ONYX Drive HUD v4.2 SafeExit",
        "subtitle": "DRIVE HUD KONTROLLZENTRUM · EIN PROZESS · BLACKOUT BLUE",
        "general": "Allgemein", "tiles": "Kacheln", "peak": "Peak-Werte",
        "design": "Design", "language": "Sprache", "hotkeys": "Tasten",
        "save": "Speichern", "show_overlay": "Overlay anzeigen", "hide_overlay": "Overlay verstecken",
        "reset": "Alles zurücksetzen", "exit_app": "ONYX beenden", "start_recording": "Aufnahme starten", "stop": "Stop",
        "reset_peaks": "Peak-Werte zurücksetzen", "export_csv": "CSV exportieren", "export_xlsx": "XLSX exportieren",
        "system": "System / Darstellung", "udp_port": "UDP-Port", "opacity": "Overlay-Deckkraft",
        "scale": "Skalierung", "tile_bg": "Kachel-Hintergrund", "edit_mode": "Bearbeitungsmodus",
        "clickthrough": "Click-through", "select_tile": "Kachel auswählen",
        "position": "Position / Größe / Farbe", "visible": "Sichtbar", "width": "Breite",
        "height": "Höhe", "label": "Label", "color": "Farbe", "choose_color": "Farbe wählen",
        "apply_tile": "Kachel übernehmen", "theme": "Theme", "lang_hint": "Englisch ist Standard. Deutsch ist vollständig drin. Weitere Hauptsprachen sind mit den wichtigsten UI-Labels drin.",
        "saved": "Gespeichert", "saved_msg": "Konfiguration gespeichert. Overlay aktualisiert sich direkt.",
        "one_exe_note": "Overlay, Manager und Peak Measurements teilen sich jetzt einen UDP-Empfänger in derselben EXE.",
    },
}

PARTIAL = {
    "es": {"language":"Idioma","save":"Guardar","show_overlay":"Mostrar overlay","hide_overlay":"Ocultar overlay","reset":"Restablecer","choose_color":"Elegir color"},
    "fr": {"language":"Langue","save":"Enregistrer","show_overlay":"Afficher overlay","hide_overlay":"Masquer overlay","reset":"Réinitialiser","choose_color":"Choisir couleur"},
    "it": {"language":"Lingua","save":"Salva","show_overlay":"Mostra overlay","hide_overlay":"Nascondi overlay","reset":"Ripristina","choose_color":"Scegli colore"},
    "pt": {"language":"Idioma","save":"Salvar","show_overlay":"Mostrar overlay","hide_overlay":"Ocultar overlay","reset":"Redefinir","choose_color":"Escolher cor"},
    "pl": {"language":"Język","save":"Zapisz","show_overlay":"Pokaż overlay","hide_overlay":"Ukryj overlay","reset":"Resetuj","choose_color":"Wybierz kolor"},
    "tr": {"language":"Dil","save":"Kaydet","show_overlay":"Overlay göster","hide_overlay":"Overlay gizle","reset":"Sıfırla","choose_color":"Renk seç"},
    "ru": {"language":"Язык","save":"Сохранить","show_overlay":"Показать overlay","hide_overlay":"Скрыть overlay","reset":"Сброс","choose_color":"Выбрать цвет"},
    "ja": {"language":"言語","save":"保存","show_overlay":"Overlay 表示","hide_overlay":"Overlay 非表示","reset":"リセット","choose_color":"色を選択"},
    "ko": {"language":"언어","save":"저장","show_overlay":"오버레이 표시","hide_overlay":"오버레이 숨김","reset":"초기화","choose_color":"색상 선택"},
    "zh": {"language":"语言","save":"保存","show_overlay":"显示 Overlay","hide_overlay":"隐藏 Overlay","reset":"重置","choose_color":"选择颜色"},
}

def tr(lang: str, key: str) -> str:
    if lang in TEXT and key in TEXT[lang]:
        return TEXT[lang][key]
    if lang in PARTIAL and key in PARTIAL[lang]:
        return PARTIAL[lang][key]
    return TEXT["en"].get(key, key)


THEMES = {
    "Blackout Blue": {"bg":"#05080d","panel":"#07111b","field":"#02060a","accent":"#00b8ff","accent2":"#00d9ff","text":"#d9f7ff"},
    "Purple Night": {"bg":"#080511","panel":"#120a22","field":"#05020a","accent":"#b84dff","accent2":"#d66bff","text":"#f1ddff"},
    "Emerald Grid": {"bg":"#03100b","panel":"#071b13","field":"#010806","accent":"#00ff99","accent2":"#55ffcc","text":"#ddfff3"},
    "Amber Track": {"bg":"#120a02","panel":"#1d1004","field":"#090500","accent":"#ff9d00","accent2":"#ffd15a","text":"#fff2dd"},
    "Glass Cyan": {"bg":"#03090d","panel":"#061620","field":"#010507","accent":"#53e8ff","accent2":"#9af4ff","text":"#ecfcff"},
}

DEFAULT_CONFIG = {
    "udp_host": "0.0.0.0",
    "udp_port": 5607,
    "language": "en",
    "manager_theme": "Blackout Blue",
    "edit_mode": True,
    "click_through": False,
    "opacity": 0.92,
    "scale": 1.0,
    "background_alpha": 115,
    "font_family": "Segoe UI",
    "hotkeys": {"toggle_edit":"Ctrl+E","toggle_click":"Ctrl+T","save_layout":"Ctrl+S","reset_layout":"Ctrl+R","hide_overlay":"Esc"},
    "cards": {
        "speed": {"x": 35, "y": 85, "w": 230, "h": 88, "label": "KMH", "color": "#00d9ff", "visible": True},
        "rpm": {"x": 35, "y": 180, "w": 230, "h": 88, "label": "RPM", "color": "#ff6a00", "visible": True},
        "gear": {"x": 35, "y": 275, "w": 230, "h": 88, "label": "GEAR", "color": "#55ff00", "visible": True},
        "power": {"x": 35, "y": 370, "w": 230, "h": 88, "label": "PS", "color": "#ffd400", "visible": True},
        "boost": {"x": 35, "y": 465, "w": 230, "h": 88, "label": "BOOST", "color": "#c74cff", "visible": True},
    }
}

CARD_LABELS = {"speed":"KMH","rpm":"RPM","gear":"Gear","power":"PS","boost":"Boost"}


def deep_copy(obj):
    return json.loads(json.dumps(obj))

def load_config():
    cfg = deep_copy(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        try:
            user = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            for k, v in user.items():
                if k not in ("cards","hotkeys"):
                    cfg[k] = v
            if "hotkeys" in user:
                cfg["hotkeys"].update(user["hotkeys"])
            if "cards" in user:
                for ck, cv in user["cards"].items():
                    if ck in cfg["cards"]:
                        cfg["cards"][ck].update(cv)
        except Exception:
            pass
    return cfg

def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")

def make_style(theme_name):
    t = THEMES.get(theme_name, THEMES["Blackout Blue"])
    return f"""
QWidget {{
    background-color: {t['bg']};
    color: {t['text']};
    font-family: Segoe UI;
    font-size: 10.5pt;
}}
QTabWidget::pane {{
    border: 1px solid {t['accent']};
    border-radius: 10px;
    background: {t['panel']};
}}
QTabBar::tab {{
    background: {t['panel']};
    color: {t['text']};
    border: 1px solid {t['accent']};
    padding: 9px 16px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}
QTabBar::tab:selected {{
    background: {t['accent']};
    color: #001018;
}}
QGroupBox {{
    border: 1px solid {t['accent']};
    border-radius: 12px;
    margin-top: 14px;
    padding: 12px;
    background-color: {t['panel']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
    color: {t['accent2']};
    font-weight: bold;
}}
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {t['field']};
    border: 1px solid {t['accent']};
    border-radius: 7px;
    padding: 6px;
    color: #ffffff;
}}
QPushButton {{
    background-color: {t['panel']};
    color: {t['text']};
    border: 1px solid {t['accent']};
    border-radius: 9px;
    padding: 9px 14px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {t['field']};
    border: 1px solid {t['accent2']};
}}
QPushButton:pressed {{
    background-color: {t['accent']};
    color: #001018;
}}
QLabel#TitleLabel {{
    color: #ffffff;
    font-size: 24pt;
    font-weight: 800;
    letter-spacing: 3px;
}}
QLabel#SubtitleLabel {{
    color: {t['accent2']};
    font-size: 10pt;
}}
QFrame#Header {{
    background-color: {t['field']};
    border: 1px solid {t['accent']};
    border-radius: 16px;
}}
"""


@dataclass
class Telemetry:
    timestamp: float = 0.0
    raw_packet_size: int = 0
    engine_max_rpm: float = 0.0
    current_engine_rpm: float = 0.0
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    velocity_z: float = 0.0
    speed_mps: float = 0.0
    power_w: float = 0.0
    torque_nm: float = 0.0
    boost: float = 0.0
    gear: int = 0
    accel: int = 0
    brake: int = 0
    steer: int = 0

    @property
    def speed_kmh(self):
        if abs(self.speed_mps) > 0.01:
            return self.speed_mps * 3.6
        return math.sqrt(self.velocity_x**2 + self.velocity_y**2 + self.velocity_z**2) * 3.6

    @property
    def rpm(self):
        return int(round(self.current_engine_rpm))

    @property
    def power_ps(self):
        return int(round(max(0.0, self.power_w) / 735.49875))

    @property
    def throttle_pct(self):
        return max(0.0, min(100.0, self.accel / 255.0 * 100.0))

    @property
    def brake_pct(self):
        return max(0.0, min(100.0, self.brake / 255.0 * 100.0))


class ForzaParser:
    def parse(self, data: bytes):
        if len(data) < 200:
            return None
        t = Telemetry(timestamp=time.time(), raw_packet_size=len(data))
        o = 0
        def read(fmt):
            nonlocal o
            size = struct.calcsize("<" + fmt)
            if o + size > len(data):
                raise ValueError("short")
            val = struct.unpack_from("<" + fmt, data, o)[0]
            o += size
            return val
        try:
            read("i"); read("I")
            t.engine_max_rpm = read("f")
            read("f")
            t.current_engine_rpm = read("f")
            read("f"); read("f"); read("f")
            t.velocity_x = read("f"); t.velocity_y = read("f"); t.velocity_z = read("f")
            for _ in range(6): read("f")
            for _ in range(4): read("f")
            for _ in range(4): read("f")
            for _ in range(4): read("f")
            for _ in range(4): read("i")
            for _ in range(4): read("f")
            for _ in range(4): read("f")
            for _ in range(4): read("f")
            for _ in range(4): read("f")
            for _ in range(4): read("f")
            if o + 20 <= len(data):
                for _ in range(5): read("i")
            candidates = []
            for base in (o, 232, 244):
                if base + 79 <= len(data):
                    try:
                        speed = struct.unpack_from("<f", data, base + 12)[0]
                        power = struct.unpack_from("<f", data, base + 16)[0]
                        torque = struct.unpack_from("<f", data, base + 20)[0]
                        boost = struct.unpack_from("<f", data, base + 40)[0] if base + 44 <= len(data) else 0.0
                        co = base + 68
                        accel = struct.unpack_from("<B", data, co + 3)[0]
                        brake = struct.unpack_from("<B", data, co + 4)[0]
                        gear = struct.unpack_from("<B", data, co + 7)[0]
                        steer = struct.unpack_from("<b", data, co + 8)[0]
                        score = 0
                        if 0 <= speed < 250: score += 3
                        if 0 <= gear <= 15: score += 1
                        if -127 <= steer <= 127: score += 1
                        candidates.append((score, speed, power, torque, boost, accel, brake, gear, steer))
                    except Exception:
                        pass
            if candidates:
                candidates.sort(reverse=True)
                _, t.speed_mps, t.power_w, t.torque_nm, t.boost, t.accel, t.brake, t.gear, t.steer = candidates[0]
            return t
        except Exception:
            return None


class UdpReceiver:
    def __init__(self, host, port, queue):
        self.host, self.port, self.queue = host, int(port), queue
        self.parser = ForzaParser()
        self.stop_event = threading.Event()
        self.thread = None
        self.sock = None
        self.raw_count = 0
        self.parsed_count = 0
        self.last_sender = "-"
        self.last_error = ""

    def start(self):
        self.stop()
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.sock:
            try: self.sock.close()
            except Exception: pass
        self.sock = None

    def _run(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.settimeout(0.5)
            self.sock = s
            self.last_error = ""
            while not self.stop_event.is_set():
                try:
                    data, addr = s.recvfrom(4096)
                    self.raw_count += 1
                    self.last_sender = f"{addr[0]}:{addr[1]}"
                    tel = self.parser.parse(data)
                    if tel:
                        self.parsed_count += 1
                        self.queue.put(tel)
                except socket.timeout:
                    pass
                except OSError:
                    break
                except Exception as e:
                    self.last_error = str(e)
        except Exception as e:
            self.last_error = str(e)


class Card:
    def __init__(self, key, cfg):
        self.key = key
        self.cfg = cfg
        self.drag_offset = QPoint(0,0)

    @property
    def rect(self):
        return QRectF(float(self.cfg["x"]), float(self.cfg["y"]), float(self.cfg["w"]), float(self.cfg["h"]))

    def contains(self, p):
        return self.rect.contains(float(p.x()), float(p.y()))

    def value(self, tel):
        if tel is None:
            return {"speed":"0","rpm":"0","gear":"N","power":"0","boost":"0,00"}.get(self.key,"-")
        if self.key == "speed": return f"{tel.speed_kmh:.0f}"
        if self.key == "rpm": return f"{tel.rpm:,}".replace(",", ".")
        if self.key == "gear": return "R/N" if tel.gear == 0 else str(tel.gear)
        if self.key == "power": return str(tel.power_ps)
        if self.key == "boost": return f"{tel.boost:.2f}".replace(".", ",")
        return "-"


class OverlayWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.config = manager.config
        self.cards = {k: Card(k, self.config["cards"][k]) for k in self.config["cards"]}
        self.telemetry = None
        self.selected = None
        self.shortcuts = []
        self.setWindowTitle(APP_NAME + " Overlay")
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.apply_window_flags()
        self.register_shortcuts()

    def sync_config(self):
        self.config = self.manager.config
        self.cards = {k: Card(k, self.config["cards"][k]) for k in self.config["cards"]}
        self.apply_window_flags()
        self.register_shortcuts()
        self.update()

    def register_shortcuts(self):
        for s in self.shortcuts:
            s.setEnabled(False)
        self.shortcuts = []
        hk = self.config.get("hotkeys", {})
        actions = {
            "toggle_edit": self.manager.toggle_edit,
            "toggle_click": self.manager.toggle_click,
            "save_layout": self.manager.save_config_now,
            "reset_layout": self.manager.reset_all,
            "hide_overlay": self.hide
        }
        for name, func in actions.items():
            key = hk.get(name)
            if key:
                sc = QShortcut(QKeySequence(key), self)
                sc.activated.connect(func)
                self.shortcuts.append(sc)

    def apply_window_flags(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setWindowOpacity(float(self.config["opacity"]))
        self.show()
        if WIN32_OK:
            hwnd = int(self.winId())
            ex = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
            if self.config.get("click_through"):
                ex |= win32con.WS_EX_TRANSPARENT
            else:
                ex &= ~win32con.WS_EX_TRANSPARENT
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        for text, func in [
            ("Show Manager", self.manager.show),
            ("Reload Config", self.sync_config),
            ("Toggle edit mode", self.manager.toggle_edit),
            ("Toggle click-through", self.manager.toggle_click),
            ("Save layout", self.manager.save_config_now),
            ("Exit", QApplication.quit)
        ]:
            a = QAction(text, self)
            a.triggered.connect(func)
            menu.addAction(a)
        menu.exec(event.globalPos())

    def mousePressEvent(self, event):
        if not self.config.get("edit_mode", True) or event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.position().toPoint()
        for c in reversed(list(self.cards.values())):
            if c.cfg.get("visible", True) and c.contains(pos):
                self.selected = c
                r = c.rect
                c.drag_offset = QPoint(int(pos.x()-r.x()), int(pos.y()-r.y()))
                return

    def mouseMoveEvent(self, event):
        if not self.config.get("edit_mode", True) or not self.selected:
            return
        pos = event.position().toPoint()
        self.selected.cfg["x"] = int(pos.x() - self.selected.drag_offset.x())
        self.selected.cfg["y"] = int(pos.y() - self.selected.drag_offset.y())
        self.update()

    def mouseReleaseEvent(self, event):
        if self.selected:
            save_config(self.config)
            self.manager.reload_forms_from_config()
        self.selected = None

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.config.get("edit_mode", True):
            self.draw_hint(p)
        for c in self.cards.values():
            if c.cfg.get("visible", True):
                self.draw_card(p, c)

    def draw_hint(self, p):
        p.setPen(QColor(0, 220, 255, 210))
        p.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        r = self.manager.receiver
        p.drawText(18, 28, "ONYX ONEEXE | EDIT MODE | one UDP receiver")
        p.setFont(QFont("Segoe UI", 8))
        p.drawText(18, 48, f"UDP {self.config['udp_port']} | Raw {r.raw_count} | Parsed {r.parsed_count} | {r.last_sender}")

    def draw_card(self, p, c):
        scale = float(self.config["scale"])
        r = c.rect
        x, y, w, h = r.x(), r.y(), r.width()*scale, r.height()*scale
        col = QColor(c.cfg["color"])
        rect = QRectF(x,y,w,h)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor(0,0,0,min(220,int(self.config["background_alpha"])+45))))
        p.drawRoundedRect(rect.adjusted(6,6,6,6), 17, 17)
        p.setPen(QPen(QColor(col.red(), col.green(), col.blue(), 230), 2))
        p.setBrush(QBrush(QColor(2,8,14,int(self.config["background_alpha"]))))
        p.drawRoundedRect(rect, 16, 16)
        p.setPen(QPen(col, 4))
        p.drawLine(int(x+14), int(y+18), int(x+14), int(y+h-18))
        fs = int((34 if c.key == "rpm" else 38) * scale)
        p.setFont(QFont(self.config["font_family"], fs, QFont.Weight.Bold))
        p.setPen(QColor(235,250,255) if c.key == "speed" else col)
        p.drawText(QRectF(x+45,y+8,w-65,h*0.62), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, c.value(self.telemetry))
        p.setFont(QFont(self.config["font_family"], int(15*scale), QFont.Weight.Bold))
        p.setPen(col)
        label = c.cfg.get("label", c.key.upper())
        if c.key == "boost":
            label = label + "  bar" if "bar" not in label.lower() else label
        p.drawText(QRectF(x+47,y+h-35,w-60,32), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, label)
        p.setPen(QPen(QColor(col.red(), col.green(), col.blue(), 160), 2))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QRectF(x+w-42, y+14, 26, 26))



class DynoGraph(QWidget):
    """
    Clean dyno graph:
    - does NOT connect raw telemetry in time order
    - filters to full-throttle pull samples
    - bins by RPM and keeps the strongest/cleanest value per RPM bucket
    - draws sorted RPM curves only, so steering/shifting/coasting no longer creates rectangles
    """
    def __init__(self):
        super().__init__()
        self.samples = []
        self.setMinimumHeight(330)

    def set_samples(self, samples):
        self.samples = samples[-12000:]
        self.update()

    def _build_dyno_points(self):
        if not self.samples:
            return []

        # Clean pull filter. This removes steering/coasting/shifting garbage.
        valid = [
            s for s in self.samples
            if s.rpm >= 1200
            and s.throttle_pct >= 85
            and s.brake_pct <= 3
            and s.gear > 0
            and s.power_ps >= 0
            and s.speed_kmh >= 10
        ]

        # Fallback: if the user recorded too little clean full-throttle data.
        if len(valid) < 8:
            valid = [
                s for s in self.samples
                if s.rpm >= 1200 and s.gear > 0 and s.speed_kmh >= 10 and s.power_ps >= 0
            ]

        if len(valid) < 4:
            return []

        # Bin by RPM. For each RPM bucket, keep the highest PS sample.
        # This behaves much more like a real dyno curve.
        bucket_size = 150
        buckets = {}
        for s in valid:
            bucket = int(round(s.rpm / bucket_size) * bucket_size)
            old = buckets.get(bucket)
            if old is None or s.power_ps > old.power_ps:
                buckets[bucket] = s

        points = [buckets[k] for k in sorted(buckets)]
        if len(points) < 4:
            return []

        # Light smoothing over PS/NM/Boost to avoid telemetry spikes.
        smoothed = []
        for i, s in enumerate(points):
            lo = max(0, i - 1)
            hi = min(len(points), i + 2)
            window = points[lo:hi]
            # Create a lightweight copy-like object via original sample mutation-free wrapper.
            class P: pass
            p = P()
            p.rpm = s.rpm
            p.speed_kmh = sum(x.speed_kmh for x in window) / len(window)
            p.power_ps = sum(x.power_ps for x in window) / len(window)
            p.torque_nm = sum(x.torque_nm for x in window) / len(window)
            p.boost = sum(x.boost for x in window) / len(window)
            smoothed.append(p)
        return smoothed

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(14, 14, -14, -14)
        plot = rect.adjusted(62, 42, -34, -56)

        bg = QColor(3, 9, 15)
        grid = QColor(0, 180, 255, 65)
        cyan = QColor(0, 217, 255)
        amber = QColor(255, 190, 0)
        purple = QColor(190, 80, 255)
        green = QColor(85, 255, 0)

        p.setPen(QPen(QColor(0, 184, 255), 1))
        p.setBrush(QBrush(bg))
        p.drawRoundedRect(rect, 16, 16)

        p.setPen(QPen(grid, 1))
        for i in range(7):
            x = plot.left() + plot.width() * i / 6
            p.drawLine(int(x), plot.top(), int(x), plot.bottom())
        for i in range(5):
            y = plot.top() + plot.height() * i / 4
            p.drawLine(plot.left(), int(y), plot.right(), int(y))

        p.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        p.setPen(QColor(220, 250, 255))
        p.drawText(rect.left() + 18, rect.top() + 24, "PEAK MEASUREMENTS · DYNO CLEAN VIEW")

        points = self._build_dyno_points()
        if len(points) < 4:
            p.setFont(QFont("Segoe UI", 12))
            p.drawText(plot, Qt.AlignmentFlag.AlignCenter, "No clean pull yet. Use one gear, full throttle, no braking.")
            return

        min_rpm = max(0, min(s.rpm for s in points) - 250)
        max_rpm = max(s.rpm for s in points) + 250
        max_ps = max(1, max(s.power_ps for s in points))
        max_nm = max(1, max(abs(s.torque_nm) for s in points))
        max_boost = max(0.01, max(abs(s.boost) for s in points))
        y_max = max(max_ps, max_nm)

        def x_for(rpm):
            return plot.left() + (rpm - min_rpm) / max(1, (max_rpm - min_rpm)) * plot.width()

        def y_for_power(v):
            return plot.bottom() - v / max(1, y_max) * plot.height()

        def y_for_boost(v):
            # Boost as separate scaled overlay, lower intensity.
            return plot.bottom() - abs(v) / max_boost * plot.height()

        def draw_curve(values, color, width=3, boost=False):
            p.setPen(QPen(color, width))
            prev = None
            for s, value in values:
                y = y_for_boost(value) if boost else y_for_power(value)
                pt = QPointF(x_for(s.rpm), y)
                if prev:
                    p.drawLine(prev, pt)
                prev = pt

        # PS curve
        draw_curve([(s, s.power_ps) for s in points], cyan, 3, False)

        # NM curve
        draw_curve([(s, abs(s.torque_nm)) for s in points], amber, 2, False)

        # Boost curve, scaled to graph height
        if max_boost > 0.05:
            draw_curve([(s, s.boost) for s in points], purple, 2, True)

        # Labels
        p.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        p.setPen(cyan)
        p.drawText(plot.left() + 8, plot.top() + 20, "PS")
        p.setPen(amber)
        p.drawText(plot.left() + 48, plot.top() + 20, "NM")
        p.setPen(purple)
        p.drawText(plot.left() + 92, plot.top() + 20, "BOOST")
        p.setPen(QColor(220, 250, 255))
        p.drawText(plot.left(), rect.bottom() - 20, f"RPM {min_rpm:.0f} → {max_rpm:.0f}")

        peak_ps = max(points, key=lambda s: s.power_ps)
        peak_nm = max(points, key=lambda s: abs(s.torque_nm))
        peak_speed = max(self.samples, key=lambda s: s.speed_kmh) if self.samples else None
        peak_boost = max(points, key=lambda s: abs(s.boost))

        p.setPen(green)
        p.drawText(
            plot.left() + 160,
            rect.bottom() - 20,
            f"Peak {peak_ps.power_ps:.0f} PS @ {peak_ps.rpm:.0f} rpm · {abs(peak_nm.torque_nm):.0f} NM · {peak_boost.boost:.2f} bar · {peak_speed.speed_kmh:.1f} km/h"
        )


class PeakTab(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.samples = []
        self.recording = False
        self.build_ui()

    def build_ui(self):
        root = QVBoxLayout(self)
        box = QGroupBox("Peak Measurements / Dyno Lab")
        grid = QGridLayout(box)
        root.addWidget(box)
        self.labels = {}
        names = ["status","samples","peak_speed","peak_rpm","peak_ps","peak_nm","100_200","200_300"]
        defaults = ["Status: stopped","Samples: 0","Peak Speed: 0 km/h","Peak RPM: 0","Peak PS: 0","Peak NM: 0","100–200: -","200–300: -"]
        for i,(n,dv) in enumerate(zip(names,defaults)):
            lab = QLabel(dv)
            lab.setStyleSheet("font-weight:bold; color:#d9f7ff;")
            self.labels[n] = lab
            grid.addWidget(lab, i//2, i%2)
        row = QHBoxLayout()
        root.addLayout(row)
        self.btn_start = QPushButton(tr(self.manager.lang(), "start_recording"))
        self.btn_start.clicked.connect(self.start)
        row.addWidget(self.btn_start)
        self.btn_stop = QPushButton(tr(self.manager.lang(), "stop"))
        self.btn_stop.clicked.connect(self.stop)
        row.addWidget(self.btn_stop)
        self.btn_reset = QPushButton(tr(self.manager.lang(), "reset_peaks"))
        self.btn_reset.clicked.connect(self.clear)
        row.addWidget(self.btn_reset)
        self.btn_csv = QPushButton(tr(self.manager.lang(), "export_csv"))
        self.btn_csv.clicked.connect(self.export_csv)
        row.addWidget(self.btn_csv)
        self.btn_xlsx = QPushButton(tr(self.manager.lang(), "export_xlsx"))
        self.btn_xlsx.clicked.connect(self.export_xlsx)
        row.addWidget(self.btn_xlsx)
        self.graph = DynoGraph()
        root.addWidget(self.graph, 1)
        hint = QLabel("Tip: Clean dyno uses only RPM, KMH, PS, NM and Boost from full-throttle pull samples. Steering/braking/coasting are filtered out.")
        hint.setWordWrap(True)
        root.addWidget(hint)

    def start(self):
        self.samples = []
        self.recording = True
        self.labels["status"].setText("Status: Recording")

    def stop(self):
        self.recording = False
        self.labels["status"].setText("Status: stopped")

    def clear(self):
        self.samples = []
        self.graph.set_samples([])
        self.update_labels()

    def add_sample(self, t):
        if self.recording:
            self.samples.append(t)
            if len(self.samples) > 60000:
                self.samples = self.samples[-60000:]
            self.update_labels()
            self.graph.set_samples(self.samples)

    def calc_accel(self, low, high):
        best = None
        start = None
        for s in self.samples:
            if start is None and s.speed_kmh >= low and s.throttle_pct > 80:
                start = s
            if start is not None and s.speed_kmh >= high:
                dt = s.timestamp - start.timestamp
                if dt > 0:
                    best = dt if best is None else min(best, dt)
                start = None
        return "-" if best is None else f"{best:.2f} s"

    def update_labels(self):
        if not self.samples:
            self.labels["samples"].setText("Samples: 0")
            self.labels["peak_speed"].setText("Peak Speed: 0 km/h")
            self.labels["peak_rpm"].setText("Peak RPM: 0")
            self.labels["peak_ps"].setText("Peak PS: 0")
            self.labels["peak_nm"].setText("Peak NM: 0")
            self.labels["100_200"].setText("100–200: -")
            self.labels["200_300"].setText("200–300: -")
            return
        peak_speed = max(self.samples, key=lambda s:s.speed_kmh)
        peak_rpm = max(self.samples, key=lambda s:s.rpm)
        peak_ps = max(self.samples, key=lambda s:s.power_ps)
        peak_nm = max(self.samples, key=lambda s:abs(s.torque_nm))
        self.labels["samples"].setText(f"Samples: {len(self.samples)}")
        self.labels["peak_speed"].setText(f"Peak Speed: {peak_speed.speed_kmh:.1f} km/h")
        self.labels["peak_rpm"].setText(f"Peak RPM: {peak_rpm.rpm:.0f}")
        self.labels["peak_ps"].setText(f"Peak PS: {peak_ps.power_ps:.0f} @ {peak_ps.rpm:.0f} rpm")
        self.labels["peak_nm"].setText(f"Peak NM: {abs(peak_nm.torque_nm):.0f} @ {peak_nm.rpm:.0f} rpm")
        self.labels["100_200"].setText(f"100–200: {self.calc_accel(100,200)}")
        self.labels["200_300"].setText(f"200–300: {self.calc_accel(200,300)}")

    def rows(self):
        if not self.samples: return []
        t0 = self.samples[0].timestamp
        return [{
            "time_s": round(s.timestamp-t0,4),
            "speed_kmh": round(s.speed_kmh,3),
            "rpm": round(s.rpm,1),
            "power_ps": round(s.power_ps,3),
            "torque_nm": round(s.torque_nm,3),
            "gear": s.gear,
            "throttle_pct": round(s.throttle_pct,2),
            "brake_pct": round(s.brake_pct,2),
            "boost_bar": round(s.boost,4),
        } for s in self.samples]

    def export_csv(self):
        rows = self.rows()
        if not rows:
            QMessageBox.warning(self, "No data", "No samples.")
            return
        path,_ = QFileDialog.getSaveFileName(self, "Export CSV", "onyx_peak_measurements.csv", "CSV (*.csv)")
        if not path: return
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
            w.writeheader(); w.writerows(rows)
        QMessageBox.information(self, "Export", f"CSV saved:\n{path}")

    def export_xlsx(self):
        rows = self.rows()
        if not rows:
            QMessageBox.warning(self, "No data", "No samples.")
            return
        if not OPENPYXL_OK:
            QMessageBox.warning(self, "Missing dependency", "openpyxl missing.")
            return
        path,_ = QFileDialog.getSaveFileName(self, "Export XLSX", "onyx_peak_measurements.xlsx", "Excel (*.xlsx)")
        if not path: return
        wb = Workbook()
        ws = wb.active
        ws.title = "Peak Measurements"
        headers = list(rows[0].keys())
        ws.append(headers)
        for r in rows:
            ws.append([r[h] for h in headers])
        fill = PatternFill("solid", fgColor="00111A")
        font = Font(color="FFFFFF", bold=True)
        thin = Side(style="thin", color="00B8FF")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)
        for c in ws[1]:
            c.fill = fill; c.font = font; c.border = border; c.alignment = Alignment(horizontal="center")
        for col in ws.columns:
            max_len = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 22)
        summary = wb.create_sheet("Summary")
        peak_speed = max(self.samples, key=lambda s:s.speed_kmh)
        peak_rpm = max(self.samples, key=lambda s:s.rpm)
        peak_ps = max(self.samples, key=lambda s:s.power_ps)
        peak_nm = max(self.samples, key=lambda s:abs(s.torque_nm))
        for r in [
            ["Metric","Value"],["Peak Speed km/h",round(peak_speed.speed_kmh,2)],["Peak RPM",round(peak_rpm.rpm,0)],
            ["Peak PS",round(peak_ps.power_ps,2)],["Peak PS RPM",round(peak_ps.rpm,0)],
            ["Peak Torque NM",round(abs(peak_nm.torque_nm),2)],["Peak Torque RPM",round(peak_nm.rpm,0)],
            ["100-200 km/h",self.calc_accel(100,200)],["200-300 km/h",self.calc_accel(200,300)],["Samples",len(self.samples)]
        ]:
            summary.append(r)
        wb.save(path)
        QMessageBox.information(self, "Export", f"XLSX saved:\n{path}")


class ManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.queue = Queue()
        self.receiver = UdpReceiver(self.config["udp_host"], self.config["udp_port"], self.queue)
        self.receiver.start()
        self.latest = None
        self.overlay = None
        self.setWindowTitle(tr(self.lang(), "title"))
        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))
        self.resize(920, 760)
        self.setStyleSheet(make_style(self.config.get("manager_theme", "Blackout Blue")))
        self.build_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(33)

        self.exit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.exit_shortcut.activated.connect(self.force_exit)

    def lang(self):
        return self.config.get("language", "en")

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16,16,16,16)
        root.setSpacing(12)
        header = QFrame(); header.setObjectName("Header")
        hl = QVBoxLayout(header)
        title = QLabel("ONYX"); title.setObjectName("TitleLabel")
        sub = QLabel(tr(self.lang(), "subtitle")); sub.setObjectName("SubtitleLabel")
        hl.addWidget(title); hl.addWidget(sub)
        root.addWidget(header)
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)
        self.tabs.addTab(self.build_general_tab(), tr(self.lang(), "general"))
        self.tabs.addTab(self.build_tiles_tab(), tr(self.lang(), "tiles"))
        self.peak_tab = PeakTab(self)
        self.tabs.addTab(self.peak_tab, tr(self.lang(), "peak"))
        self.tabs.addTab(self.build_design_tab(), tr(self.lang(), "design"))
        self.tabs.addTab(self.build_language_tab(), tr(self.lang(), "language"))
        self.tabs.addTab(self.build_hotkeys_tab(), tr(self.lang(), "hotkeys"))
        row = QHBoxLayout()
        root.addLayout(row)
        self.btn_save = QPushButton(tr(self.lang(), "save")); self.btn_save.clicked.connect(self.save_from_forms); row.addWidget(self.btn_save)
        self.btn_overlay = QPushButton(tr(self.lang(), "show_overlay")); self.btn_overlay.clicked.connect(self.show_overlay); row.addWidget(self.btn_overlay)
        self.btn_hide = QPushButton(tr(self.lang(), "hide_overlay")); self.btn_hide.clicked.connect(lambda: self.overlay.hide() if self.overlay else None); row.addWidget(self.btn_hide)
        self.btn_reset = QPushButton(tr(self.lang(), "reset")); self.btn_reset.clicked.connect(self.reset_all); row.addWidget(self.btn_reset)
        self.btn_exit = QPushButton(tr(self.lang(), "exit_app")); self.btn_exit.clicked.connect(self.force_exit); row.addWidget(self.btn_exit)

    def build_general_tab(self):
        w = QWidget(); outer = QVBoxLayout(w)
        box = QGroupBox(tr(self.lang(), "system")); form = QFormLayout(box); outer.addWidget(box)
        self.udp_port = QSpinBox(); self.udp_port.setRange(1,65535); self.udp_port.setValue(int(self.config["udp_port"]))
        form.addRow(tr(self.lang(),"udp_port")+":", self.udp_port)
        self.opacity = QDoubleSpinBox(); self.opacity.setRange(0.25,1.0); self.opacity.setSingleStep(0.05); self.opacity.setValue(float(self.config["opacity"]))
        form.addRow(tr(self.lang(),"opacity")+":", self.opacity)
        self.scale = QDoubleSpinBox(); self.scale.setRange(0.6,1.8); self.scale.setSingleStep(0.05); self.scale.setValue(float(self.config["scale"]))
        form.addRow(tr(self.lang(),"scale")+":", self.scale)
        self.bg_alpha = QSpinBox(); self.bg_alpha.setRange(0,255); self.bg_alpha.setValue(int(self.config["background_alpha"]))
        form.addRow(tr(self.lang(),"tile_bg")+":", self.bg_alpha)
        self.edit_mode = QCheckBox("enabled"); self.edit_mode.setChecked(bool(self.config["edit_mode"]))
        form.addRow(tr(self.lang(),"edit_mode")+":", self.edit_mode)
        self.click = QCheckBox("enabled"); self.click.setChecked(bool(self.config["click_through"]))
        form.addRow(tr(self.lang(),"clickthrough")+":", self.click)
        info = QLabel(tr(self.lang(),"one_exe_note")); info.setWordWrap(True); form.addRow("Info:", info)
        outer.addStretch(1); return w

    def build_tiles_tab(self):
        w = QWidget(); layout = QVBoxLayout(w)
        box_sel = QGroupBox(tr(self.lang(),"select_tile")); row = QHBoxLayout(box_sel)
        self.card_select = QComboBox()
        for key,label in CARD_LABELS.items(): self.card_select.addItem(label, key)
        self.card_select.currentIndexChanged.connect(self.load_card_to_form)
        row.addWidget(QLabel("Element:")); row.addWidget(self.card_select); layout.addWidget(box_sel)
        box = QGroupBox(tr(self.lang(),"position")); form = QFormLayout(box); layout.addWidget(box)
        self.card_visible = QCheckBox(tr(self.lang(),"visible"))
        self.card_x = QSpinBox(); self.card_x.setRange(-5000,5000)
        self.card_y = QSpinBox(); self.card_y.setRange(-5000,5000)
        self.card_w = QSpinBox(); self.card_w.setRange(80,2000)
        self.card_h = QSpinBox(); self.card_h.setRange(50,1000)
        self.card_label = QLineEdit()
        self.card_color_btn = QPushButton(tr(self.lang(),"choose_color")); self.card_color_btn.clicked.connect(self.choose_color)
        form.addRow(tr(self.lang(),"visible")+":", self.card_visible)
        form.addRow("X:", self.card_x); form.addRow("Y:", self.card_y)
        form.addRow(tr(self.lang(),"width")+":", self.card_w); form.addRow(tr(self.lang(),"height")+":", self.card_h)
        form.addRow(tr(self.lang(),"label")+":", self.card_label); form.addRow(tr(self.lang(),"color")+":", self.card_color_btn)
        btn = QPushButton(tr(self.lang(),"apply_tile")); btn.clicked.connect(self.apply_current_card); layout.addWidget(btn)
        layout.addStretch(1); self.load_card_to_form(); return w

    def build_design_tab(self):
        w = QWidget(); outer = QVBoxLayout(w)
        box = QGroupBox("Manager Design / Theme"); form = QFormLayout(box); outer.addWidget(box)
        self.theme_select = QComboBox()
        for name in THEMES: self.theme_select.addItem(name)
        idx = self.theme_select.findText(self.config.get("manager_theme","Blackout Blue"))
        if idx >= 0: self.theme_select.setCurrentIndex(idx)
        self.theme_select.currentTextChanged.connect(self.apply_theme_preview)
        form.addRow(tr(self.lang(),"theme")+":", self.theme_select)
        outer.addStretch(1); return w

    def build_language_tab(self):
        w = QWidget(); outer = QVBoxLayout(w)
        box = QGroupBox("Language / Sprache"); form = QFormLayout(box); outer.addWidget(box)
        self.language_select = QComboBox()
        for code,name in LANGUAGES.items(): self.language_select.addItem(name, code)
        idx = self.language_select.findData(self.lang())
        if idx >= 0: self.language_select.setCurrentIndex(idx)
        form.addRow("Language:", self.language_select)
        hint = QLabel(tr(self.lang(),"lang_hint")); hint.setWordWrap(True); form.addRow("Info:", hint)
        btn = QPushButton("Apply / Anwenden"); btn.clicked.connect(self.apply_language); form.addRow(btn)
        outer.addStretch(1); return w

    def build_hotkeys_tab(self):
        w = QWidget(); outer = QVBoxLayout(w)
        box = QGroupBox("Keyboard shortcuts"); form = QFormLayout(box); outer.addWidget(box)
        hk = self.config.get("hotkeys",{})
        self.hk_toggle_edit = QLineEdit(hk.get("toggle_edit","Ctrl+E"))
        self.hk_toggle_click = QLineEdit(hk.get("toggle_click","Ctrl+T"))
        self.hk_save = QLineEdit(hk.get("save_layout","Ctrl+S"))
        self.hk_reset = QLineEdit(hk.get("reset_layout","Ctrl+R"))
        self.hk_hide = QLineEdit(hk.get("hide_overlay","Esc"))
        form.addRow("Edit mode:", self.hk_toggle_edit); form.addRow("Click-through:", self.hk_toggle_click)
        form.addRow("Save layout:", self.hk_save); form.addRow("Reset layout:", self.hk_reset); form.addRow("Hide overlay:", self.hk_hide)
        outer.addStretch(1); return w

    def current_card_key(self): return self.card_select.currentData()

    def load_card_to_form(self):
        if not hasattr(self, "card_select"): return
        key = self.current_card_key()
        if not key: return
        c = self.config["cards"][key]
        self.card_visible.setChecked(bool(c.get("visible",True)))
        self.card_x.setValue(int(c.get("x",0))); self.card_y.setValue(int(c.get("y",0)))
        self.card_w.setValue(int(c.get("w",230))); self.card_h.setValue(int(c.get("h",88)))
        self.card_label.setText(str(c.get("label", CARD_LABELS.get(key,key))))
        self.card_color_btn.setStyleSheet(f"background-color:{c.get('color','#fff')}; color:#001018;")

    def reload_forms_from_config(self):
        if hasattr(self, "card_select"):
            self.load_card_to_form()

    def apply_current_card(self):
        if not hasattr(self, "card_select"): return
        key = self.current_card_key()
        c = self.config["cards"][key]
        c["visible"] = self.card_visible.isChecked()
        c["x"] = int(self.card_x.value()); c["y"] = int(self.card_y.value())
        c["w"] = int(self.card_w.value()); c["h"] = int(self.card_h.value())
        c["label"] = self.card_label.text().strip()

    def choose_color(self):
        key = self.current_card_key()
        col = QColorDialog.getColor(QColor(self.config["cards"][key].get("color","#fff")), self)
        if col.isValid():
            self.config["cards"][key]["color"] = col.name()
            self.card_color_btn.setStyleSheet(f"background-color:{col.name()}; color:#001018;")

    def collect_forms(self):
        self.apply_current_card()
        self.config["udp_port"] = int(self.udp_port.value())
        self.config["opacity"] = float(self.opacity.value())
        self.config["scale"] = float(self.scale.value())
        self.config["background_alpha"] = int(self.bg_alpha.value())
        self.config["edit_mode"] = self.edit_mode.isChecked()
        self.config["click_through"] = self.click.isChecked()
        self.config["manager_theme"] = self.theme_select.currentText() if hasattr(self,"theme_select") else self.config.get("manager_theme","Blackout Blue")
        self.config["language"] = self.language_select.currentData() if hasattr(self,"language_select") else self.lang()
        self.config["hotkeys"] = {
            "toggle_edit": self.hk_toggle_edit.text().strip(),
            "toggle_click": self.hk_toggle_click.text().strip(),
            "save_layout": self.hk_save.text().strip(),
            "reset_layout": self.hk_reset.text().strip(),
            "hide_overlay": self.hk_hide.text().strip(),
        }

    def save_from_forms(self):
        old_port = self.config["udp_port"]
        self.collect_forms()
        save_config(self.config)
        if int(old_port) != int(self.config["udp_port"]):
            self.restart_receiver()
        if self.overlay:
            self.overlay.sync_config()
        QMessageBox.information(self, tr(self.lang(),"saved"), tr(self.lang(),"saved_msg"))

    def save_config_now(self):
        save_config(self.config)

    def apply_language(self):
        self.collect_forms()
        save_config(self.config)
        QMessageBox.information(self, "OK", "Language saved. Manager will restart.")
        self.rebuild_ui()

    def apply_theme_preview(self, name):
        self.config["manager_theme"] = name
        self.setStyleSheet(make_style(name))

    def rebuild_ui(self):
        self.setWindowTitle(tr(self.lang(), "title"))
        old_overlay_visible = self.overlay.isVisible() if self.overlay else False
        self.takeCentralWidget()
        self.build_ui()
        self.setStyleSheet(make_style(self.config.get("manager_theme","Blackout Blue")))
        if self.overlay:
            self.overlay.sync_config()
            if old_overlay_visible: self.overlay.show()

    def show_overlay(self):
        self.save_from_forms()
        if not self.overlay:
            self.overlay = OverlayWindow(self)
            screen = QApplication.primaryScreen()
            if screen: self.overlay.setGeometry(screen.geometry())
        self.overlay.show()
        self.overlay.raise_()

    def toggle_edit(self):
        self.config["edit_mode"] = not self.config.get("edit_mode", True)
        save_config(self.config)
        if self.overlay: self.overlay.sync_config()

    def toggle_click(self):
        self.config["click_through"] = not self.config.get("click_through", False)
        save_config(self.config)
        if self.overlay: self.overlay.sync_config()

    def reset_all(self):
        self.config = deep_copy(DEFAULT_CONFIG)
        save_config(self.config)
        self.restart_receiver()
        self.rebuild_ui()

    def restart_receiver(self):
        self.receiver.stop()
        self.receiver = UdpReceiver(self.config["udp_host"], self.config["udp_port"], self.queue)
        self.receiver.start()

    def tick(self):
        changed = False
        try:
            while True:
                self.latest = self.queue.get_nowait()
                changed = True
                if hasattr(self, "peak_tab"):
                    self.peak_tab.add_sample(self.latest)
        except Empty:
            pass
        if changed and self.overlay:
            self.overlay.telemetry = self.latest
            self.overlay.update()

    def force_exit(self):
        """
        SafeExit / Killswitch:
        - saves config
        - stops UDP socket
        - hides overlay
        - quits Qt
        - hard-exits the Python process so no frozen window/thread remains
        """
        try:
            save_config(self.config)
        except Exception:
            pass

        try:
            if self.receiver:
                self.receiver.stop()
        except Exception:
            pass

        try:
            if self.overlay:
                self.overlay.hide()
        except Exception:
            pass

        try:
            app = QApplication.instance()
            if app:
                app.quit()
        except Exception:
            pass

        os._exit(0)

    def closeEvent(self, event):
        event.accept()
        self.force_exit()


def main():
    app = QApplication(sys.argv)
    if ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(ICON_PATH)))
    w = ManagerWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
