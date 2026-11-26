import ctypes
import glob
import hashlib
import io
import json
import math
import os
import platform
import random
import re
import shutil
import struct
import subprocess
import sys
import threading
import tempfile
import time
import urllib.parse
import wave
import zipfile
from collections import deque
import webbrowser
import winsound
from datetime import datetime, timezone

# 1. DPI awareness immediately after imports so Windows scaling (125%, 150%, 175%)
# renders the launcher and PhotoRBX\photoloading.jpg at 100% with zero margins/bars.
if platform.system().lower() == "windows":
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

import base64
import tkinter
from tkinter import filedialog

import customtkinter as ctk
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk

CURRENT_VERSION = "1.4.5"
PUBLISHER_NAME = "Kilon"
GITHUB_REPO = "debliksmen-lab/RBX-Client"
GITHUB_API_LATEST = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_API_TAGS = f"https://api.github.com/repos/{GITHUB_REPO}/tags"
PROTOCOL_SCHEME = "rbxclient"
RBX_AI_ENDPOINT = "https://text.pollinations.ai/openai"
RBX_AI_MODEL = "openai"

APP_WIDTH = 1160
APP_HEIGHT = 720
APP_ALPHA = 0.96
SPLASH_NORMAL_SEC = 6.5
SPLASH_FIRST_RUN_SEC = 11.0
ONLINE_REFRESH_INTERVAL_SEC = 20

COLOR_BG = "#090C10"
COLOR_BORDER = "#222C3D"
COLOR_SURFACE = "#11161F"
COLOR_SURFACE_ALT = "#171E2B"
COLOR_SURFACE_HOVER = "#1F2938"
COLOR_ACCENT = "#3B82F6"
COLOR_ACCENT_HOVER = "#2563EB"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"
COLOR_TEXT = "#F3F6FA"
COLOR_TEXT_MUTED = "#8B98A9"
COLOR_TEXT_DIM = "#5A6577"

WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
GWL_EXSTYLE = -20
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020
SW_MINIMIZE = 6
SW_RESTORE = 9
SW_MAXIMIZE = 3

SUPPORTED_LANGUAGES = ("ru", "en", "uk", "de", "fr", "es", "pt", "tr", "ja", "ko")

