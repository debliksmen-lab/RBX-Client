import os
import re
import glob
import math
import json
import wave
import random
import tempfile
import subprocess
import threading
import webbrowser
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import customtkinter as ctk
from PIL import Image, ImageDraw

try:
    import winsound
except ImportError:
    winsound = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "launcher_config.json"
RBX_PHOTOS_DIR = "PhotoRBX"
GAME_PHOTOS_DIR = "PhotoGames"
AVATAR_CACHE_DIR = "AvatarCache"
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")

SEASONS = {
    "Зимний": {
        "title_icon": "❄",
        "banner": "ЗИМНИЙ СЕЗОН • БЫСТРЫЙ ЗАПУСК",
        "decor_frames": ["❄  ❅  ❆", "❆  ❄  ❅", "❅  ❆  ❄"],
        "bulbs": ["#ef4444", "#22c55e", "#38bdf8", "#eab308", "#a855f7", "#ef4444", "#22c55e", "#38bdf8"],
        "neon_left": ["#38bdf8", "#0284c7", "#7dd3fc", "#22d3ee"],
        "neon_right": ["#f43f5e", "#a855f7", "#38bdf8", "#22c55e"],
        "bg_main": "#070d19",
        "bg_sidebar": "#0b1526",
        "bg_card": "#08101e",
        "btn_bg": "#12223a",
        "btn_hover": "#1d365c",
        "accent": "#38bdf8",
        "accent_soft": "#7dd3fc",
        "text_main": "#f0f9ff",
        "text_muted": "#94a3b8",
        "play_bg": "#dc2626",
        "play_hover": "#b91c1c",
        "slides_palette": [
            ("#0c192c", "#1e3a5f", "#38bdf8"),
            ("#1a1025", "#3b1d5e", "#f43f5e"),
            ("#0a221c", "#144538", "#10b981"),
        ],
    },
    "Весенний": {
        "title_icon": "🌸",
        "banner": "ВЕСЕННИЙ СЕЗОН • БЫСТРЫЙ ЗАПУСК",
        "decor_frames": ["🌸  🌿  🍃", "🌿  🍃  🌸", "🍃  🌸  🌿"],
        "bulbs": ["#f472b6", "#4ade80", "#a78bfa", "#facc15", "#34d399", "#f472b6", "#4ade80", "#a78bfa"],
        "neon_left": ["#4ade80", "#22c55e", "#34d399", "#a3e635"],
        "neon_right": ["#f472b6", "#c084fc", "#38bdf8", "#facc15"],
        "bg_main": "#091410",
        "bg_sidebar": "#0e211a",
        "bg_card": "#071711",
        "btn_bg": "#153328",
        "btn_hover": "#1f4d3c",
        "accent": "#4ade80",
        "accent_soft": "#86efac",
        "text_main": "#f0fdf4",
        "text_muted": "#86a898",
        "play_bg": "#16a34a",
        "play_hover": "#15803d",
        "slides_palette": [
            ("#0d241b", "#1b4d3a", "#4ade80"),
            ("#1f1429", "#4a2a66", "#f472b6"),
            ("#10222e", "#1e4661", "#38bdf8"),
        ],
    },
    "Летний": {
        "title_icon": "☀",
        "banner": "ЛЕТНИЙ СЕЗОН • БЫСТРЫЙ ЗАПУСК",
        "decor_frames": ["☀  🌴  🌊", "🌴  🌊  ☀", "🌊  ☀  🌴"],
        "bulbs": ["#fb923c", "#facc15", "#38bdf8", "#2dd4bf", "#f43f5e", "#fb923c", "#facc15", "#38bdf8"],
        "neon_left": ["#facc15", "#fb923c", "#fde047", "#38bdf8"],
        "neon_right": ["#2dd4bf", "#38bdf8", "#f472b6", "#facc15"],
        "bg_main": "#091521",
        "bg_sidebar": "#0e2236",
        "bg_card": "#071421",
        "btn_bg": "#13324f",
        "btn_hover": "#1d4b75",
        "accent": "#facc15",
        "accent_soft": "#fde047",
        "text_main": "#fefce8",
        "text_muted": "#93b4cc",
        "play_bg": "#ea580c",
        "play_hover": "#c2410c",
        "slides_palette": [
            ("#0c243b", "#164e7d", "#facc15"),
            ("#26180c", "#5c3716", "#fb923c"),
            ("#082426", "#115054", "#2dd4bf"),
        ],
    },
    "Осенний": {
        "title_icon": "🍂",
        "banner": "ОСЕННИЙ СЕЗОН • БЫСТРЫЙ ЗАПУСК",
        "decor_frames": ["🍂  🍁  🌫", "🍁  🌫  🍂", "🌫  🍂  🍁"],
        "bulbs": ["#f97316", "#eab308", "#dc2626", "#d97706", "#a16207", "#f97316", "#eab308", "#dc2626"],
        "neon_left": ["#fb923c", "#f97316", "#eab308", "#ef4444"],
        "neon_right": ["#eab308", "#f59e0b", "#fb7185", "#fb923c"],
        "bg_main": "#140e09",
        "bg_sidebar": "#21160e",
        "bg_card": "#120c08",
        "btn_bg": "#362214",
        "btn_hover": "#4f321e",
        "accent": "#fb923c",
        "accent_soft": "#fdba74",
        "text_main": "#fff7ed",
        "text_muted": "#b59d8a",
        "play_bg": "#d97706",
        "play_hover": "#b45309",
        "slides_palette": [
            ("#26170c", "#543118", "#fb923c"),
            ("#291111", "#5c2222", "#ef4444"),
            ("#1f1b10", "#473d22", "#eab308"),
        ],
    },
}


class SoundEngine:
    """Генератор звуков с записью во временные WAV-файлы для надёжного воспроизведения в Windows."""

    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.temp_dir = os.path.join(tempfile.gettempdir(), "rbx_launcher_sounds")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.click_path = os.path.join(self.temp_dir, "soft_click.wav")
        self.startup_path = os.path.join(self.temp_dir, "win7_startup.wav")
        self._ensure_wavs()

    def _write_wav(self, filepath, samples):
        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            frames = bytearray()
            for s in samples:
                val = max(-32767, min(32767, int(s * 32767)))
                frames.extend(val.to_bytes(2, byteorder="little", signed=True))
            wf.writeframes(bytes(frames))

    def _ensure_wavs(self):
        click_dur = 0.055
        click_n = int(self.sample_rate * click_dur)
        click_samples = []
        for i in range(click_n):
            t = i / self.sample_rate
            env = math.exp(-t * 65.0) * min(1.0, i / 35.0)
            freq = 740.0 + 240.0 * math.exp(-t * 40.0)
            w = 0.75 * math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(2 * math.pi * (freq * 2) * t)
            click_samples.append(w * env * 0.16)
        self._write_wav(self.click_path, click_samples)

        startup_dur = 1.45
        startup_n = int(self.sample_rate * startup_dur)
        startup_samples = [0.0] * startup_n
        notes = [
            (0.00, 0.60, 523.25, 0.16),
            (0.12, 0.70, 659.25, 0.15),
            (0.24, 0.80, 783.99, 0.14),
            (0.38, 1.00, 987.77, 0.13),
            (0.54, 0.88, 1046.50, 0.12),
        ]
        for start_t, dur_t, freq, amp in notes:
            start_idx = int(start_t * self.sample_rate)
            end_idx = min(startup_n, int((start_t + dur_t) * self.sample_rate))
            length = max(1, end_idx - start_idx)
            for k in range(length):
                local_t = k / self.sample_rate
                attack = min(1.0, k / (0.045 * self.sample_rate))
                release = math.exp(-local_t * (3.0 / max(0.2, dur_t)))
                env = attack * release
                tone = math.sin(2 * math.pi * freq * local_t) + 0.22 * math.sin(2 * math.pi * (freq * 1.5) * local_t)
                startup_samples[start_idx + k] += tone * env * amp
        self._write_wav(self.startup_path, startup_samples)

    def _play_file(self, path):
        if winsound is None or not os.path.exists(path):
            return
        try:
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
        except Exception:
            try:
                winsound.Beep(780, 45)
            except Exception:
                pass

    def play_click(self, enabled=True):
        if not enabled:
            return
        threading.Thread(target=lambda: self._play_file(self.click_path), daemon=True).start()

    def play_startup(self, enabled=True):
        if not enabled:
            return
        threading.Thread(target=lambda: self._play_file(self.startup_path), daemon=True).start()


