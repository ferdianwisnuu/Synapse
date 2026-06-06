# Synapse

Synapse adalah asisten AI modular untuk server Discord yang dirancang super ringan, efisien, dan ramah resource. Dibangun menggunakan `discord.py` dan berjalan sepenuhnya secara asinkronus menggunakan koneksi HTTP murni via `aiohttp` (tanpa OpenAI SDK), membuat bot ini sangat optimal.

## Features

- ** Advanced Reasoning & Coding Specialist:** Menggunakan model `openai/gpt-oss-120b:free` via OpenRouter untuk menangani penalaran logika tingkat tinggi dan memberikan solusi pemrograman yang bersih.
- ** In-Memory Image Decoding:** Mengubah data string Base64 dari API langsung menjadi file gambar (`.png`) di dalam RAM (BytesIO) tanpa mengotori penyimpanan lokal.
- ** Smart Short-Term Memory:** Mengingat hingga 10 riwayat percakapan terakhir per pengguna agar obrolan mengalir secara kontekstual.
- ** Reply-Based Continuation & Retag Reset:** Lanjut mengobrol cukup dengan me-reply pesan bot, atau tag ulang bot untuk mereset memori dan memulai sesi baru.
- ** Dual-Logger System:** Sistem pencatatan log otomatis yang rapi ke terminal (Console) dan file permanen (`logs/bot.log`) dengan fitur *auto-rotating* per 5MB.

## 📁 Struktur Proyek
```
synapse/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── commands/
│   │   └── general/
│   │       ├── ping.py
│   │       ├── ai.py
│   │       └── image.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py
│   └── utils/
│       └── logger.py
├── logs/
│   └── bot.log
├── .env
├── index.py
└── README.md
```

## Teknologi

- **Language:** Python 3
- **Framework:** `discord.py`
- **HTTP Client:** `aiohttp` (Asynchronous HTTP Requests)
- **API Provider:** OpenRouter AI
- **Environment Management:** `python-dotenv`

## Cara Instalasi & Menjalankan

1. **Clone Repositori:**
   git clone https://github.com/ferdianwisnuu/Synapse.git
   cd synapse

2. **Install Dependensi:**
   pip install discord.py aiohttp python-dotenv

3. **Konfigurasi `.env`:**
   Buat file `.env` di root folder dan masukkan token API kamu:
   DISCORD_TOKEN=your_discord_bot_token
   OPENROUTER_API_KEY=your_openrouter_api_key

4. **Jalankan Bot:**
   python index.py