UI_TRANSLATIONS = {
    "ru": {
        "window_title": "RBX Client",
        "nav_launcher": "Лаунчер",
        "nav_profile": "Профиль",
        "nav_search": "Поиск игр",
        "nav_servers": "Server Hopper",
        "nav_settings": "Настройки",
        "load": "Загрузить",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "ИГРАТЬ",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "en": {
        "window_title": "RBX Client",
        "nav_launcher": "Launcher",
        "nav_profile": "Profile",
        "nav_search": "Game Search",
        "nav_servers": "Server Hopper",
        "nav_settings": "Settings",
        "load": "Load",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "PLAY",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "uk": {
        "window_title": "RBX Client",
        "nav_launcher": "Лаунчер",
        "nav_profile": "Профіль",
        "nav_search": "Пошук ігор",
        "nav_servers": "Server Hopper",
        "nav_settings": "Налаштування",
        "load": "Завантажити",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "ГРАТИ",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "de": {
        "window_title": "RBX Client",
        "nav_launcher": "Launcher",
        "nav_profile": "Profil",
        "nav_search": "Spielesuche",
        "nav_servers": "Server Hopper",
        "nav_settings": "Einstellungen",
        "load": "Laden",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "SPIELEN",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "fr": {
        "window_title": "RBX Client",
        "nav_launcher": "Lanceur",
        "nav_profile": "Profil",
        "nav_search": "Recherche",
        "nav_servers": "Server Hopper",
        "nav_settings": "Paramètres",
        "load": "Charger",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "JOUER",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "es": {
        "window_title": "RBX Client",
        "nav_launcher": "Lanzador",
        "nav_profile": "Perfil",
        "nav_search": "Buscar juegos",
        "nav_servers": "Server Hopper",
        "nav_settings": "Ajustes",
        "load": "Cargar",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "JUGAR",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "pt": {
        "window_title": "RBX Client",
        "nav_launcher": "Inicializador",
        "nav_profile": "Perfil",
        "nav_search": "Buscar jogos",
        "nav_servers": "Server Hopper",
        "nav_settings": "Configurações",
        "load": "Carregar",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "JOGAR",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "tr": {
        "window_title": "RBX Client",
        "nav_launcher": "Başlatıcı",
        "nav_profile": "Profil",
        "nav_search": "Oyun Ara",
        "nav_servers": "Server Hopper",
        "nav_settings": "Ayarlar",
        "load": "Yükle",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "OYNA",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "ja": {
        "window_title": "RBX Client",
        "nav_launcher": "ランチャー",
        "nav_profile": "プロフィール",
        "nav_search": "ゲーム検索",
        "nav_servers": "Server Hopper",
        "nav_settings": "設定",
        "load": "読込",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "プレイ",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
    "ko": {
        "window_title": "RBX Client",
        "nav_launcher": "런처",
        "nav_profile": "프로필",
        "nav_search": "게임 검색",
        "nav_servers": "Server Hopper",
        "nav_settings": "설정",
        "load": "불러오기",
        "copy_link": "Copy Link",
        "rejoin": "Rejoin",
        "play": "플레이",
        "shield_ok": "Protected • No threats detected",
        "shield_alert": "Warning • Threat detected by RBX Shield",
        "shield_off": "RBX Shield disabled",
        "clear_roblox_cache": "Clear Roblox Cache",
    },
}

for _lang_pack in UI_TRANSLATIONS.values():
    _lang_pack.setdefault("nav_ai", "RBX AI")

DEFAULT_CONFIG = {
    "language": "ru",
    "theme_mode": "dark",
    "window_alpha": APP_ALPHA,
    "sound_click": True,
    "sound_startup": True,
    "auto_fullscreen_f11": True,
    "minimize_on_launch": False,
    "auto_join_emptiest": False,
    "show_toasts": True,
    "show_fps_ping_overlay": False,
    "security_guard_enabled": True,
    "last_place_id": 2753915549,
    "fps_cap": 144,
    "render_engine": "DirectX 11",
    "disable_shadows": False,
    "disable_grass": False,
    "disable_telemetry": True,
    "disable_motion_blur": True,
    "low_texture_quality": False,
    "classic_oof_sound": False,
    "disable_overlay_analytics": True,
    "quality_level": "Авто",
    "custom_shaders_path": "",
    "shaders_installed": False,
}

FALLBACK_GAMES = [
    {"place_id": 2753915549, "universe_id": 994732206, "name": "Blox Fruits", "creator": "Gamer Robot Inc", "playing": 420000},
    {"place_id": 920587237, "universe_id": 383310974, "name": "Adopt Me!", "creator": "Uplift Games", "playing": 215000},
    {"place_id": 155615604, "universe_id": 688426624, "name": "Prison Life", "creator": "Aesthetical", "playing": 48000},
    {"place_id": 292439477, "universe_id": 115797356, "name": "Phantom Forces", "creator": "StyLiS Studios", "playing": 19500},
    {"place_id": 606849621, "universe_id": 245662005, "name": "Jailbreak", "creator": "Badimo", "playing": 34000},
    {"place_id": 142823291, "universe_id": 66654135, "name": "Murder Mystery 2", "creator": "Nikilis", "playing": 89000},
    {"place_id": 1962086868, "universe_id": 73885730, "name": "Tower of Hell", "creator": "YXCeption", "playing": 26400},
    {"place_id": 1537690962, "universe_id": 6011308632, "name": "Bee Swarm Simulator", "creator": "Onett", "playing": 41200},
    {"place_id": 286090429, "universe_id": 111958650, "name": "Arsenal", "creator": "ROLVe Community", "playing": 31800},
    {"place_id": 6284583030, "universe_id": 2380077519, "name": "Pet Simulator X", "creator": "BIG Games Pets", "playing": 12400},
]

SECURITY_POLICY_TEXT = f"""RBX CLIENT v{CURRENT_VERSION} — ПОЛИТИКА БЕЗОПАСНОСТИ, КОНФИДЕНЦИАЛЬНОСТИ И ЧЕСТНОЙ ИГРЫ

1. ОФИЦИАЛЬНЫЙ ИЗДАТЕЛЬ И ЗАЩИТА ОТ ПОДДЕЛОК
Единственным официальным разработчиком и издателем лаунчера RBX Client является {PUBLISHER_NAME}.
В сети могут встречаться фейковые сборки, клоны и модифицированные архивы с вредоносным ПО или стилерами.
Перед запуском и обновлением всегда убеждайтесь, что издатель — {PUBLISHER_NAME}, а дистрибутив и обновления получены исключительно из официального репозитория:
https://github.com/{GITHUB_REPO}

2. КАКИЕ ЛОКАЛЬНЫЕ ДАННЫЕ ЧИТАЕТ ЛАУНЧЕР
RBX Client разработан с приоритетом локальной приватности:
• Лаунчер читает только локальные файлы конфигурации, логов Roblox и кэш (например, appStorage.json и журналы в %LOCALAPPDATA%\\Roblox), чтобы определить ваш открытый User ID и отобразить карточку профиля.
• Лаунчер НЕ запрашивает, НЕ считывает и НЕ передаёт пароли, токены авторизации, файлы cookie (.ROBLOSECURITY) или иные приватные учётные данные третьим лицам.
• Избранные игры, настройки интерфейса и параметры запуска сохраняются локально на вашем устройстве в папке assets/.

3. FASTFLAGS, ОПТИМИЗАЦИЯ И ОТВЕТСТВЕННОСТЬ ПОЛЬЗОВАТЕЛЯ
• Модуль настройки графики записывает параметры производительности и FastFlags в ClientAppSettings.json для улучшения стабильности кадров и отклика клиента.
• Пользователь несёт самостоятельную ответственность за соблюдение правил Roblox и условий конкретных плейсов/серверов.
• Разработчик ({PUBLISHER_NAME}) не несёт ответственности за действия сторонних модификаций, сетевые сбои на стороне Roblox или изменения, внесённые пользователем вручную вне штатных функций лаунчера.

4. БЕЗОПАСНОСТЬ СЕТИ, RBX SHIELD И САМОДИАГНОСТИКА
• Встроенный модуль LauncherSecurityGuard (RBX Shield) проверяет целостность критических ресурсов, hosts-файл и процессы в памяти, а SelfHealEngine восстанавливает повреждённые JSON и кэш.
• При обнаружении подозрительных файлов или несовпадении источника рекомендуем удалить стороннюю копию и скачать чистую сборку с официального GitHub.
• RBX Shield проверяет SHA-256 критических файлов, hosts на подмену доменов Roblox/GitHub, фильтрует слишком частые запросы (Anti-DDoS) и сканирует процессы на отладчики и инжекторы. Статус защиты виден в шапке окна и в Настройках.

5. ЗАЩИТА АККАУНТА
• Лаунчер никогда не просит пароль и не хранит его. Вход в аккаунт выполняет официальный клиент Roblox.
• Никому не передавайте файлы cookie и содержимое .ROBLOSECURITY. Администрация {PUBLISHER_NAME} и поддержка RBX Client не запрашивают эти данные.
• Включите двухэтапную проверку в настройках аккаунта Roblox и скачивайте лаунчер только с официального GitHub.

6. АНТИ-ЧИТ И ЧЕСТНАЯ ИГРА
• RBX Client не содержит читов, эксплойтов и инструментов обхода античита Roblox (Hyperion/Byfron) и не поддерживает их.
• FastFlags и FPS Unlocker применяются только из разрешённого набора параметров ClientAppSettings.json; значения вне списка не записываются.
• Пользовательские шейдеры и текстуры допускаются только как визуальные файлы. Исполняемые файлы (.exe, .bat, .dll, .ps1) при установке шейдеров блокируются.

7. ПРАВИЛА ИСПОЛЬЗОВАНИЯ RBX AI
• RBX AI — встроенный помощник на базе ChatGPT. Запрос отправляется на сторонний сервис, поэтому не вводите пароли, токены и личные данные.
• Вложенные скриншоты и лог-файлы отправляются только по вашему действию. Перед вложением проверьте, что в них нет приватной информации.
• Ответы ИИ носят справочный характер. Проверяйте советы по настройкам перед применением.

8. ХРАНЕНИЕ И УДАЛЕНИЕ ДАННЫХ
• Всё хранится локально: config, избранное, история недавних игр, трекер времени, журналы и резервные копии шейдеров лежат в папке assets/ рядом с лаунчером.
• Чтобы удалить данные, закройте лаунчер и удалите папку assets/ или воспользуйтесь кнопками очистки кэша и логов в Настройках.

9. ОБНОВЛЕНИЯ
• Лаунчер проверяет новые версии в репозиторий https://github.com/{GITHUB_REPO} и принимает только версии строго выше текущей ({CURRENT_VERSION}).

10. КОНТАКТЫ ИЗДАТЕЛЯ
• Издатель и автор: {PUBLISHER_NAME}. Telegram: https://t.me/RobloxLauncher. GitHub: https://github.com/{GITHUB_REPO}
• Нажимая «Принять и продолжить», вы подтверждаете, что ознакомились с политикой полностью.
"""


def get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def get_bundle_dir() -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return getattr(sys, "_MEIPASS")
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
BUNDLE_DIR = get_bundle_dir()
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CACHE_DIR = os.path.join(ASSETS_DIR, "cache")
LAUNCHER_LOGS_DIR = os.path.join(ASSETS_DIR, "logs")
PHOTO_GAMES_DIR = os.path.join(BASE_DIR, "PhotoGames")
PHOTO_RBX_DIR = os.path.join(BASE_DIR, "PhotoRBX")
CONFIG_PATH = os.path.join(ASSETS_DIR, "config.json")
FAVORITES_PATH = os.path.join(ASSETS_DIR, "favorites.json")
INSTALLED_FLAG_PATH = os.path.join(ASSETS_DIR, "installed.flag")
TERMS_FLAG_PATH = os.path.join(ASSETS_DIR, "terms_accepted.flag")
CLICK_SOUND_PATH = os.path.join(ASSETS_DIR, "click_tyk.wav")
STARTUP_SOUND_PATH = os.path.join(ASSETS_DIR, "vice_startup.wav")
ICON_PATH = os.path.join(BASE_DIR, "icon.ico")
EXPLICIT_SPLASH_PATH = r"D:\RobloxLauncher\PhotoRBX\photoloading.jpg"

HOTFIX_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/hotfix.json"
HOTFIX_STATE_PATH = os.path.join(ASSETS_DIR, "hotfix_applied.json")
CRASH_FIX_LOG_PATH = os.path.join(ASSETS_DIR, "crash_fix.log")
SECURITY_GUARD_LOG_PATH = os.path.join(ASSETS_DIR, "security_guard.log")


def ensure_directories() -> None:
    for folder in (ASSETS_DIR, CACHE_DIR, LAUNCHER_LOGS_DIR, PHOTO_GAMES_DIR, PHOTO_RBX_DIR):
        os.makedirs(folder, exist_ok=True)


def write_launcher_log(message: str) -> None:
    try:
        ensure_directories()
        log_file = os.path.join(LAUNCHER_LOGS_DIR, f"rbxclient_{datetime.now().strftime('%Y-%m-%d')}.log")
        ts = datetime.now().strftime("%H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {message}\n")
    except Exception:
        pass


def write_crash_fix_log(context: str, exc: BaseException | str) -> None:
    try:
        os.makedirs(ASSETS_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CRASH_FIX_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] [{context}] {exc}\n")
    except Exception:
        pass


def write_security_incident_log(level: str, detail: str) -> None:
    try:
        os.makedirs(ASSETS_DIR, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(SECURITY_GUARD_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] [{level}] {detail}\n")
    except Exception:
        pass


def load_json_safe(path: str, fallback):
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(fallback, dict) and isinstance(data, dict):
                merged = dict(fallback)
                merged.update(data)
                return merged
            if isinstance(fallback, list) and isinstance(data, list):
                return data
            return fallback
    except Exception as exc:
        write_crash_fix_log(f"load_json_safe:{os.path.basename(path)}", exc)
        return fallback


def save_json_safe(path: str, data) -> None:
    ensure_directories()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        write_crash_fix_log(f"save_json_safe:{os.path.basename(path)}", exc)


def resolve_splash_image_path() -> str | None:
    candidates = [
        os.path.join(BASE_DIR, "PhotoRBX", "photoloading.jpg"),
        os.path.join(BUNDLE_DIR, "PhotoRBX", "photoloading.jpg"),
        EXPLICIT_SPLASH_PATH,
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def parse_roblox_game_input(raw_text: str, default_place_id: int = 2753915549) -> dict:
    """Extract placeId and privateServerLinkCode (or gameInstanceId) from digits or full Roblox URL."""
    text = (raw_text or "").strip()
    place_id: int | None = None
    link_code: str = ""
    job_id: str = ""

    if text:
        m_url = re.search(r"roblox\.com/games/(\d+)", text, flags=re.IGNORECASE)
        if m_url:
            place_id = int(m_url.group(1))
            try:
                parsed = urllib.parse.urlparse(text if "://" in text else f"https://{text}")
                qs = urllib.parse.parse_qs(parsed.query)
                if "privateServerLinkCode" in qs and qs["privateServerLinkCode"]:
                    link_code = str(qs["privateServerLinkCode"][0]).strip()
                elif "linkCode" in qs and qs["linkCode"]:
                    link_code = str(qs["linkCode"][0]).strip()
                if "gameInstanceId" in qs and qs["gameInstanceId"]:
                    job_id = str(qs["gameInstanceId"][0]).strip()
            except Exception:
                pass
        else:
            digits = "".join(ch for ch in text if ch.isdigit())
            if digits:
                place_id = int(digits)

    if not place_id or place_id <= 0:
        place_id = int(default_place_id)

    canonical_url = f"https://www.roblox.com/games/{place_id}"
    if link_code:
        canonical_url = f"{canonical_url}?privateServerLinkCode={urllib.parse.quote(link_code)}"

    return {
        "place_id": int(place_id),
        "link_code": link_code,
        "job_id": job_id,
        "canonical_url": canonical_url,
    }


def is_roblox_player_beta_running_windows() -> bool:
    """Return True strictly if RobloxPlayerBeta.exe is present in Windows tasklist."""
    if platform.system().lower() != "windows":
        return False
    try:
        proc = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            timeout=3,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        for line in (proc.stdout or "").splitlines():
            cols = [c.strip('"').strip().lower() for c in line.split('","')]
            if cols and cols[0] == "robloxplayerbeta.exe":
                return True
    except Exception:
        pass
    return False


class RobloxProcessWatcher:
    """Опрашивает tasklist строго в фоновом потоке (раз в 15 секунд), UI читает только готовый флаг."""

    def __init__(self, interval_sec: float = 15.0) -> None:
        self.running = False
        self._interval = float(interval_sec)
        self._kick = threading.Event()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()

        def _loop():
            while not self._stop.is_set():
                try:
                    self.running = is_roblox_player_beta_running_windows()
                except Exception:
                    self.running = False
                self._kick.wait(self._interval)
                self._kick.clear()

        self._thread = threading.Thread(target=_loop, daemon=True)
        self._thread.start()

    def kick(self) -> None:
        self._kick.set()

    def stop(self) -> None:
        self._stop.set()
        self._kick.set()


ROBLOX_WATCHER = RobloxProcessWatcher()


class LauncherSecurityGuard:
    """
    RBX Shield: 4-tier security guard running in background:
      1) File Integrity & SHA-256 Guard (icon.ico, PhotoRBX\\photoloading.jpg, external exe/bat block, release SHA-256 check)
      2) Anti-Phishing & DNS Hosts Guard (hosts check for roblox.com / github.com, official domain allowlist)
      3) Process & Memory Shield (tasklist debugger/sniffer/injector detection + security_guard.log)
      4) Settings UI state & status reporting
    """

    THREAT_PROCESS_KEYWORDS = (
        "cheatengine",
        "x64dbg",
        "x32dbg",
        "ollydbg",
        "ida64",
        "processhacker",
        "fiddler",
        "wireshark",
        "httpdebugger",
        "dnspy",
    )

    ALLOWED_EXTERNAL_HOSTS = (
        "roblox.com",
        "www.roblox.com",
        "github.com",
        "api.github.com",
        "raw.githubusercontent.com",
        "t.me",
    )

    def __init__(self, config_getter) -> None:
        self._get_config = config_getter
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self.threat_detected: bool = False
        self.last_threat_reason: str = ""
        self.last_scan_summary: str = "Protected • No threats detected"
        self.file_hashes: dict[str, str] = {}
        self._capture_baseline_hashes()

    def _compute_sha256(self, file_path: str) -> str:
        h = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return ""

    def _capture_baseline_hashes(self) -> None:
        for fp in (ICON_PATH, resolve_splash_image_path() or ""):
            if fp and os.path.isfile(fp):
                digest = self._compute_sha256(fp)
                if digest:
                    self.file_hashes[os.path.abspath(fp)] = digest

    def verify_expected_sha256(self, file_path: str, expected_sha256: str | None) -> bool:
        if not expected_sha256:
            return True
        clean_exp = expected_sha256.strip().lower()
        if not clean_exp:
            return True
        actual = self._compute_sha256(file_path).lower()
        ok = bool(actual) and actual == clean_exp
        if not ok:
            self._flag_threat("File Integrity", f"SHA-256 mismatch for {file_path}")
        return ok

    def is_external_url_allowed(self, url: str) -> bool:
        try:
            parsed = urllib.parse.urlparse((url or "").strip())
            host = (parsed.hostname or "").lower()
            if not host:
                return False
            if host == "t.me":
                path_low = (parsed.path or "").lower()
                allowed = path_low.startswith("/robloxlauncher")
                if not allowed:
                    self._flag_threat("Anti-Phishing", f"Blocked non-official Telegram link: {url}")
                return allowed
            for allowed_h in self.ALLOWED_EXTERNAL_HOSTS:
                if allowed_h == "t.me":
                    continue
                if host == allowed_h or host.endswith("." + allowed_h):
                    return True
            self._flag_threat("Anti-Phishing", f"Blocked untrusted external URL: {url}")
            return False
        except Exception:
            return False

    def is_external_executable_allowed(self, target_path: str) -> bool:
        if not target_path:
            return False
        ext = os.path.splitext(target_path)[1].lower()
        if ext in (".exe", ".bat", ".cmd", ".ps1", ".vbs", ".msi"):
            abs_target = os.path.abspath(target_path)
            abs_base = os.path.abspath(BASE_DIR)
            try:
                in_base = os.path.commonpath([abs_target, abs_base]) == abs_base
            except Exception:
                in_base = abs_target.startswith(abs_base + os.sep)
            if not in_base:
                self._flag_threat("File Integrity", f"Blocked external binary/script outside launcher dir: {abs_target}")
                return False
        return True

    def check_critical_resources(self) -> tuple[bool, str]:
        splash_fp = resolve_splash_image_path()
        missing = []
        if not os.path.isfile(ICON_PATH):
            missing.append("icon.ico")
        if not splash_fp or not os.path.isfile(splash_fp):
            missing.append(r"PhotoRBX\photoloading.jpg")
        if missing:
            return False, f"Missing critical resource(s): {', '.join(missing)}"

        for fp, old_hash in list(self.file_hashes.items()):
            if os.path.isfile(fp):
                cur_hash = self._compute_sha256(fp)
                if cur_hash and old_hash and cur_hash != old_hash:
                    self.file_hashes[fp] = cur_hash
        return True, "Critical resources intact"

    def check_hosts_file(self) -> tuple[bool, str]:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        if not os.path.isfile(hosts_path):
            return True, "hosts file not present"
        try:
            with open(hosts_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    low = s.lower()
                    if ("roblox.com" in low or "github.com" in low) and (
                        "127.0.0.1" in low or "0.0.0.0" in low
                    ):
                        return False, f"Suspicious hosts redirection detected: {s[:80]}"
            return True, "hosts file clean"
        except Exception as exc:
            return True, f"hosts check skipped ({exc})"

    def check_running_threats(self) -> tuple[bool, str]:
        if platform.system().lower() != "windows":
            return True, "Process check OK"
        try:
            proc = subprocess.run(
                ["tasklist", "/FO", "CSV", "/NH"],
                capture_output=True,
                text=True,
                timeout=3,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            detected: list[str] = []
            for line in (proc.stdout or "").splitlines():
                cols = [c.strip('"').strip().lower() for c in line.split('","')]
                if not cols or not cols[0]:
                    continue
                proc_name = cols[0]
                for kw in self.THREAT_PROCESS_KEYWORDS:
                    if kw in proc_name:
                        detected.append(proc_name)
                        break
            if detected:
                uniq = ", ".join(sorted(set(detected)))
                return False, f"Detected debugger/sniffer/injector process: {uniq}"
            return True, "No debugger/injector processes detected"
        except Exception as exc:
            return True, f"Process check warning ({exc})"

    def _flag_threat(self, category: str, reason: str) -> None:
        with self._lock:
            self.threat_detected = True
            self.last_threat_reason = reason
            self.last_scan_summary = f"Warning • {reason}"
        write_security_incident_log(category, reason)
        write_launcher_log(f"[RBX Shield ALERT][{category}] {reason}")

    def run_scan_once(self) -> tuple[bool, str]:
        cfg = self._get_config() if callable(self._get_config) else {}
        enabled = bool(cfg.get("security_guard_enabled", True))
        if not enabled:
            with self._lock:
                self.threat_detected = False
                self.last_threat_reason = ""
                self.last_scan_summary = "RBX Shield disabled"
            return True, "RBX Shield disabled"

        res_ok, res_msg = self.check_critical_resources()
        if not res_ok:
            self._flag_threat("File Integrity", res_msg)
            return False, res_msg

        hosts_ok, hosts_msg = self.check_hosts_file()
        if not hosts_ok:
            self._flag_threat("DNS Hosts Guard", hosts_msg)
            return False, hosts_msg

        proc_ok, proc_msg = self.check_running_threats()
        if not proc_ok:
            self._flag_threat("Process & Memory Shield", proc_msg)
            return False, proc_msg

        with self._lock:
            self.threat_detected = False
            self.last_threat_reason = ""
            self.last_scan_summary = "Protected • No threats detected"
        return True, "Protected • No threats detected"

    def start_background_loop(self, interval_sec: float = 5.0, on_update=None) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()

        def _worker():
            while not self._stop_event.is_set():
                ok, summary = self.run_scan_once()
                if callable(on_update):
                    try:
                        on_update(ok, summary)
                    except Exception:
                        pass
                self._stop_event.wait(interval_sec)

        self._thread = threading.Thread(target=_worker, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()


class SelfHealEngine:
    """Автоматическая самодиагностика, автолечение файлов и тихие хотфиксы с GitHub."""

    def __init__(self, client_settings_path_getter, config_getter, config_setter, security_guard=None) -> None:
        self._get_client_settings_path = client_settings_path_getter
        self._get_config = config_getter
        self._set_config = config_setter
        self._security_guard = security_guard
        self._lock = threading.Lock()
        self.fixes_applied_count: int = 0
        self.last_report: list[str] = []

    def _record_fix(self, reason: str) -> None:
        with self._lock:
            self.fixes_applied_count += 1
            self.last_report.append(reason)
        write_launcher_log(f"[SelfHeal] {reason}")
        write_crash_fix_log("AUTO-FIX", reason)

    def ensure_folders(self) -> None:
        for folder in (ASSETS_DIR, CACHE_DIR, LAUNCHER_LOGS_DIR, PHOTO_GAMES_DIR, PHOTO_RBX_DIR):
            if not os.path.isdir(folder):
                try:
                    os.makedirs(folder, exist_ok=True)
                    self._record_fix(f"Создана отсутствующая папка: {folder}")
                except Exception as exc:
                    write_crash_fix_log("ensure_folders", exc)

    def _backup_corrupted_file(self, file_path: str) -> None:
        if not os.path.isfile(file_path):
            return
        try:
            bak_path = f"{file_path}.{int(time.time())}.bak"
            shutil.copy2(file_path, bak_path)
        except Exception as exc:
            write_crash_fix_log("backup_corrupted_file", exc)

    def validate_and_heal_json_files(self) -> None:
        self._heal_single_json(
            path=CONFIG_PATH,
            fallback=dict(DEFAULT_CONFIG),
            expected_type=dict,
            on_healed=lambda healed: self._set_config(healed),
        )
        self._heal_single_json(
            path=FAVORITES_PATH,
            fallback=[],
            expected_type=list,
            on_healed=None,
        )
        client_json = self._get_client_settings_path()
        if client_json and os.path.exists(client_json):
            self._heal_single_json(
                path=client_json,
                fallback={},
                expected_type=dict,
                on_healed=None,
            )

    def _heal_single_json(self, path: str, fallback, expected_type, on_healed=None) -> None:
        if not os.path.exists(path):
            save_json_safe(path, fallback)
            if callable(on_healed):
                on_healed(fallback)
            return

        need_repair = False
        repaired_data = fallback

        try:
            if os.path.getsize(path) == 0:
                need_repair = True
            else:
                with open(path, "r", encoding="utf-8") as f:
                    parsed = json.load(f)
                if not isinstance(parsed, expected_type):
                    need_repair = True
                elif expected_type is dict:
                    merged = dict(fallback)
                    merged.update(parsed)
                    repaired_data = merged
                else:
                    repaired_data = parsed
        except Exception as exc:
            write_crash_fix_log(f"JSON:{os.path.basename(path)}", exc)
            need_repair = True

        if need_repair:
            self._backup_corrupted_file(path)
            save_json_safe(path, repaired_data)
            if callable(on_healed):
                on_healed(repaired_data)
            self._record_fix(f"Восстановлен повреждённый JSON: {os.path.basename(path)}")

    def clean_corrupted_image_cache(self) -> int:
        if not os.path.isdir(CACHE_DIR):
            return 0
        removed = 0
        for fname in os.listdir(CACHE_DIR):
            fp = os.path.join(CACHE_DIR, fname)
            if not os.path.isfile(fp):
                continue
            try:
                if os.path.getsize(fp) == 0:
                    os.remove(fp)
                    removed += 1
                    self._record_fix(f"Удалён пустой файл кэша (0 байт): {fname}")
                    continue
                if fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    with Image.open(fp) as im:
                        im.verify()
            except Exception:
                try:
                    os.remove(fp)
                    removed += 1
                    self._record_fix(f"Удалён битый файл кэша изображений: {fname}")
                except Exception as del_exc:
                    write_crash_fix_log("clean_cache", del_exc)
        return removed

    def fetch_and_apply_github_hotfix(self, timeout_sec: float = 3.0) -> bool:
        applied_any = False
        hotfix_payload: dict | None = None

        try:
            resp = requests.get(
                HOTFIX_URL,
                timeout=timeout_sec,
                headers={"User-Agent": f"RBXClient/{CURRENT_VERSION}"},
            )
            if resp.status_code == 200 and resp.text.strip():
                data = resp.json()
                if isinstance(data, dict):
                    hotfix_payload = data
        except Exception as exc:
            write_crash_fix_log("hotfix_raw_fetch", exc)

        if hotfix_payload is None:
            try:
                rel_resp = requests.get(
                    GITHUB_API_LATEST,
                    timeout=timeout_sec,
                    headers={"User-Agent": f"RBXClient/{CURRENT_VERSION}"},
                )
                if rel_resp.status_code == 200:
                    rel_json = rel_resp.json()
                    if isinstance(rel_json, dict):
                        for asset in rel_json.get("assets") or []:
                            if str(asset.get("name") or "").lower() == "hotfix.json":
                                dl_url = asset.get("browser_download_url")
                                if dl_url:
                                    hf_r = requests.get(dl_url, timeout=timeout_sec)
                                    if hf_r.status_code == 200:
                                        parsed = hf_r.json()
                                        if isinstance(parsed, dict):
                                            hotfix_payload = parsed
                                break
            except Exception as exc:
                write_crash_fix_log("hotfix_release_fetch", exc)

        if not isinstance(hotfix_payload, dict):
            return False

        patch_id = str(hotfix_payload.get("patch_id") or hotfix_payload.get("version") or "").strip()
        if not patch_id:
            return False

        state_data = load_json_safe(HOTFIX_STATE_PATH, {"applied_patches": []})
        applied_list = state_data.get("applied_patches") if isinstance(state_data, dict) else []
        if not isinstance(applied_list, list):
            applied_list = []

        if patch_id in applied_list:
            return False

        cfg_patch = hotfix_payload.get("config_patch")
        if isinstance(cfg_patch, dict) and cfg_patch:
            cur_cfg = dict(self._get_config())
            cur_cfg.update(cfg_patch)
            self._set_config(cur_cfg)
            save_json_safe(CONFIG_PATH, cur_cfg)
            applied_any = True

        fflags_patch = hotfix_payload.get("client_app_settings_patch")
        client_settings_path = self._get_client_settings_path()
        if isinstance(fflags_patch, dict) and fflags_patch and client_settings_path:
            try:
                os.makedirs(os.path.dirname(client_settings_path), exist_ok=True)
                existing_flags: dict = {}
                if os.path.isfile(client_settings_path):
                    try:
                        with open(client_settings_path, "r", encoding="utf-8") as f:
                            loaded = json.load(f)
                            if isinstance(loaded, dict):
                                existing_flags = loaded
                    except Exception:
                        existing_flags = {}
                existing_flags.update(fflags_patch)
                with open(client_settings_path, "w", encoding="utf-8") as f:
                    json.dump(existing_flags, f, ensure_ascii=False, indent=2)
                applied_any = True
            except Exception as exc:
                write_crash_fix_log("hotfix_client_settings", exc)

        files_list = hotfix_payload.get("files")
        if isinstance(files_list, list):
            for item in files_list:
                if not isinstance(item, dict):
                    continue
                rel_target = str(item.get("target") or "").strip().lstrip("/\\")
                file_url = str(item.get("url") or "").strip()
                expected_sha = str(item.get("sha256") or "").strip()
                if not rel_target or not file_url:
                    continue
                dest_abs = os.path.abspath(os.path.join(BASE_DIR, rel_target))
                if not dest_abs.startswith(os.path.abspath(BASE_DIR)):
                    continue
                try:
                    f_resp = requests.get(file_url, timeout=timeout_sec)
                    if f_resp.status_code == 200 and f_resp.content:
                        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
                        tmp_path = dest_abs + ".tmp_hf"
                        with open(tmp_path, "wb") as out_f:
                            out_f.write(f_resp.content)
                        if self._security_guard and expected_sha:
                            if not self._security_guard.verify_expected_sha256(tmp_path, expected_sha):
                                try:
                                    os.remove(tmp_path)
                                except Exception:
                                    pass
                                continue
                        shutil.move(tmp_path, dest_abs)
                        applied_any = True
                except Exception as exc:
                    write_crash_fix_log(f"hotfix_file:{rel_target}", exc)

        applied_list.append(patch_id)
        save_json_safe(HOTFIX_STATE_PATH, {"applied_patches": applied_list, "last_patch": patch_id})
        if applied_any:
            self._record_fix(f"Применён тихий хотфикс с GitHub: {patch_id}")
        return applied_any

    def run_startup_diagnostics(self, status_callback=None) -> None:
        def _set_status(text: str) -> None:
            if callable(status_callback):
                status_callback(text)

        try:
            _set_status("Проверка папок и структуры файлов...")
            self.ensure_folders()

            _set_status("Валидация JSON и восстановление конфигов...")
            self.validate_and_heal_json_files()

            _set_status("Очистка битого кэша изображений...")
            self.clean_corrupted_image_cache()

            _set_status("Проверка исправлений (Hotfix) на GitHub...")
            did_hotfix = self.fetch_and_apply_github_hotfix(timeout_sec=3.0)
            if did_hotfix:
                _set_status("Применение исправлений (Hotfix)...")
                time.sleep(0.35)
        except Exception as exc:
            write_crash_fix_log("run_startup_diagnostics", exc)


def get_primary_screen_size(fallback_widget=None) -> tuple[int, int]:
    """Реальный размер основного монитора Windows (GetSystemMetrics 0/1) с запасным вариантом через Tk."""
    try:
        if platform.system().lower() == "windows":
            w = int(ctypes.windll.user32.GetSystemMetrics(0))
            h = int(ctypes.windll.user32.GetSystemMetrics(1))
            if w > 0 and h > 0:
                return w, h
    except Exception:
        pass
    try:
        if fallback_widget is not None:
            return int(fallback_widget.winfo_screenwidth()), int(fallback_widget.winfo_screenheight())
    except Exception:
        pass
    return 1920, 1080


def parse_version_tuple(version_str: str) -> tuple[int, ...]:
    clean = re.sub(r"^[vV]\s*", "", (version_str or "").strip())
    parts = re.findall(r"\d+", clean)
    if not parts:
        return (0,)
    return tuple(int(p) for p in parts)


def is_strictly_newer_version(candidate: str, current: str = CURRENT_VERSION) -> bool:
    cand_t = parse_version_tuple(candidate)
    curr_t = parse_version_tuple(current)
    max_len = max(len(cand_t), len(curr_t))
    cand_padded = cand_t + (0,) * (max_len - len(cand_t))
    curr_padded = curr_t + (0,) * (max_len - len(curr_t))
    return cand_padded > curr_padded


def format_number(num: int | float | None) -> str:
    if num is None:
        return "0"
    try:
        return f"{int(num):,}".replace(",", " ")
    except (ValueError, TypeError):
        return str(num)


def format_account_age(created_iso: str | None) -> tuple[str, str]:
    if not created_iso:
        return "Неизвестно", "Возраст аккаунта не определен"
    try:
        normalized = created_iso.replace("Z", "+00:00")
        created_dt = datetime.fromisoformat(normalized)
        if created_dt.tzinfo is None:
            created_dt = created_dt.replace(tzinfo=timezone.utc)
        now_dt = datetime.now(timezone.utc)
        if created_dt > now_dt:
            created_dt = now_dt
        delta_days = max(0, (now_dt - created_dt).days)
        years = delta_days // 365
        rem_days = delta_days % 365
        months = rem_days // 30
        date_str = created_dt.strftime("%d.%m.%Y")
        if years > 0:
            age_str = f"{years} г. {months} мес. ({delta_days} дн.)"
        elif months > 0:
            age_str = f"{months} мес. ({delta_days} дн.)"
        else:
            age_str = f"{delta_days} дн."
        return date_str, age_str
    except Exception:
        return str(created_iso)[:10], "Возраст уточняется"


class WindowsTaskbarHelper:
    def __init__(self) -> None:
        self._is_win = platform.system().lower() == "windows"
        self._user32 = None
        if self._is_win:
            try:
                self._user32 = ctypes.windll.user32
            except Exception:
                self._user32 = None

    def apply_taskbar_style(self, tk_window: ctk.CTk) -> None:
        if not self._is_win or not self._user32:
            return
        try:
            tk_window.update_idletasks()
            hwnd = self._user32.GetParent(tk_window.winfo_id())
            if not hwnd:
                hwnd = tk_window.winfo_id()
            ex_style = self._user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            new_style = (ex_style | WS_EX_APPWINDOW) & ~WS_EX_TOOLWINDOW
            self._user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
            self._user32.SetWindowPos(
                hwnd,
                0,
                0,
                0,
                0,
                0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
            )
        except Exception:
            pass

    def minimize_window(self, tk_window: ctk.CTk) -> None:
        if not self._is_win or not self._user32:
            tk_window.iconify()
            return
        try:
            hwnd = self._user32.GetParent(tk_window.winfo_id())
            if not hwnd:
                hwnd = tk_window.winfo_id()
            self.apply_taskbar_style(tk_window)
            self._user32.ShowWindow(hwnd, SW_MINIMIZE)
        except Exception:
            tk_window.iconify()

    def restore_window(self, tk_window: ctk.CTk) -> None:
        if not self._is_win or not self._user32:
            tk_window.deiconify()
            return
        try:
            hwnd = self._user32.GetParent(tk_window.winfo_id())
            if not hwnd:
                hwnd = tk_window.winfo_id()
            self.apply_taskbar_style(tk_window)
            self._user32.ShowWindow(hwnd, SW_RESTORE)
            tk_window.deiconify()
            tk_window.lift()
            tk_window.focus_force()
        except Exception:
            tk_window.deiconify()


class SoundEngine:
    def __init__(self, config_getter) -> None:
        self._get_config = config_getter
        self._is_win = platform.system().lower() == "windows"
        self._lock = threading.Lock()
        self.generate_assets()

    def generate_assets(self) -> None:
        ensure_directories()
        if not os.path.exists(CLICK_SOUND_PATH):
            self._write_click_tyk(CLICK_SOUND_PATH)
        if not os.path.exists(STARTUP_SOUND_PATH):
            self._write_vice_startup(STARTUP_SOUND_PATH)

    def _write_pcm_wav(self, path: str, samples: list[float], sample_rate: int = 44100) -> None:
        with self._lock:
            with wave.open(path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                frames = bytearray()
                for s in samples:
                    clamped = max(-1.0, min(1.0, s))
                    val = int(clamped * 32767.0)
                    frames.extend(struct.pack("<h", val))
                wf.writeframes(bytes(frames))

    def _write_click_tyk(self, path: str) -> None:
        sample_rate = 44100
        duration = 0.020
        total_samples = int(sample_rate * duration)
        samples: list[float] = []
        for i in range(total_samples):
            t = i / sample_rate
            norm = i / max(1, total_samples - 1)
            envelope = math.sin(math.pi * norm) ** 2.4
            freq = 420.0 * math.exp(-t * 95.0) + 135.0
            wave_val = 0.72 * math.sin(2.0 * math.pi * freq * t) + 0.28 * math.sin(2.0 * math.pi * (freq * 2.15) * t)
            samples.append(wave_val * envelope * 0.22)
        self._write_pcm_wav(path, samples, sample_rate)

    def _write_vice_startup(self, path: str) -> None:
        sample_rate = 44100
        duration = 6.8
        total_samples = int(sample_rate * duration)
        chord_freqs = [130.81, 164.81, 196.00, 246.94, 293.66]
        samples: list[float] = []

        for i in range(total_samples):
            t = i / sample_rate
            if t < 0.9:
                env = (t / 0.9) ** 1.4
            elif t > duration - 1.4:
                env = max(0.0, (duration - t) / 1.4) ** 1.6
            else:
                env = 1.0

            warmth = 0.86 + 0.14 * math.sin(2.0 * math.pi * 0.55 * t)
            pad_sum = 0.0
            for idx, base_f in enumerate(chord_freqs):
                detune_lfo = 1.0 + 0.0022 * math.sin(2.0 * math.pi * (0.28 + idx * 0.07) * t + idx)
                f1 = base_f * detune_lfo
                f2 = base_f * (1.0035 - idx * 0.0007)
                saw1 = 2.0 * ((t * f1) % 1.0) - 1.0
                saw2 = 2.0 * ((t * f2) % 1.0) - 1.0
                sub = math.sin(2.0 * math.pi * (base_f * 0.5) * t)
                tone = 0.42 * saw1 + 0.36 * saw2 + 0.22 * sub
                pad_sum += tone / len(chord_freqs)

            shimmer = 0.04 * math.sin(2.0 * math.pi * 523.25 * t) * (0.5 + 0.5 * math.sin(2.0 * math.pi * 0.4 * t))
            samples.append((pad_sum + shimmer) * env * warmth * 0.26)

        self._write_pcm_wav(path, samples, sample_rate)

    def play_click(self) -> None:
        cfg = self._get_config()
        if not cfg.get("sound_click", True):
            return
        if not self._is_win or not os.path.exists(CLICK_SOUND_PATH):
            return
        try:
            winsound.PlaySound(
                CLICK_SOUND_PATH,
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NOSTOP,
            )
        except Exception:
            pass

    def play_startup_loop(self) -> None:
        cfg = self._get_config()
        if not cfg.get("sound_startup", True):
            return
        if not self._is_win or not os.path.exists(STARTUP_SOUND_PATH):
            return
        try:
            winsound.PlaySound(
                STARTUP_SOUND_PATH,
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
            )
        except Exception:
            pass

    def stop_sound(self) -> None:
        if not self._is_win:
            return
        try:
            winsound.PlaySound(None, 0)
        except Exception:
            pass


def _load_pil_font(px: int, bold: bool = False):
    font_files = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
    ]
    fonts_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    for fname in font_files:
        fp = os.path.join(fonts_dir, fname)
        if os.path.isfile(fp):
            try:
                return ImageFont.truetype(fp, px)
            except Exception:
                pass
    return ImageFont.load_default()


def apply_bottom_gradient_and_text(
    pil_img: Image.Image,
    size: tuple[int, int] = (660, 371),
    title: str = "",
    creator: str = "",
    place_id: int = 0,
    playing: int = 0,
) -> ctk.CTkImage:
    w, h = size
    fitted = ImageOps.fit(pil_img.convert("RGBA"), (w, h), Image.Resampling.LANCZOS)

    grad_h = max(116, int(h * 0.45))
    grad_layer = Image.new("RGBA", (w, grad_h), (0, 0, 0, 0))
    draw_grad = ImageDraw.Draw(grad_layer)
    for y in range(grad_h):
        t = y / max(1, grad_h - 1)
        alpha = int(230 * (t ** 1.65))
        draw_grad.line([(0, y), (w, y)], fill=(9, 12, 16, alpha))

    fitted.paste(grad_layer, (0, h - grad_h), grad_layer)

    draw = ImageDraw.Draw(fitted)
    f_title = _load_pil_font(23, bold=True)
    f_creator = _load_pil_font(13, bold=False)
    f_meta = _load_pil_font(11, bold=False)

    pad_x = 20
    meta_line = f"Place ID: {place_id}   •   Playing: {format_number(playing)}"
    creator_line = f"Создатель: {creator or 'Roblox'}"

    y_meta = h - 22
    y_creator = y_meta - 19
    y_title = y_creator - 30

    draw.text((pad_x + 1, y_title + 1), title, font=f_title, fill=(0, 0, 0, 190))
    draw.text((pad_x, y_title), title, font=f_title, fill=(243, 246, 250, 255))

    draw.text((pad_x + 1, y_creator + 1), creator_line, font=f_creator, fill=(0, 0, 0, 190))
    draw.text((pad_x, y_creator), creator_line, font=f_creator, fill=(214, 222, 233, 245))

    draw.text((pad_x + 1, y_meta + 1), meta_line, font=f_meta, fill=(0, 0, 0, 190))
    draw.text((pad_x, y_meta), meta_line, font=f_meta, fill=(148, 163, 184, 235))

    return ctk.CTkImage(light_image=fitted, dark_image=fitted, size=(w, h))


def build_welcome_banner_image(size: tuple[int, int] = (660, 371)) -> ctk.CTkImage:
    w, h = size
    base_pil: Image.Image | None = None
    candidates = [
        os.path.join(BASE_DIR, "PhotoRBX", "welcome.jpg"),
        os.path.join(BASE_DIR, "PhotoRBX", "welcome.png"),
        os.path.join(BUNDLE_DIR, "PhotoRBX", "welcome.jpg"),
        os.path.join(BUNDLE_DIR, "PhotoRBX", "welcome.png"),
        resolve_splash_image_path() or "",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            try:
                base_pil = ImageOps.fit(Image.open(path).convert("RGBA"), (w, h), Image.Resampling.LANCZOS)
                break
            except Exception:
                base_pil = None

    if base_pil is None:
        base_pil = Image.new("RGBA", (w, h), (14, 19, 26, 255))
        draw_bg = ImageDraw.Draw(base_pil)
        for y in range(h):
            t = y / max(1, h - 1)
            r = int(14 + 18 * t)
            g = int(20 + 34 * t)
            b = int(32 + 56 * t)
            draw_bg.line([(0, y), (w, y)], fill=(r, g, b, 255))

    overlay = Image.new("RGBA", (w, h), (9, 12, 16, 155))
    composed = Image.alpha_composite(base_pil, overlay)

    grad_h = int(h * 0.52)
    grad = Image.new("RGBA", (w, grad_h), (0, 0, 0, 0))
    d_grad = ImageDraw.Draw(grad)
    for y in range(grad_h):
        t = y / max(1, grad_h - 1)
        d_grad.line([(0, y), (w, y)], fill=(9, 12, 16, int(235 * (t ** 1.4))))
    composed.paste(grad, (0, h - grad_h), grad)

    draw = ImageDraw.Draw(composed)
    f_badge = _load_pil_font(12, bold=True)
    f_title = _load_pil_font(26, bold=True)
    f_sub = _load_pil_font(14, bold=False)
    f_hint = _load_pil_font(12, bold=False)

    draw.rounded_rectangle((22, 22, 245, 50), radius=8, fill=(59, 130, 246, 220))
    draw.text((34, 28), f"ОБЪЯВЛЕНИЕ • ОБНОВЛЕНИЕ {CURRENT_VERSION}", font=f_badge, fill=(255, 255, 255, 255))

    draw.text((22, h - 118), f"RBX Client {CURRENT_VERSION} by {PUBLISHER_NAME}", font=f_title, fill=(243, 246, 250, 255))
    draw.text(
        (22, h - 82),
        "Серверы и API Roblox: готовы  •  RBX Shield и самодиагностика активны",
        font=f_sub,
        fill=(148, 210, 172, 255),
    )
    draw.text(
        (22, h - 46),
        "Выберите игру из списка справа или введите Place ID / ссылку для запуска.",
        font=f_hint,
        fill=(186, 198, 214, 245),
    )

    return ctk.CTkImage(light_image=composed, dark_image=composed, size=(w, h))


class SplashOverlay(ctk.CTkCanvas):
    """Full-bleed splash screen rendering PhotoRBX\\photoloading.jpg at 100% with zero margins/bars."""

    def __init__(
        self,
        parent,
        width: int,
        height: int,
        is_first_run: bool,
        on_complete,
        show_status_text: bool = True,
    ) -> None:
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=COLOR_BG,
            highlightthickness=0,
            bd=0,
        )
        self._width = max(1, int(width))
        self._height = max(1, int(height))
        self._on_complete = on_complete
        self._show_status_text = bool(show_status_text)
        self._duration = SPLASH_FIRST_RUN_SEC if is_first_run else SPLASH_NORMAL_SEC
        self._start_time = time.perf_counter()
        self._anim_job = None
        self._bg_source_pil: Image.Image | None = None
        self._bg_photo: ImageTk.PhotoImage | None = None
        self._rendered_size: tuple[int, int] = (0, 0)
        self._override_status: str | None = None
        self._finished = False
        self._screen_w, self._screen_h = get_primary_screen_size(self)
        try:
            top = self.winfo_toplevel()
            center_fn = getattr(top, "_center_on_screen", None)
            if callable(center_fn):
                center_fn()
        except Exception:
            pass

        self._stages = [
            (0.00, f"Инициализация RBX Client v{CURRENT_VERSION} by {PUBLISHER_NAME}..."),
            (0.20, "Проверка RBX Shield..."),
            (0.45, "Загрузка профиля..."),
            (0.70, "Синхронизация каталога игр..."),
            (0.92, "Готово"),
        ]

        img_path = resolve_splash_image_path()
        if img_path:
            try:
                self._bg_source_pil = Image.open(img_path).convert("RGB")
            except Exception as exc:
                write_crash_fix_log("SplashOverlay.load_image", exc)
                self._bg_source_pil = None

        self.bind("<Configure>", self._on_canvas_resize)
        self._render_background()
        self._animate_frame()

    def set_status_message(self, text: str) -> None:
        self._override_status = str(text) if text else None

    def _on_canvas_resize(self, event) -> None:
        nw = max(1, int(getattr(event, "width", 0) or self.winfo_width() or self._width))
        nh = max(1, int(getattr(event, "height", 0) or self.winfo_height() or self._height))
        if (nw, nh) != (self._width, self._height):
            self._width = nw
            self._height = nh
            self._render_background()

    def _render_background(self) -> None:
        w = max(1, int(self.winfo_width() or self._width))
        h = max(1, int(self.winfo_height() or self._height))
        self._width = w
        self._height = h

        if self._bg_source_pil is not None:
            try:
                if self._rendered_size != (w, h) or self._bg_photo is None:
                    stretched = self._bg_source_pil.resize((w, h), Image.Resampling.LANCZOS)
                    self._bg_photo = ImageTk.PhotoImage(stretched)
                    self._rendered_size = (w, h)

                self.delete("bg")
                self.create_image(0, 0, anchor="nw", image=self._bg_photo, tags="bg")
                self.tag_lower("bg")
                return
            except Exception as exc:
                write_crash_fix_log("SplashOverlay._render_background", exc)

        self.delete("bg")
        self.create_rectangle(0, 0, w, h, fill=COLOR_BG, outline="", tags="bg")
        self.tag_lower("bg")

    def _current_status_text(self, progress: float) -> str:
        if self._override_status:
            return self._override_status
        chosen = self._stages[0][1]
        for threshold, text in self._stages:
            if progress >= threshold:
                chosen = text
        return chosen

    def _animate_frame(self) -> None:
        if self._finished:
            return

        cur_w = max(1, int(self.winfo_width() or self._width))
        cur_h = max(1, int(self.winfo_height() or self._height))
        if (cur_w, cur_h) != self._rendered_size and self._bg_source_pil is not None:
            self._width = cur_w
            self._height = cur_h
            self._render_background()

        elapsed = time.perf_counter() - self._start_time
        progress = min(1.0, elapsed / max(0.1, self._duration))

        self.delete("spinner")
        self.delete("status_label")
        self.delete("progress_bar")

        cx = cur_w // 2
        cy = cur_h - max(68, int(cur_h * 0.11))
        radius = 22

        angle_period = 1.35
        cycle_pos = (elapsed % angle_period) / angle_period
        sweep_phase = 0.5 - 0.5 * math.cos(2.0 * math.pi * cycle_pos)
        extent_deg = 45.0 + 245.0 * sweep_phase
        start_deg = -(elapsed * 290.0) % 360.0

        self.create_arc(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            start=start_deg,
            extent=-extent_deg,
            style="arc",
            outline="#FFFFFF",
            width=3,
            tags="spinner",
        )
        self.tag_raise("spinner")

        if self._show_status_text:
            status_msg = self._current_status_text(progress)
            self.create_text(
                cx,
                cy + 42,
                text=status_msg,
                fill="#F3F6FA",
                font=("Segoe UI", 12),
                anchor="center",
                tags="status_label",
            )
            self.tag_raise("status_label")

            bar_w = max(220, min(380, int(cur_w * 0.34)))
            bx0 = cx - bar_w // 2
            by0 = cy + 66
            self.delete("progress_bar")
            self.create_rectangle(bx0, by0, bx0 + bar_w, by0 + 5, fill="#1B2433", outline="", tags="progress_bar")
            fill_w = max(6, int(bar_w * progress))
            self.create_rectangle(bx0, by0, bx0 + fill_w, by0 + 5, fill=COLOR_ACCENT, outline="", tags="progress_bar")
            self.tag_raise("progress_bar")

        if elapsed >= self._duration:
            self._finish()
            return

        self._anim_job = self.after(16, self._animate_frame)

    def _finish(self) -> None:
        if self._finished:
            return
        self._finished = True
        if self._anim_job is not None:
            try:
                self.after_cancel(self._anim_job)
            except Exception:
                pass
            self._anim_job = None
        if callable(self._on_complete):
            self._on_complete()


class SecurityConsentOverlay(ctk.CTkFrame):
    """Экран безопасности и конфиденциальности: Шаг 1 Капча -> Шаг 2 Чекбокс -> Шаг 3 Кнопка запуска."""

    def __init__(self, parent, on_accept, sound_engine=None, closable: bool = False) -> None:
        super().__init__(parent, fg_color=COLOR_BG, corner_radius=0, border_width=0)
        self._on_accept = on_accept
        self._sound = sound_engine
        self._closable = closable
        self._captcha_code = ""
        self._captcha_solved = False

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 10))

        ctk.CTkLabel(
            header,
            text=f"Безопасность и конфиденциальность — RBX Client v{CURRENT_VERSION} (Издатель: {PUBLISHER_NAME})",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(side="left", padx=16, pady=12)

        if self._closable:
            ctk.CTkButton(
                header,
                text="Закрыть",
                width=90,
                height=30,
                corner_radius=8,
                border_width=0,
                fg_color=COLOR_SURFACE_ALT,
                hover_color=COLOR_SURFACE_HOVER,
                text_color=COLOR_TEXT_MUTED,
                font=("Segoe UI", 12),
                command=self._close_view,
            ).pack(side="right", padx=14)

        self.doc_box = ctk.CTkScrollableFrame(
            self,
            corner_radius=12,
            border_width=1,
            border_color="#222C3D",
            fg_color=COLOR_SURFACE,
            scrollbar_button_color="#222C3D",
            scrollbar_button_hover_color=COLOR_ACCENT,
        )
        self.doc_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 16))
        self.grid_rowconfigure(2, weight=0)
        ctk.CTkLabel(
            self.doc_box,
            text=SECURITY_POLICY_TEXT.strip(),
            font=("Segoe UI", 13),
            text_color=COLOR_TEXT,
            justify="left",
            anchor="w",
            wraplength=max(500, APP_WIDTH - 140),
        ).pack(fill="x", padx=18, pady=(14, 10))

        ctk.CTkLabel(
            self.doc_box,
            text="Проверка безопасности — пройдите капчу и подтвердите согласие",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_ACCENT,
            anchor="w",
        ).pack(fill="x", padx=18, pady=(10, 4))

        bottom_panel = ctk.CTkFrame(self.doc_box, fg_color=COLOR_SURFACE_ALT, corner_radius=12, border_width=1, border_color="#222C3D")
        bottom_panel.pack(fill="x", padx=14, pady=(0, 18))

        step1_row = ctk.CTkFrame(bottom_panel, fg_color="transparent", border_width=0)
        step1_row.pack(fill="x", padx=16, pady=(12, 8))

        ctk.CTkLabel(
            step1_row,
            text="Шаг 1. Капча:",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
        ).pack(side="left", padx=(0, 10))

        self.captcha_canvas = ctk.CTkCanvas(
            step1_row,
            width=144,
            height=40,
            bg=COLOR_SURFACE,
            highlightthickness=0,
            bd=0,
        )
        self.captcha_canvas.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            step1_row,
            text="↻ Обновить код",
            width=112,
            height=34,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT_MUTED,
            font=("Segoe UI", 12),
            command=self._generate_captcha,
        ).pack(side="left", padx=(0, 10))

        self.entry_captcha = ctk.CTkEntry(
            step1_row,
            width=120,
            height=34,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 13, "bold"),
            placeholder_text="Код...",
        )
        self.entry_captcha.pack(side="left", padx=(0, 8))
        self.entry_captcha.bind("<Return>", lambda _e: self._verify_captcha())

        self.btn_verify_captcha = ctk.CTkButton(
            step1_row,
            text="Проверить",
            width=96,
            height=34,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self._verify_captcha,
        )
        self.btn_verify_captcha.pack(side="left", padx=(0, 10))

        self.lbl_captcha_status = ctk.CTkLabel(
            step1_row,
            text="Введите код с картинки",
            font=("Segoe UI", 12),
            text_color=COLOR_TEXT_MUTED,
        )
        self.lbl_captcha_status.pack(side="left")

        self.step2_frame = ctk.CTkFrame(bottom_panel, fg_color="transparent", border_width=0)
        self.agree_var = ctk.IntVar(value=0)
        self.chk_agree = ctk.CTkCheckBox(
            self.step2_frame,
            text=f"Я прочитал(а) правила безопасности и конфиденциальности, убедился(ась), что издатель — {PUBLISHER_NAME}, и принимаю условия",
            variable=self.agree_var,
            onvalue=1,
            offvalue=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12, "bold"),
            command=self._on_checkbox_toggled,
        )
        self.chk_agree.pack(side="left")

        self.step3_frame = ctk.CTkFrame(bottom_panel, fg_color="transparent", border_width=0)
        self.btn_launch = ctk.CTkButton(
            self.step3_frame,
            text="Принять и продолжить",
            height=38,
            width=220,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SUCCESS,
            hover_color="#16A34A",
            text_color="#FFFFFF",
            font=("Segoe UI", 13, "bold"),
            command=self._on_launch_clicked,
        )
        self.btn_launch.pack(side="right")

        self._generate_captcha()

    def _play_click(self) -> None:
        if self._sound:
            self._sound.play_click()

    def _generate_captcha(self) -> None:
        self._play_click()
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        self._captcha_code = "".join(random.choice(chars) for _ in range(5))
        self._captcha_solved = False
        self.agree_var.set(0)
        self.step2_frame.pack_forget()
        self.step3_frame.pack_forget()
        self.entry_captcha.configure(state="normal")
        self.entry_captcha.delete(0, "end")
        self.btn_verify_captcha.configure(state="normal")
        self.lbl_captcha_status.configure(text="Введите код с картинки", text_color=COLOR_TEXT_MUTED)

        self.captcha_canvas.delete("all")
        w, h = 144, 40
        for _ in range(7):
            self.captcha_canvas.create_line(
                random.randint(0, w), random.randint(0, h),
                random.randint(0, w), random.randint(0, h),
                fill=random.choice(["#2A3950", "#3B82F6", "#64748B"]),
                width=1,
            )
        for _ in range(28):
            px, py = random.randint(0, w - 1), random.randint(0, h - 1)
            self.captcha_canvas.create_oval(px, py, px + 2, py + 2, fill="#94A3B8", outline="")

        for idx, ch in enumerate(self._captcha_code):
            cx = 18 + idx * 24 + random.randint(-2, 2)
            cy = 20 + random.randint(-4, 4)
            self.captcha_canvas.create_text(cx, cy, text=ch, fill="#F8FAFC", font=("Consolas", 17, "bold"))

    def _verify_captcha(self) -> None:
        self._play_click()
        typed = self.entry_captcha.get().strip().upper()
        if typed == self._captcha_code and len(typed) == 5:
            self._captcha_solved = True
            self.entry_captcha.configure(state="disabled")
            self.btn_verify_captcha.configure(state="disabled")
            self.lbl_captcha_status.configure(text="✓ Капча пройдена", text_color=COLOR_SUCCESS)
            self.step2_frame.pack(fill="x", padx=16, pady=(0, 8))
        else:
            self.lbl_captcha_status.configure(text="✕ Неверный код", text_color=COLOR_DANGER)
            self._generate_captcha()

    def _on_checkbox_toggled(self) -> None:
        self._play_click()
        if not self._captcha_solved:
            self.agree_var.set(0)
            return
        if int(self.agree_var.get()) == 1:
            self.step3_frame.pack(fill="x", padx=16, pady=(0, 12))
        else:
            self.step3_frame.pack_forget()

    def _on_launch_clicked(self) -> None:
        self._play_click()
        if not self._captcha_solved or int(self.agree_var.get()) != 1:
            return
        if callable(self._on_accept):
            self._on_accept()

    def _close_view(self) -> None:
        self._play_click()
        self.destroy()


class AntiDdosFilter:
    """RBX Shield Anti-DDoS: скользящее окно запросов по каждому хосту. Режет только реальный шквал запросов."""

    def __init__(self, guard=None, limit: int = 120, window_sec: float = 10.0) -> None:
        self._guard = guard
        self._limit = int(limit)
        self._window = float(window_sec)
        self._hits: dict[str, deque] = {}
        self._lock = threading.Lock()
        self._last_log = 0.0
        self.blocked_total = 0

    def _enabled(self) -> bool:
        try:
            getter = getattr(self._guard, "_get_config", None)
            cfg = getter() if callable(getter) else {}
            return bool(cfg.get("security_guard_enabled", True))
        except Exception:
            return True

    def allow(self, url: str) -> bool:
        if not self._enabled():
            return True
        host = urllib.parse.urlparse(str(url)).netloc.lower() or "unknown"
        now = time.monotonic()
        with self._lock:
            dq = self._hits.setdefault(host, deque())
            while dq and now - dq[0] > self._window:
                dq.popleft()
            if len(dq) >= self._limit:
                self.blocked_total += 1
                if now - self._last_log > 30.0:
                    self._last_log = now
                    write_security_incident_log("WARN", f"Anti-DDoS: превышен лимит запросов к {host}")
                return False
            dq.append(now)
        return True


class RobloxApiClient:
    def __init__(self, security_guard: LauncherSecurityGuard | None = None) -> None:
        self._security_guard = security_guard
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) RBXClient/{CURRENT_VERSION}",
            "Accept": "application/json, text/plain, */*",
        })
        self._mem_cache: dict[str, tuple[float, object]] = {}
        self._lock = threading.Lock()
        self._ddos = AntiDdosFilter(security_guard)

    def _cache_get(self, key: str, ttl: float):
        with self._lock:
            item = self._mem_cache.get(key)
            if not item:
                return None
            ts, value = item
            if (time.monotonic() - ts) <= ttl:
                return value
            return None

    def _cache_set(self, key: str, value) -> None:
        with self._lock:
            self._mem_cache[key] = (time.monotonic(), value)

    def _get_json(self, url: str, params: dict | None = None, timeout: float = 8.0, ttl: float = 0.0):
        cache_key = f"json:{url}:{urllib.parse.urlencode(params or {})}"
        if ttl > 0:
            cached = self._cache_get(cache_key, ttl)
            if cached is not None:
                return cached
        if not self._ddos.allow(url):
            return None
        try:
            resp = self._session.get(url, params=params, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                if ttl > 0:
                    self._cache_set(cache_key, data)
                return data
        except Exception as exc:
            write_crash_fix_log(f"API_JSON:{url}", exc)
        return None

    def _get_bytes(self, url: str, timeout: float = 8.0, ttl: float = 120.0) -> bytes | None:
        if not self._ddos.allow(url):
            return None
        if not url:
            return None
        cache_key = f"bytes:{url}"
        if ttl > 0:
            cached = self._cache_get(cache_key, ttl)
            if isinstance(cached, bytes):
                return cached
        try:
            resp = self._session.get(url, timeout=timeout)
            if resp.status_code == 200 and resp.content:
                data = resp.content
                if ttl > 0:
                    self._cache_set(cache_key, data)
                return data
        except Exception as exc:
            write_crash_fix_log(f"API_BYTES:{url}", exc)
        return None

    def resolve_universe_from_place(self, place_id: int) -> int | None:
        data = self._get_json(
            f"https://apis.roblox.com/universes/v1/places/{place_id}/universe",
            timeout=7.0,
            ttl=300.0,
        )
        if isinstance(data, dict) and data.get("universeId"):
            try:
                return int(data["universeId"])
            except (ValueError, TypeError):
                return None
        return None

    def get_games_details_by_universes(self, universe_ids: list[int]) -> list[dict]:
        clean_ids = []
        seen = set()
        for uid in universe_ids:
            try:
                ival = int(uid)
                if ival > 0 and ival not in seen:
                    seen.add(ival)
                    clean_ids.append(ival)
            except (ValueError, TypeError):
                continue
        if not clean_ids:
            return []

        results: list[dict] = []
        chunk_size = 50
        for idx in range(0, len(clean_ids), chunk_size):
            chunk = clean_ids[idx:idx + chunk_size]
            ids_str = ",".join(str(x) for x in chunk)
            data = self._get_json(
                "https://games.roblox.com/v1/games",
                params={"universeIds": ids_str},
                timeout=8.0,
                ttl=3.0,
            )
            if isinstance(data, dict) and isinstance(data.get("data"), list):
                for item in data["data"]:
                    creator_obj = item.get("creator") or {}
                    pid = int(item.get("rootPlaceId") or 0)
                    results.append({
                        "place_id": pid,
                        "placeId": pid,
                        "universe_id": int(item.get("id") or 0),
                        "name": str(item.get("name") or "Roblox Game"),
                        "creator": str(creator_obj.get("name") or "Roblox"),
                        "playing": int(item.get("playing") or 0),
                        "visits": int(item.get("visits") or 0),
                        "max_players": int(item.get("maxPlayers") or 0),
                    })
        return results

    def get_game_info_by_place(self, place_id: int) -> dict:
        universe_id = self.resolve_universe_from_place(place_id)
        if universe_id:
            details = self.get_games_details_by_universes([universe_id])
            if details:
                info = dict(details[0])
                info["place_id"] = int(place_id)
                info["placeId"] = int(place_id)
                return info
        return {
            "place_id": int(place_id),
            "placeId": int(place_id),
            "universe_id": universe_id or 0,
            "name": f"Place #{place_id}",
            "creator": "Roblox",
            "playing": 0,
            "visits": 0,
            "max_players": 0,
        }

    def get_thumbnail_16x9_bytes(self, universe_id: int, place_id: int) -> bytes | None:
        local_candidates = [
            os.path.join(PHOTO_GAMES_DIR, f"{place_id}.jpg"),
            os.path.join(PHOTO_GAMES_DIR, f"{place_id}.png"),
            os.path.join(PHOTO_GAMES_DIR, f"{universe_id}.jpg"),
            os.path.join(PHOTO_GAMES_DIR, f"{universe_id}.png"),
        ]
        for path in local_candidates:
            if universe_id == 0 and f"{universe_id}." in path:
                continue
            if os.path.isfile(path):
                try:
                    with open(path, "rb") as f:
                        b = f.read()
                        if b:
                            return b
                except Exception:
                    pass

        cache_key_hash = hashlib.md5(f"thumb169:{universe_id}:{place_id}".encode("utf-8")).hexdigest()
        cache_file = os.path.join(CACHE_DIR, f"{cache_key_hash}.jpg")
        if os.path.isfile(cache_file):
            try:
                with open(cache_file, "rb") as f:
                    b = f.read()
                    if b:
                        return b
            except Exception:
                pass

        if universe_id and universe_id > 0:
            thumb_api = self._get_json(
                "https://thumbnails.roblox.com/v1/games/multiget/thumbnails",
                params={
                    "universeIds": str(universe_id),
                    "countPerUniverse": "1",
                    "defaults": "true",
                    "size": "768x432",
                    "format": "Jpeg",
                    "isCircular": "false",
                },
                timeout=8.0,
                ttl=600.0,
            )
            if isinstance(thumb_api, dict) and isinstance(thumb_api.get("data"), list):
                for entry in thumb_api["data"]:
                    thumbs = entry.get("thumbnails") or []
                    for t_item in thumbs:
                        img_url = t_item.get("imageUrl")
                        if img_url:
                            raw = self._get_bytes(img_url, timeout=8.0, ttl=600.0)
                            if raw:
                                try:
                                    with open(cache_file, "wb") as f:
                                        f.write(raw)
                                except Exception:
                                    pass
                                return raw

        icon_bytes = self.get_game_icon_bytes(universe_id)
        if icon_bytes:
            return icon_bytes
        return self.get_place_icon_bytes(place_id)

    def get_place_icon_bytes(self, place_id: int) -> bytes | None:
        """Запасной вариант: квадратная иконка places/gameicons (растягивается через ImageOps.fit при сборке баннера)."""
        if not place_id:
            return None
        data = self._get_json(
            "https://thumbnails.roblox.com/v1/places/gameicons",
            params={"placeIds": str(place_id), "returnPolicy": "PlaceHolder", "size": "512x512", "format": "Png", "isCircular": "false"},
            timeout=8.0,
            ttl=600.0,
        )
        if isinstance(data, dict):
            for item in data.get("data") or []:
                url = item.get("imageUrl")
                if url:
                    raw = self._get_bytes(url, timeout=8.0, ttl=600.0)
                    if raw:
                        return raw
        return None

    def get_game_icon_bytes(self, universe_id: int) -> bytes | None:
        if not universe_id or universe_id <= 0:
            return None
        cache_file = os.path.join(CACHE_DIR, f"icon_{universe_id}.jpg")
        if os.path.isfile(cache_file):
            try:
                with open(cache_file, "rb") as f:
                    b = f.read()
                    if b:
                        return b
            except Exception:
                pass

        data = self._get_json(
            "https://thumbnails.roblox.com/v1/games/icons",
            params={
                "universeIds": str(universe_id),
                "returnPolicy": "PlaceHolder",
                "size": "150x150",
                "format": "Jpeg",
                "isCircular": "false",
            },
            timeout=7.0,
            ttl=600.0,
        )
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            for item in data["data"]:
                img_url = item.get("imageUrl")
                if img_url:
                    raw = self._get_bytes(img_url, timeout=7.0, ttl=600.0)
                    if raw:
                        try:
                            with open(cache_file, "wb") as f:
                                f.write(raw)
                        except Exception:
                            pass
                        return raw
        return None

    def get_active_games_feed(self, query: str = "", min_playing: int = 100) -> list[dict]:
        collected: list[dict] = []
        seen_universes: set[int] = set()

        clean_q = (query or "").strip()
        if clean_q:
            omni = self._get_json(
                "https://apis.roblox.com/search-api/omni-search",
                params={
                    "searchQuery": clean_q,
                    "pageType": "games",
                    "sessionId": "rbxclient-145",
                },
                timeout=8.0,
                ttl=4.0,
            )
            if isinstance(omni, dict):
                search_results = omni.get("searchResults") or []
                for block in search_results:
                    contents = block.get("contents") or []
                    for item in contents:
                        uid = item.get("universeId") or item.get("id")
                        pid = item.get("rootPlaceId") or item.get("placeId")
                        if uid:
                            try:
                                u_int = int(uid)
                                if u_int not in seen_universes:
                                    seen_universes.add(u_int)
                                    pid_int = int(pid or 0)
                                    collected.append({
                                        "universe_id": u_int,
                                        "place_id": pid_int,
                                        "placeId": pid_int,
                                        "name": str(item.get("name") or "Roblox Game"),
                                        "creator": str(item.get("creatorName") or "Roblox"),
                                        "playing": int(item.get("playerCount") or 0),
                                    })
                            except (ValueError, TypeError):
                                pass

        rolimons = self._get_json(
            "https://api.rolimons.com/games/v1/gamelist",
            timeout=8.0,
            ttl=4.0,
        )
        if isinstance(rolimons, dict) and isinstance(rolimons.get("games"), dict):
            games_map = rolimons["games"]
            candidate_uids: list[tuple[int, int, str]] = []
            for uid_str, arr in games_map.items():
                if not isinstance(arr, list) or len(arr) < 3:
                    continue
                try:
                    playing_val = int(arr[2] or 0)
                    u_int = int(uid_str)
                except (ValueError, TypeError):
                    continue
                if playing_val >= min_playing:
                    name_val = str(arr[0] or f"Game {u_int}")
                    if clean_q and clean_q.lower() not in name_val.lower():
                        continue
                    candidate_uids.append((playing_val, u_int, name_val))

            candidate_uids.sort(key=lambda x: x[0], reverse=True)
            top_uids = [item[1] for item in candidate_uids[:60]]
            if top_uids:
                enriched = self.get_games_details_by_universes(top_uids)
                for g in enriched:
                    u_int = g["universe_id"]
                    if g["playing"] >= min_playing and u_int not in seen_universes:
                        seen_universes.add(u_int)
                        collected.append(g)

        if not collected:
            for fg in FALLBACK_GAMES:
                if fg["playing"] < min_playing:
                    continue
                if clean_q and clean_q.lower() not in fg["name"].lower():
                    continue
                item_copy = dict(fg)
                item_copy["placeId"] = item_copy["place_id"]
                collected.append(item_copy)

        if collected and len(collected) <= 60:
            u_list = [g["universe_id"] for g in collected if g.get("universe_id", 0) > 0]
            fresh_details = {d["universe_id"]: d for d in self.get_games_details_by_universes(u_list)}
            for g in collected:
                fd = fresh_details.get(g.get("universe_id", 0))
                if fd:
                    g["playing"] = fd["playing"]
                    if fd.get("place_id"):
                        g["place_id"] = fd["place_id"]
                        g["placeId"] = fd["place_id"]
                    if fd.get("name"):
                        g["name"] = fd["name"]
                    if fd.get("creator"):
                        g["creator"] = fd["creator"]

        filtered = [g for g in collected if int(g.get("playing") or 0) >= min_playing]
        filtered.sort(key=lambda x: int(x.get("playing") or 0), reverse=True)
        return filtered[:45]

    def get_public_servers(self, place_id: int) -> list[dict]:
        servers: list[dict] = []
        cursor = ""
        for _ in range(3):
            params = {"sortOrder": "Asc", "limit": "100"}
            if cursor:
                params["cursor"] = cursor
            data = self._get_json(
                f"https://games.roblox.com/v1/games/{place_id}/servers/Public",
                params=params,
                timeout=8.0,
                ttl=3.0,
            )
            if not isinstance(data, dict):
                break
            rows = data.get("data") or []
            for r in rows:
                job_id = str(r.get("id") or "")
                if not job_id:
                    continue
                playing = int(r.get("playing") or 0)
                max_p = int(r.get("maxPlayers") or 0)
                ping = int(r.get("ping") or 0)
                fps = float(r.get("fps") or 0.0)
                servers.append({
                    "job_id": job_id,
                    "playing": playing,
                    "max_players": max_p,
                    "ping": ping,
                    "fps": fps,
                })
            cursor = str(data.get("nextPageCursor") or "")
            if not cursor:
                break

        servers.sort(key=lambda s: (s["playing"], s["ping"] if s["ping"] > 0 else 9999))
        return servers

    def get_user_profile(self, user_id: int) -> dict | None:
        profile_data = self._get_json(
            f"https://users.roblox.com/v1/users/{user_id}",
            timeout=8.0,
            ttl=120.0,
        )
        if not isinstance(profile_data, dict) or not profile_data.get("id"):
            return None

        friends_count = 0
        friends_data = self._get_json(
            f"https://friends.roblox.com/v1/users/{user_id}/friends/count",
            timeout=6.0,
            ttl=120.0,
        )
        if isinstance(friends_data, dict):
            friends_count = int(friends_data.get("count") or 0)

        followers_count = 0
        followers_data = self._get_json(
            f"https://friends.roblox.com/v1/users/{user_id}/followers/count",
            timeout=6.0,
            ttl=120.0,
        )
        if isinstance(followers_data, dict):
            followers_count = int(followers_data.get("count") or 0)

        friends_list: list[dict] = []
        friends_list_resp = self._get_json(
            f"https://friends.roblox.com/v1/users/{user_id}/friends",
            timeout=7.0,
            ttl=120.0,
        )
        if isinstance(friends_list_resp, dict) and isinstance(friends_list_resp.get("data"), list):
            for f_item in friends_list_resp["data"][:200]:
                fid = f_item.get("id")
                if fid:
                    friends_list.append({
                        "id": int(fid),
                        "name": str(f_item.get("name") or f"User_{fid}"),
                        "display_name": str(f_item.get("displayName") or f_item.get("name") or f"User_{fid}"),
                    })

        if friends_list:
            details = self.get_users_batch([f["id"] for f in friends_list])
            for f in friends_list:
                d = details.get(f["id"])
                if d:
                    f["name"] = str(d.get("name") or f["name"])
                    f["display_name"] = str(d.get("displayName") or d.get("name") or f["display_name"])
            friends_list.sort(key=lambda f: str(f["display_name"]).lower())

        return {
            "id": int(profile_data.get("id")),
            "username": str(profile_data.get("name") or ""),
            "display_name": str(profile_data.get("displayName") or profile_data.get("name") or ""),
            "description": str(profile_data.get("description") or ""),
            "created": str(profile_data.get("created") or ""),
            "is_banned": bool(profile_data.get("isBanned") or False),
            "friends_count": friends_count,
            "followers_count": followers_count,
            "friends": friends_list,
        }

    def get_user_id_by_username(self, username: str) -> int | None:
        clean_name = (username or "").strip().lstrip("@")
        if not clean_name:
            return None
        resp = None
        try:
            r = self._session.post(
                "https://users.roblox.com/v1/usernames/users",
                json={"usernames": [clean_name], "excludeBannedUsers": False},
                timeout=8.0,
            )
            if r.status_code == 200:
                resp = r.json()
        except Exception as exc:
            write_crash_fix_log("API_POST:usernames/users", exc)
            resp = None
        if isinstance(resp, dict) and isinstance(resp.get("data"), list) and resp["data"]:
            uid = resp["data"][0].get("id")
            if uid:
                return int(uid)
        return None

    def get_user_headshot_bytes(self, user_id: int) -> bytes | None:
        if not user_id or user_id <= 0:
            return None
        cache_file = os.path.join(CACHE_DIR, f"avatar_{user_id}.png")
        if os.path.isfile(cache_file):
            try:
                with open(cache_file, "rb") as f:
                    b = f.read()
                    if b:
                        return b
            except Exception:
                pass

        data = self._get_json(
            "https://thumbnails.roblox.com/v1/users/avatar-headshot",
            params={
                "userIds": str(user_id),
                "size": "150x150",
                "format": "Png",
                "isCircular": "false",
            },
            timeout=7.0,
            ttl=600.0,
        )
        if isinstance(data, dict) and isinstance(data.get("data"), list):
            for item in data["data"]:
                img_url = item.get("imageUrl")
                if img_url:
                    raw = self._get_bytes(img_url, timeout=7.0, ttl=600.0)
                    if raw:
                        try:
                            with open(cache_file, "wb") as f:
                                f.write(raw)
                        except Exception:
                            pass
                        return raw
        return None

    def get_users_batch(self, user_ids: list[int]) -> dict[int, dict]:
        out: dict[int, dict] = {}
        ids = [int(i) for i in user_ids if int(i or 0) > 0]
        for i in range(0, len(ids), 100):
            chunk = ids[i:i + 100]
            if not self._ddos.allow("https://users.roblox.com/v1/users"):
                break
            try:
                resp = self._session.post(
                    "https://users.roblox.com/v1/users",
                    json={"userIds": chunk, "excludeBannedUsers": False},
                    timeout=8.0,
                )
                if resp.status_code == 200:
                    for u in (resp.json().get("data") or []):
                        if u.get("id"):
                            out[int(u["id"])] = u
            except Exception as exc:
                write_crash_fix_log("API_USERS_BATCH", exc)
        return out

    def get_headshots_batch_bytes(self, user_ids: list[int], max_users: int = 150) -> dict[int, bytes]:
        from concurrent.futures import ThreadPoolExecutor

        out: dict[int, bytes] = {}
        ids = [int(i) for i in user_ids if int(i or 0) > 0][:max_users]
        urls: dict[int, str] = {}
        for i in range(0, len(ids), 100):
            chunk = ids[i:i + 100]
            data = self._get_json(
                "https://thumbnails.roblox.com/v1/users/avatar-headshot",
                params={"userIds": ",".join(str(x) for x in chunk), "size": "150x150", "format": "Png", "isCircular": "true"},
                timeout=9.0,
                ttl=300.0,
            )
            if isinstance(data, dict):
                for it in data.get("data") or []:
                    if it.get("imageUrl") and it.get("targetId"):
                        urls[int(it["targetId"])] = str(it["imageUrl"])

        def _dl(item):
            uid, url = item
            cache_file = os.path.join(CACHE_DIR, f"avatarc_{uid}.png")
            if os.path.isfile(cache_file):
                try:
                    with open(cache_file, "rb") as f:
                        b = f.read()
                    if b:
                        return uid, b
                except Exception:
                    pass
            raw = self._get_bytes(url, timeout=8.0, ttl=600.0)
            if raw:
                try:
                    with open(cache_file, "wb") as f:
                        f.write(raw)
                except Exception:
                    pass
            return uid, raw

        if urls:
            with ThreadPoolExecutor(max_workers=8) as pool:
                for uid, raw in pool.map(_dl, list(urls.items())):
                    if raw:
                        out[uid] = raw
        return out

    def check_github_latest_version(self) -> dict:
        latest_data = self._get_json(GITHUB_API_LATEST, timeout=7.0, ttl=30.0)
        if isinstance(latest_data, dict):
            tag = str(latest_data.get("tag_name") or latest_data.get("name") or "").strip()
            html_url = str(latest_data.get("html_url") or f"https://github.com/{GITHUB_REPO}/releases").strip()
            expected_sha = ""
            for asset in latest_data.get("assets") or []:
                if isinstance(asset, dict):
                    digest_raw = str(asset.get("digest") or "")
                    if digest_raw.lower().startswith("sha256:"):
                        expected_sha = digest_raw.split(":", 1)[1].strip()
                        break
            if tag and is_strictly_newer_version(tag, CURRENT_VERSION):
                return {
                    "has_update": True,
                    "latest_version": tag.lstrip("vV"),
                    "url": html_url,
                    "sha256": expected_sha,
                }

        tags_data = self._get_json(GITHUB_API_TAGS, timeout=7.0, ttl=30.0)
        if isinstance(tags_data, list):
            best_tag = ""
            for t_obj in tags_data:
                if not isinstance(t_obj, dict):
                    continue
                t_name = str(t_obj.get("name") or "").strip()
                if t_name and is_strictly_newer_version(t_name, CURRENT_VERSION):
                    if not best_tag or is_strictly_newer_version(t_name, best_tag):
                        best_tag = t_name
            if best_tag:
                return {
                    "has_update": True,
                    "latest_version": best_tag.lstrip("vV"),
                    "url": f"https://github.com/{GITHUB_REPO}/releases/tag/{best_tag}",
                    "sha256": "",
                }

        return {
            "has_update": False,
            "latest_version": CURRENT_VERSION,
            "url": f"https://github.com/{GITHUB_REPO}/releases",
            "sha256": "",
        }


class LocalAccountDetector:
    def __init__(self) -> None:
        self._local_app_data = os.environ.get("LOCALAPPDATA", "")

    def detect_local_user_id(self) -> int | None:
        uid = self._read_app_storage_user_id()
        if uid:
            return uid
        uid = self._scan_roblox_logs_user_id()
        if uid:
            return uid
        uid = self._scan_browser_history_user_id()
        if uid:
            return uid
        return None

    def _read_app_storage_user_id(self) -> int | None:
        if not self._local_app_data:
            return None
        path = os.path.join(self._local_app_data, "Roblox", "LocalStorage", "appStorage.json")
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
            data = json.loads(raw_text)
            if isinstance(data, dict):
                for key in ("UserId", "userId", "LastUserId", "AuthenticatedUserId"):
                    val = data.get(key)
                    if val is not None:
                        s_val = str(val).strip().strip('"')
                        if s_val.isdigit() and int(s_val) > 0:
                            return int(s_val)
            m = re.search(r'"UserId"\s*:\s*"?(\d+)"?', raw_text)
            if m:
                uid_val = int(m.group(1))
                if uid_val > 0:
                    return uid_val
        except Exception:
            pass
        return None

    def _scan_roblox_logs_user_id(self) -> int | None:
        if not self._local_app_data:
            return None
        logs_dir = os.path.join(self._local_app_data, "Roblox", "logs")
        if not os.path.isdir(logs_dir):
            return None
        try:
            log_files = glob.glob(os.path.join(logs_dir, "*.log"))
            log_files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
            for log_path in log_files[:8]:
                try:
                    file_size = os.path.getsize(log_path)
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                        if file_size > 2_500_000:
                            f.seek(file_size - 2_500_000)
                        content = f.read()
                    matches = re.findall(r"userid\s*[:=]\s*(\d+)", content, flags=re.IGNORECASE)
                    for uid_str in reversed(matches):
                        uid_val = int(uid_str)
                        if uid_val > 0:
                            return uid_val
                except Exception:
                    continue
        except Exception:
            pass
        return None

    def _scan_browser_history_user_id(self) -> int | None:
        if not self._local_app_data:
            return None
        history_candidates = [
            os.path.join(self._local_app_data, "Google", "Chrome", "User Data", "Default", "History"),
            os.path.join(self._local_app_data, "Microsoft", "Edge", "User Data", "Default", "History"),
            os.path.join(self._local_app_data, "BraveSoftware", "Brave-Browser", "User Data", "Default", "History"),
            os.path.join(self._local_app_data, "Yandex", "YandexBrowser", "User Data", "Default", "History"),
        ]
        for h_path in history_candidates:
            if not os.path.isfile(h_path):
                continue
            try:
                size = os.path.getsize(h_path)
                with open(h_path, "rb") as f:
                    if size > 4_000_000:
                        f.seek(size - 4_000_000)
                    raw = f.read()
                text = raw.decode("latin-1", errors="ignore")
                matches = re.findall(r"roblox\.com/users/(\d+)/profile", text, flags=re.IGNORECASE)
                if matches:
                    uid_val = int(matches[-1])
                    if uid_val > 0:
                        return uid_val
            except Exception:
                continue
        return None


class RobloxSystemManager:
    def __init__(self, sound_engine: SoundEngine, config_getter, security_guard: LauncherSecurityGuard | None = None) -> None:
        self._sound = sound_engine
        self._get_config = config_getter
        self._security_guard = security_guard
        self._local_app_data = os.environ.get("LOCALAPPDATA", "")

    def find_roblox_player_exe(self) -> str | None:
        if not self._local_app_data:
            return None
        versions_dir = os.path.join(self._local_app_data, "Roblox", "Versions")
        if not os.path.isdir(versions_dir):
            return None
        candidates = glob.glob(os.path.join(versions_dir, "*", "RobloxPlayerBeta.exe"))
        if not candidates:
            candidates = glob.glob(os.path.join(versions_dir, "*", "RobloxPlayerLauncher.exe"))
        if not candidates:
            return None
        candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return candidates[0]

    def get_client_settings_path(self) -> str:
        base = self._local_app_data or BASE_DIR
        exe_path = self.find_roblox_player_exe()
        if exe_path:
            ver_dir = os.path.dirname(exe_path)
            return os.path.join(ver_dir, "ClientSettings", "ClientAppSettings.json")
        return os.path.join(base, "Roblox", "ClientSettings", "ClientAppSettings.json")

    def ensure_valid_client_app_settings(self) -> tuple[bool, str]:
        """Validate ClientAppSettings.json before every launch; backup .bak and rebuild from config if invalid."""
        target_path = self.get_client_settings_path()
        cfg = self._get_config() if callable(self._get_config) else {}
        needs_rebuild = False

        if not os.path.isfile(target_path):
            needs_rebuild = True
        else:
            try:
                if os.path.getsize(target_path) == 0:
                    needs_rebuild = True
                else:
                    with open(target_path, "r", encoding="utf-8") as f:
                        parsed = json.load(f)
                    if not isinstance(parsed, dict):
                        needs_rebuild = True
            except Exception as exc:
                write_crash_fix_log("validate_ClientAppSettings", exc)
                needs_rebuild = True

        if needs_rebuild:
            if os.path.isfile(target_path):
                try:
                    shutil.copy2(target_path, f"{target_path}.{int(time.time())}.bak")
                except Exception:
                    pass
            ok, msg = self.apply_extended_client_tweaks(
                fps_cap=int(cfg.get("fps_cap", 144)),
                render_engine=str(cfg.get("render_engine", "DirectX 11")),
                disable_shadows=bool(cfg.get("disable_shadows", False)),
                disable_grass=bool(cfg.get("disable_grass", False)),
                disable_telemetry=bool(cfg.get("disable_telemetry", True)),
                disable_motion_blur=bool(cfg.get("disable_motion_blur", True)),
                low_texture_quality=bool(cfg.get("low_texture_quality", False)),
                disable_overlay_analytics=bool(cfg.get("disable_overlay_analytics", True)),
                quality_level=str(cfg.get("quality_level", "Авто")),
            )
            if ok:
                write_launcher_log("[SelfHeal] Пересобран повреждённый ClientAppSettings.json (.bak сохранён)")
            return ok, msg

        return True, "ClientAppSettings.json valid"

    def detect_hardware_preset(self) -> dict:
        cpu_count = os.cpu_count() or 4
        ram_gb = 8.0
        if platform.system().lower() == "windows":
            try:
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                    ram_gb = round(stat.ullTotalPhys / (1024 ** 3), 1)
            except Exception:
                pass

        if ram_gb < 8 or cpu_count <= 4:
            return {
                "preset_name": "Низкие FPS",
                "fps_cap": 60,
                "render_engine": "DirectX 11",
                "disable_shadows": True,
                "disable_grass": True,
                "disable_telemetry": True,
                "disable_motion_blur": True,
                "low_texture_quality": True,
                "quality_level": "Низкая",
                "summary": f"CPU: {cpu_count} потоков, ОЗУ: {ram_gb} ГБ -> Низкие FPS (60)",
            }
        if ram_gb < 16 or cpu_count <= 8:
            return {
                "preset_name": "Средние",
                "fps_cap": 120,
                "render_engine": "DirectX 11",
                "disable_shadows": False,
                "disable_grass": True,
                "disable_telemetry": True,
                "disable_motion_blur": True,
                "low_texture_quality": False,
                "quality_level": "Средняя",
                "summary": f"CPU: {cpu_count} потоков, ОЗУ: {ram_gb} ГБ -> Средние (120)",
            }
        return {
            "preset_name": "Высокие",
            "fps_cap": 240,
            "render_engine": "DirectX 11",
            "disable_shadows": False,
            "disable_grass": False,
            "disable_telemetry": True,
            "disable_motion_blur": False,
            "low_texture_quality": False,
            "quality_level": "Максимальная",
            "summary": f"CPU: {cpu_count} потоков, ОЗУ: {ram_gb} ГБ -> Высокие (240)",
        }

    def apply_client_app_settings(
        self,
        fps_cap: int,
        render_engine: str,
        disable_shadows: bool,
        disable_grass: bool,
        disable_telemetry: bool,
    ) -> tuple[bool, str]:
        target_path = self.get_client_settings_path()
        settings_dir = os.path.dirname(target_path)
        try:
            os.makedirs(settings_dir, exist_ok=True)
            existing: dict = {}
            if os.path.isfile(target_path):
                try:
                    with open(target_path, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                        if isinstance(loaded, dict):
                            existing = loaded
                except Exception:
                    existing = {}

            existing["FFlagDebugForceFutureIsBrightPhase3"] = False
            existing["FFlagDebugForceFSMCPState"] = True
            existing["DFIntTaskSchedulerTargetFps"] = int(max(30, min(999, fps_cap)))

            engine_map = {
                "DirectX 11": ("FFlagDebugForceD3D11", True, "FFlagDebugForceVulkan", False, "FFlagDebugForceOpenGL", False),
                "DirectX 10": ("FFlagDebugForceD3D11", False, "FFlagDebugForceVulkan", False, "FFlagDebugForceOpenGL", False),
                "Vulkan": ("FFlagDebugForceD3D11", False, "FFlagDebugForceVulkan", True, "FFlagDebugForceOpenGL", False),
                "OpenGL": ("FFlagDebugForceD3D11", False, "FFlagDebugForceVulkan", False, "FFlagDebugForceOpenGL", True),
            }
            dx_key, dx_val, vk_key, vk_val, gl_key, gl_val = engine_map.get(
                render_engine,
                engine_map["DirectX 11"],
            )
            existing[dx_key] = dx_val
            existing[vk_key] = vk_val
            existing[gl_key] = gl_val

            if disable_shadows:
                existing["FIntRenderShadowIntensity"] = 0
                existing["DFIntDebugFRMRenderShadowIntensity"] = 0
            else:
                existing.pop("FIntRenderShadowIntensity", None)
                existing.pop("DFIntDebugFRMRenderShadowIntensity", None)

            if disable_grass:
                existing["FIntFRMMinGrassDistance"] = 0
                existing["FIntFRMMaxGrassDistance"] = 0
                existing["DFIntRenderGrassDetailRadius"] = 0
            else:
                existing.pop("FIntFRMMinGrassDistance", None)
                existing.pop("FIntFRMMaxGrassDistance", None)
                existing.pop("DFIntRenderGrassDetailRadius", None)

            if disable_telemetry:
                existing["FFlagEnableTelemetryV2"] = False
                existing["FFlagDebugDisableTelemetryEphemeralCounter"] = True
                existing["FFlagDebugDisableTelemetryEphemeralStat"] = True
                existing["FFlagDebugDisableTelemetryEventIngest"] = True
            else:
                existing["FFlagEnableTelemetryV2"] = True
                existing["FFlagDebugDisableTelemetryEphemeralCounter"] = False
                existing["FFlagDebugDisableTelemetryEphemeralStat"] = False
                existing["FFlagDebugDisableTelemetryEventIngest"] = False

            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)

            write_launcher_log(f"Сохранен ClientAppSettings.json: {target_path}")
            return True, f"Сохранено: {target_path}"
        except Exception as exc:
            write_launcher_log(f"Ошибка записи ClientAppSettings.json: {exc}")
            return False, f"Ошибка записи: {exc}"

    def apply_extended_client_tweaks(
        self,
        fps_cap: int,
        render_engine: str,
        disable_shadows: bool,
        disable_grass: bool,
        disable_telemetry: bool,
        disable_motion_blur: bool,
        low_texture_quality: bool,
        disable_overlay_analytics: bool,
        quality_level: str,
    ) -> tuple[bool, str]:
        ok, msg = self.apply_client_app_settings(
            fps_cap=fps_cap,
            render_engine=render_engine,
            disable_shadows=disable_shadows,
            disable_grass=disable_grass,
            disable_telemetry=disable_telemetry,
        )
        if not ok:
            return False, msg

        target_path = self.get_client_settings_path()
        try:
            existing: dict = {}
            if os.path.isfile(target_path):
                with open(target_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        existing = loaded

            existing["FFlagDisableMotionBlur"] = bool(disable_motion_blur)
            existing["DFIntDebugFRMRenderTextureQuality"] = 0 if low_texture_quality else 3
            existing["FFlagDebugForceTextureQuality"] = bool(low_texture_quality)

            if disable_overlay_analytics:
                existing["FFlagEnableInGameMenuChromeABTest"] = False
                existing["FFlagDisableTelemetryV2"] = False
                existing["FFlagDebugDisableTelemetrySession"] = True
            else:
                existing["FFlagDebugDisableTelemetrySession"] = False

            quality_map = {
                "Авто": 0,
                "Низкая": 1,
                "Средняя": 5,
                "Максимальная": 10,
            }
            q_val = quality_map.get(quality_level, 0)
            if q_val > 0:
                existing["DFIntDebugFRMForcedQualityLevel"] = q_val
            else:
                existing.pop("DFIntDebugFRMForcedQualityLevel", None)

            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
            return True, f"Применено: {target_path}"
        except Exception as exc:
            return False, f"Ошибка сохранения твиков: {exc}"

    def reset_client_app_settings(self) -> tuple[bool, str]:
        target_path = self.get_client_settings_path()
        try:
            if os.path.isfile(target_path):
                os.remove(target_path)
            write_launcher_log("Сброшены настройки графики ClientAppSettings.json")
            return True, "Стандартные настройки графики восстановлены"
        except Exception as exc:
            return False, f"Ошибка сброса: {exc}"

    def _write_classic_oof_file(self, target_path: str) -> None:
        sample_rate = 22050
        duration = 0.22
        n_samples = int(sample_rate * duration)
        pcm = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            env = min(1.0, t / 0.015) * max(0.0, 1.0 - (t / duration))
            freq = 165.0 + 35.0 * math.sin(2.0 * math.pi * 6.0 * t)
            val = (
                0.65 * math.sin(2.0 * math.pi * freq * t)
                + 0.25 * math.sin(2.0 * math.pi * (freq * 2.0) * t)
                + 0.10 * math.sin(2.0 * math.pi * (freq * 3.0) * t)
            ) * env * 0.55
            s16 = int(max(-1.0, min(1.0, val)) * 32767.0)
            pcm.extend(struct.pack("<h", s16))

        with wave.open(target_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(bytes(pcm))

    def apply_classic_oof_sound(self, enabled: bool) -> str:
        exe_path = self.find_roblox_player_exe()
        if not exe_path:
            return "Клиент Roblox не найден для замены звука Oof"
        ver_dir = os.path.dirname(exe_path)
        sound_candidates = [
            os.path.join(ver_dir, "content", "sounds", "ouch.ogg"),
            os.path.join(ver_dir, "content", "sounds", "uuhhh.wav"),
        ]
        updated = 0
        for s_path in sound_candidates:
            if os.path.isfile(s_path):
                bak_path = s_path + ".rbxclient_bak"
                try:
                    if enabled:
                        if not os.path.isfile(bak_path):
                            shutil.copy2(s_path, bak_path)
                        self._write_classic_oof_file(s_path)
                        updated += 1
                    else:
                        if os.path.isfile(bak_path):
                            shutil.move(bak_path, s_path)
                            updated += 1
                except Exception:
                    continue
        if updated > 0:
            return "Звук смерти (Oof) обновлён" if enabled else "Стандартный звук смерти восстановлен"
        return "Звук Oof сохранён в параметрах клиента"

    def get_cache_size_mb(self) -> float:
        total = 0
        for folder in (CACHE_DIR, PHOTO_GAMES_DIR):
            if not os.path.isdir(folder):
                continue
            for root, _, files in os.walk(folder):
                for fname in files:
                    fp = os.path.join(root, fname)
                    try:
                        total += os.path.getsize(fp)
                    except Exception:
                        pass
        return round(total / (1024 * 1024), 2)

    def clear_image_cache(self) -> tuple[bool, str]:
        removed = 0
        freed = 0
        if os.path.isdir(CACHE_DIR):
            for fname in os.listdir(CACHE_DIR):
                fp = os.path.join(CACHE_DIR, fname)
                if os.path.isfile(fp):
                    try:
                        freed += os.path.getsize(fp)
                        os.remove(fp)
                        removed += 1
                    except Exception:
                        pass
        mb = round(freed / (1024 * 1024), 2)
        write_launcher_log(f"Очищен кэш картинок: {removed} файлов ({mb} МБ)")
        return True, f"Очищено файлов кэша: {removed} ({mb} МБ)"

    def clear_roblox_shader_and_temp_cache(self) -> tuple[bool, float]:
        """Clear %LOCALAPPDATA%\\Temp\\Roblox and Roblox HTTP/texture/shader caches; return (ok, freed_mb)."""
        freed_bytes = 0
        target_dirs: list[str] = []
        if self._local_app_data:
            target_dirs.extend([
                os.path.join(self._local_app_data, "Temp", "Roblox"),
                os.path.join(self._local_app_data, "Roblox", "http"),
                os.path.join(self._local_app_data, "Roblox", "LocalStorage", "cache"),
            ])
            rbx_root = os.path.join(self._local_app_data, "Roblox")
            if os.path.isdir(rbx_root):
                for entry in os.listdir(rbx_root):
                    low = entry.lower()
                    if "cache" in low or "shader" in low:
                        full_entry = os.path.join(rbx_root, entry)
                        if os.path.isdir(full_entry):
                            target_dirs.append(full_entry)

        seen: set[str] = set()
        for d in target_dirs:
            norm = os.path.abspath(d)
            if norm in seen or not os.path.isdir(norm):
                continue
            seen.add(norm)
            for root, dirs, files in os.walk(norm, topdown=False):
                for fname in files:
                    fp = os.path.join(root, fname)
                    try:
                        sz = os.path.getsize(fp)
                        os.remove(fp)
                        freed_bytes += sz
                    except Exception:
                        pass
                for dname in dirs:
                    dp = os.path.join(root, dname)
                    try:
                        os.rmdir(dp)
                    except Exception:
                        pass

        freed_mb = round(freed_bytes / (1024 * 1024), 2)
        write_launcher_log(f"Clear Roblox Cache: освобождено {freed_mb} МБ")
        return True, freed_mb

    SHADER_BLOCKED_EXT = (".exe", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".msi", ".scr", ".com", ".jar", ".lnk")

    def get_shaders_dir(self) -> str | None:
        exe = self.find_roblox_player_exe()
        if not exe:
            return None
        return os.path.join(os.path.dirname(exe), "shaders")

    def _shader_backup_dir(self, version_name: str) -> str:
        return os.path.join(ASSETS_DIR, "shaders_backup", version_name)

    def _backup_original_shaders(self, target: str) -> None:
        backup = self._shader_backup_dir(os.path.basename(os.path.dirname(target)))
        if os.path.isdir(backup):
            return
        os.makedirs(os.path.dirname(backup), exist_ok=True)
        if os.path.isdir(target):
            shutil.copytree(target, backup)
        else:
            os.makedirs(backup, exist_ok=True)
            with open(os.path.join(backup, ".empty_original"), "w", encoding="utf-8") as f:
                f.write("original shaders folder did not exist\n")

    def install_custom_shaders(self, source_path: str) -> tuple[bool, str]:
        target = self.get_shaders_dir()
        if not target:
            return False, "Roblox не найден: установите Roblox и запустите его хотя бы один раз"
        if not source_path or not os.path.exists(source_path):
            return False, "Источник шейдеров не найден"
        tmp_dir = None
        try:
            self._backup_original_shaders(target)
            src_root = source_path
            if os.path.isfile(source_path):
                if not source_path.lower().endswith(".zip"):
                    return False, "Поддерживаются папки и .zip архивы"
                tmp_dir = tempfile.mkdtemp(prefix="rbx_shaders_")
                with zipfile.ZipFile(source_path) as zf:
                    for info in zf.infolist():
                        name = info.filename.replace("\\", "/")
                        if name.startswith("/") or ".." in name.split("/"):
                            return False, "Архив отклонён RBX Shield: небезопасные пути"
                    zf.extractall(tmp_dir)
                src_root = tmp_dir
            os.makedirs(target, exist_ok=True)
            copied = 0
            skipped = 0
            for root, _dirs, files in os.walk(src_root):
                rel = os.path.relpath(root, src_root)
                dest_dir = target if rel == "." else os.path.join(target, rel)
                os.makedirs(dest_dir, exist_ok=True)
                for fname in files:
                    if fname.lower().endswith(self.SHADER_BLOCKED_EXT):
                        skipped += 1
                        continue
                    shutil.copy2(os.path.join(root, fname), os.path.join(dest_dir, fname))
                    copied += 1
            write_launcher_log(f"Custom Shaders: скопировано {copied}, заблокировано {skipped}")
            note = f", заблокировано исполняемых: {skipped}" if skipped else ""
            return True, f"Шейдеры установлены: {copied} файлов{note}"
        except Exception as exc:
            write_crash_fix_log("install_custom_shaders", exc)
            return False, f"Ошибка установки шейдеров: {exc}"
        finally:
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)

    def reset_custom_shaders(self) -> tuple[bool, str]:
        target = self.get_shaders_dir()
        if not target:
            return False, "Roblox не найден"
        backup = self._shader_backup_dir(os.path.basename(os.path.dirname(target)))
        if not os.path.isdir(backup):
            return False, "Резервной копии нет: пользовательские шейдеры не устанавливались"
        try:
            if os.path.isdir(target):
                shutil.rmtree(target, ignore_errors=True)
            if os.path.isfile(os.path.join(backup, ".empty_original")):
                return True, "Шейдеры сброшены к исходным"
            shutil.copytree(backup, target)
            return True, "Оригинальные шейдеры восстановлены из бэкапа"
        except Exception as exc:
            write_crash_fix_log("reset_custom_shaders", exc)
            return False, f"Ошибка сброса: {exc}"

    def get_latest_rejoin_target_from_logs(self) -> tuple[int | None, str | None]:
        """Read latest gameId / JobId (and placeId if present) from most recent %LOCALAPPDATA%\\Roblox\\logs file."""
        if not self._local_app_data:
            return None, None
        logs_dir = os.path.join(self._local_app_data, "Roblox", "logs")
        if not os.path.isdir(logs_dir):
            return None, None
        try:
            log_files = glob.glob(os.path.join(logs_dir, "*.log"))
            if not log_files:
                return None, None
            log_files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
            for log_path in log_files[:6]:
                try:
                    size = os.path.getsize(log_path)
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                        if size > 3_500_000:
                            f.seek(size - 3_500_000)
                        content = f.read()

                    job_matches = re.findall(
                        r"(?:gameId|jobId|gameInstanceId)\s*[:=]\s*['\"]?([0-9a-fA-F-]{16,64})['\"]?",
                        content,
                        flags=re.IGNORECASE,
                    )
                    place_matches = re.findall(
                        r"(?:placeId|placeid)\s*[:=]\s*(\d+)",
                        content,
                        flags=re.IGNORECASE,
                    )
                    if job_matches:
                        last_job = job_matches[-1].strip()
                        last_place = int(place_matches[-1]) if place_matches else None
                        return last_place, last_job
                except Exception:
                    continue
        except Exception:
            pass
        return None, None

    def open_launcher_logs_folder(self) -> tuple[bool, str]:
        ensure_directories()
        if self._security_guard and not self._security_guard.is_external_executable_allowed(LAUNCHER_LOGS_DIR):
            return False, "Заблокировано RBX Shield"
        try:
            if platform.system().lower() == "windows":
                os.startfile(LAUNCHER_LOGS_DIR)
            else:
                subprocess.Popen(["xdg-open", LAUNCHER_LOGS_DIR])
            return True, f"Открыта папка: {LAUNCHER_LOGS_DIR}"
        except Exception as exc:
            return False, f"Ошибка открытия папки: {exc}"

    def clear_roblox_logs(self) -> tuple[bool, str]:
        if not self._local_app_data:
            return False, "Не найден LOCALAPPDATA"
        logs_dir = os.path.join(self._local_app_data, "Roblox", "logs")
        if not os.path.isdir(logs_dir):
            return True, "Папка логов пуста или отсутствует"
        removed = 0
        freed_bytes = 0
        for entry in glob.glob(os.path.join(logs_dir, "*")):
            try:
                if os.path.isfile(entry):
                    freed_bytes += os.path.getsize(entry)
                    os.remove(entry)
                    removed += 1
            except Exception:
                continue
        mb_freed = round(freed_bytes / (1024 * 1024), 2)
        write_launcher_log(f"Очищены логи Roblox: {removed} файлов ({mb_freed} МБ)")
        return True, f"Удалено файлов: {removed} ({mb_freed} МБ)"

    def register_rbxclient_protocol(self) -> tuple[bool, str]:
        if platform.system().lower() != "windows":
            return False, "Регистрация протокола доступна только в Windows"
        try:
            import winreg
        except ImportError:
            return False, "Модуль winreg недоступен"

        if getattr(sys, "frozen", False):
            target_cmd = f'"{os.path.abspath(sys.executable)}" "%1"'
        else:
            python_exe = sys.executable
            script_path = os.path.abspath(__file__)
            target_cmd = f'"{python_exe}" "{script_path}" "%1"'

        try:
            base_key_path = rf"Software\Classes\{PROTOCOL_SCHEME}"
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, base_key_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, None, 0, winreg.REG_SZ, f"URL:{PROTOCOL_SCHEME} Protocol")
                winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")

            cmd_key_path = rf"{base_key_path}\shell\open\command"
            with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, cmd_key_path, 0, winreg.KEY_WRITE) as cmd_key:
                winreg.SetValueEx(cmd_key, None, 0, winreg.REG_SZ, target_cmd)

            write_launcher_log(f"Зарегистрирован протокол {PROTOCOL_SCHEME}://")
            return True, f"Протокол {PROTOCOL_SCHEME}:// привязан в HKCU"
        except Exception as exc:
            return False, f"Ошибка реестра: {exc}"

    def launch_roblox_game(
        self,
        place_id: int,
        job_id: str | None = None,
        link_code: str | None = None,
        on_status=None,
    ) -> None:
        """
        Launch selected place directly via os.startfile(roblox://placeId=...) with optional
        gameInstanceId or VIP linkCode, validate ClientAppSettings.json beforehand, and apply
        ShowWindow(hwnd, 3) + SetForegroundWindow(hwnd) + F11 strictly to RobloxPlayerBeta.exe.
        """
        cfg = self._get_config()
        auto_f11 = bool(cfg.get("auto_fullscreen_f11", True))
        target_place_id = int(place_id)
        clean_job_id = (job_id or "").strip()
        clean_link_code = (link_code or "").strip()

        def _worker():
            if self._security_guard is not None:
                ok_sec, sec_msg = self._security_guard.run_scan_once()
                if not ok_sec and bool(cfg.get("security_guard_enabled", True)):
                    write_security_incident_log("LAUNCH_BLOCKED", sec_msg)
                    if callable(on_status):
                        on_status(f"Заблокировано RBX Shield: {sec_msg}")
                    return

            self.ensure_valid_client_app_settings()

            proto_url = f"roblox://placeId={target_place_id}"
            if clean_job_id:
                proto_url += f"&gameInstanceId={urllib.parse.quote(clean_job_id)}"
            if clean_link_code:
                proto_url += f"&linkCode={urllib.parse.quote(clean_link_code)}"

            write_launcher_log(f"Прямой запуск: {proto_url}")
            if callable(on_status):
                on_status("Запуск клиента Roblox...")

            protocol_opened = False
            try:
                if platform.system().lower() == "windows":
                    os.startfile(proto_url)
                else:
                    subprocess.Popen(["xdg-open", proto_url])
                protocol_opened = True
            except Exception as exc:
                write_launcher_log(f"Протокол roblox:// не сработал для Place ID={target_place_id}: {exc}")
                write_crash_fix_log("launch_roblox_game.protocol", exc)

            if not protocol_opened:
                web_url = f"https://www.roblox.com/games/{target_place_id}"
                if clean_link_code:
                    web_url += f"?privateServerLinkCode={urllib.parse.quote(clean_link_code)}"
                if callable(on_status):
                    on_status("Клиент не найден, открываю страницу игры в браузере...")
                try:
                    webbrowser.open(web_url)
                    if callable(on_status):
                        on_status("Клиент запущен")
                    return
                except Exception as web_exc:
                    write_crash_fix_log("launch_roblox_game.webbrowser", web_exc)
                    if callable(on_status):
                        on_status(f"Ошибка запуска: {web_exc}")
                    return

            if auto_f11 and platform.system().lower() == "windows":
                for _ in range(30):
                    time.sleep(0.5)
                    hwnd = self._find_roblox_player_beta_hwnd()
                    if hwnd:
                        time.sleep(0.8)
                        self._focus_and_send_f11_to_player_beta(hwnd)
                        break

            if callable(on_status):
                on_status("Клиент запущен")

        threading.Thread(target=_worker, daemon=True).start()

    def launch_roblox_place(self, place_id: int, job_id: str | None = None, on_status=None) -> None:
        self.launch_roblox_game(place_id=place_id, job_id=job_id, link_code=None, on_status=on_status)

    def _get_process_module_base_name_windows(self, pid: int) -> str:
        """Resolve executable base name for a given Windows PID using OpenProcess + GetModuleBaseNameW."""
        if platform.system().lower() != "windows" or pid <= 0:
            return ""
        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi
        h_proc = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        if not h_proc:
            return ""
        try:
            buf = ctypes.create_unicode_buffer(260)
            copied = psapi.GetModuleBaseNameW(h_proc, None, buf, 260)
            if copied > 0:
                return os.path.basename(buf.value).lower()
            return ""
        except Exception:
            return ""
        finally:
            try:
                kernel32.CloseHandle(h_proc)
            except Exception:
                pass

    def _find_roblox_player_beta_hwnd(self) -> int:
        """Find visible window HWND strictly owned by RobloxPlayerBeta.exe."""
        if platform.system().lower() != "windows":
            return 0
        try:
            user32 = ctypes.windll.user32
            found_hwnd = 0
            WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

            def _enum_cb(hwnd, _lparam):
                nonlocal found_hwnd
                if not user32.IsWindowVisible(hwnd):
                    return True
                pid = ctypes.c_ulong(0)
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if pid.value > 0:
                    exe_name = self._get_process_module_base_name_windows(int(pid.value))
                    if exe_name == "robloxplayerbeta.exe":
                        found_hwnd = int(hwnd)
                        return False
                return True

            user32.EnumWindows(WNDENUMPROC(_enum_cb), 0)
            return found_hwnd
        except Exception:
            return 0

    def _focus_and_send_f11_to_player_beta(self, hwnd: int) -> None:
        """Apply ShowWindow(hwnd, 3) + SetForegroundWindow(hwnd) + F11 strictly if HWND belongs to RobloxPlayerBeta.exe."""
        if platform.system().lower() != "windows" or not hwnd:
            return
        try:
            user32 = ctypes.windll.user32
            pid = ctypes.c_ulong(0)
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            exe_name = self._get_process_module_base_name_windows(int(pid.value))
            if exe_name != "robloxplayerbeta.exe":
                return

            user32.ShowWindow(hwnd, SW_MAXIMIZE)
            user32.SetForegroundWindow(hwnd)
            time.sleep(0.15)
            VK_F11 = 0x7A
            KEYEVENTF_KEYUP = 0x0002
            user32.keybd_event(VK_F11, 0, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(VK_F11, 0, KEYEVENTF_KEYUP, 0)
        except Exception:
            pass

    def _find_roblox_window_hwnd(self) -> int:
        return self._find_roblox_player_beta_hwnd()

    def _focus_and_send_f11(self, hwnd: int) -> None:
        self._focus_and_send_f11_to_player_beta(hwnd)


class FpsPingGameOverlay(ctk.CTkToplevel):
    """Smart FPS Cap & Ping overlay shown strictly when enabled in Settings AND RobloxPlayerBeta.exe is running."""

    def __init__(self, parent, config_getter) -> None:
        super().__init__(parent)
        self._get_config = config_getter
        self._closed = False
        self._after_id = None

        self.overrideredirect(True)
        try:
            self.attributes("-topmost", True)
            self.attributes("-alpha", 0.90)
        except Exception:
            pass
        self.configure(fg_color=COLOR_SURFACE)
        self.geometry("+24+24")

        self.lbl_metric = ctk.CTkLabel(
            self,
            text="FPS Cap: 144  •  Ping: -- ms",
            font=("Consolas", 12, "bold"),
            text_color=COLOR_TEXT,
        )
        self.lbl_metric.pack(padx=12, pady=6)
        self._tick()

    def _measure_ping_ms(self) -> str:
        try:
            t0 = time.perf_counter()
            requests.head("https://www.roblox.com", timeout=1.2)
            dt_ms = int((time.perf_counter() - t0) * 1000)
            return f"{max(1, dt_ms)} ms"
        except Exception:
            return "-- ms"

    def _tick(self) -> None:
        if self._closed:
            return
        try:
            if not self.winfo_exists():
                return
            cfg = self._get_config() if callable(self._get_config) else {}
            enabled = bool(cfg.get("show_fps_ping_overlay", False))
            if not enabled or not ROBLOX_WATCHER.running:
                self.close_overlay()
                return
            fps_cap = int(cfg.get("fps_cap", 144))

            def _ping_worker():
                p_str = self._measure_ping_ms()
                if not self._closed and self.winfo_exists():
                    try:
                        self.after(0, lambda ps=p_str, fc=fps_cap: self.lbl_metric.configure(text=f"FPS Cap: {fc}  •  Ping: {ps}") if self.winfo_exists() else None)
                    except Exception:
                        pass

            threading.Thread(target=_ping_worker, daemon=True).start()
            self._after_id = self.after(2000, self._tick)
        except Exception:
            self.close_overlay()

    def close_overlay(self) -> None:
        self._closed = True
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        try:
            if self.winfo_exists():
                self.destroy()
        except Exception:
            pass


class RBXClientApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.config_data: dict = load_json_safe(CONFIG_PATH, DEFAULT_CONFIG)
        self.favorites: list[dict] = load_json_safe(FAVORITES_PATH, [])
        self.is_first_run: bool = not os.path.isfile(INSTALLED_FLAG_PATH)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(f"RBX Client {CURRENT_VERSION}")
        self.overrideredirect(True)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        initial_alpha = float(self.config_data.get("window_alpha", APP_ALPHA))
        try:
            self.attributes("-alpha", max(0.78, min(1.0, initial_alpha)))
        except Exception:
            pass

        self._center_on_screen()

        if os.path.isfile(ICON_PATH):
            try:
                self.iconbitmap(ICON_PATH)
            except Exception:
                pass

        self.taskbar = WindowsTaskbarHelper()
        self.sound = SoundEngine(lambda: self.config_data)
        self.security_guard = LauncherSecurityGuard(lambda: self.config_data)
        self.api = RobloxApiClient(security_guard=self.security_guard)
        self.account_detector = LocalAccountDetector()
        self.sys_manager = RobloxSystemManager(
            self.sound,
            lambda: self.config_data,
            security_guard=self.security_guard,
        )
        self.self_heal = SelfHealEngine(
            client_settings_path_getter=self.sys_manager.get_client_settings_path,
            config_getter=lambda: self.config_data,
            config_setter=lambda new_cfg: setattr(self, "config_data", new_cfg),
            security_guard=self.security_guard,
        )
        self.report_callback_exception = self._on_tk_callback_exception

        self._drag_x = 0
        self._drag_y = 0
        self._active_tab = "launcher"
        self._has_user_selected_game = False
        default_pid = int(self.config_data.get("last_place_id", 2753915549))
        self._current_game: dict = {
            "place_id": default_pid,
            "placeId": default_pid,
            "universe_id": 994732206,
            "name": "Blox Fruits",
            "creator": "Gamer Robot Inc",
            "playing": 420000,
            "link_code": "",
        }
        self._banner_ctk_image: ctk.CTkImage | None = None
        self._fav_icon_images: dict[int, ctk.CTkImage] = {}
        self._profile_avatar_image: ctk.CTkImage | None = None
        self._friend_avatar_images: dict[int, ctk.CTkImage] = {}
        self._search_card_images: dict[int, ctk.CTkImage] = {}
        self._search_row_widgets: dict[int, dict] = {}
        self._search_games_cache: list[dict] = []
        self._search_auto_refresh_enabled = True
        self._search_refresh_thread: threading.Thread | None = None
        self._search_stop_event = threading.Event()
        self._profile_hidden = False
        self._current_profile_data: dict | None = None
        self._detected_user_id: int | None = None
        self._servers_list: list[dict] = []
        self._connect_overlay: ctk.CTkFrame | None = None
        self._connect_splash_canvas: SplashOverlay | None = None
        self._consent_overlay: SecurityConsentOverlay | None = None
        self._fps_ping_overlay: FpsPingGameOverlay | None = None
        self._overlay_monitor_after_id = None
        self._toast_after_id = None

        self._build_main_shell()
        self._show_welcome_banner()
        self._apply_language(str(self.config_data.get("language", "ru")))
        self.after(20, self._open_splash_immediately)
        self.after(120, self._finalize_window_taskbar_and_bg_tasks)

    def _tr(self, key: str) -> str:
        lang = str(self.config_data.get("language", "ru")).lower()
        table = UI_TRANSLATIONS.get(lang) or UI_TRANSLATIONS["en"]
        return table.get(key) or UI_TRANSLATIONS["en"].get(key, key)

    def _apply_language(self, lang_code: str) -> None:
        code = lang_code if lang_code in UI_TRANSLATIONS else "ru"
        self.config_data["language"] = code
        self._save_config()

        if hasattr(self, "title_lbl") and self.title_lbl.winfo_exists():
            self.title_lbl.configure(text=f"{self._tr('window_title')} v{CURRENT_VERSION} by {PUBLISHER_NAME}")
        if hasattr(self, "nav_buttons"):
            mapping = {
                "launcher": ("▶", self._tr("nav_launcher")),
                "search": ("⌕", self._tr("nav_search")),
                "servers": ("☷", self._tr("nav_servers")),
                "profile": ("☺", self._tr("nav_profile")),
                "ai": ("✦", self._tr("nav_ai")),
                "settings": ("⚙", self._tr("nav_settings")),
            }
            for k, (ic, lbl) in mapping.items():
                if k in self.nav_buttons and self.nav_buttons[k].winfo_exists():
                    self.nav_buttons[k].configure(text=f"{ic}   {lbl}")
        if hasattr(self, "btn_load_place") and self.btn_load_place.winfo_exists():
            self.btn_load_place.configure(text=self._tr("load"))
        if hasattr(self, "btn_copy_link") and self.btn_copy_link.winfo_exists():
            self.btn_copy_link.configure(text=self._tr("copy_link"))
        if hasattr(self, "btn_rejoin_server") and self.btn_rejoin_server.winfo_exists():
            self.btn_rejoin_server.configure(text=self._tr("rejoin"))
        if hasattr(self, "btn_play_main") and self.btn_play_main.winfo_exists():
            self.btn_play_main.configure(text=self._tr("play"))
        if hasattr(self, "btn_clear_roblox_cache") and self.btn_clear_roblox_cache.winfo_exists():
            self.btn_clear_roblox_cache.configure(text=self._tr("clear_roblox_cache"))
        self._refresh_security_guard_ui()

    def _on_tk_callback_exception(self, exc_type, exc_value, exc_tb) -> None:
        write_crash_fix_log("TkCallback", f"{exc_type.__name__}: {exc_value}")
        write_launcher_log(f"[SelfHeal] Перехвачен сбой виджета/коллбэка: {exc_value}")
        try:
            if hasattr(self, "self_heal"):
                self.self_heal.fixes_applied_count += 1
            self._refresh_self_heal_ui()
        except Exception:
            pass

    def _center_on_screen(self) -> None:
        self.update_idletasks()
        sw, sh = get_primary_screen_size(self)
        try:
            scale = float(ctk.ScalingTracker.get_window_scaling(self))
            scaled_ok = True
        except Exception:
            scale = 1.0
            scaled_ok = False
        w = int(round(APP_WIDTH * scale))
        h = int(round(APP_HEIGHT * scale))
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        try:
            if not scaled_ok:
                raise RuntimeError("no scaling info")
            # Реальные пиксели напрямую в Tk: CTk не масштабирует смещение x/y, из-за чего окно уезжало вправо-вниз.
            tkinter.Tk.geometry(self, f"{w}x{h}+{x}+{y}")
        except Exception:
            self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")
        self.update_idletasks()

    def _center_window(self) -> None:
        self._center_on_screen()

    def _save_config(self) -> None:
        save_json_safe(CONFIG_PATH, self.config_data)

    def _save_favorites(self) -> None:
        save_json_safe(FAVORITES_PATH, self.favorites)

    def _copy_text_to_clipboard(self, text: str, toast_msg: str | None = None) -> None:
        if not text:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update_idletasks()
        except Exception as exc:
            write_crash_fix_log("clipboard", exc)
        if toast_msg:
            self._show_toast(toast_msg)

    def _show_toast(self, message: str, duration_ms: int = 2600) -> None:
        if not bool(self.config_data.get("show_toasts", True)):
            return
        try:
            if not hasattr(self, "toast_frame") or not self.toast_frame.winfo_exists():
                return
            if self._toast_after_id is not None:
                try:
                    self.after_cancel(self._toast_after_id)
                except Exception:
                    pass
                self._toast_after_id = None
            self.toast_label.configure(text=message)
            self.toast_frame.place(relx=0.5, rely=0.93, anchor="center")
            self.toast_frame.lift()
            self._toast_after_id = self.after(duration_ms, self._hide_toast)
        except Exception:
            pass

    def _hide_toast(self) -> None:
        self._toast_after_id = None
        try:
            if hasattr(self, "toast_frame") and self.toast_frame.winfo_exists():
                self.toast_frame.place_forget()
        except Exception:
            pass

    def _open_splash_immediately(self) -> None:
        self.sound.play_startup_loop()
        self.update_idletasks()
        cur_w = max(APP_WIDTH, int(self.winfo_width() or APP_WIDTH))
        cur_h = max(APP_HEIGHT, int(self.winfo_height() or APP_HEIGHT))
        self.splash = SplashOverlay(
            self,
            width=cur_w,
            height=cur_h,
            is_first_run=self.is_first_run,
            on_complete=self._on_splash_finished,
            show_status_text=True,
        )
        self.splash.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        self.splash.lift()

        def _diag_worker():
            self.self_heal.run_startup_diagnostics(
                status_callback=lambda msg: self.after(
                    0,
                    lambda m=msg: self.splash.set_status_message(m)
                    if hasattr(self, "splash") and self.splash.winfo_exists()
                    else None,
                )
            )
            self.security_guard.run_scan_once()
            self.after(0, self._refresh_self_heal_ui)
            self.after(0, self._refresh_security_guard_ui)

        threading.Thread(target=_diag_worker, daemon=True).start()

    def _on_splash_finished(self) -> None:
        self.sound.stop_sound()
        if self.is_first_run:
            try:
                with open(INSTALLED_FLAG_PATH, "w", encoding="utf-8") as f:
                    f.write(f"installed_version={CURRENT_VERSION}\n")
                self.is_first_run = False
            except Exception:
                pass
        if hasattr(self, "splash") and self.splash.winfo_exists():
            self.splash.destroy()
        self.taskbar.apply_taskbar_style(self)

        if not os.path.isfile(TERMS_FLAG_PATH):
            self._open_security_consent_screen(closable=False)

    def _open_security_consent_screen(self, closable: bool = False) -> None:
        if self._consent_overlay is not None and self._consent_overlay.winfo_exists():
            self._consent_overlay.lift()
            return

        def _accept_terms() -> None:
            try:
                os.makedirs(ASSETS_DIR, exist_ok=True)
                with open(TERMS_FLAG_PATH, "w", encoding="utf-8") as f:
                    f.write(f"accepted_version={CURRENT_VERSION};publisher={PUBLISHER_NAME}\n")
            except Exception as exc:
                write_crash_fix_log("save_terms_flag", exc)
            if self._consent_overlay is not None and self._consent_overlay.winfo_exists():
                self._consent_overlay.destroy()
            self._consent_overlay = None
            self._show_toast("Условия приняты. Добро пожаловать в RBX Client")

        overlay = SecurityConsentOverlay(
            self,
            on_accept=_accept_terms,
            sound_engine=self.sound,
            closable=closable,
        )
        overlay.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        overlay.lift()
        self._consent_overlay = overlay

    def _show_welcome_banner(self) -> None:
        if hasattr(self, "banner_img_label") and self.banner_img_label.winfo_exists():
            self._banner_ctk_image = build_welcome_banner_image((660, 371))
            self.banner_img_label.configure(image=self._banner_ctk_image, text="")

    def _finalize_window_taskbar_and_bg_tasks(self) -> None:
        self.taskbar.apply_taskbar_style(self)
        if not self._has_user_selected_game:
            self._show_welcome_banner()
        self._render_favorites_list()
        self._start_auto_profile_detection()
        self._start_search_background_loop()
        self.security_guard.start_background_loop(
            interval_sec=15.0,
            on_update=lambda _ok, _summary: self.after(0, self._refresh_security_guard_ui),
        )
        ROBLOX_WATCHER.start()
        self._monitor_game_overlay_loop()

    def _monitor_game_overlay_loop(self) -> None:
        """Show FPS & Ping overlay ONLY when enabled in Settings AND RobloxPlayerBeta.exe is running."""
        try:
            enabled = bool(self.config_data.get("show_fps_ping_overlay", False))
            running = ROBLOX_WATCHER.running
            if enabled and running:
                if self._fps_ping_overlay is None or not self._fps_ping_overlay.winfo_exists():
                    self._fps_ping_overlay = FpsPingGameOverlay(self, lambda: self.config_data)
            else:
                if self._fps_ping_overlay is not None:
                    self._fps_ping_overlay.close_overlay()
                    self._fps_ping_overlay = None
        except Exception:
            pass
        self._overlay_monitor_after_id = self.after(1500, self._monitor_game_overlay_loop)

    def _build_main_shell(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_bar = ctk.CTkFrame(
            self,
            height=42,
            fg_color=COLOR_SURFACE,
            corner_radius=0,
            border_width=0,
        )
        self.title_bar.grid(row=0, column=0, sticky="ew")
        self.title_bar.grid_propagate(False)
        self.title_bar.bind("<ButtonPress-1>", self._on_title_drag_start)
        self.title_bar.bind("<B1-Motion>", self._on_title_drag_motion)

        self.title_logo = ctk.CTkLabel(
            self.title_bar,
            text="RX",
            width=28,
            height=24,
            corner_radius=7,
            fg_color=COLOR_ACCENT,
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
        )
        self.title_logo.pack(side="left", padx=(14, 0))
        self.title_logo.bind("<ButtonPress-1>", self._on_title_drag_start)
        self.title_logo.bind("<B1-Motion>", self._on_title_drag_motion)

        self.title_lbl = ctk.CTkLabel(
            self.title_bar,
            text=f"{self._tr('window_title')} v{CURRENT_VERSION} by {PUBLISHER_NAME}",
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXT,
        )
        self.title_lbl.pack(side="left", padx=(10, 12))
        self.title_lbl.bind("<ButtonPress-1>", self._on_title_drag_start)
        self.title_lbl.bind("<B1-Motion>", self._on_title_drag_motion)

        self.title_shield_lbl = ctk.CTkLabel(
            self.title_bar,
            text="●  RBX Shield: Protected",
            font=("Segoe UI", 11, "bold"),
            text_color=COLOR_SUCCESS,
        )
        self.title_shield_lbl.pack(side="left", padx=(0, 8))
        self.title_shield_lbl.bind("<ButtonPress-1>", self._on_title_drag_start)
        self.title_shield_lbl.bind("<B1-Motion>", self._on_title_drag_motion)

        win_controls = ctk.CTkFrame(self.title_bar, fg_color="transparent", border_width=0, height=42)
        win_controls.pack(side="right", padx=8, pady=0)
        win_controls.pack_propagate(True)

        btn_min = ctk.CTkButton(
            win_controls,
            text="—",
            width=34,
            height=28,
            corner_radius=6,
            border_width=0,
            fg_color="transparent",
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT_MUTED,
            font=("Segoe UI", 12, "bold"),
            command=self._on_minimize_click,
        )
        btn_min.pack(side="left", padx=2, pady=7)

        btn_close = ctk.CTkButton(
            win_controls,
            text="✕",
            width=34,
            height=28,
            corner_radius=6,
            border_width=0,
            fg_color="transparent",
            hover_color=COLOR_DANGER,
            text_color=COLOR_TEXT_MUTED,
            font=("Segoe UI", 12, "bold"),
            command=self._on_close_click,
        )
        btn_close.pack(side="left", padx=2, pady=7)

        self.body_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_BG,
            corner_radius=0,
            border_width=0,
        )
        self.body_frame.grid(row=1, column=0, sticky="nsew")
        self.body_frame.grid_columnconfigure(1, weight=1)
        self.body_frame.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self.body_frame,
            width=210,
            fg_color=COLOR_SURFACE,
            corner_radius=0,
            border_width=0,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.nav_indicators: dict[str, ctk.CTkFrame] = {}
        ctk.CTkLabel(
            self.sidebar,
            text="МЕНЮ",
            font=("Segoe UI", 10, "bold"),
            text_color=COLOR_TEXT_DIM,
            anchor="w",
        ).pack(fill="x", padx=20, pady=(18, 4))
        nav_items = [
            ("launcher", "▶", self._tr("nav_launcher")),
            ("search", "⌕", self._tr("nav_search")),
            ("servers", "☷", self._tr("nav_servers")),
            ("profile", "☺", self._tr("nav_profile")),
            ("ai", "✦", self._tr("nav_ai")),
            ("settings", "⚙", self._tr("nav_settings")),
        ]
        for tab_key, tab_icon, tab_label in nav_items:
            row = ctk.CTkFrame(self.sidebar, fg_color="transparent", border_width=0, height=42)
            row.pack(fill="x", padx=(8, 12), pady=2)
            row.pack_propagate(False)
            ind = ctk.CTkFrame(
                row,
                width=3,
                corner_radius=2,
                fg_color=COLOR_ACCENT if tab_key == "launcher" else "transparent",
                border_width=0,
            )
            ind.pack(side="left", fill="y", pady=8)
            btn = ctk.CTkButton(
                row,
                text=f"{tab_icon}   {tab_label}",
                height=38,
                corner_radius=8,
                border_width=0,
                anchor="w",
                fg_color=COLOR_SURFACE_ALT if tab_key == "launcher" else "transparent",
                hover_color=COLOR_SURFACE_HOVER,
                text_color=COLOR_TEXT if tab_key == "launcher" else COLOR_TEXT_MUTED,
                font=("Segoe UI", 13, "bold" if tab_key == "launcher" else "normal"),
                command=lambda k=tab_key: self._switch_tab(k),
            )
            btn.pack(side="left", fill="x", expand=True, padx=(6, 0))
            self.nav_buttons[tab_key] = btn
            self.nav_indicators[tab_key] = ind

        ctk.CTkLabel(
            self.sidebar,
            text=f"v{CURRENT_VERSION}  •  {PUBLISHER_NAME}",
            font=("Segoe UI", 10),
            text_color=COLOR_TEXT_DIM,
        ).pack(side="bottom", pady=14)

        self.content_container = ctk.CTkFrame(
            self.body_frame,
            fg_color=COLOR_BG,
            corner_radius=0,
            border_width=0,
        )
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.tab_frames: dict[str, ctk.CTkFrame] = {}
        for tab_key in ("launcher", "profile", "search", "servers", "ai", "settings"):
            f = ctk.CTkFrame(self.content_container, fg_color=COLOR_BG, corner_radius=0, border_width=0)
            f.grid(row=0, column=0, sticky="nsew")
            self.tab_frames[tab_key] = f

        self._build_launcher_tab()
        self._build_profile_tab()
        self._build_search_tab()
        self._build_servers_tab()
        self._build_ai_tab()
        self._build_settings_tab()

        self.toast_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_SURFACE_ALT,
            corner_radius=10,
            border_width=0,
        )
        self.toast_label = ctk.CTkLabel(
            self.toast_frame,
            text="",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
        )
        self.toast_label.pack(padx=18, pady=9)

        self._switch_tab("launcher")

    def _on_title_drag_start(self, event) -> None:
        self._drag_x = event.x_root - self.winfo_x()
        self._drag_y = event.y_root - self.winfo_y()

    def _on_title_drag_motion(self, event) -> None:
        nx = event.x_root - self._drag_x
        ny = event.y_root - self._drag_y
        self.geometry(f"+{nx}+{ny}")

    def _on_minimize_click(self) -> None:
        self.sound.play_click()
        self.taskbar.minimize_window(self)

    def _on_close_click(self) -> None:
        self.sound.play_click()
        self._search_stop_event.set()
        self.security_guard.stop()
        if self._fps_ping_overlay is not None:
            self._fps_ping_overlay.close_overlay()
            self._fps_ping_overlay = None
        self.sound.stop_sound()
        ROBLOX_WATCHER.stop()
        self._save_config()
        self._save_favorites()
        self.destroy()

    def _switch_tab(self, tab_key: str) -> None:
        self.sound.play_click()
        self._active_tab = tab_key
        for key, btn in self.nav_buttons.items():
            active = key == tab_key
            btn.configure(
                fg_color=COLOR_SURFACE_ALT if active else "transparent",
                hover_color=COLOR_SURFACE_HOVER,
                text_color=COLOR_TEXT if active else COLOR_TEXT_MUTED,
                font=("Segoe UI", 13, "bold" if active else "normal"),
            )
            ind = self.nav_indicators.get(key)
            if ind is not None:
                ind.configure(fg_color=COLOR_ACCENT if active else "transparent")
        target_frame = self.tab_frames.get(tab_key)
        if target_frame is not None:
            target_frame.tkraise()

        if tab_key == "servers":
            if time.time() - getattr(self, "_servers_last_refresh", 0.0) > 15.0:
                self._servers_last_refresh = time.time()
                self._refresh_servers_list()
        elif tab_key == "search":
            sig = tuple((g.get("place_id"), g.get("playing")) for g in self._search_games_cache)
            if sig != getattr(self, "_search_render_sig", None):
                self._search_render_sig = sig
                self._render_search_results(self._search_games_cache)
        elif tab_key == "settings":
            self._animate_settings_open()

    def _build_launcher_tab(self) -> None:
        parent = self.tab_frames["launcher"]
        parent.grid_columnconfigure(0, weight=3)
        parent.grid_columnconfigure(1, weight=2)
        parent.grid_rowconfigure(0, weight=1)

        left_col = ctk.CTkFrame(parent, fg_color="transparent", border_width=0)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(18, 10), pady=16)
        left_col.grid_columnconfigure(0, weight=1)

        self.banner_card = ctk.CTkFrame(
            left_col,
            fg_color=COLOR_SURFACE,
            corner_radius=12,
            border_width=0,
        )
        self.banner_card.grid(row=0, column=0, sticky="ew")

        self.banner_img_label = ctk.CTkLabel(
            self.banner_card,
            text="",
            width=660,
            height=371,
            corner_radius=12,
        )
        self.banner_img_label.pack(fill="both", expand=True)

        input_row = ctk.CTkFrame(left_col, fg_color="transparent", border_width=0)
        input_row.grid(row=1, column=0, sticky="ew", pady=(14, 12))
        input_row.grid_columnconfigure(0, weight=1)

        self.entry_place_id = ctk.CTkEntry(
            input_row,
            height=42,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE,
            text_color=COLOR_TEXT,
            placeholder_text="Place ID или ссылка roblox.com/games/... (?privateServerLinkCode=...)",
            font=("Segoe UI", 13),
        )
        self.entry_place_id.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.entry_place_id.insert(0, str(self._current_game.get("placeId") or self._current_game.get("place_id") or ""))
        self.entry_place_id.bind("<Return>", lambda _e: self._on_load_place_clicked())

        self.btn_load_place = ctk.CTkButton(
            input_row,
            text=self._tr("load"),
            width=96,
            height=42,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12, "bold"),
            command=self._on_load_place_clicked,
        )
        self.btn_load_place.grid(row=0, column=1, padx=(0, 6))

        self.btn_copy_link = ctk.CTkButton(
            input_row,
            text=self._tr("copy_link"),
            width=96,
            height=42,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_ACCENT,
            font=("Segoe UI", 12, "bold"),
            command=self._on_copy_current_game_link,
        )
        self.btn_copy_link.grid(row=0, column=2, padx=(0, 6))

        self.btn_fav_toggle = ctk.CTkButton(
            input_row,
            text="☆",
            width=46,
            height=42,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 14, "bold"),
            command=self._on_toggle_favorite_clicked,
        )
        self.btn_fav_toggle.grid(row=0, column=3)

        action_row = ctk.CTkFrame(left_col, fg_color="transparent", border_width=0)
        action_row.grid(row=2, column=0, sticky="ew")
        action_row.grid_columnconfigure(0, weight=1)

        self.btn_play_main = ctk.CTkButton(
            action_row,
            text=self._tr("play"),
            height=52,
            corner_radius=12,
            border_width=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=("Segoe UI", 16, "bold"),
            command=self._on_play_button_clicked,
        )
        self.btn_play_main.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.btn_rejoin_server = ctk.CTkButton(
            action_row,
            text=self._tr("rejoin"),
            width=108,
            height=52,
            corner_radius=12,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 13, "bold"),
            command=self._on_rejoin_clicked,
        )
        self.btn_rejoin_server.grid(row=0, column=1)

        right_col = ctk.CTkFrame(
            parent,
            fg_color=COLOR_SURFACE,
            corner_radius=12,
            border_width=0,
        )
        right_col.grid(row=0, column=1, sticky="nsew", padx=(8, 18), pady=16)
        right_col.grid_columnconfigure(0, weight=1)
        right_col.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            right_col,
            text="Избранное",
            font=("Segoe UI", 15, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))

        self.fav_scroll = ctk.CTkScrollableFrame(
            right_col,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        self.fav_scroll.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 10))
        self.fav_scroll.grid_columnconfigure(0, weight=1)

    def _get_current_place_and_link_code(self) -> tuple[int, str, str]:
        raw_val = ""
        if hasattr(self, "entry_place_id") and self.entry_place_id.winfo_exists():
            raw_val = self.entry_place_id.get().strip()
        fallback_pid = int(
            (self._current_game or {}).get("placeId")
            or (self._current_game or {}).get("place_id")
            or self.config_data.get("last_place_id")
            or 2753915549
        )
        parsed = parse_roblox_game_input(raw_val, default_place_id=fallback_pid)
        return parsed["place_id"], parsed["link_code"], parsed["job_id"]

    def _on_copy_current_game_link(self) -> None:
        self.sound.play_click()
        pid, link_code, _ = self._get_current_place_and_link_code()
        url = f"https://www.roblox.com/games/{pid}"
        if link_code:
            url += f"?privateServerLinkCode={urllib.parse.quote(link_code)}"
        self._copy_text_to_clipboard(url, f"Ссылка скопирована: {url}")

    def _on_rejoin_clicked(self) -> None:
        self.sound.play_click()
        cur_pid, _, _ = self._get_current_place_and_link_code()

        def _worker():
            log_pid, log_job = self.sys_manager.get_latest_rejoin_target_from_logs()
            target_pid = int(log_pid or cur_pid or 2753915549)
            if not log_job:
                self.after(0, lambda: self._show_toast("Не найден последний JobId в логах Roblox"))
                return
            self.after(
                0,
                lambda p=target_pid, j=log_job: self._launch_specific_place_id(p, job_id=j),
            )

        threading.Thread(target=_worker, daemon=True).start()

    def _update_favorite_button_state(self, place_id: int) -> None:
        exists = any(int(item.get("place_id") or item.get("placeId") or 0) == int(place_id) for item in self.favorites)
        if exists:
            self.btn_fav_toggle.configure(text="★", fg_color=COLOR_SURFACE_HOVER, text_color=COLOR_WARNING)
        else:
            self.btn_fav_toggle.configure(text="☆", fg_color=COLOR_SURFACE_ALT, text_color=COLOR_TEXT)

    def _on_toggle_favorite_clicked(self) -> None:
        self.sound.play_click()
        pid, _, _ = self._get_current_place_and_link_code()
        if pid <= 0:
            return

        idx_found = None
        for idx, item in enumerate(self.favorites):
            if int(item.get("place_id") or item.get("placeId") or 0) == pid:
                idx_found = idx
                break

        if idx_found is not None:
            self.favorites.pop(idx_found)
            self._save_favorites()
            self._update_favorite_button_state(pid)
            self._render_favorites_list()
            self._show_toast(f"Удалено из избранного: {pid}")
            return

        info = dict(self._current_game) if int(self._current_game.get("placeId") or self._current_game.get("place_id") or 0) == pid else {}
        entry = {
            "place_id": pid,
            "placeId": pid,
            "universe_id": int(info.get("universe_id") or 0),
            "name": str(info.get("name") or f"Place #{pid}"),
            "creator": str(info.get("creator") or "Roblox"),
            "playing": int(info.get("playing") or 0),
        }
        self.favorites.insert(0, entry)
        self._save_favorites()
        self._update_favorite_button_state(pid)
        self._render_favorites_list()
        self._show_toast(f"Добавлено в избранное: {entry['name']}")

        def _enrich_fav():
            full = self.api.get_game_info_by_place(pid)
            for item in self.favorites:
                if int(item.get("place_id") or item.get("placeId") or 0) == pid:
                    item["universe_id"] = full.get("universe_id", item.get("universe_id", 0))
                    item["name"] = full.get("name", item.get("name"))
                    item["creator"] = full.get("creator", item.get("creator"))
                    item["playing"] = full.get("playing", item.get("playing", 0))
            self._save_favorites()
            self.after(0, self._render_favorites_list)

        threading.Thread(target=_enrich_fav, daemon=True).start()

    def _render_favorites_list(self) -> None:
        if not hasattr(self, "fav_scroll") or not self.fav_scroll.winfo_exists():
            return
        for child in self.fav_scroll.winfo_children():
            child.destroy()

        if not self.favorites:
            ctk.CTkLabel(
                self.fav_scroll,
                text="Список избранного пуст.\nДобавьте игру через кнопку «☆».",
                font=("Segoe UI", 12),
                text_color=COLOR_TEXT_MUTED,
                justify="center",
            ).pack(pady=36)
            return

        for item in self.favorites:
            pid = int(item.get("place_id") or item.get("placeId") or 0)
            uid = int(item.get("universe_id") or 0)
            name = str(item.get("name") or f"Place #{pid}")
            playing = int(item.get("playing") or 0)

            row = ctk.CTkFrame(
                self.fav_scroll,
                fg_color=COLOR_SURFACE_ALT,
                corner_radius=10,
                border_width=0,
            )
            row.pack(fill="x", padx=4, pady=4)
            row.grid_columnconfigure(1, weight=1)

            icon_lbl = ctk.CTkLabel(row, text="", width=42, height=42, corner_radius=8)
            icon_lbl.grid(row=0, column=0, padx=(8, 8), pady=8)
            if pid in self._fav_icon_images:
                icon_lbl.configure(image=self._fav_icon_images[pid])
            else:
                self._load_fav_icon_async(pid, uid, icon_lbl)

            info_box = ctk.CTkFrame(row, fg_color="transparent", border_width=0)
            info_box.grid(row=0, column=1, sticky="ew", pady=6)
            info_box.grid_columnconfigure(0, weight=1)

            lbl_name = ctk.CTkLabel(
                info_box,
                text=name,
                font=("Segoe UI", 12, "bold"),
                text_color=COLOR_TEXT,
                anchor="w",
            )
            lbl_name.grid(row=0, column=0, sticky="ew")

            lbl_sub = ctk.CTkLabel(
                info_box,
                text=f"ID: {pid}  •  Онлайн: {format_number(playing)}",
                font=("Segoe UI", 11),
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
            )
            lbl_sub.grid(row=1, column=0, sticky="ew")

            btn_launch = ctk.CTkButton(
                row,
                text="▶",
                width=34,
                height=34,
                corner_radius=8,
                border_width=0,
                fg_color=COLOR_ACCENT,
                hover_color=COLOR_ACCENT_HOVER,
                text_color="#FFFFFF",
                font=("Segoe UI", 12, "bold"),
                command=lambda p=pid: self._launch_specific_place_id(p),
            )
            btn_launch.grid(row=0, column=2, padx=(4, 4))

            btn_del = ctk.CTkButton(
                row,
                text="✕",
                width=30,
                height=34,
                corner_radius=8,
                border_width=0,
                fg_color="transparent",
                hover_color=COLOR_DANGER,
                text_color=COLOR_TEXT_MUTED,
                font=("Segoe UI", 12, "bold"),
                command=lambda p=pid: self._remove_favorite_by_id(p),
            )
            btn_del.grid(row=0, column=3, padx=(0, 8))

            for w in (row, info_box, lbl_name, lbl_sub):
                w.bind("<Button-1>", lambda _e, p=pid: self._load_game_into_launcher(p))

    def _remove_favorite_by_id(self, place_id: int) -> None:
        self.sound.play_click()
        self.favorites = [
            x for x in self.favorites if int(x.get("place_id") or x.get("placeId") or 0) != int(place_id)
        ]
        self._save_favorites()
        self._update_favorite_button_state(place_id)
        self._render_favorites_list()

    def _load_fav_icon_async(self, place_id: int, universe_id: int, target_label: ctk.CTkLabel) -> None:
        cached_im = self._fav_icon_images.get(place_id)
        if cached_im is not None:
            target_label.configure(image=cached_im)
            return

        def _worker():
            uid = universe_id
            if not uid:
                uid = self.api.resolve_universe_from_place(place_id) or 0
                if uid:
                    for item in self.favorites:
                        if int(item.get("place_id") or item.get("placeId") or 0) == place_id:
                            item["universe_id"] = uid
                    self._save_favorites()
            raw = self.api.get_game_icon_bytes(uid)
            if not raw:
                raw = self.api.get_thumbnail_16x9_bytes(uid, place_id)
            if not raw:
                return
            try:
                pil_im = Image.open(io.BytesIO(raw)).convert("RGBA")
                fitted = ImageOps.fit(pil_im, (42, 42), Image.Resampling.LANCZOS)
                ctk_im = ctk.CTkImage(light_image=fitted, dark_image=fitted, size=(42, 42))
                self._fav_icon_images[place_id] = ctk_im
                self.after(0, lambda: target_label.configure(image=ctk_im) if target_label.winfo_exists() else None)
            except Exception:
                pass

        threading.Thread(target=_worker, daemon=True).start()

    def _on_load_place_clicked(self) -> None:
        self.sound.play_click()
        raw = self.entry_place_id.get().strip() if hasattr(self, "entry_place_id") else ""
        parsed = parse_roblox_game_input(raw, default_place_id=0)
        if not raw or (not re.search(r"roblox\.com/games/(\d+)", raw, flags=re.IGNORECASE) and not any(ch.isdigit() for ch in raw)):
            self._show_toast("Введите Place ID или ссылку на игру Roblox")
            return
        self._load_game_into_launcher(parsed["place_id"], play_click=False, link_code=parsed["link_code"])

    def _load_game_into_launcher(self, place_id: int, play_click: bool = True, link_code: str = "") -> None:
        if play_click:
            self.sound.play_click()
        place_id = int(place_id)
        self._has_user_selected_game = True
        self.config_data["last_place_id"] = place_id
        self._save_config()

        self.entry_place_id.delete(0, "end")
        self.entry_place_id.insert(0, str(place_id))
        self._update_favorite_button_state(place_id)

        if not hasattr(self, "_game_banner_cache"):
            self._game_banner_cache: dict[int, dict] = {}
        self._banner_request_id = getattr(self, "_banner_request_id", 0) + 1
        req_id = self._banner_request_id
        clean_link = (link_code or "").strip()

        cached = self._game_banner_cache.get(place_id)
        if cached is not None:
            info0 = dict(cached["info"])
            info0["link_code"] = clean_link
            self._current_game = info0
            self._banner_ctk_image = cached["image"]
            self.banner_img_label.configure(image=cached["image"], text="")
        else:
            # Мгновенная реакция: баннер сразу заменяется на заглушку выбранной игры, Play уже работает.
            self._current_game = {"placeId": place_id, "place_id": place_id, "link_code": clean_link, "name": f"Place #{place_id}", "creator": "Roblox", "playing": 0}
            try:
                self._banner_ctk_image = apply_bottom_gradient_and_text(
                    Image.new("RGB", (660, 371), (18, 24, 34)),
                    size=(660, 371),
                    title=f"Загрузка игры…",
                    creator="Roblox",
                    place_id=place_id,
                    playing=0,
                )
                self.banner_img_label.configure(image=self._banner_ctk_image, text="")
            except Exception as exc:
                write_crash_fix_log("_load_game_into_launcher.placeholder", exc)

        def _fetch_worker():
            try:
                info = self.api.get_game_info_by_place(place_id)
                info["placeId"] = place_id
                info["place_id"] = place_id
                info["link_code"] = clean_link
                thumb_bytes = self.api.get_thumbnail_16x9_bytes(info.get("universe_id", 0), place_id)
                src_img = None
                if thumb_bytes:
                    try:
                        src_img = Image.open(io.BytesIO(thumb_bytes)).convert("RGB")
                    except Exception as exc:
                        write_crash_fix_log("_load_game_into_launcher.PIL", exc)
                        src_img = None
                if src_img is None:
                    src_img = Image.new("RGB", (660, 371), (18, 24, 34))
                banner_img = apply_bottom_gradient_and_text(
                    src_img,
                    size=(660, 371),
                    title=str(info.get("name") or f"Place #{place_id}"),
                    creator=str(info.get("creator") or "Roblox"),
                    place_id=place_id,
                    playing=int(info.get("playing", 0) or 0),
                )
            except Exception as exc:
                write_crash_fix_log("_load_game_into_launcher.worker", exc)
                return

            def _apply_ui():
                if req_id != getattr(self, "_banner_request_id", 0):
                    return
                self._current_game = info
                self._banner_ctk_image = banner_img
                self._game_banner_cache[place_id] = {"info": dict(info), "image": banner_img}
                if self.banner_img_label.winfo_exists():
                    self.banner_img_label.configure(image=banner_img, text="")

            self.after(0, _apply_ui)

        threading.Thread(target=_fetch_worker, daemon=True).start()

    def _launch_specific_place_id(self, place_id: int, job_id: str | None = None, link_code: str | None = None) -> None:
        self.sound.play_click()
        self._has_user_selected_game = True
        pid = int(place_id)
        if not isinstance(self._current_game, dict):
            self._current_game = {}
        self._current_game["placeId"] = pid
        self._current_game["place_id"] = pid
        self.config_data["last_place_id"] = pid
        self._save_config()

        web_url = f"https://www.roblox.com/games/{pid}"
        if link_code:
            web_url += f"?privateServerLinkCode={urllib.parse.quote(str(link_code))}"
        self._copy_text_to_clipboard(web_url, None)

        self._start_game_launch(pid, job_id=job_id, link_code=link_code)

    def _on_play_button_clicked(self) -> None:
        pid, link_code, job_id_from_url = self._get_current_place_and_link_code()
        if pid <= 0:
            self._show_toast("Укажите корректный Place ID игры")
            return

        if not isinstance(self._current_game, dict):
            self._current_game = {}
        self._current_game["placeId"] = pid
        self._current_game["place_id"] = pid
        self.config_data["last_place_id"] = pid
        self._save_config()

        web_url = f"https://www.roblox.com/games/{pid}"
        if link_code:
            web_url += f"?privateServerLinkCode={urllib.parse.quote(link_code)}"
        self._copy_text_to_clipboard(web_url, f"Ссылка скопирована: {web_url}")

        if job_id_from_url:
            self._start_game_launch(pid, job_id=job_id_from_url, link_code=link_code)
        elif bool(self.config_data.get("auto_join_emptiest", False)) and not link_code:
            self.sound.play_click()

            def _worker(target_pid=pid):
                servers = self.api.get_public_servers(target_pid)
                jid = servers[0]["job_id"] if servers else None
                self.after(0, lambda p=target_pid, j=jid: self._start_game_launch(p, job_id=j, link_code=None))

            threading.Thread(target=_worker, daemon=True).start()
        else:
            self._start_game_launch(pid, job_id=None, link_code=link_code or None)

    def _start_game_launch(self, place_id: int, job_id: str | None = None, link_code: str | None = None) -> None:
        self._show_connect_overlay("Подготовка запуска...")
        for _delay in (6000, 14000):
            self.after(_delay, ROBLOX_WATCHER.kick)

        def _on_status_update(msg: str) -> None:
            self.after(0, lambda m=msg: self._update_connect_status(m))
            if msg == "Клиент запущен" or str(msg).startswith("Заблокировано RBX Shield"):
                self.after(900, self._hide_connect_overlay)
                if msg == "Клиент запущен" and bool(self.config_data.get("minimize_on_launch", False)):
                    self.after(950, lambda: self.taskbar.minimize_window(self))

        self.sys_manager.launch_roblox_game(
            place_id=int(place_id),
            job_id=job_id,
            link_code=link_code,
            on_status=_on_status_update,
        )

    def _show_connect_overlay(self, initial_text: str) -> None:
        """Full-bleed 100% splash overlay on PLAY with PhotoRBX\\photoloading.jpg and white spinner bottom-center."""
        self._hide_connect_overlay()
        self.update_idletasks()
        cur_w = max(APP_WIDTH, int(self.winfo_width() or APP_WIDTH))
        cur_h = max(APP_HEIGHT, int(self.winfo_height() or APP_HEIGHT))

        splash_play = SplashOverlay(
            self,
            width=cur_w,
            height=cur_h,
            is_first_run=False,
            on_complete=self._hide_connect_overlay,
            show_status_text=False,
        )
        splash_play._duration = 12.0
        splash_play.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        splash_play.lift()

        self._connect_overlay = splash_play
        self._connect_splash_canvas = splash_play
        self._connect_status_label = None

    def _update_connect_status(self, text: str) -> None:
        if text and str(text).startswith("Заблокировано RBX Shield"):
            self._show_toast(text, duration_ms=3600)

    def _hide_connect_overlay(self) -> None:
        if self._connect_splash_canvas is not None:
            try:
                self._connect_splash_canvas._finish()
            except Exception:
                pass
            self._connect_splash_canvas = None
        if self._connect_overlay is not None and self._connect_overlay.winfo_exists():
            self._connect_overlay.destroy()
        self._connect_overlay = None
        self._connect_status_label = None

    def _build_profile_tab(self) -> None:
        parent = self.tab_frames["profile"]
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        top_card = ctk.CTkFrame(parent, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        top_card.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
        top_card.grid_columnconfigure(1, weight=1)

        self.profile_avatar_label = ctk.CTkLabel(top_card, text="", width=108, height=108, corner_radius=12)
        self.profile_avatar_label.grid(row=0, column=0, rowspan=3, padx=16, pady=16)

        self.lbl_profile_display = ctk.CTkLabel(
            top_card,
            text="Определение профиля...",
            font=("Segoe UI", 19, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        self.lbl_profile_display.grid(row=0, column=1, sticky="ew", padx=(4, 12), pady=(16, 2))

        self.lbl_profile_handle = ctk.CTkLabel(
            top_card,
            text="@---  •  ID: ---",
            font=("Segoe UI", 12),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.lbl_profile_handle.grid(row=1, column=1, sticky="ew", padx=(4, 12))

        self.lbl_profile_status = ctk.CTkLabel(
            top_card,
            text="Автопоиск локального аккаунта Roblox...",
            font=("Segoe UI", 12),
            text_color=COLOR_ACCENT,
            anchor="w",
        )
        self.lbl_profile_status.grid(row=2, column=1, sticky="ew", padx=(4, 12), pady=(2, 16))

        btn_col = ctk.CTkFrame(top_card, fg_color="transparent", border_width=0)
        btn_col.grid(row=0, column=2, rowspan=3, padx=16, pady=14)

        self.btn_hide_profile = ctk.CTkButton(
            btn_col,
            text="Скрыть профиль",
            width=145,
            height=34,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
            command=self._toggle_hide_profile,
        )
        self.btn_hide_profile.pack(pady=(0, 8))

        ctk.CTkButton(
            btn_col,
            text="Обновить автопоиск",
            width=145,
            height=34,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self._start_auto_profile_detection,
        ).pack()

        bottom_grid = ctk.CTkFrame(parent, fg_color="transparent", border_width=0)
        bottom_grid.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 16))
        bottom_grid.grid_columnconfigure(0, weight=1)
        bottom_grid.grid_columnconfigure(1, weight=1)
        bottom_grid.grid_rowconfigure(0, weight=1)

        info_card = ctk.CTkFrame(bottom_grid, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        info_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        info_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            info_card,
            text="Данные аккаунта",
            font=("Segoe UI", 15, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 8))

        self.lbl_reg_date = ctk.CTkLabel(
            info_card,
            text="Регистрация: ---",
            font=("Segoe UI", 13),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        self.lbl_reg_date.pack(fill="x", padx=16, pady=4)

        self.lbl_acc_age = ctk.CTkLabel(
            info_card,
            text="Возраст аккаунта: ---",
            font=("Segoe UI", 13),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.lbl_acc_age.pack(fill="x", padx=16, pady=4)

        self.lbl_friends_followers = ctk.CTkLabel(
            info_card,
            text="Друзья: ---   •   Подписчики: ---",
            font=("Segoe UI", 13),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        self.lbl_friends_followers.pack(fill="x", padx=16, pady=4)

        self.txt_profile_bio = ctk.CTkTextbox(
            info_card,
            height=130,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            text_color=COLOR_TEXT_MUTED,
            font=("Segoe UI", 12),
        )
        self.txt_profile_bio.pack(fill="both", expand=True, padx=16, pady=(10, 16))
        self.txt_profile_bio.configure(state="disabled")

        friends_card = ctk.CTkFrame(bottom_grid, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        friends_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        friends_card.grid_columnconfigure(0, weight=1)
        friends_card.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            friends_card,
            text="Друзья в Roblox",
            font=("Segoe UI", 15, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        self.friends_scroll = ctk.CTkScrollableFrame(
            friends_card,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        self.friends_scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 12))
        self.friends_scroll.grid_columnconfigure(0, weight=1)

    def _start_auto_profile_detection(self) -> None:
        self.sound.play_click()
        if hasattr(self, "lbl_profile_status") and self.lbl_profile_status.winfo_exists():
            self.lbl_profile_status.configure(text="Поиск локального аккаунта Roblox...", text_color=COLOR_ACCENT)

        def _worker():
            uid = self.account_detector.detect_local_user_id()
            if not uid:
                self.after(0, self._on_profile_not_found)
                return
            self._detected_user_id = uid
            profile = self.api.get_user_profile(uid)
            avatar_bytes = self.api.get_user_headshot_bytes(uid)
            friend_avatars: dict[int, bytes] = {}
            if profile and isinstance(profile.get("friends"), list):
                friend_avatars = self.api.get_headshots_batch_bytes([int(fr.get("id") or 0) for fr in profile["friends"]])
            self.after(0, lambda p=profile, av=avatar_bytes, favs=friend_avatars: self._apply_profile_ui(p, av, favs))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_profile_not_found(self) -> None:
        if not hasattr(self, "lbl_profile_display") or not self.lbl_profile_display.winfo_exists():
            return
        self.lbl_profile_display.configure(text="Аккаунт не найден")
        self.lbl_profile_handle.configure(text="Войдите в клиент Roblox или откройте профиль в браузере")
        self.lbl_profile_status.configure(text="Локальные данные аккаунта не обнаружены", text_color=COLOR_WARNING)

    def _toggle_hide_profile(self) -> None:
        self.sound.play_click()
        self._profile_hidden = not self._profile_hidden
        self.btn_hide_profile.configure(text="Показать профиль" if self._profile_hidden else "Скрыть профиль")
        if self._current_profile_data:
            self._apply_profile_ui(self._current_profile_data, None, None)

    def _apply_profile_ui(
        self,
        profile: dict | None,
        avatar_bytes: bytes | None,
        friend_avatars: dict[int, bytes] | None,
    ) -> None:
        if not profile:
            self._on_profile_not_found()
            return
        self._current_profile_data = profile

        if avatar_bytes:
            try:
                im = ImageOps.fit(Image.open(io.BytesIO(avatar_bytes)).convert("RGBA"), (108, 108), Image.Resampling.LANCZOS)
                self._profile_avatar_image = ctk.CTkImage(light_image=im, dark_image=im, size=(108, 108))
            except Exception:
                pass

        if self._profile_avatar_image and self.profile_avatar_label.winfo_exists():
            self.profile_avatar_label.configure(image=self._profile_avatar_image)

        if self._profile_hidden:
            self.lbl_profile_display.configure(text="Скрытый профиль")
            self.lbl_profile_handle.configure(text="@hidden  •  ID: ******")
            self.lbl_profile_status.configure(text="Данные скрыты в интерфейсе", text_color=COLOR_TEXT_MUTED)
            self.lbl_reg_date.configure(text="Регистрация: скрыто")
            self.lbl_acc_age.configure(text="Возраст аккаунта: скрыто")
            self.lbl_friends_followers.configure(text="Друзья: скрыто   •   Подписчики: скрыто")
            self._set_profile_bio_text("Описание скрыто.")
            self._render_friends_list([], {})
            return

        disp = profile.get("display_name") or profile.get("username") or "Player"
        uname = profile.get("username") or ""
        uid = profile.get("id") or 0
        reg_date, acc_age = format_account_age(profile.get("created"))

        self.lbl_profile_display.configure(text=disp)
        self.lbl_profile_handle.configure(text=f"@{uname}  •  ID: {uid}")
        self.lbl_profile_status.configure(text="Автоматически определено на ПК", text_color=COLOR_SUCCESS)
        self.lbl_reg_date.configure(text=f"Регистрация: {reg_date}")
        self.lbl_acc_age.configure(text=f"Возраст аккаунта: {acc_age}")
        self.lbl_friends_followers.configure(
            text=f"Друзья: {format_number(profile.get('friends_count', 0))}   •   Подписчики: {format_number(profile.get('followers_count', 0))}"
        )
        self._set_profile_bio_text(profile.get("description") or "Описание профиля отсутствует.")
        self._render_friends_list(profile.get("friends") or [], friend_avatars or {})

    def _set_profile_bio_text(self, text: str) -> None:
        if not hasattr(self, "txt_profile_bio") or not self.txt_profile_bio.winfo_exists():
            return
        self.txt_profile_bio.configure(state="normal")
        self.txt_profile_bio.delete("1.0", "end")
        self.txt_profile_bio.insert("1.0", text)
        self.txt_profile_bio.configure(state="disabled")

    def _render_friends_list(self, friends: list[dict], friend_avatars: dict[int, bytes]) -> None:
        if not hasattr(self, "friends_scroll") or not self.friends_scroll.winfo_exists():
            return
        self._friends_render_token = getattr(self, "_friends_render_token", 0) + 1
        token = self._friends_render_token
        for w in self.friends_scroll.winfo_children():
            w.destroy()

        if not friends:
            ctk.CTkLabel(
                self.friends_scroll,
                text="Список друзей пуст или недоступен",
                font=("Segoe UI", 12),
                text_color=COLOR_TEXT_MUTED,
            ).pack(pady=24)
            return

        ctk.CTkLabel(
            self.friends_scroll,
            text=f"Друзья: {len(friends)}",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        ).pack(fill="x", padx=8, pady=(2, 4))
        self._render_friends_chunk(friends, friend_avatars, 0, token)

    def _render_friends_chunk(self, friends: list[dict], friend_avatars: dict[int, bytes], start: int, token: int) -> None:
        if token != getattr(self, "_friends_render_token", 0):
            return
        if not hasattr(self, "friends_scroll") or not self.friends_scroll.winfo_exists():
            return
        for fr in friends[start:start + 20]:
            fid = int(fr.get("id") or 0)
            fname = str(fr.get("display_name") or fr.get("name") or f"User_{fid}")
            handle = str(fr.get("name") or "")

            row = ctk.CTkFrame(self.friends_scroll, fg_color=COLOR_SURFACE_ALT, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            row.pack(fill="x", padx=4, pady=3)
            row.grid_columnconfigure(1, weight=1)

            av_lbl = ctk.CTkLabel(row, text="", width=40, height=40)
            av_lbl.grid(row=0, column=0, padx=8, pady=6)

            raw_av = friend_avatars.get(fid)
            if raw_av:
                try:
                    im = Image.open(io.BytesIO(raw_av)).convert("RGBA").resize((40, 40), Image.Resampling.LANCZOS)
                    mask = Image.new("L", (40, 40), 0)
                    ImageDraw.Draw(mask).ellipse((0, 0, 39, 39), fill=255)
                    im.putalpha(mask)
                    ctk_im = ctk.CTkImage(light_image=im, dark_image=im, size=(40, 40))
                    self._friend_avatar_images[fid] = ctk_im
                    av_lbl.configure(image=ctk_im)
                except Exception:
                    pass
            elif fid in self._friend_avatar_images:
                av_lbl.configure(image=self._friend_avatar_images[fid])

            ctk.CTkLabel(
                row,
                text=f"{fname}  (@{handle})" if handle else fname,
                font=("Segoe UI", 12),
                text_color=COLOR_TEXT,
                anchor="w",
            ).grid(row=0, column=1, sticky="ew", padx=(2, 10))

        nxt = start + 20
        if nxt < len(friends):
            self.after(25, lambda: self._render_friends_chunk(friends, friend_avatars, nxt, token))

    def _build_ai_tab(self) -> None:
        parent = self.tab_frames["ai"]
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        self._ai_history: list[dict] = []
        self._ai_attachments: list[dict] = []
        self._ai_busy = False
        self._ai_last_send = 0.0

        head = ctk.CTkFrame(parent, fg_color=COLOR_SURFACE, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        head.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
        ctk.CTkLabel(head, text="✦  RBX AI", font=("Segoe UI", 16, "bold"), text_color=COLOR_TEXT).pack(side="left", padx=16, pady=12)
        ctk.CTkLabel(head, text="Помощник на базе ChatGPT • без API-ключей", font=("Segoe UI", 12), text_color=COLOR_TEXT_MUTED).pack(side="left")
        ctk.CTkButton(
            head, text="Очистить чат", width=110, height=30, corner_radius=8, border_width=0,
            fg_color=COLOR_SURFACE_ALT, hover_color=COLOR_SURFACE_HOVER, text_color=COLOR_TEXT_MUTED,
            font=("Segoe UI", 12), command=self._ai_clear_chat,
        ).pack(side="right", padx=14)

        self.ai_scroll = ctk.CTkScrollableFrame(parent, fg_color=COLOR_SURFACE, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        self.ai_scroll.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 10))
        self._ai_add_bubble("assistant", "Привет! Я RBX AI. Спросите про Roblox, FastFlags, FPS, ошибки запуска или RBX Client. Можно прикрепить скриншот или лог-файл.")

        self.lbl_ai_attach = ctk.CTkLabel(parent, text="", font=("Segoe UI", 11), text_color=COLOR_ACCENT, anchor="w")
        self.lbl_ai_attach.grid(row=2, column=0, sticky="ew", padx=22)

        bar = ctk.CTkFrame(parent, fg_color=COLOR_SURFACE, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        bar.grid(row=3, column=0, sticky="ew", padx=18, pady=(2, 16))
        bar.grid_columnconfigure(2, weight=1)
        for col, (txt, cmd) in enumerate((("🖼", self._ai_attach_screenshot), ("📄", self._ai_attach_log))):
            ctk.CTkButton(
                bar, text=txt, width=40, height=38, corner_radius=8, border_width=0,
                fg_color=COLOR_SURFACE_ALT, hover_color=COLOR_SURFACE_HOVER, text_color=COLOR_TEXT,
                font=("Segoe UI", 14), command=cmd,
            ).grid(row=0, column=col, padx=(10 if col == 0 else 4, 0), pady=10)
        self.entry_ai = ctk.CTkEntry(
            bar, height=38, corner_radius=8, border_width=0, fg_color=COLOR_SURFACE_ALT, text_color=COLOR_TEXT,
            placeholder_text="Напишите сообщение…", font=("Segoe UI", 13),
        )
        self.entry_ai.grid(row=0, column=2, sticky="ew", padx=8)
        self.entry_ai.bind("<Return>", lambda _e: self._ai_send())
        self.btn_ai_send = ctk.CTkButton(
            bar, text="Отправить", width=110, height=38, corner_radius=8, border_width=0,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"), command=self._ai_send,
        )
        self.btn_ai_send.grid(row=0, column=3, padx=(0, 10))

    def _ai_add_bubble(self, role: str, text: str):
        mine = role == "user"
        holder = ctk.CTkFrame(self.ai_scroll, fg_color="transparent", border_width=0)
        holder.pack(fill="x", pady=4)
        lbl = ctk.CTkLabel(
            holder,
            text=text,
            wraplength=560,
            justify="left",
            anchor="w",
            font=("Segoe UI", 13),
            text_color="#FFFFFF" if mine else COLOR_TEXT,
            fg_color=COLOR_ACCENT_HOVER if mine else COLOR_SURFACE_ALT,
            corner_radius=12,
        )
        lbl.pack(side="right" if mine else "left", padx=8, ipadx=10, ipady=6)
        self.after(30, lambda: self.ai_scroll._parent_canvas.yview_moveto(1.0))
        return lbl

    def _ai_clear_chat(self) -> None:
        self.sound.play_click()
        self._ai_history.clear()
        self._ai_attachments.clear()
        self.lbl_ai_attach.configure(text="")
        for w in self.ai_scroll.winfo_children():
            w.destroy()
        self._ai_add_bubble("assistant", "Чат очищен. О чём поговорим?")

    @staticmethod
    def _ai_redact(text: str) -> str:
        text = re.sub(r"_\|WARNING:-DO-NOT-SHARE-THIS[^\s\"']+", "[REDACTED]", text)
        text = re.sub(r"(?i)\.ROBLOSECURITY\S*", "[REDACTED]", text)
        return text

    def _ai_attach_screenshot(self) -> None:
        self.sound.play_click()
        path = filedialog.askopenfilename(title="Скриншот", filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
        if not path:
            return
        try:
            im = Image.open(path).convert("RGB")
            im.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=82)
            self._ai_attachments.append({"kind": "image", "name": os.path.basename(path), "data": base64.b64encode(buf.getvalue()).decode("ascii")})
            self._ai_refresh_attach_label()
        except Exception as exc:
            write_crash_fix_log("ai_attach_screenshot", exc)
            self._show_toast("Не удалось прочитать изображение")

    def _ai_attach_log(self) -> None:
        self.sound.play_click()
        path = filedialog.askopenfilename(title="Лог-файл", filetypes=[("Logs", "*.log *.txt *.json"), ("All", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                body = f.read()[-12000:]
            self._ai_attachments.append({"kind": "text", "name": os.path.basename(path), "data": self._ai_redact(body)})
            self._ai_refresh_attach_label()
        except Exception as exc:
            write_crash_fix_log("ai_attach_log", exc)
            self._show_toast("Не удалось прочитать файл")

    def _ai_refresh_attach_label(self) -> None:
        names = ", ".join(a["name"] for a in self._ai_attachments)
        self.lbl_ai_attach.configure(text=f"Вложения: {names}" if names else "")

    def _ai_send(self) -> None:
        if self._ai_busy:
            return
        text = self.entry_ai.get().strip()
        if not text and not self._ai_attachments:
            return
        now = time.time()
        if now - self._ai_last_send < 1.5:
            return
        self._ai_last_send = now
        self.sound.play_click()
        self.entry_ai.delete(0, "end")
        atts = list(self._ai_attachments)
        self._ai_attachments.clear()
        self._ai_refresh_attach_label()

        shown = text or "(вложение)"
        if atts:
            shown += "\n📎 " + ", ".join(a["name"] for a in atts)
        self._ai_add_bubble("user", shown)

        parts: list[dict] = [{"type": "text", "text": text or "Проанализируй вложение."}]
        for a in atts:
            if a["kind"] == "text":
                parts[0]["text"] += f"\n\n--- {a['name']} ---\n{a['data']}"
            else:
                parts.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + a["data"]}})
        content = parts if len(parts) > 1 else parts[0]["text"]
        self._ai_history.append({"role": "user", "content": content})
        self._ai_history = self._ai_history[-12:]

        self._ai_busy = True
        self.btn_ai_send.configure(state="disabled", text="…")
        typing = self._ai_add_bubble("assistant", "RBX AI печатает…")
        messages = [{"role": "system", "content": (
            "Ты RBX AI — встроенный помощник лаунчера RBX Client by Kilon. Помогаешь с Roblox, FPS, FastFlags, "
            "ошибками запуска и настройкой лаунчера. Отвечай кратко и по делу на языке пользователя. "
            "Не проси пароли, cookie и .ROBLOSECURITY и не помогай с читами и обходом античита."
        )}] + list(self._ai_history)
        endpoint = str(self.config_data.get("ai_endpoint") or RBX_AI_ENDPOINT)

        def _worker():
            answer = ""
            try:
                resp = requests.post(endpoint, json={"model": RBX_AI_MODEL, "messages": messages}, timeout=60)
                if resp.status_code == 200:
                    answer = str(resp.json()["choices"][0]["message"]["content"]).strip()
                else:
                    answer = f"Сервис ИИ вернул ошибку {resp.status_code}. Попробуйте позже."
            except Exception as exc:
                write_crash_fix_log("rbx_ai_request", exc)
                answer = "Не удалось связаться с сервисом ИИ. Проверьте интернет и повторите."
            self.after(0, lambda: self._ai_done(typing, answer))

        threading.Thread(target=_worker, daemon=True).start()

    def _ai_done(self, typing_lbl, answer: str) -> None:
        if typing_lbl.winfo_exists():
            typing_lbl.configure(text=answer or "Пустой ответ")
        self._ai_history.append({"role": "assistant", "content": answer})
        self._ai_busy = False
        self.btn_ai_send.configure(state="normal", text="Отправить")
        self.after(30, lambda: self.ai_scroll._parent_canvas.yview_moveto(1.0))

    def _build_search_tab(self) -> None:
        parent = self.tab_frames["search"]
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        top_bar = ctk.CTkFrame(parent, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        top_bar.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
        top_bar.grid_columnconfigure(0, weight=1)

        self.entry_search_games = ctk.CTkEntry(
            top_bar,
            height=38,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            text_color=COLOR_TEXT,
            placeholder_text="Поиск активных игр Roblox (онлайн 100+)...",
            font=("Segoe UI", 13),
        )
        self.entry_search_games.grid(row=0, column=0, sticky="ew", padx=(12, 8), pady=12)
        self.entry_search_games.bind("<Return>", lambda _e: self._trigger_manual_game_search())

        ctk.CTkButton(
            top_bar,
            text="Найти",
            width=100,
            height=38,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self._trigger_manual_game_search,
        ).grid(row=0, column=1, padx=(0, 12), pady=12)

        self.search_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        self.search_scroll.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 16))
        self.search_scroll.grid_columnconfigure(0, weight=1)

    def _trigger_manual_game_search(self) -> None:
        self.sound.play_click()
        q = self.entry_search_games.get().strip() if hasattr(self, "entry_search_games") else ""
        threading.Thread(target=lambda query=q: self._fetch_and_update_search_feed(query), daemon=True).start()

    def _start_search_background_loop(self) -> None:
        if self._search_refresh_thread is not None and self._search_refresh_thread.is_alive():
            return
        self._search_stop_event.clear()

        def _loop():
            while not self._search_stop_event.is_set():
                if self._search_auto_refresh_enabled:
                    q = ""
                    try:
                        if hasattr(self, "entry_search_games") and self.entry_search_games.winfo_exists():
                            q = self.entry_search_games.get().strip()
                    except Exception:
                        q = ""
                    self._fetch_and_update_search_feed(q)
                self._search_stop_event.wait(ONLINE_REFRESH_INTERVAL_SEC)

        self._search_refresh_thread = threading.Thread(target=_loop, daemon=True)
        self._search_refresh_thread.start()

    def _fetch_and_update_search_feed(self, query: str) -> None:
        games = self.api.get_active_games_feed(query=query, min_playing=10)
        self._search_games_cache = games
        self.after(0, lambda g=games: self._render_search_results(g))

    def _render_search_results(self, games: list[dict]) -> None:
        if not hasattr(self, "search_scroll") or not self.search_scroll.winfo_exists():
            return

        incoming_ids = [int(g.get("place_id") or g.get("placeId") or 0) for g in games if int(g.get("place_id") or g.get("placeId") or 0) > 0]
        existing_ids = list(self._search_row_widgets.keys())

        structure_changed = (incoming_ids != existing_ids)
        if structure_changed:
            for w in self.search_scroll.winfo_children():
                w.destroy()
            self._search_row_widgets.clear()

            if not games:
                ctk.CTkLabel(
                    self.search_scroll,
                    text="Активные игры с онлайном 10+ не найдены",
                    font=("Segoe UI", 13),
                    text_color=COLOR_TEXT_MUTED,
                ).pack(pady=36)
                return

            for g in games:
                pid = int(g.get("place_id") or g.get("placeId") or 0)
                if pid <= 0:
                    continue
                uid = int(g.get("universe_id") or 0)
                name = str(g.get("name") or "Roblox Game")
                creator = str(g.get("creator") or "Roblox")
                playing = int(g.get("playing") or 0)

                card = ctk.CTkFrame(self.search_scroll, fg_color=COLOR_SURFACE, corner_radius=10, border_width=0)
                card.pack(fill="x", pady=4)
                card.grid_columnconfigure(1, weight=1)

                thumb_lbl = ctk.CTkLabel(card, text="", width=96, height=54, corner_radius=8)
                thumb_lbl.grid(row=0, column=0, padx=10, pady=8)
                if pid in self._search_card_images:
                    thumb_lbl.configure(image=self._search_card_images[pid])
                else:
                    self._load_search_thumb_async(pid, uid, thumb_lbl)

                meta_box = ctk.CTkFrame(card, fg_color="transparent", border_width=0)
                meta_box.grid(row=0, column=1, sticky="ew", padx=4)
                meta_box.grid_columnconfigure(0, weight=1)

                lbl_title = ctk.CTkLabel(
                    meta_box,
                    text=name,
                    font=("Segoe UI", 13, "bold"),
                    text_color=COLOR_TEXT,
                    anchor="w",
                )
                lbl_title.grid(row=0, column=0, sticky="ew")

                lbl_sub = ctk.CTkLabel(
                    meta_box,
                    text=f"Создатель: {creator}  •  ID: {pid}  •  Онлайн: {format_number(playing)}",
                    font=("Segoe UI", 11),
                    text_color=COLOR_TEXT_MUTED,
                    anchor="w",
                )
                lbl_sub.grid(row=1, column=0, sticky="ew")

                btn_sel = ctk.CTkButton(
                    card,
                    text="Выбрать",
                    width=84,
                    height=34,
                    corner_radius=8,
                    border_width=0,
                    fg_color=COLOR_SURFACE_ALT,
                    hover_color=COLOR_SURFACE_HOVER,
                    text_color=COLOR_TEXT,
                    font=("Segoe UI", 12, "bold"),
                    command=lambda p=pid: self._select_game_from_search(p),
                )
                btn_sel.grid(row=0, column=2, padx=(4, 5))

                btn_copy = ctk.CTkButton(
                    card,
                    text=self._tr("copy_link"),
                    width=88,
                    height=34,
                    corner_radius=8,
                    border_width=0,
                    fg_color=COLOR_SURFACE_ALT,
                    hover_color=COLOR_SURFACE_HOVER,
                    text_color=COLOR_ACCENT,
                    font=("Segoe UI", 11, "bold"),
                    command=lambda p=pid: (
                        self.sound.play_click(),
                        self._copy_text_to_clipboard(f"https://www.roblox.com/games/{p}", f"Ссылка скопирована: https://www.roblox.com/games/{p}"),
                    ),
                )
                btn_copy.grid(row=0, column=3, padx=(0, 5))

                btn_go = ctk.CTkButton(
                    card,
                    text="Играть",
                    width=80,
                    height=34,
                    corner_radius=8,
                    border_width=0,
                    fg_color=COLOR_ACCENT,
                    hover_color=COLOR_ACCENT_HOVER,
                    text_color="#FFFFFF",
                    font=("Segoe UI", 12, "bold"),
                    command=lambda p=pid: self._launch_specific_place_id(p),
                )
                btn_go.grid(row=0, column=4, padx=(0, 10))

                self._search_row_widgets[pid] = {
                    "card": card,
                    "title": lbl_title,
                    "sub": lbl_sub,
                }
        else:
            for g in games:
                pid = int(g.get("place_id") or g.get("placeId") or 0)
                w_map = self._search_row_widgets.get(pid)
                if not w_map:
                    continue
                name = str(g.get("name") or "Roblox Game")
                creator = str(g.get("creator") or "Roblox")
                playing = int(g.get("playing") or 0)
                try:
                    if w_map["title"].winfo_exists():
                        w_map["title"].configure(text=name)
                    if w_map["sub"].winfo_exists():
                        w_map["sub"].configure(
                            text=f"Создатель: {creator}  •  ID: {pid}  •  Онлайн: {format_number(playing)}"
                        )
                except Exception:
                    pass

    def _load_search_thumb_async(self, place_id: int, universe_id: int, target_label: ctk.CTkLabel) -> None:
        cached_im = self._search_card_images.get(place_id)
        if cached_im is not None:
            target_label.configure(image=cached_im)
            return

        def _worker():
            raw = self.api.get_thumbnail_16x9_bytes(universe_id, place_id)
            if not raw:
                return
            try:
                im = ImageOps.fit(Image.open(io.BytesIO(raw)).convert("RGBA"), (96, 54), Image.Resampling.LANCZOS)
                ctk_im = ctk.CTkImage(light_image=im, dark_image=im, size=(96, 54))
                self._search_card_images[place_id] = ctk_im
                self.after(0, lambda: target_label.configure(image=ctk_im) if target_label.winfo_exists() else None)
            except Exception:
                pass

        threading.Thread(target=_worker, daemon=True).start()

    def _select_game_from_search(self, place_id: int) -> None:
        self.sound.play_click()
        self._load_game_into_launcher(place_id, play_click=False)
        self._switch_tab("launcher")

    def _build_servers_tab(self) -> None:
        parent = self.tab_frames["servers"]
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        top_bar = ctk.CTkFrame(parent, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        top_bar.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
        top_bar.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            top_bar,
            text="Server Hopper",
            font=("Segoe UI", 15, "bold"),
            text_color=COLOR_TEXT,
        ).grid(row=0, column=0, padx=(16, 10), pady=12)

        self.lbl_hopper_place = ctk.CTkLabel(
            top_bar,
            text="Place ID: ---",
            font=("Segoe UI", 12),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.lbl_hopper_place.grid(row=0, column=1, sticky="ew")

        ctk.CTkButton(
            top_bar,
            text="Join Emptiest",
            height=36,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self._join_emptiest_server,
        ).grid(row=0, column=2, padx=(0, 8), pady=12)

        ctk.CTkButton(
            top_bar,
            text="Обновить",
            width=96,
            height=36,
            corner_radius=8,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12, "bold"),
            command=self._refresh_servers_list,
        ).grid(row=0, column=3, padx=(0, 14), pady=12)

        filter_bar = ctk.CTkFrame(top_bar, fg_color="transparent", border_width=0)
        filter_bar.grid(row=1, column=0, columnspan=4, sticky="ew", padx=14, pady=(0, 12))
        filter_bar.grid_columnconfigure(2, weight=1)
        self.srv_region_var = ctk.StringVar(value="Все регионы")
        ctk.CTkOptionMenu(
            filter_bar,
            values=["Все регионы", "Рядом (≤60 мс)", "Регион (≤120 мс)", "Далеко (>120 мс)"],
            variable=self.srv_region_var,
            width=170, height=34, corner_radius=8,
            fg_color=COLOR_SURFACE_ALT, button_color=COLOR_SURFACE_HOVER, button_hover_color=COLOR_ACCENT,
            text_color=COLOR_TEXT, font=("Segoe UI", 12),
            command=lambda _v: self._render_servers_list(self._get_target_servers_place_id(), self._servers_list),
        ).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(filter_bar, text="Job ID:", font=("Segoe UI", 12, "bold"), text_color=COLOR_TEXT_MUTED).grid(row=0, column=1, padx=(0, 6))
        self.entry_job_id = ctk.CTkEntry(
            filter_bar, height=34, corner_radius=8, border_width=1, border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE_ALT, text_color=COLOR_TEXT, placeholder_text="Вставьте Job ID сервера",
            font=("Segoe UI", 12),
        )
        self.entry_job_id.grid(row=0, column=2, sticky="ew", padx=(0, 8))
        self.entry_job_id.bind("<Return>", lambda _e: self._join_by_job_id())
        ctk.CTkButton(
            filter_bar, text="Зайти по Job ID", width=130, height=34, corner_radius=8, border_width=0,
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"), command=self._join_by_job_id,
        ).grid(row=0, column=3)

        self.servers_scroll = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            corner_radius=0,
            border_width=0,
        )
        self.servers_scroll.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 16))
        self.servers_scroll.grid_columnconfigure(0, weight=1)

    def _get_target_servers_place_id(self) -> int:
        pid, _, _ = self._get_current_place_and_link_code()
        return int(pid or 2753915549)

    def _refresh_servers_list(self) -> None:
        self.sound.play_click()
        pid = self._get_target_servers_place_id()
        if hasattr(self, "lbl_hopper_place") and self.lbl_hopper_place.winfo_exists():
            self.lbl_hopper_place.configure(text=f"Place ID: {pid}  •  Загрузка серверов...")

        def _worker():
            servers = self.api.get_public_servers(pid)
            self._servers_list = servers
            self.after(0, lambda p=pid, s=servers: self._render_servers_list(p, s))

        threading.Thread(target=_worker, daemon=True).start()

    def _render_servers_list(self, place_id: int, servers: list[dict]) -> None:
        if not hasattr(self, "servers_scroll") or not self.servers_scroll.winfo_exists():
            return
        if hasattr(self, "lbl_hopper_place") and self.lbl_hopper_place.winfo_exists():
            self.lbl_hopper_place.configure(text=f"Place ID: {place_id}  •  Найдено серверов: {len(servers)}")
        servers = self._filter_servers(servers)

        for w in self.servers_scroll.winfo_children():
            w.destroy()

        if not servers:
            ctk.CTkLabel(
                self.servers_scroll,
                text="Публичные серверы не найдены или игра недоступна",
                font=("Segoe UI", 13),
                text_color=COLOR_TEXT_MUTED,
            ).pack(pady=36)
            return

        for srv in servers[:40]:
            jid = srv["job_id"]
            playing = srv["playing"]
            max_p = srv["max_players"]
            ping = srv["ping"]
            fps = srv["fps"]

            row = ctk.CTkFrame(self.servers_scroll, fg_color=COLOR_SURFACE, corner_radius=10, border_width=0)
            row.pack(fill="x", pady=4)
            row.grid_columnconfigure(0, weight=1)

            info_txt = f"Игроки: {playing}/{max_p}   •   Ping: {ping if ping > 0 else '—'} ms   •   FPS: {round(fps, 1) if fps > 0 else '—'}   •   Job: {jid[:12]}..."
            ctk.CTkLabel(
                row,
                text=info_txt,
                font=("Segoe UI", 12),
                text_color=COLOR_TEXT,
                anchor="w",
            ).grid(row=0, column=0, sticky="ew", padx=14, pady=10)

            ctk.CTkButton(
                row,
                text="Зайти на сервер",
                width=130,
                height=32,
                corner_radius=8,
                border_width=0,
                fg_color=COLOR_ACCENT,
                hover_color=COLOR_ACCENT_HOVER,
                text_color="#FFFFFF",
                font=("Segoe UI", 12, "bold"),
                command=lambda p=place_id, j=jid: self._launch_specific_place_id(p, job_id=j),
            ).grid(row=0, column=1, padx=12, pady=8)

    def _filter_servers(self, servers: list[dict]) -> list[dict]:
        mode = self.srv_region_var.get() if hasattr(self, "srv_region_var") else "Все регионы"

        def _ok(p: int) -> bool:
            if mode.startswith("Рядом"):
                return 0 < p <= 60
            if mode.startswith("Регион"):
                return 60 < p <= 120
            if mode.startswith("Далеко"):
                return p > 120
            return True

        return [sv for sv in servers if _ok(int(sv.get("ping") or 0))]

    def _join_by_job_id(self) -> None:
        self.sound.play_click()
        jid = self.entry_job_id.get().strip()
        if not re.fullmatch(r"[0-9a-fA-F\-]{8,40}", jid):
            self._show_toast("Некорректный Job ID")
            return
        self._launch_specific_place_id(self._get_target_servers_place_id(), job_id=jid)

    def _join_emptiest_server(self) -> None:
        self.sound.play_click()
        pid = self._get_target_servers_place_id()

        def _worker():
            servers = self._servers_list if self._servers_list else self.api.get_public_servers(pid)
            servers = self._filter_servers(servers) or servers
            if servers:
                emptiest = servers[0]
                self.after(0, lambda p=pid, j=emptiest["job_id"]: self._launch_specific_place_id(p, job_id=j))
            else:
                self.after(0, lambda p=pid: self._launch_specific_place_id(p, job_id=None))

        threading.Thread(target=_worker, daemon=True).start()

    def _build_settings_tab(self) -> None:
        parent = self.tab_frames["settings"]
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)
        parent.grid_rowconfigure(0, weight=1)

        left_scroll = ctk.CTkScrollableFrame(parent, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        left_scroll.grid(row=0, column=0, sticky="nsew", padx=(18, 9), pady=16)
        left_scroll.grid_columnconfigure(0, weight=1)

        self._settings_right_open = True
        self._settings_right_w_open = 470
        self._settings_right_w_closed = 200
        self._settings_anim_job = None
        self.right_wrap = ctk.CTkFrame(parent, width=self._settings_right_w_open, fg_color="transparent", corner_radius=0, border_width=0)
        self.right_wrap.grid(row=0, column=1, sticky="nsew", padx=(9, 18), pady=16)
        self.right_wrap.grid_propagate(False)
        self.right_wrap.grid_columnconfigure(0, weight=1)
        self.right_wrap.grid_rowconfigure(1, weight=1)

        self.btn_toggle_right = ctk.CTkButton(
            self.right_wrap,
            text="Доп. инструменты ▾",
            height=36,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDER,
            fg_color=COLOR_SURFACE,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            anchor="w",
            font=("Segoe UI", 13, "bold"),
            command=self._toggle_settings_right_panel,
        )
        self.btn_toggle_right.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        right_scroll = ctk.CTkScrollableFrame(self.right_wrap, fg_color=COLOR_SURFACE, corner_radius=12, border_width=0)
        right_scroll.grid(row=1, column=0, sticky="nsew")
        right_scroll.grid_columnconfigure(0, weight=1)
        self.right_scroll_panel = right_scroll

        ctk.CTkLabel(
            left_scroll,
            text="Графика и производительность",
            font=("Segoe UI", 15, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 10))

        self.lbl_hw_preset = ctk.CTkLabel(
            left_scroll,
            text="Автоподбор пресета по ПК: ---",
            font=("Segoe UI", 12),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.lbl_hw_preset.pack(fill="x", padx=16, pady=(0, 8))

        preset_row = ctk.CTkFrame(left_scroll, fg_color="transparent", border_width=0)
        preset_row.pack(fill="x", padx=16, pady=(0, 12))
        for p_name in ("Низкие FPS", "Средние", "Высокие"):
            ctk.CTkButton(
                preset_row,
                text=p_name,
                height=32,
                corner_radius=8,
                border_width=0,
                fg_color=COLOR_SURFACE_ALT,
                hover_color=COLOR_SURFACE_HOVER,
                text_color=COLOR_TEXT,
                font=("Segoe UI", 12, "bold"),
                command=lambda pn=p_name: self._apply_quick_preset(pn),
            ).pack(side="left", expand=True, fill="x", padx=2)

        ctk.CTkLabel(
            left_scroll,
            text="Лимит FPS",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(4, 2))

        self.fps_var = ctk.IntVar(value=int(self.config_data.get("fps_cap", 144)))
        self.lbl_fps_val = ctk.CTkLabel(
            left_scroll,
            text=f"{self.fps_var.get()} FPS",
            font=("Segoe UI", 12),
            text_color=COLOR_ACCENT,
            anchor="w",
        )
        self.lbl_fps_val.pack(fill="x", padx=16)

        self.fps_slider = ctk.CTkSlider(
            left_scroll,
            from_=30,
            to=360,
            number_of_steps=66,
            variable=self.fps_var,
            button_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER,
            progress_color=COLOR_ACCENT,
            command=lambda v: self.lbl_fps_val.configure(text=f"{int(float(v))} FPS"),
        )
        self.fps_slider.pack(fill="x", padx=16, pady=(2, 10))

        ctk.CTkLabel(
            left_scroll,
            text="Движок рендера",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(2, 4))

        self.render_engine_var = ctk.StringVar(value=str(self.config_data.get("render_engine", "DirectX 11")))
        ctk.CTkOptionMenu(
            left_scroll,
            values=["DirectX 11", "DirectX 10", "Vulkan", "OpenGL"],
            variable=self.render_engine_var,
            fg_color=COLOR_SURFACE_ALT,
            button_color=COLOR_SURFACE_HOVER,
            button_hover_color=COLOR_ACCENT,
            text_color=COLOR_TEXT,
            dropdown_fg_color=COLOR_SURFACE_ALT,
            dropdown_text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
        ).pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(
            left_scroll,
            text="Качество графики",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(2, 4))

        self.quality_level_var = ctk.StringVar(value=str(self.config_data.get("quality_level", "Авто")))
        ctk.CTkOptionMenu(
            left_scroll,
            values=["Авто", "Низкая", "Средняя", "Максимальная"],
            variable=self.quality_level_var,
            fg_color=COLOR_SURFACE_ALT,
            button_color=COLOR_SURFACE_HOVER,
            button_hover_color=COLOR_ACCENT,
            text_color=COLOR_TEXT,
            dropdown_fg_color=COLOR_SURFACE_ALT,
            dropdown_text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
        ).pack(fill="x", padx=16, pady=(0, 10))

        self.sw_shadows = self._make_switch(left_scroll, "Отключить тени", "disable_shadows")
        self.sw_grass = self._make_switch(left_scroll, "Отключить траву", "disable_grass")
        self.sw_telemetry = self._make_switch(left_scroll, "Отключить телеметрию Roblox", "disable_telemetry")
        self.sw_motion_blur = self._make_switch(left_scroll, "Отключить размытие в движении", "disable_motion_blur")
        self.sw_low_tex = self._make_switch(left_scroll, "Понизить качество текстур", "low_texture_quality")
        self.sw_overlay_analytics = self._make_switch(left_scroll, "Отключить аналитику оверлея", "disable_overlay_analytics")
        self.sw_classic_oof = self._make_switch(left_scroll, "Классический звук смерти (Oof)", "classic_oof_sound")

        btn_apply_gfx = ctk.CTkButton(
            left_scroll,
            text="Применить настройки графики",
            height=38,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self._on_apply_graphics_clicked,
        )
        btn_apply_gfx.pack(fill="x", padx=16, pady=(12, 6))

        btn_reset_gfx = ctk.CTkButton(
            left_scroll,
            text="Сбросить настройки графики",
            height=34,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT_MUTED,
            font=("Segoe UI", 12),
            command=self._on_reset_graphics_clicked,
        )
        btn_reset_gfx.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkLabel(
            right_scroll,
            text="Лаунчер, звук и RBX Shield",
            font=("Segoe UI", 15, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(14, 10))

        self.sw_sound_click = self._make_switch(right_scroll, "Звук кликов кнопок", "sound_click")
        self.sw_sound_startup = self._make_switch(right_scroll, "Музыка при запуске", "sound_startup")
        self.sw_auto_f11 = self._make_switch(right_scroll, "Авто-полный экран (F11)", "auto_fullscreen_f11")
        self.sw_min_launch = self._make_switch(right_scroll, "Сворачивать при запуске игры", "minimize_on_launch")
        self.sw_auto_empty = self._make_switch(right_scroll, "Автозаход на пустой сервер", "auto_join_emptiest")
        self.sw_toasts = self._make_switch(right_scroll, "Показывать уведомления", "show_toasts")
        self.sw_fps_ping_overlay = self._make_switch(
            right_scroll,
            "Оверлей FPS & Ping (только в игре)",
            "show_fps_ping_overlay",
            on_after_toggle=self._monitor_game_overlay_loop,
        )
        self.sw_security_guard = self._make_switch(
            right_scroll,
            "RBX Shield (Антивирус и защита)",
            "security_guard_enabled",
            on_after_toggle=lambda: (self.security_guard.run_scan_once(), self._refresh_security_guard_ui()),
        )

        self.lbl_shield_status = ctk.CTkLabel(
            right_scroll,
            text=self._tr("shield_ok"),
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_SUCCESS,
            anchor="w",
        )
        self.lbl_shield_status.pack(fill="x", padx=16, pady=(4, 6))

        ctk.CTkLabel(
            right_scroll,
            text="Прозрачность окна",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(6, 2))

        self.alpha_var = ctk.DoubleVar(value=float(self.config_data.get("window_alpha", APP_ALPHA)))
        self.lbl_alpha_val = ctk.CTkLabel(
            right_scroll,
            text=f"{int(round(self.alpha_var.get() * 100))}%",
            font=("Segoe UI", 12),
            text_color=COLOR_ACCENT,
            anchor="w",
        )
        self.lbl_alpha_val.pack(fill="x", padx=16)

        ctk.CTkSlider(
            right_scroll,
            from_=0.80,
            to=1.00,
            number_of_steps=20,
            variable=self.alpha_var,
            button_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER,
            progress_color=COLOR_ACCENT,
            command=self._on_alpha_slider_change,
        ).pack(fill="x", padx=16, pady=(2, 10))

        self.lbl_cache_info = ctk.CTkLabel(
            right_scroll,
            text=f"Кэш изображений: {self.sys_manager.get_cache_size_mb()} МБ",
            font=("Segoe UI", 12),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.lbl_cache_info.pack(fill="x", padx=16, pady=(4, 6))

        ctk.CTkButton(
            right_scroll,
            text="Очистить кэш картинок",
            height=34,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
            command=self._on_clear_cache_clicked,
        ).pack(fill="x", padx=16, pady=(0, 6))

        self.btn_clear_roblox_cache = ctk.CTkButton(
            right_scroll,
            text=self._tr("clear_roblox_cache"),
            height=34,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_ACCENT,
            font=("Segoe UI", 12, "bold"),
            command=self._on_clear_roblox_cache_clicked,
        )
        self.btn_clear_roblox_cache.pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkLabel(
            right_scroll,
            text="Custom Shaders",
            font=("Segoe UI", 12, "bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(10, 2))
        self.lbl_shaders_status = ctk.CTkLabel(
            right_scroll,
            text="Установлены пользовательские шейдеры" if self.config_data.get("shaders_installed") else "Используются оригинальные шейдеры Roblox",
            font=("Segoe UI", 11),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
            wraplength=300,
            justify="left",
        )
        self.lbl_shaders_status.pack(fill="x", padx=16, pady=(0, 4))
        shader_row = ctk.CTkFrame(right_scroll, fg_color="transparent", border_width=0)
        shader_row.pack(fill="x", padx=16, pady=(0, 6))
        shader_row.grid_columnconfigure((0, 1), weight=1)
        for col, (label, cmd, fg, tc) in enumerate((
            ("Папка…", self._on_install_shader_folder, COLOR_ACCENT, "#FFFFFF"),
            (".zip…", self._on_install_shader_zip, COLOR_ACCENT, "#FFFFFF"),
        )):
            ctk.CTkButton(
                shader_row, text=label, height=34, corner_radius=10, border_width=0,
                fg_color=fg, hover_color=COLOR_ACCENT_HOVER, text_color=tc,
                font=("Segoe UI", 12, "bold"), command=cmd,
            ).grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 4, 4 if col == 0 else 0))
        ctk.CTkButton(
            right_scroll, text="Сбросить шейдеры к оригинальным", height=34, corner_radius=10, border_width=0,
            fg_color=COLOR_SURFACE_ALT, hover_color=COLOR_SURFACE_HOVER, text_color=COLOR_WARNING,
            font=("Segoe UI", 12, "bold"), command=self._on_reset_shaders,
        ).pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkButton(
            right_scroll,
            text="Очистить логи Roblox",
            height=34,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
            command=self._on_clear_logs_clicked,
        ).pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkButton(
            right_scroll,
            text="Открыть папку логов лаунчера",
            height=34,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
            command=self._on_open_logs_folder_clicked,
        ).pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkButton(
            right_scroll,
            text="Привязать протокол rbxclient://",
            height=34,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
            command=self._on_register_protocol_clicked,
        ).pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkButton(
            right_scroll,
            text="Безопасность и конфиденциальность",
            height=34,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_SURFACE_ALT,
            hover_color=COLOR_SURFACE_HOVER,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
            command=lambda: (self.sound.play_click(), self._open_security_consent_screen(closable=True)),
        ).pack(fill="x", padx=16, pady=(0, 10))

        self.lbl_self_heal_status = ctk.CTkLabel(
            right_scroll,
            text="SelfHealEngine: исправлений 0",
            font=("Segoe UI", 12),
            text_color=COLOR_SUCCESS,
            anchor="w",
        )
        self.lbl_self_heal_status.pack(fill="x", padx=16, pady=(4, 4))

        ctk.CTkButton(
            right_scroll,
            text="Проверить обновления на GitHub",
            height=36,
            corner_radius=10,
            border_width=0,
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            command=self._on_check_updates_clicked,
        ).pack(fill="x", padx=16, pady=(4, 14))

        self._detect_and_display_hw_preset()
        self._refresh_self_heal_ui()
        self._refresh_security_guard_ui()

    def _refresh_security_guard_ui(self) -> None:
        if hasattr(self, "title_shield_lbl") and self.title_shield_lbl.winfo_exists():
            if not bool(self.config_data.get("security_guard_enabled", True)):
                self.title_shield_lbl.configure(text="●  RBX Shield: Off", text_color=COLOR_TEXT_MUTED)
            elif self.security_guard.threat_detected:
                self.title_shield_lbl.configure(text="●  RBX Shield: Threat", text_color=COLOR_DANGER)
            else:
                self.title_shield_lbl.configure(text="●  RBX Shield: Protected", text_color=COLOR_SUCCESS)
        if not hasattr(self, "lbl_shield_status") or not self.lbl_shield_status.winfo_exists():
            return
        enabled = bool(self.config_data.get("security_guard_enabled", True))
        if not enabled:
            self.lbl_shield_status.configure(text=self._tr("shield_off"), text_color=COLOR_TEXT_MUTED)
            return
        if self.security_guard.threat_detected:
            reason = self.security_guard.last_threat_reason or self._tr("shield_alert")
            self.lbl_shield_status.configure(text=f"Warning • {reason}", text_color=COLOR_DANGER)
        else:
            blocked = int(getattr(getattr(self.api, "_ddos", None), "blocked_total", 0))
            self.lbl_shield_status.configure(text=f"{self._tr('shield_ok')}  •  Anti-DDoS: {blocked}", text_color=COLOR_SUCCESS)

    def _make_switch(self, parent, text: str, config_key: str, on_after_toggle=None) -> ctk.CTkSwitch:
        var = ctk.BooleanVar(value=bool(self.config_data.get(config_key, False)))

        def _toggle():
            self.sound.play_click()
            self.config_data[config_key] = bool(var.get())
            self._save_config()
            if callable(on_after_toggle):
                on_after_toggle()

        sw = ctk.CTkSwitch(
            parent,
            text=text,
            variable=var,
            onvalue=True,
            offvalue=False,
            button_color=COLOR_ACCENT,
            button_hover_color=COLOR_ACCENT_HOVER,
            progress_color=COLOR_ACCENT,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 12),
            command=_toggle,
        )
        sw.pack(fill="x", padx=16, pady=4)
        return sw

    def _detect_and_display_hw_preset(self) -> None:
        def _worker():
            preset = self.sys_manager.detect_hardware_preset()

            def _apply():
                if hasattr(self, "lbl_hw_preset") and self.lbl_hw_preset.winfo_exists():
                    self.lbl_hw_preset.configure(text=preset["summary"])

            self.after(0, _apply)

        threading.Thread(target=_worker, daemon=True).start()

    def _apply_quick_preset(self, preset_name: str) -> None:
        self.sound.play_click()
        if preset_name == "Низкие FPS":
            self.fps_var.set(60)
            self.lbl_fps_val.configure(text="60 FPS")
            self.quality_level_var.set("Низкая")
            self.sw_shadows.select()
            self.sw_grass.select()
            self.sw_motion_blur.select()
            self.sw_low_tex.select()
        elif preset_name == "Средние":
            self.fps_var.set(120)
            self.lbl_fps_val.configure(text="120 FPS")
            self.quality_level_var.set("Средняя")
            self.sw_shadows.deselect()
            self.sw_grass.select()
            self.sw_motion_blur.select()
            self.sw_low_tex.deselect()
        else:
            self.fps_var.set(240)
            self.lbl_fps_val.configure(text="240 FPS")
            self.quality_level_var.set("Максимальная")
            self.sw_shadows.deselect()
            self.sw_grass.deselect()
            self.sw_motion_blur.deselect()
            self.sw_low_tex.deselect()
        self._on_apply_graphics_clicked()

    def _on_apply_graphics_clicked(self) -> None:
        self.sound.play_click()
        fps_val = int(self.fps_var.get())
        eng_val = str(self.render_engine_var.get())
        q_val = str(self.quality_level_var.get())
        sh_val = bool(self.sw_shadows.get())
        gr_val = bool(self.sw_grass.get())
        tel_val = bool(self.sw_telemetry.get())
        mb_val = bool(self.sw_motion_blur.get())
        lt_val = bool(self.sw_low_tex.get())
        ov_val = bool(self.sw_overlay_analytics.get())
        oof_val = bool(self.sw_classic_oof.get())

        self.config_data["fps_cap"] = fps_val
        self.config_data["render_engine"] = eng_val
        self.config_data["quality_level"] = q_val
        self.config_data["disable_shadows"] = sh_val
        self.config_data["disable_grass"] = gr_val
        self.config_data["disable_telemetry"] = tel_val
        self.config_data["disable_motion_blur"] = mb_val
        self.config_data["low_texture_quality"] = lt_val
        self.config_data["disable_overlay_analytics"] = ov_val
        self.config_data["classic_oof_sound"] = oof_val
        self._save_config()

        ok, msg = self.sys_manager.apply_extended_client_tweaks(
            fps_cap=fps_val,
            render_engine=eng_val,
            disable_shadows=sh_val,
            disable_grass=gr_val,
            disable_telemetry=tel_val,
            disable_motion_blur=mb_val,
            low_texture_quality=lt_val,
            disable_overlay_analytics=ov_val,
            quality_level=q_val,
        )
        oof_msg = self.sys_manager.apply_classic_oof_sound(oof_val)
        self._show_toast(f"{msg} • {oof_msg}" if ok else msg)

    def _on_reset_graphics_clicked(self) -> None:
        self.sound.play_click()
        ok, msg = self.sys_manager.reset_client_app_settings()
        self._show_toast(msg if ok else msg)

    def _on_alpha_slider_change(self, val) -> None:
        a = max(0.80, min(1.00, float(val)))
        self.lbl_alpha_val.configure(text=f"{int(round(a * 100))}%")
        self.config_data["window_alpha"] = round(a, 2)
        self._save_config()
        try:
            self.attributes("-alpha", a)
        except Exception:
            pass

    def _on_clear_cache_clicked(self) -> None:
        self.sound.play_click()
        _, msg = self.sys_manager.clear_image_cache()
        if hasattr(self, "lbl_cache_info") and self.lbl_cache_info.winfo_exists():
            self.lbl_cache_info.configure(text=f"Кэш изображений: {self.sys_manager.get_cache_size_mb()} МБ")
        self._show_toast(msg)

    def _animate_wrap_width(self, start: float, end: float, duration_ms: int = 280, on_done=None) -> None:
        """Пошаговая анимация ширины панели (easing out-cubic) через after(12), без блокировки UI."""
        if self._settings_anim_job is not None:
            try:
                self.after_cancel(self._settings_anim_job)
            except Exception:
                pass
            self._settings_anim_job = None
        t0 = time.perf_counter()

        def _step():
            if not self.right_wrap.winfo_exists():
                return
            p = min(1.0, (time.perf_counter() - t0) * 1000.0 / max(1, duration_ms))
            eased = 1.0 - (1.0 - p) ** 3
            self.right_wrap.configure(width=int(start + (end - start) * eased))
            if p < 1.0:
                self._settings_anim_job = self.after(12, _step)
            else:
                self._settings_anim_job = None
                if callable(on_done):
                    on_done()

        _step()

    def _toggle_settings_right_panel(self) -> None:
        self.sound.play_click()
        w_open = self._settings_right_w_open
        w_closed = self._settings_right_w_closed
        if self._settings_right_open:
            self._settings_right_open = False
            self.btn_toggle_right.configure(text="Доп. инструменты ▸")

            def _done():
                self.right_scroll_panel.grid_remove()

            self._animate_wrap_width(self.right_wrap.winfo_width() / max(0.5, self._get_ui_scale()), w_closed, on_done=_done)
        else:
            self._settings_right_open = True
            self.btn_toggle_right.configure(text="Доп. инструменты ▾")
            self.right_scroll_panel.grid(row=1, column=0, sticky="nsew")
            self._animate_wrap_width(self.right_wrap.winfo_width() / max(0.5, self._get_ui_scale()), w_open)

    def _get_ui_scale(self) -> float:
        try:
            return float(ctk.ScalingTracker.get_window_scaling(self))
        except Exception:
            return 1.0

    def _animate_settings_open(self) -> None:
        """Плавное выдвижение панели при переходе на вкладку «Настройки»."""
        if not hasattr(self, "right_wrap") or not self.right_wrap.winfo_exists():
            return
        target = self._settings_right_w_open if self._settings_right_open else self._settings_right_w_closed
        self.right_wrap.configure(width=40)
        self._animate_wrap_width(40, target, duration_ms=320)

    def _shader_task(self, func, *args) -> None:
        def _worker():
            ok, msg = func(*args)
            def _done():
                if ok and func == self.sys_manager.install_custom_shaders:
                    self.config_data["shaders_installed"] = True
                    self.config_data["custom_shaders_path"] = str(args[0])
                    self._save_config()
                elif ok and func == self.sys_manager.reset_custom_shaders:
                    self.config_data["shaders_installed"] = False
                    self.config_data["custom_shaders_path"] = ""
                    self._save_config()
                if hasattr(self, "lbl_shaders_status") and self.lbl_shaders_status.winfo_exists():
                    self.lbl_shaders_status.configure(
                        text=msg, text_color=COLOR_SUCCESS if ok else COLOR_DANGER)
                self._show_toast(msg, duration_ms=3200)
            self.after(0, _done)
        threading.Thread(target=_worker, daemon=True).start()

    def _on_install_shader_folder(self) -> None:
        self.sound.play_click()
        path = filedialog.askdirectory(title="Папка с шейдерами/текстурами")
        if path:
            self._shader_task(self.sys_manager.install_custom_shaders, path)

    def _on_install_shader_zip(self) -> None:
        self.sound.play_click()
        path = filedialog.askopenfilename(title="Архив с шейдерами", filetypes=[("ZIP", "*.zip")])
        if path:
            self._shader_task(self.sys_manager.install_custom_shaders, path)

    def _on_reset_shaders(self) -> None:
        self.sound.play_click()
        self._shader_task(self.sys_manager.reset_custom_shaders)

    def _on_clear_roblox_cache_clicked(self) -> None:
        self.sound.play_click()
        _, freed_mb = self.sys_manager.clear_roblox_shader_and_temp_cache()
        self._show_toast(f"Roblox cache cleared: {freed_mb} MB freed")

    def _on_clear_logs_clicked(self) -> None:
        self.sound.play_click()
        _, msg = self.sys_manager.clear_roblox_logs()
        self._show_toast(msg)

    def _on_open_logs_folder_clicked(self) -> None:
        self.sound.play_click()
        _, msg = self.sys_manager.open_launcher_logs_folder()
        self._show_toast(msg)

    def _on_register_protocol_clicked(self) -> None:
        self.sound.play_click()
        _, msg = self.sys_manager.register_rbxclient_protocol()
        self._show_toast(msg)

    def _refresh_self_heal_ui(self) -> None:
        if hasattr(self, "lbl_self_heal_status") and self.lbl_self_heal_status.winfo_exists():
            cnt = self.self_heal.fixes_applied_count if hasattr(self, "self_heal") else 0
            self.lbl_self_heal_status.configure(text=f"SelfHealEngine: исправлений {cnt}")

    def _on_check_updates_clicked(self) -> None:
        self.sound.play_click()
        self._show_toast("Проверка релизов на GitHub...")

        def _worker():
            info = self.api.check_github_latest_version()
            self.after(0, lambda d=info: self._on_update_check_done(d))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_update_check_done(self, info: dict) -> None:
        if info.get("has_update"):
            ver = info.get("latest_version")
            url = info.get("url")
            self._show_toast(f"Доступна версия {ver}! Открываю GitHub...")
            if url and self.security_guard.is_external_url_allowed(str(url)):
                try:
                    webbrowser.open(str(url))
                except Exception:
                    pass
        else:
            self._show_toast(f"Установлена актуальная версия {CURRENT_VERSION}")


def main() -> None:
    try:
        ensure_directories()
        write_launcher_log(f"Старт RBX Client {CURRENT_VERSION} by {PUBLISHER_NAME}")
    except Exception as exc:
        write_crash_fix_log("main.init_dirs", exc)

    try:
        app = RBXClientApp()
        app.mainloop()
    except Exception as exc:
        write_crash_fix_log("main.mainloop", exc)
        try:
            temp_cfg = dict(DEFAULT_CONFIG)
            save_json_safe(CONFIG_PATH, temp_cfg)
            app = RBXClientApp()
            app.mainloop()
        except Exception as retry_exc:
            write_crash_fix_log("main.retry_after_heal", retry_exc)


if __name__ == "__main__":
    main()