class RobloxProfileService:
    """Поиск Roblox Player, локального аккаунта и загрузка профиля + всех друзей."""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.roblox.com/",
    }

    def _get_json(self, url, timeout=10):
        req = urllib.request.Request(url, headers=self.HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))

    def _get_bytes(self, url, timeout=10):
        req = urllib.request.Request(url, headers=self.HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()

    def find_roblox_player(self):
        found_exes = []
        local_app = os.environ.get("LOCALAPPDATA", "")
        candidate_roots = [
            os.path.join(local_app, "Roblox", "Versions"),
            os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "Roblox"),
            os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "Roblox"),
        ]

        for root in candidate_roots:
            if root and os.path.isdir(root):
                for exe_path in glob.glob(os.path.join(root, "**", "RobloxPlayerBeta.exe"), recursive=True):
                    found_exes.append(exe_path)

        found_exes.sort(key=lambda p: os.path.getmtime(p), reverse=True)

        running = False
        try:
            out = subprocess.check_output(
                ["tasklist", "/FI", "IMAGENAME eq RobloxPlayerBeta.exe"],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                text=True,
                errors="ignore"
            )
            running = "RobloxPlayerBeta.exe" in out
        except Exception:
            running = False

        return {
            "installed": len(found_exes) > 0,
            "running": running,
            "latest_exe": found_exes[0] if found_exes else None,
        }

    def detect_local_roblox_account(self):
        local_app = os.environ.get("LOCALAPPDATA", "")
        roblox_dir = os.path.join(local_app, "Roblox")
        if not roblox_dir or not os.path.isdir(roblox_dir):
            return None

        logs_dir = os.path.join(roblox_dir, "logs")
        log_files = []
        if os.path.isdir(logs_dir):
            log_files = sorted(
                glob.glob(os.path.join(logs_dir, "*.log")),
                key=os.path.getmtime,
                reverse=True
            )[:12]

        id_patterns = [
            re.compile(r'"userId"\s*:\s*(\d{3,15})', re.IGNORECASE),
            re.compile(r'"UserId"\s*:\s*(\d{3,15})', re.IGNORECASE),
            re.compile(r'\buserid[:=\s]+(\d{3,15})\b', re.IGNORECASE),
        ]
        name_patterns = [
            re.compile(r'"username"\s*:\s*"([A-Za-z0-9_]{3,20})"', re.IGNORECASE),
            re.compile(r'"UserName"\s*:\s*"([A-Za-z0-9_]{3,20})"', re.IGNORECASE),
            re.compile(r'authenticated user[:\s]+([A-Za-z0-9_]{3,20})', re.IGNORECASE),
        ]

        for path in log_files:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()[-350000:]
                for pat in id_patterns:
                    m = pat.search(text)
                    if m and m.group(1) != "0":
                        return {"user_id": int(m.group(1)), "username": None, "source": os.path.basename(path)}
                for pat in name_patterns:
                    m = pat.search(text)
                    if m:
                        return {"user_id": None, "username": m.group(1), "source": os.path.basename(path)}
            except Exception:
                continue

        return None

    def resolve_user(self, query_text):
        q = (query_text or "").strip()
        if not q:
            return None

        user_id = None
        username = None

        if q.isdigit():
            user_id = int(q)
        else:
            payload = json.dumps({"usernames": [q], "excludeBannedUsers": False}).encode("utf-8")
            hdrs = dict(self.HEADERS)
            hdrs["Content-Type"] = "application/json"
            req = urllib.request.Request(
                "https://users.roblox.com/v1/usernames/users",
                data=payload,
                headers=hdrs
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
            items = data.get("data") or []
            if not items:
                return None
            user_id = int(items[0]["id"])
            username = items[0].get("name")

        details = self._get_json(f"https://users.roblox.com/v1/users/{user_id}")
        return {
            "id": int(details.get("id", user_id)),
            "name": details.get("name") or username or str(user_id),
            "displayName": details.get("displayName") or details.get("name") or str(user_id),
            "description": (details.get("description") or "").strip(),
        }

    def fetch_friends(self, user_id, limit=None):
        """Получает всех доступных друзей пользователя по User ID без искусственной обрезки."""
        endpoints = [
            f"https://friends.roblox.com/v1/users/{user_id}/friends?userSort=DisplayName",
            f"https://friends.roblox.com/v1/users/{user_id}/friends",
        ]
        for url in endpoints:
            try:
                data = self._get_json(url)
                friends = data.get("data") or []
                if isinstance(friends, list):
                    return friends[:limit] if limit else friends, None
            except urllib.error.HTTPError as exc:
                if exc.code in (401, 403):
                    return [], f"API друзей вернул HTTP {exc.code}"
            except Exception:
                continue
        return [], "Список друзей недоступен"

    def fetch_avatars_map(self, user_ids, size="150x150"):
        result = {}
        clean_ids = [int(uid) for uid in user_ids if uid]
        for i in range(0, len(clean_ids), 100):
            chunk = clean_ids[i:i + 100]
            ids_str = ",".join(str(x) for x in chunk)
            url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={ids_str}&size={size}&format=Png&isCircular=false"
            try:
                data = self._get_json(url)
                for item in data.get("data") or []:
                    uid = item.get("targetId")
                    img_url = item.get("imageUrl")
                    if uid and img_url:
                        result[int(uid)] = img_url
            except Exception:
                continue
        return result

    def get_cached_avatar_path(self, user_id, image_url=None):
        os.makedirs(AVATAR_CACHE_DIR, exist_ok=True)
        cache_path = os.path.join(AVATAR_CACHE_DIR, f"user_{user_id}.png")
        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            return cache_path
        if not image_url:
            avatars = self.fetch_avatars_map([user_id], size="150x150")
            image_url = avatars.get(int(user_id))
        if not image_url:
            return None
        raw = self._get_bytes(image_url)
        img = Image.open(io.BytesIO(raw)).convert("RGBA")
        img.save(cache_path, format="PNG")
        return cache_path

    def download_avatars_parallel(self, user_ids, url_map, max_workers=8):
        """Быстро скачивает недостающие аватарки в пуле потоков."""
        paths = {}
        missing = []
        for uid in user_ids:
            p = os.path.join(AVATAR_CACHE_DIR, f"user_{uid}.png")
            if os.path.exists(p) and os.path.getsize(p) > 0:
                paths[uid] = p
            else:
                missing.append(uid)

        if not missing:
            return paths

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(self.get_cached_avatar_path, uid, url_map.get(uid)): uid
                for uid in missing
            }
            for fut in as_completed(futures):
                uid = futures[fut]
                try:
                    p = fut.result()
                    if p:
                        paths[uid] = p
                except Exception:
                    pass
        return paths


class RobloxLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x610")
        self.resizable(False, False)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 500
        y = (self.winfo_screenheight() // 2) - 305
        self.geometry(f"1000x610+{x}+{y}")

        os.makedirs(RBX_PHOTOS_DIR, exist_ok=True)
        os.makedirs(GAME_PHOTOS_DIR, exist_ok=True)
        os.makedirs(AVATAR_CACHE_DIR, exist_ok=True)

        self.sound = SoundEngine()
        self.profile_service = RobloxProfileService()
        self.config_data = self.load_config()
        self.current_slide = 0
        self.game_icons = []
        self.avatar_images = []
        self.slides = []
        self.auto_slide_job = None
        self.decor_job = None
        self.loading_job = None
        self.neon_job = None
        self.restore_job = None
        self.settings_win = None
        self.profile_win = None

        self.apply_window_title()
        if self.config_data.get("show_loading_screen", True):
            self.show_loading_screen()
        else:
            self.build_main_window()

    def current_season_name(self):
        name = self.config_data.get("season", "Зимний")
        return name if name in SEASONS else "Зимний"

    def current_theme(self):
        return SEASONS[self.current_season_name()]

    def apply_window_title(self):
        t = self.current_theme()
        s_name = self.current_season_name()
        low_tag = " • LOW PC" if self.config_data.get("low_end_mode", False) else ""
        self.title(f"{t['title_icon']} RBX Client — {s_name}{low_tag}")

    def load_config(self):
        default_data = {
            "last_place_id": "",
            "last_game_name": "Меню Roblox",
            "season": "Зимний",
            "low_end_mode": False,
            "auto_slide": True,
            "sound_clicks": True,
            "sound_startup": True,
            "show_loading_screen": True,
            "roblox_hide_mode": "Свернуть",
            "restore_delay_sec": 10,
            "profile_query": "",
            "saved_profile": None,
            "saved_friends": [],
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    default_data.update(data)
            except Exception:
                pass
        return default_data

    def save_config(self):
        if hasattr(self, "place_entry") and self.place_entry.winfo_exists():
            self.config_data["last_place_id"] = self.place_entry.get().strip()
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def play_click_sound(self):
        self.sound.play_click(self.config_data.get("sound_clicks", True))

    def find_image_in_folder(self, folder, candidates):
        if not os.path.isdir(folder):
            return None
        for name in candidates:
            for ext in IMAGE_EXTS:
                for variant in (f"{name}{ext}", f"{name}{ext.upper()}"):
                    p = os.path.join(folder, variant)
                    if os.path.exists(p):
                        return p
        return None

    def make_fallback_icon(self, seed_text, size=(28, 28)):
        t = self.current_theme()
        rng = random.Random(seed_text)
        bg = t["btn_bg"]
        fg = rng.choice([t["accent"], t["accent_soft"], "#e2e8f0"])
        w, h = size
        img = Image.new("RGB", (w, h), bg)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([2, 2, w - 2, h - 2], radius=6, outline=fg, width=2)
        cx, cy = w // 2, h // 2
        r = max(3, min(w, h) // 6)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fg)
        icon = ctk.CTkImage(light_image=img, dark_image=img, size=size)
        self.game_icons.append(icon)
        return icon

    def load_game_icon(self, label, place_id, key_name):
        candidates = []
        if key_name:
            candidates.append(key_name)
        if place_id:
            candidates.append(str(place_id))
        candidates.append(label)

        img_path = self.find_image_in_folder(GAME_PHOTOS_DIR, candidates)
        if img_path:
            try:
                resample = Image.Resampling.NEAREST if self.config_data.get("low_end_mode") else Image.Resampling.LANCZOS
                img = Image.open(img_path).convert("RGB").resize((30, 30), resample)
                icon = ctk.CTkImage(light_image=img, dark_image=img, size=(30, 30))
                self.game_icons.append(icon)
                return icon
            except Exception:
                pass
        return self.make_fallback_icon(f"{label}_{place_id}", size=(28, 28))

    def load_avatar_ctk_image(self, cache_path, seed_text, size=(46, 46)):
        if cache_path and os.path.exists(cache_path):
            try:
                resample = Image.Resampling.NEAREST if self.config_data.get("low_end_mode") else Image.Resampling.LANCZOS
                img = Image.open(cache_path).convert("RGB").resize(size, resample)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                self.avatar_images.append(ctk_img)
                return ctk_img
            except Exception:
                pass
        return self.make_fallback_icon(seed_text, size=size)

    def load_slides(self):
        t = self.current_theme()
        slides = []
        slide_name_sets = [
            ["1", "bg1", "slide1", "rbx1"],
            ["2", "bg2", "slide2", "rbx2"],
            ["3", "bg3", "slide3", "rbx3"],
        ]

        extra_files = []
        if os.path.isdir(RBX_PHOTOS_DIR):
            for fname in sorted(os.listdir(RBX_PHOTOS_DIR)):
                if fname.lower().endswith(IMAGE_EXTS):
                    extra_files.append(os.path.join(RBX_PHOTOS_DIR, fname))

        for idx in range(3):
            img_path = self.find_image_in_folder(RBX_PHOTOS_DIR, slide_name_sets[idx])
            if not img_path and idx < len(extra_files):
                img_path = extra_files[idx]

            img = None
            if img_path:
                try:
                    resample = Image.Resampling.NEAREST if self.config_data.get("low_end_mode") else Image.Resampling.LANCZOS
                    img = Image.open(img_path).convert("RGB").resize((650, 340), resample)
                except Exception:
                    img = None

            if img is None:
                c1, c2, accent = t["slides_palette"][idx]
                img = Image.new("RGB", (650, 340), c1)
                draw = ImageDraw.Draw(img)
                r1, g1, b1 = tuple(int(c1.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
                r2, g2, b2 = tuple(int(c2.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
                for y in range(340):
                    ratio = y / 340
                    r = int(r1 + (r2 - r1) * ratio)
                    g = int(g1 + (g2 - g1) * ratio)
                    b = int(b1 + (b2 - b1) * ratio)
                    draw.line([(0, y), (650, y)], fill=(r, g, b))

                rng = random.Random(idx * 77 + len(self.current_season_name()))
                dots_count = 15 if self.config_data.get("low_end_mode") else 45
                for _ in range(dots_count):
                    sx = rng.randint(15, 635)
                    sy = rng.randint(15, 325)
                    sr = rng.randint(1, 3)
                    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill="#e2e8f0")

                draw.rectangle([14, 14, 636, 326], outline=accent, width=2)
                draw.text((28, 298), f"PhotoRBX // SLIDE 0{idx + 1}", fill="#cbd5e1")

            slides.append(ctk.CTkImage(light_image=img, dark_image=img, size=(650, 340)))
        return slides

    def show_loading_screen(self):
        t = self.current_theme()
        self.loading_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=t["bg_main"])
        self.loading_frame.pack(fill="both", expand=True)

        left_rail = ctk.CTkFrame(self.loading_frame, width=18, fg_color="transparent")
        left_rail.pack(side="left", fill="y", padx=(14, 0), pady=28)
        left_rail.pack_propagate(False)

        right_rail = ctk.CTkFrame(self.loading_frame, width=18, fg_color="transparent")
        right_rail.pack(side="right", fill="y", padx=(0, 14), pady=28)
        right_rail.pack_propagate(False)

        self.left_neon_bars = []
        self.right_neon_bars = []
        for _ in range(7):
            lb = ctk.CTkFrame(left_rail, width=10, height=58, corner_radius=5, fg_color=t["btn_bg"])
            lb.pack(pady=6)
            self.left_neon_bars.append(lb)

            rb = ctk.CTkFrame(right_rail, width=10, height=58, corner_radius=5, fg_color=t["btn_bg"])
            rb.pack(pady=6)
            self.right_neon_bars.append(rb)

        center_box = ctk.CTkFrame(self.loading_frame, fg_color="transparent")
        center_box.pack(expand=True)

        ctk.CTkLabel(
            center_box,
            text=f"{t['title_icon']}  RBX CLIENT  {t['title_icon']}",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=t["text_main"]
        ).pack(pady=(35, 6))

        ctk.CTkLabel(
            center_box,
            text=f"{self.current_season_name().upper()} MODE • 2026",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t["accent"]
        ).pack(pady=(0, 26))

        self.loading_status = ctk.CTkLabel(
            center_box,
            text="0% • Подготовка...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=t["text_muted"]
        )
        self.loading_status.pack(pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(
            center_box,
            width=440,
            height=14,
            corner_radius=7,
            fg_color=t["btn_bg"],
            progress_color=t["accent"]
        )
        self.progress_bar.set(0)
        self.progress_bar.pack()

        self.progress_percent_label = ctk.CTkLabel(
            center_box,
            text="0%",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["accent_soft"]
        )
        self.progress_percent_label.pack(pady=(12, 0))

        self.progress_float = 0.0
        self.neon_phase = 0.0
        self.animate_neon_bars()
        self.run_loading_step()

    def animate_neon_bars(self):
        if not hasattr(self, "loading_frame") or not self.loading_frame.winfo_exists():
            return
        t = self.current_theme()
        dim = t["btn_bg"]
        left_cols = t["neon_left"]
        right_cols = t["neon_right"]

        total = len(self.left_neon_bars)
        idx_l = int(self.neon_phase) % total
        idx_r = (total - 1 - int(self.neon_phase)) % total

        for i in range(total):
            dl = min((i - idx_l) % total, (idx_l - i) % total)
            if dl == 0:
                col_l = left_cols[i % len(left_cols)]
            elif dl == 1:
                col_l = t["accent_soft"]
            else:
                col_l = dim
            self.left_neon_bars[i].configure(fg_color=col_l)

            dr = min((i - idx_r) % total, (idx_r - i) % total)
            if dr == 0:
                col_r = right_cols[i % len(right_cols)]
            elif dr == 1:
                col_r = t["accent"]
            else:
                col_r = dim
            self.right_neon_bars[i].configure(fg_color=col_r)

        self.neon_phase = (self.neon_phase + 0.35) % total
        self.neon_job = self.after(32, self.animate_neon_bars)

    def run_loading_step(self):
        steps = [
            "Проверка папок PhotoRBX и PhotoGames...",
            "Загрузка аватарок режимов...",
            "Инициализация сезонной темы...",
            "Запуск интерфейса..."
        ]
        if self.progress_float < 100.0:
            # Плавное замедление ближе к 100%
            remaining = 100.0 - self.progress_float
            step_delta = max(0.45, min(1.8, remaining * 0.035))
            if self.config_data.get("low_end_mode"):
                step_delta *= 1.6
            self.progress_float = min(100.0, self.progress_float + step_delta)
            pct = int(round(self.progress_float))
            self.progress_bar.set(self.progress_float / 100.0)
            msg_index = min(pct // 26, len(steps) - 1)
            self.loading_status.configure(text=steps[msg_index])
            self.progress_percent_label.configure(text=f"{pct}%")
            self.loading_job = self.after(24, self.run_loading_step)
        else:
            self.progress_bar.set(1.0)
            self.progress_percent_label.configure(text="100%")
            if self.neon_job:
                self.after_cancel(self.neon_job)
                self.neon_job = None
            self.sound.play_startup(self.config_data.get("sound_startup", True))
            self.loading_job = self.after(180, self._finish_loading)

    def _finish_loading(self):
        if hasattr(self, "loading_frame") and self.loading_frame.winfo_exists():
            self.loading_frame.destroy()
        self.build_main_window()

    def rebuild_ui(self):
        self.stop_jobs()
        self.game_icons = []
        self.avatar_images = []
        self.slides = self.load_slides()
        self.apply_window_title()
        for widget in self.winfo_children():
            widget.destroy()
        self.build_main_window()

    def stop_jobs(self):
        for job_attr in ("auto_slide_job", "decor_job", "loading_job", "neon_job", "restore_job"):
            job = getattr(self, job_attr, None)
            if job:
                self.after_cancel(job)
                setattr(self, job_attr, None)

    def build_main_window(self):
        t = self.current_theme()
        self.slides = self.load_slides()
        self.current_slide = self.current_slide % len(self.slides)

        sidebar = ctk.CTkFrame(self, width=305, corner_radius=0, fg_color=t["bg_sidebar"])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        garland = ctk.CTkFrame(sidebar, fg_color="transparent", height=24)
        garland.pack(fill="x", padx=16, pady=(12, 2))
        for col in t["bulbs"]:
            dot = ctk.CTkLabel(garland, text="●", text_color=col, font=ctk.CTkFont(size=13))
            dot.pack(side="left", expand=True)

        header_row = ctk.CTkFrame(sidebar, fg_color="transparent")
        header_row.pack(fill="x", padx=14, pady=(6, 8))

        ctk.CTkLabel(
            header_row,
            text=f"{t['title_icon']} RBX",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=t["text_main"]
        ).pack(side="left")

        ctk.CTkButton(
            header_row,
            text="⚙",
            width=36,
            height=30,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            text_color=t["accent_soft"],
            command=lambda: (self.play_click_sound(), self.open_settings_window())
        ).pack(side="right")

        ctk.CTkButton(
            header_row,
            text="👤 Профиль",
            width=96,
            height=30,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            text_color=t["accent_soft"],
            command=lambda: (self.play_click_sound(), self.open_profile_window())
        ).pack(side="right", padx=(0, 6))

        ctk.CTkLabel(
            sidebar,
            text="РЕЖИМЫ И СЕРВЕРА",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=t["accent_soft"]
        ).pack(anchor="w", padx=18, pady=(0, 6))

        games_scroll = ctk.CTkScrollableFrame(
            sidebar,
            fg_color=t["bg_card"],
            corner_radius=10,
            scrollbar_button_color=t["btn_bg"],
            scrollbar_button_hover_color=t["accent"]
        )
        games_scroll.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        presets = [
            ("Меню Roblox", "", "roblox_menu"),
            ("Сан-Аури", "104841616983113", "SanAuru"),
            ("Слово пацана РП", "18537219148", "SlovoPatsana"),
            ("[Большое обновление] Симулятор автомобильных аварий V3", "103589142326933", "CCSV3"),
            ("【ОБНОВЛЕНИЕ КАРТЫ】 Чечня 1994", "3279760276", "Chechnya"),
            ("Brookhaven RP", "4924922222", "Brookhaven"),
            ("Blox Fruits", "2753915549", "BloxFruit"),
            ("Murder Mystery 2", "142823291", "MurderMistery2"),
            ("Adopt Me!", "920587237", "AdoptMe"),
            ("Tower of Hell", "1962086868", "TowerOfHell"),
            ("BedWars", "6872265039", "BedWars"),
            ("Doors", "6516141723", "Doors"),
            ("Blade Ball", "13772394625", "BladeBall"),
            ("The Strongest Battlegrounds", "10449761463", "TheStrongestBattleGrounds"),
            ("Dress To Impress", "15101393044", "DressToImpress"),
        ]

        for label, place_id, key_name in presets:
            short_label = label if len(label) <= 27 else label[:25] + "..."
            icon = self.load_game_icon(label, place_id, key_name)
            btn = ctk.CTkButton(
                games_scroll,
                text=f" {short_label}",
                image=icon,
                compound="left",
                anchor="w",
                height=38,
                font=ctk.CTkFont(size=12),
                fg_color=t["btn_bg"],
                hover_color=t["btn_hover"],
                text_color=t["text_main"],
                command=lambda n=label, p=place_id: (self.play_click_sound(), self.choose_preset(n, p))
            )
            btn.pack(fill="x", padx=4, pady=3)

        saved_prof = self.config_data.get("saved_profile")
        prof_tag = f" • @{saved_prof['name']}" if isinstance(saved_prof, dict) and saved_prof.get("name") else ""
        status_text = f"Выбрано: {self.config_data.get('last_game_name', 'Меню Roblox')}{prof_tag}"
        if self.config_data.get("low_end_mode"):
            status_text += "  [Слабый ПК]"

        self.active_mode_label = ctk.CTkLabel(
            sidebar,
            text=status_text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=t["accent_soft"],
            wraplength=270,
            justify="left"
        )
        self.active_mode_label.pack(side="bottom", anchor="w", padx=18, pady=(4, 14))

        content = ctk.CTkFrame(self, corner_radius=0, fg_color=t["bg_main"])
        content.pack(side="right", fill="both", expand=True)

        top_bar = ctk.CTkFrame(content, fg_color="transparent")
        top_bar.pack(fill="x", padx=28, pady=(16, 8))

        ctk.CTkLabel(
            top_bar,
            text=f"✦ {t['banner']}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=t["accent_soft"]
        ).pack(side="left")

        self.decor_ticker = ctk.CTkLabel(
            top_bar,
            text=t["decor_frames"][0],
            font=ctk.CTkFont(size=14),
            text_color=t["accent"]
        )
        self.decor_ticker.pack(side="right")

        self.slide_box = ctk.CTkLabel(content, text="", image=self.slides[self.current_slide], corner_radius=12)
        self.slide_box.pack(pady=(6, 10))

        controls = ctk.CTkFrame(content, fg_color="transparent")
        controls.pack()

        ctk.CTkButton(
            controls,
            text="◀",
            width=44,
            height=30,
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            command=lambda: (self.play_click_sound(), self.prev_slide())
        ).pack(side="left", padx=6)

        self.slide_info = ctk.CTkLabel(
            controls,
            text=f"{self.current_slide + 1} / {len(self.slides)}",
            text_color=t["text_muted"],
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.slide_info.pack(side="left", padx=12)

        ctk.CTkButton(
            controls,
            text="▶",
            width=44,
            height=30,
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            command=lambda: (self.play_click_sound(), self.next_slide())
        ).pack(side="left", padx=6)

        launch_panel = ctk.CTkFrame(
            content,
            fg_color=t["bg_sidebar"],
            border_width=1,
            border_color=t["btn_bg"],
            height=96,
            corner_radius=14
        )
        launch_panel.pack(fill="x", padx=28, pady=(20, 18))
        launch_panel.pack_propagate(False)

        self.place_entry = ctk.CTkEntry(
            launch_panel,
            placeholder_text="ID плейса (пусто = обычное меню)",
            fg_color=t["bg_main"],
            border_color=t["btn_bg"],
            width=290,
            height=44
        )
        last_id = self.config_data.get("last_place_id", "")
        if last_id:
            self.place_entry.insert(0, last_id)
        self.place_entry.pack(side="left", padx=18)

        self.launch_status = ctk.CTkLabel(
            launch_panel,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4ade80"
        )
        self.launch_status.pack(side="left")

        ctk.CTkButton(
            launch_panel,
            text=f"{t['title_icon']}  ИГРАТЬ",
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color=t["play_bg"],
            hover_color=t["play_hover"],
            width=195,
            height=48,
            corner_radius=10,
            command=lambda: (self.play_click_sound(), self.start_roblox())
        ).pack(side="right", padx=18)

        if self.config_data.get("auto_slide", True):
            self.schedule_auto_slide()
        if not self.config_data.get("low_end_mode", False):
            self.animate_decor()

    def open_profile_window(self):
        if self.profile_win and self.profile_win.winfo_exists():
            self.profile_win.focus()
            return

        t = self.current_theme()
        win = ctk.CTkToplevel(self)
        self.profile_win = win
        win.title("Профиль и друзья Roblox")
        win.geometry("620x650")
        win.resizable(False, False)
        win.configure(fg_color=t["bg_main"])
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="👤 ПРОФИЛЬ И ДРУЗЬЯ",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["text_main"]
        ).pack(pady=(14, 8))

        search_box = ctk.CTkFrame(win, fg_color=t["bg_sidebar"], corner_radius=12)
        search_box.pack(fill="x", padx=18, pady=6)

        row1 = ctk.CTkFrame(search_box, fg_color="transparent")
        row1.pack(fill="x", padx=12, pady=(12, 8))

        profile_entry = ctk.CTkEntry(
            row1,
            placeholder_text="Ник или User ID игрока Roblox...",
            fg_color=t["bg_main"],
            border_color=t["btn_bg"],
            height=36
        )
        init_q = self.config_data.get("profile_query") or ""
        if not init_q and isinstance(self.config_data.get("saved_profile"), dict):
            init_q = self.config_data["saved_profile"].get("name", "")
        if init_q:
            profile_entry.insert(0, init_q)
        profile_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        fetch_btn = ctk.CTkButton(
            row1,
            text="Загрузить",
            width=105,
            height=36,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=t["play_bg"],
            hover_color=t["play_hover"]
        )
        fetch_btn.pack(side="left", padx=(0, 6))

        auto_btn = ctk.CTkButton(
            row1,
            text="Найти в Roblox",
            width=125,
            height=36,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            text_color=t["accent_soft"]
        )
        auto_btn.pack(side="left")

        add_row = ctk.CTkFrame(search_box, fg_color="transparent")
        add_row.pack(fill="x", padx=12, pady=(0, 8))

        target_friend_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Ник или ID игрока, чтобы открыть профиль для добавления в друзья",
            fg_color=t["bg_main"],
            border_color=t["btn_bg"],
            height=32,
            font=ctk.CTkFont(size=11)
        )
        target_friend_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        def open_target_profile():
            self.play_click_sound()
            val = target_friend_entry.get().strip()
            if not val:
                status_lbl.configure(text="Введи ник или ID игрока", text_color="#facc15")
                return
            status_lbl.configure(text="Поиск игрока...", text_color=t["text_muted"])

            def worker():
                try:
                    info = self.profile_service.resolve_user(val)
                    if info:
                        url = f"https://www.roblox.com/users/{info['id']}/profile"
                        webbrowser.open(url)
                        self.after(0, lambda: status_lbl.configure(
                            text=f"Открыт профиль {info['name']} ({info['id']}) — можно кинуть запрос в друзья",
                            text_color="#4ade80"
                        ))
                    else:
                        self.after(0, lambda: status_lbl.configure(
                            text="Игрок не найден", text_color="#f87171"
                        ))
                except Exception as exc:
                    self.after(0, lambda e=exc: status_lbl.configure(
                        text=f"Ошибка сети: {e}", text_color="#f87171"
                    ))

            threading.Thread(target=worker, daemon=True).start()

        ctk.CTkButton(
            add_row,
            text="Открыть профиль",
            width=130,
            height=32,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            text_color=t["accent_soft"],
            command=open_target_profile
        ).pack(side="left")

        status_lbl = ctk.CTkLabel(
            search_box,
            text="Проверка Roblox Player...",
            font=ctk.CTkFont(size=11),
            text_color=t["text_muted"],
            anchor="w"
        )
        status_lbl.pack(fill="x", padx=12, pady=(0, 10))

        card = ctk.CTkFrame(win, fg_color=t["bg_sidebar"], corner_radius=12)
        card.pack(fill="x", padx=18, pady=6)

        self.avatar_images = []
        default_av = self.make_fallback_icon("profile_default", size=(64, 64))
        prof_avatar_lbl = ctk.CTkLabel(card, text="", image=default_av)
        prof_avatar_lbl.pack(side="left", padx=14, pady=12)

        prof_text_box = ctk.CTkFrame(card, fg_color="transparent")
        prof_text_box.pack(side="left", fill="both", expand=True, pady=12, padx=(0, 12))

        prof_title_lbl = ctk.CTkLabel(
            prof_text_box,
            text="Аккаунт не выбран",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=t["text_main"],
            anchor="w"
        )
        prof_title_lbl.pack(fill="x")

        prof_meta_lbl = ctk.CTkLabel(
            prof_text_box,
            text="ID: — • Друзей: —",
            font=ctk.CTkFont(size=12),
            text_color=t["accent_soft"],
            anchor="w"
        )
        prof_meta_lbl.pack(fill="x", pady=(2, 2))

        prof_bio_lbl = ctk.CTkLabel(
            prof_text_box,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=t["text_muted"],
            anchor="w",
            justify="left",
            wraplength=440
        )
        prof_bio_lbl.pack(fill="x")

        ctk.CTkLabel(
            win,
            text="ДРУЗЬЯ АККАУНТА (С АВАТАРКАМИ)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=t["accent_soft"]
        ).pack(anchor="w", padx=20, pady=(8, 4))

        friends_scroll = ctk.CTkScrollableFrame(
            win,
            fg_color=t["bg_card"],
            corner_radius=12,
            scrollbar_button_color=t["btn_bg"],
            scrollbar_button_hover_color=t["accent"]
        )
        friends_scroll.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        def render_profile_and_friends(profile_info, friends_list, avatar_paths):
            if not win.winfo_exists():
                return
            for w in friends_scroll.winfo_children():
                w.destroy()

            if not profile_info:
                prof_title_lbl.configure(text="Аккаунт не выбран")
                prof_meta_lbl.configure(text="ID: — • Друзей: —")
                prof_bio_lbl.configure(text="")
                return

            uid = profile_info["id"]
            av_img = self.load_avatar_ctk_image(avatar_paths.get(uid), f"u_{uid}", size=(64, 64))
            prof_avatar_lbl.configure(image=av_img)
            prof_title_lbl.configure(text=f"{profile_info['displayName']} (@{profile_info['name']})")
            prof_meta_lbl.configure(text=f"User ID: {uid}  •  Друзей загружено: {len(friends_list)}")
            bio = profile_info.get("description") or "Описание профиля пустое"
            if len(bio) > 130:
                bio = bio[:127] + "..."
            prof_bio_lbl.configure(text=bio)

            if not friends_list:
                ctk.CTkLabel(
                    friends_scroll,
                    text="Список друзей пуст или скрыт настройками приватности.",
                    font=ctk.CTkFont(size=12),
                    text_color=t["text_muted"]
                ).pack(pady=24)
                return

            for fr in friends_list:
                f_id = fr.get("id")
                f_name = fr.get("name") or f"User_{f_id}"
                f_disp = fr.get("displayName") or f_name
                row = ctk.CTkFrame(friends_scroll, fg_color=t["btn_bg"], corner_radius=10)
                row.pack(fill="x", padx=6, pady=4)

                f_av = self.load_avatar_ctk_image(avatar_paths.get(f_id), f"fr_{f_id}", size=(42, 42))
                ctk.CTkLabel(row, text="", image=f_av).pack(side="left", padx=8, pady=6)

                txt = ctk.CTkFrame(row, fg_color="transparent")
                txt.pack(side="left", fill="both", expand=True, pady=6)
                ctk.CTkLabel(
                    txt,
                    text=f"{f_disp}",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=t["text_main"],
                    anchor="w"
                ).pack(fill="x")
                ctk.CTkLabel(
                    txt,
                    text=f"@{f_name}  •  ID: {f_id}",
                    font=ctk.CTkFont(size=11),
                    text_color=t["text_muted"],
                    anchor="w"
                ).pack(fill="x")

                ctk.CTkButton(
                    row,
                    text="Профиль",
                    width=82,
                    height=28,
                    font=ctk.CTkFont(size=11, weight="bold"),
                    fg_color=t["bg_sidebar"],
                    hover_color=t["btn_hover"],
                    text_color=t["accent_soft"],
                    command=lambda pid=f_id: (
                        self.play_click_sound(),
                        webbrowser.open(f"https://www.roblox.com/users/{pid}/profile")
                    )
                ).pack(side="right", padx=10)

        def load_by_query(q_text, play_snd=True):
            if play_snd:
                self.play_click_sound()
            q_clean = (q_text or "").strip()
            if not q_clean:
                status_lbl.configure(text="Введи никнейм или User ID", text_color="#facc15")
                return
            status_lbl.configure(text="Загрузка профиля, всех друзей и фото...", text_color=t["accent_soft"])

            def worker():
                try:
                    prof = self.profile_service.resolve_user(q_clean)
                    if not prof:
                        self.after(0, lambda: status_lbl.configure(
                            text="Аккаунт Roblox не найден", text_color="#f87171"
                        ))
                        return
                    friends, friends_err = self.profile_service.fetch_friends(prof["id"], limit=None)
                    all_ids = [prof["id"]] + [f.get("id") for f in friends if f.get("id")]
                    url_map = self.profile_service.fetch_avatars_map(all_ids, size="150x150")
                    paths = self.profile_service.download_avatars_parallel(all_ids, url_map, max_workers=8)

                    self.config_data["profile_query"] = prof["name"]
                    self.config_data["saved_profile"] = prof
                    self.config_data["saved_friends"] = friends
                    self.save_config()

                    msg = f"Готово: @{prof['name']} • друзей: {len(friends)}"
                    if friends_err:
                        msg += f" ({friends_err})"

                    self.after(0, lambda m=msg: (
                        render_profile_and_friends(prof, friends, paths),
                        self.rebuild_status_label(),
                        status_lbl.configure(text=m, text_color="#4ade80" if not friends_err else "#facc15")
                    ))
                except Exception as exc:
                    self.after(0, lambda e=exc: status_lbl.configure(
                        text=f"Не удалось загрузить: {e}", text_color="#f87171"
                    ))

            threading.Thread(target=worker, daemon=True).start()

        def detect_from_roblox(play_snd=True):
            if play_snd:
                self.play_click_sound()
            status_lbl.configure(text="Поиск Roblox Player и аккаунта на ПК...", text_color=t["accent_soft"])

            def worker():
                player_info = self.profile_service.find_roblox_player()
                player_note = (
                    "Roblox Player найден (запущен)" if player_info.get("running")
                    else ("Roblox Player найден" if player_info.get("installed") else "Roblox Player не найден")
                )
                found = self.profile_service.detect_local_roblox_account()
                if not found:
                    self.after(0, lambda: status_lbl.configure(
                        text=f"{player_note} • Аккаунт в логах не виден — введи ник/ID вручную",
                        text_color="#facc15"
                    ))
                    return
                q_val = str(found["user_id"]) if found.get("user_id") else str(found.get("username"))
                self.after(0, lambda: (
                    profile_entry.delete(0, "end"),
                    profile_entry.insert(0, q_val),
                    status_lbl.configure(text=f"{player_note} • Найден {q_val}, загружаю...", text_color=t["accent_soft"]),
                    load_by_query(q_val, play_snd=False)
                ))

            threading.Thread(target=worker, daemon=True).start()

        fetch_btn.configure(command=lambda: load_by_query(profile_entry.get(), play_snd=True))
        auto_btn.configure(command=lambda: detect_from_roblox(play_snd=True))

        saved_p = self.config_data.get("saved_profile")
        saved_f = self.config_data.get("saved_friends") or []
        if isinstance(saved_p, dict) and saved_p.get("id"):
            cached_paths = {}
            for uid in [saved_p["id"]] + [x.get("id") for x in saved_f if x.get("id")]:
                p = os.path.join(AVATAR_CACHE_DIR, f"user_{uid}.png")
                if os.path.exists(p):
                    cached_paths[uid] = p
            render_profile_and_friends(saved_p, saved_f, cached_paths)
            player_info = self.profile_service.find_roblox_player()
            p_txt = "Roblox Player запущен" if player_info.get("running") else ("Roblox Player найден" if player_info.get("installed") else "Roblox Player не найден")
            status_lbl.configure(text=f"{p_txt} • Показан сохранённый профиль @{saved_p['name']}", text_color=t["text_muted"])
        else:
            detect_from_roblox(play_snd=False)

    def rebuild_status_label(self):
        if hasattr(self, "active_mode_label") and self.active_mode_label.winfo_exists():
            saved_prof = self.config_data.get("saved_profile")
            prof_tag = f" • @{saved_prof['name']}" if isinstance(saved_prof, dict) and saved_prof.get("name") else ""
            low_tag = "  [Слабый ПК]" if self.config_data.get("low_end_mode") else ""
            game_name = self.config_data.get("last_game_name", "Меню Roblox")
            self.active_mode_label.configure(text=f"Выбрано: {game_name}{prof_tag}{low_tag}")

    def open_settings_window(self):
        if self.settings_win and self.settings_win.winfo_exists():
            self.settings_win.focus()
            return

        t = self.current_theme()
        win = ctk.CTkToplevel(self)
        self.settings_win = win
        win.title("Настройки лаунчера")
        win.geometry("500x610")
        win.resizable(False, False)
        win.configure(fg_color=t["bg_main"])
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="⚙ НАСТРОЙКИ",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=t["text_main"]
        ).pack(pady=(16, 10))

        scroll = ctk.CTkScrollableFrame(
            win,
            fg_color="transparent",
            scrollbar_button_color=t["btn_bg"],
            scrollbar_button_hover_color=t["accent"]
        )
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        season_box = ctk.CTkFrame(scroll, fg_color=t["bg_sidebar"], corner_radius=12)
        season_box.pack(fill="x", padx=4, pady=6)

        ctk.CTkLabel(
            season_box,
            text="Время года / тема лаунчера:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=t["accent_soft"]
        ).pack(anchor="w", padx=14, pady=(10, 6))

        season_var = ctk.StringVar(value=self.current_season_name())
        ctk.CTkSegmentedButton(
            season_box,
            values=["Зимний", "Весенний", "Летний", "Осенний"],
            variable=season_var,
            selected_color=t["play_bg"],
            selected_hover_color=t["play_hover"],
            unselected_color=t["btn_bg"],
            unselected_hover_color=t["btn_hover"],
            command=lambda _: self.play_click_sound()
        ).pack(fill="x", padx=14, pady=(0, 12))

        launch_box = ctk.CTkFrame(scroll, fg_color=t["bg_sidebar"], corner_radius=12)
        launch_box.pack(fill="x", padx=4, pady=6)

        ctk.CTkLabel(
            launch_box,
            text="Окно лаунчера при запуске Roblox:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=t["accent_soft"]
        ).pack(anchor="w", padx=14, pady=(10, 6))

        hide_mode_var = ctk.StringVar(value=self.config_data.get("roblox_hide_mode", "Свернуть"))
        ctk.CTkSegmentedButton(
            launch_box,
            values=["Свернуть", "Скрыть и вернуть", "Не трогать"],
            variable=hide_mode_var,
            selected_color=t["play_bg"],
            selected_hover_color=t["play_hover"],
            unselected_color=t["btn_bg"],
            unselected_hover_color=t["btn_hover"],
            command=lambda _: self.play_click_sound()
        ).pack(fill="x", padx=14, pady=(0, 8))

        delay_row = ctk.CTkFrame(launch_box, fg_color="transparent")
        delay_row.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkLabel(
            delay_row,
            text="Вернуть скрытое окно через:",
            font=ctk.CTkFont(size=12),
            text_color=t["text_main"]
        ).pack(side="left")

        delay_var = ctk.StringVar(value=f"{self.config_data.get('restore_delay_sec', 10)} сек")
        ctk.CTkOptionMenu(
            delay_row,
            values=["5 сек", "10 сек", "20 сек", "30 сек"],
            variable=delay_var,
            width=110,
            fg_color=t["btn_bg"],
            button_color=t["btn_hover"],
            button_hover_color=t["accent"],
            command=lambda _: self.play_click_sound()
        ).pack(side="right")

        media_box = ctk.CTkFrame(scroll, fg_color=t["bg_sidebar"], corner_radius=12)
        media_box.pack(fill="x", padx=4, pady=6)

        click_snd_var = ctk.BooleanVar(value=self.config_data.get("sound_clicks", True))
        startup_snd_var = ctk.BooleanVar(value=self.config_data.get("sound_startup", True))
        loading_scr_var = ctk.BooleanVar(value=self.config_data.get("show_loading_screen", True))

        ctk.CTkSwitch(
            media_box,
            text="Тихий звук «тынь» при нажатии кнопок",
            variable=click_snd_var,
            progress_color=t["accent"],
            text_color=t["text_main"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.sound.play_click(click_snd_var.get())
        ).pack(anchor="w", padx=14, pady=(12, 6))

        ctk.CTkSwitch(
            media_box,
            text="Звук запуска в стиле Windows 7 на 100%",
            variable=startup_snd_var,
            progress_color=t["accent"],
            text_color=t["text_main"],
            font=ctk.CTkFont(size=12),
            command=lambda: self.play_click_sound()
        ).pack(anchor="w", padx=14, pady=6)

        ctk.CTkSwitch(
            media_box,
            text="Экран загрузки (0–100%) с неоном по бокам",
            variable=loading_scr_var,
            progress_color=t["accent"],
            text_color=t["text_main"],
            font=ctk.CTkFont(size=12),
            command=lambda: self.play_click_sound()
        ).pack(anchor="w", padx=14, pady=6)

        test_row = ctk.CTkFrame(media_box, fg_color="transparent")
        test_row.pack(fill="x", padx=14, pady=(4, 12))

        ctk.CTkButton(
            test_row,
            text="🔊 Тест звука запуска",
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            text_color=t["accent_soft"],
            command=lambda: self.sound.play_startup(True)
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            test_row,
            text="🔔 Тест клика",
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=t["btn_bg"],
            hover_color=t["btn_hover"],
            text_color=t["accent_soft"],
            command=lambda: self.sound.play_click(True)
        ).pack(side="left")

        perf_box = ctk.CTkFrame(scroll, fg_color=t["bg_sidebar"], corner_radius=12)
        perf_box.pack(fill="x", padx=4, pady=6)

        low_var = ctk.BooleanVar(value=self.config_data.get("low_end_mode", False))
        auto_var = ctk.BooleanVar(value=self.config_data.get("auto_slide", True))

        ctk.CTkSwitch(
            perf_box,
            text="Режим слабого ПК (меньше анимаций и нагрузки)",
            variable=low_var,
            progress_color=t["accent"],
            text_color=t["text_main"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.play_click_sound()
        ).pack(anchor="w", padx=14, pady=(12, 6))

        ctk.CTkSwitch(
            perf_box,
            text="Автопереключение слайдов каждые 5 сек",
            variable=auto_var,
            progress_color=t["accent"],
            text_color=t["text_main"],
            font=ctk.CTkFont(size=12),
            command=lambda: self.play_click_sound()
        ).pack(anchor="w", padx=14, pady=(0, 6))

        ctk.CTkLabel(
            perf_box,
            text="Подсказка: в самом Roblox поставь графику на 2–3\nв меню игры (Esc → Settings → Graphics Mode: Manual).",
            font=ctk.CTkFont(size=11),
            text_color=t["text_muted"],
            justify="left"
        ).pack(anchor="w", padx=14, pady=(0, 12))

        def apply_and_close():
            self.play_click_sound()
            self.config_data["season"] = season_var.get()
            self.config_data["roblox_hide_mode"] = hide_mode_var.get()
            try:
                self.config_data["restore_delay_sec"] = int(delay_var.get().split()[0])
            except Exception:
                self.config_data["restore_delay_sec"] = 10
            self.config_data["sound_clicks"] = bool(click_snd_var.get())
            self.config_data["sound_startup"] = bool(startup_snd_var.get())
            self.config_data["show_loading_screen"] = bool(loading_scr_var.get())
            self.config_data["low_end_mode"] = bool(low_var.get())
            self.config_data["auto_slide"] = bool(auto_var.get())
            self.save_config()
            win.destroy()
            self.settings_win = None
            self.rebuild_ui()

        ctk.CTkButton(
            win,
            text="Сохранить и применить",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=t["play_bg"],
            hover_color=t["play_hover"],
            command=apply_and_close
        ).pack(fill="x", padx=20, pady=(6, 14))

    def animate_decor(self):
        t = self.current_theme()
        frames = t["decor_frames"]
        if hasattr(self, "decor_ticker") and self.decor_ticker.winfo_exists():
            current = self.decor_ticker.cget("text")
            next_idx = (frames.index(current) + 1) % len(frames) if current in frames else 0
            self.decor_ticker.configure(text=frames[next_idx])
            self.decor_job = self.after(950, self.animate_decor)

    def choose_preset(self, name, place_id):
        self.config_data["last_game_name"] = name
        self.rebuild_status_label()
        self.place_entry.delete(0, "end")
        if place_id:
            self.place_entry.insert(0, place_id)
        self.save_config()

    def prev_slide(self):
        self.current_slide = (self.current_slide - 1) % len(self.slides)
        self.refresh_slide()

    def next_slide(self):
        self.current_slide = (self.current_slide + 1) % len(self.slides)
        self.refresh_slide()

    def refresh_slide(self):
        if hasattr(self, "slide_box") and self.slide_box.winfo_exists():
            self.slide_box.configure(image=self.slides[self.current_slide])
            self.slide_info.configure(text=f"{self.current_slide + 1} / {len(self.slides)}")

    def schedule_auto_slide(self):
        if self.auto_slide_job:
            self.after_cancel(self.auto_slide_job)
        if self.config_data.get("auto_slide", True):
            self.auto_slide_job = self.after(5000, self._auto_slide_tick)

    def _auto_slide_tick(self):
        self.next_slide()
        self.schedule_auto_slide()

    def _apply_roblox_window_action(self):
        mode = self.config_data.get("roblox_hide_mode", "Свернуть")
        if self.restore_job:
            self.after_cancel(self.restore_job)
            self.restore_job = None

        if mode == "Свернуть":
            self.after(350, self.iconify)
        elif mode == "Скрыть и вернуть":
            delay_ms = int(self.config_data.get("restore_delay_sec", 10)) * 1000
            self.after(350, self.withdraw)
            self.restore_job = self.after(350 + delay_ms, self.deiconify)

    def start_roblox(self):
        self.save_config()
        place_id = self.place_entry.get().strip()
        low_note = " (low-PC)" if self.config_data.get("low_end_mode") else ""
        if place_id.isdigit():
            webbrowser.open(f"roblox://placeId={place_id}")
            self.launch_status.configure(text=f"Запуск {place_id}{low_note}...")
        else:
            webbrowser.open("roblox://")
            self.launch_status.configure(text=f"Запуск Roblox{low_note}...")

        self._apply_roblox_window_action()


if __name__ == "__main__":
    app = RobloxLauncher()
    app.mainloop()