# Online Book Catalog Organizer

Aplikasi berbasis Python untuk mengambil, membersihkan, mengorganisasi, dan menyimpan informasi buku dari situs [Books to Scrape](https://books.toscrape.com/).

Program menggunakan teknik **web scraping** untuk mengambil informasi buku dari halaman katalog dan halaman detail buku. Data yang diperoleh kemudian disimpan dalam format TXT dan CSV, dilengkapi laporan ringkas, serta dapat dikemas ke dalam arsip ZIP.

---

## Daftar Isi

1. [Gambaran Umum](#gambaran-umum)
2. [Tujuan Program](#tujuan-program)
3. [Teknologi dan Library](#teknologi-dan-library)
4. [Fitur](#fitur)
5. [Persiapan Lingkungan](#persiapan-lingkungan)
6. [Struktur Proyek](#struktur-proyek)
7. [Instalasi](#instalasi)
8. [Menjalankan Program](#menjalankan-program)
9. [Argumen Command Line Interface](#argumen-command-line-interface)
10. [Contoh Penggunaan](#contoh-penggunaan)
11. [Hasil dan Struktur Keluaran](#hasil-dan-struktur-keluaran)
12. [Skenario Pengujian](#skenario-pengujian)
13. [Penanganan Kesalahan](#penanganan-kesalahan)
14. [Dokumentasi Pengujian](#dokumentasi-pengujian)
15. [Batasan Program](#batasan-program)
16. [Sumber Data](#sumber-data)

---

## Gambaran Umum

**Online Book Catalog Organizer** merupakan program CLI (Command Line Interface) yang mengambil data buku dari website Books to Scrape.

Informasi yang dikumpulkan meliputi:

| Data | Keterangan |
|---|---|
| Judul | Nama atau judul buku |
| Harga | Harga buku dalam format numerik |
| Rating | Nilai rating buku |
| Ketersediaan | Informasi stok atau ketersediaan buku |
| Kategori | Kategori buku yang diperoleh dari halaman detail |
| URL | Alamat halaman detail buku |

Program dirancang agar hasil dari setiap eksekusi dapat disimpan pada direktori yang berbeda. Dengan demikian, hasil pengujian atau pengambilan data sebelumnya tidak tercampur dengan hasil eksekusi berikutnya selama menggunakan nama direktori keluaran yang berbeda.

## Tujuan Program

Program ini dibuat untuk menerapkan beberapa materi pemrograman, khususnya:

- Mengakses halaman website menggunakan HTTP request.
- Mengambil informasi dari struktur HTML.
- Membersihkan dan memvalidasi data menggunakan Regular Expression.
- Membaca dan menulis data ke dalam file.
- Mengorganisasi file dan direktori.
- Membuat arsip ZIP.
- Menyediakan antarmuka berbasis command line.
- Menangani kesalahan selama proses program berjalan.

## Teknologi dan Library

| Teknologi / Library | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Requests | Mengirim HTTP request ke website |
| BeautifulSoup | Mem-parsing HTML dan mengambil elemen data buku |
| Regular Expression (`re`) | Membersihkan teks dan memvalidasi format harga |
| CSV | Menyimpan data buku dalam format terstruktur |
| `pathlib` | Mengelola lokasi file dan direktori |
| `zipfile` | Membuat arsip ZIP untuk backup |
| `argparse` | Membaca argumen dari command line |
| `collections.Counter` | Menghitung jumlah buku berdasarkan kategori |

Library `re`, `csv`, `pathlib`, `zipfile`, `argparse`, dan `collections` merupakan bagian dari standard library Python. Library eksternal yang perlu dipasang melalui `requirements.txt` adalah `requests` dan `beautifulsoup4`.

## Fitur

1. **Web Scraping** — Mengambil informasi buku dari website Books to Scrape.
2. **Pagination** — Melanjutkan pengambilan data ke halaman berikutnya apabila jumlah data yang diminta belum terpenuhi.
3. **Pembersihan Data dengan Regex** — Merapikan spasi, membersihkan simbol pada harga, dan memvalidasi format harga.
4. **Penyimpanan TXT** — Menyimpan data mentah hasil scraping ke dalam `raw_data.txt`.
5. **Penyimpanan CSV** — Menyimpan data buku dalam bentuk tabel pada `hasil_scraping.csv`.
6. **Laporan Otomatis** — Membuat `laporan.txt` yang berisi ringkasan proses scraping, termasuk jumlah data dan ringkasan kategori.
7. **Pembuatan Direktori Otomatis** — Membuat folder `data`, `output`, dan folder `backup` jika opsi backup digunakan.
8. **Backup ZIP** — Mengemas file hasil scraping dan laporan ke dalam `backup_data.zip`.
9. **Command Line Interface** — Mengatur URL, keyword, jumlah buku, direktori keluaran, dan backup melalui argumen terminal.
10. **Error Handling** — Menangani nilai limit yang tidak valid serta kesalahan permintaan atau penyimpanan file.

---

## Persiapan Lingkungan

Sebelum menjalankan program, siapkan hal-hal berikut:

- Sistem operasi Windows, Linux, atau macOS.
- Python yang sudah terpasang.
- Terminal, seperti PowerShell, Command Prompt, atau terminal VSCode.
- Koneksi internet untuk mengakses website Books to Scrape.
- Folder proyek yang berisi `main.py` dan `requirements.txt`.

### 1. Memeriksa Instalasi Python

Buka terminal, kemudian jalankan:

```bash
python --version
```

Jika perintah `python` tidak dikenali, pada beberapa lingkungan Windows dapat menggunakan:

```bash
py --version
```

Pastikan Python dapat dijalankan sebelum melanjutkan ke instalasi dependency.

### 2. Membuka Direktori Proyek

Masuk ke direktori utama proyek. Contoh pada Windows PowerShell:

```powershell
cd path\ke\UTS_Project_Kelompok
```

Pastikan terminal berada di folder yang sama dengan file `main.py` dan `requirements.txt`.

### 3. Memeriksa File Proyek

Jalankan perintah berikut untuk melihat isi direktori:

```powershell
Get-ChildItem
```

File utama yang harus tersedia:

```text
main.py
requirements.txt
README.md
```

## Struktur Proyek

Struktur direktori utama proyek:

```text
UTS_Project_Kelompok/
├── arsip/
│   ├── dokumentasi/
│   ├── pengujian terpisah/
│   ├── percobaan/
│   ├── main_awal.py
│   ├── README.md
│   └── requirements.txt
├── dokumentasi/
│   ├── 1. Instalasi dependency.png
│   ├── 2. Pengujian 1 — Pengambilan data (30 buku).png
│   ├── 3. Pengujian 2 — Pagination (30 buku).png
│   ├── 4. Pengujian 3 — Regex.png
│   ├── 5. Pengujian 4 — Penyimpanan TXT.png
│   ├── 6. Pengujian 5 — Penyimpanan CSV.png
│   ├── 7. Pengujian 6 — Pembuatan folder otomatis.png
│   ├── 8. Pengujian 7 — Backup ZIP.png
│   ├── 9. Pengujian 8 — Command Line Interface - 1. Lihat daftar argumen.png
│   ├── 9. Pengujian 8 — Command Line Interface - 2. Uji pencarian berdasarkan keyword.png
│   ├── 10. Pengujian 9 — Error handling - 1. Uji limit tidak valid.png
│   └── 10. Pengujian 9 — Error handling - 2. Uji kegagalan koneksi.png
├── hasil_uji/
│   ├── 01_pengambilan_data/
│   ├── 02_pagination/
│   ├── 03_regex/
│   ├── 04_penyimpanan_txt/
│   ├── 05_penyimpanan_csv/
│   ├── 06_pembuatan_folder/
│   ├── 07_backup_zip/
│   ├── 08_cli/
│   └── 09_error_handling/
├── main.py
├── requirements.txt
└── README.md
```

Folder `arsip` menyimpan versi percobaan dan pengujian terdahulu. Program utama yang digunakan untuk menjalankan aplikasi berada di `main.py` pada direktori utama proyek.

---

## Instalasi

### 1. Memasang Dependency

Jalankan perintah berikut dari direktori utama proyek:

```bash
python -m pip install -r requirements.txt
```

Perintah tersebut memasang library yang tercantum pada `requirements.txt`.

Isi `requirements.txt`:

```text
requests
beautifulsoup4
```

### 2. Memastikan Dependency Terpasang

Untuk memeriksa paket yang terpasang, jalankan:

```bash
python -m pip show requests beautifulsoup4
```

Jika informasi paket ditampilkan, dependency terkait sudah tersedia pada lingkungan Python yang sedang digunakan.

---

## Menjalankan Program

Program dijalankan melalui terminal dengan format umum:

```bash
python main.py [argumen]
```

Contoh menjalankan scraping untuk mengambil maksimal 30 buku:

```bash
python main.py --limit 30 --run-dir hasil_uji/01_pengambilan_data
```

Program akan mengakses website, mengambil data buku hingga jumlah yang diminta terpenuhi atau halaman yang tersedia habis, kemudian menyimpan hasilnya pada direktori yang ditentukan.

### Melihat Panduan Penggunaan

Untuk melihat daftar argumen dan petunjuk penggunaannya:

```bash
python main.py --help
```

## Argumen Command Line Interface

| Argumen | Fungsi | Contoh |
|---|---|---|
| `--url` | Menentukan URL awal katalog yang akan diambil datanya. | `--url "https://books.toscrape.com/"` |
| `--keyword` | Memfilter buku berdasarkan keyword yang cocok dengan judul atau kategori. | `--keyword "Attic"` |
| `--limit` | Menentukan jumlah maksimum buku yang ingin diambil. | `--limit 30` |
| `--run-dir` | Menentukan direktori untuk menyimpan hasil satu eksekusi. | `--run-dir hasil_uji/01_pengambilan_data` |
| `--backup` | Mengaktifkan pembuatan arsip ZIP. | `--backup` |

### Nilai Default

Apabila argumen tertentu tidak diberikan, program menggunakan nilai default yang telah ditentukan di dalam kode:

- URL awal: `https://books.toscrape.com/`
- Jumlah maksimum buku: `30`
- Direktori keluaran: `hasil_utama`
- Keyword: tidak digunakan
- Backup: tidak diaktifkan

### Catatan Penggunaan Argumen

- `--limit` harus berupa bilangan lebih besar dari `0`.
- `--keyword` bersifat opsional. Jika digunakan, hasil difilter berdasarkan kecocokan keyword pada judul atau kategori.
- `--backup` merupakan argumen pilihan. Tanpa argumen ini, program tidak membuat arsip ZIP.
- Gunakan nama `--run-dir` yang berbeda untuk setiap eksekusi apabila ingin mempertahankan hasil sebelumnya. Jika direktori yang sama digunakan kembali, file dengan nama yang sama di dalamnya dapat ditimpa.

---

## Contoh Penggunaan

### 1. Mengambil 30 Buku

```bash
python main.py --limit 30 --run-dir hasil_uji/01_pengambilan_data
```

### 2. Menguji Pagination

```bash
python main.py --limit 30 --run-dir hasil_uji/02_pagination
```

Jumlah 30 digunakan untuk memperlihatkan proses pengambilan data yang berlanjut ke halaman berikutnya.

### 3. Mengambil Data dan Menyimpan ke Direktori Tertentu

```bash
python main.py --limit 10 --run-dir hasil_uji/04_penyimpanan_txt
```

### 4. Mengambil Data dengan Keyword

```bash
python main.py --keyword "Attic" --limit 1 --run-dir hasil_uji/08_cli
```

Contoh tersebut mencari buku yang judul atau kategorinya cocok dengan keyword `Attic`, dengan batas maksimum satu data.

### 5. Mengaktifkan Backup ZIP

```bash
python main.py --limit 10 --backup --run-dir hasil_uji/07_backup_zip
```

### 6. Menggunakan URL Katalog

```bash
python main.py --url "https://books.toscrape.com/" --limit 20 --run-dir hasil_uji/katalog_baru
```

URL yang digunakan harus memiliki struktur HTML yang sesuai dengan selector yang diterapkan pada program.

---

## Hasil dan Struktur Keluaran

Setiap eksekusi membuat direktori keluaran sesuai nilai `--run-dir`. Secara umum, struktur hasilnya adalah:

```text
nama_folder_pengujian/
├── data/
│   └── raw_data.txt
├── output/
│   ├── hasil_scraping.csv
│   └── laporan.txt
└── backup/
    └── backup_data.zip
```

Folder `backup` dibuat apabila program dijalankan menggunakan argumen `--backup`.

### 1. `raw_data.txt`

Berisi data hasil scraping dalam bentuk teks.

Lokasi:

```text
data/raw_data.txt
```

### 2. `hasil_scraping.csv`

Berisi data buku dalam format CSV dengan kolom:

```text
judul,harga,rating,ketersediaan,kategori,url
```

Lokasi:

```text
output/hasil_scraping.csv
```

File CSV dapat dibuka menggunakan aplikasi spreadsheet seperti Microsoft Excel, WPS Office, atau aplikasi lain yang mendukung format CSV.

### 3. `laporan.txt`

Berisi ringkasan hasil scraping, termasuk informasi proses dan perhitungan jumlah buku berdasarkan kategori.

Lokasi:

```text
output/laporan.txt
```

### 4. `backup_data.zip`

Arsip ZIP yang dibuat ketika opsi `--backup` digunakan. Arsip ini digunakan untuk menyimpan salinan file hasil scraping dan laporan.

Lokasi:

```text
backup/backup_data.zip
```

---

## Skenario Pengujian

Pengujian program dibagi menjadi sembilan skenario:

| No. | Pengujian | Tujuan |
|---:|---|---|
| 1 | Pengambilan data | Memastikan program dapat mengambil 30 data buku |
| 2 | Pagination | Memastikan program dapat melanjutkan pengambilan data ke halaman berikutnya |
| 3 | Regex | Memeriksa pembersihan teks dan validasi format harga |
| 4 | Penyimpanan TXT | Memastikan data dapat disimpan ke `raw_data.txt` |
| 5 | Penyimpanan CSV | Memastikan data dapat disimpan ke `hasil_scraping.csv` |
| 6 | Pembuatan folder otomatis | Memastikan direktori keluaran dibuat secara otomatis |
| 7 | Backup ZIP | Memastikan arsip ZIP dapat dibuat ketika opsi backup diaktifkan |
| 8 | Command Line Interface | Memeriksa daftar argumen dan pencarian berdasarkan keyword |
| 9 | Error handling | Memeriksa penanganan limit tidak valid dan kegagalan koneksi |

### Perintah Pengujian

Perintah berikut dapat digunakan untuk menjalankan skenario pengujian secara terpisah:

```powershell
# 1. Pengambilan data
python main.py --limit 30 --run-dir hasil_uji/01_pengambilan_data

# 2. Pagination
python main.py --limit 30 --run-dir hasil_uji/02_pagination

# 3. Pengujian Regex langsung melalui Python
python -c "import re; h=re.sub(r'[^0-9.]','','£51.77'); j=re.sub(r'\s+',' ','  A Light in    the Attic  ').strip(); print('Harga:',h); print('Judul:',j); print('Valid:',bool(re.fullmatch(r'\d+\.\d{2}',h)))"

# 4. Penyimpanan TXT
python main.py --limit 10 --run-dir hasil_uji/04_penyimpanan_txt

# 5. Penyimpanan CSV
python main.py --limit 15 --run-dir hasil_uji/05_penyimpanan_csv

# 6. Pembuatan folder otomatis
python main.py --limit 5 --run-dir hasil_uji/06_pembuatan_folder

# 7. Backup ZIP
python main.py --limit 10 --backup --run-dir hasil_uji/07_backup_zip

# 8a. Melihat daftar argumen CLI
python main.py --help

# 8b. Pencarian berdasarkan keyword
python main.py --keyword "Attic" --limit 1 --run-dir hasil_uji/08_cli

# 9a. Menguji limit tidak valid
python main.py --limit 0 --run-dir hasil_uji/09_error_handling

# 9b. Menguji kegagalan koneksi
python main.py --url "https://example.invalid/" --limit 1 --run-dir hasil_uji/09_error_handling
```

Pengujian Regex pada langkah ketiga menampilkan hasil langsung pada terminal. Karena itu, folder `hasil_uji/03_regex` tidak harus berisi file keluaran.

## Penanganan Kesalahan

Program memiliki penanganan untuk beberapa kondisi berikut:

| Kondisi | Respons yang diharapkan |
|---|---|
| Nilai `--limit` adalah `0` atau kurang | Program menolak argumen dan menampilkan pesan bahwa limit harus lebih besar dari 0 |
| Website tidak dapat diakses | Kesalahan permintaan ditangani dan pesan kesalahan ditampilkan |
| Terjadi kesalahan saat membaca atau menulis file | Kesalahan operasi file ditangani dan ditampilkan |
| Terjadi kesalahan terkait CSV atau ZIP | Program menangani kesalahan sesuai jenis operasi yang sedang dilakukan |

Untuk pengujian error handling, gunakan URL yang memang tidak valid atau tidak dapat diakses. Jangan menggunakan alamat tersebut sebagai URL sumber untuk pengambilan data normal.

---

## Dokumentasi Pengujian

Screenshot hasil pengujian disimpan pada folder `dokumentasi/` di direktori utama proyek.

| No. | Nama Dokumentasi |
|---:|---|
| 1 | Instalasi dependency |
| 2 | Pengujian 1 — Pengambilan data (30 buku) |
| 3 | Pengujian 2 — Pagination (30 buku) |
| 4 | Pengujian 3 — Regex |
| 5 | Pengujian 4 — Penyimpanan TXT |
| 6 | Pengujian 5 — Penyimpanan CSV |
| 7 | Pengujian 6 — Pembuatan folder otomatis |
| 8 | Pengujian 7 — Backup ZIP |
| 9 | Pengujian 8 — Command Line Interface |
| 10 | Pengujian 9 — Error handling |

Laporan pengujian yang menampilkan screenshot secara langsung tersedia pada file `Laporan_Pengujian_Program.md`.

---

## Batasan Program

1. Program dirancang berdasarkan struktur HTML website Books to Scrape.
2. Penggunaan pada website lain memerlukan penyesuaian selector HTML dan kemungkinan penyesuaian alur pengambilan data.
3. Pengambilan kategori dilakukan dengan mengakses halaman detail buku. Hal ini menambah jumlah HTTP request dan dapat membuat proses scraping lebih lama.
4. Keberhasilan pengambilan data bergantung pada ketersediaan website sumber dan koneksi internet.
5. Data yang dapat diambil terbatas pada informasi yang tersedia dan dapat dibaca dari halaman website.

## Sumber Data

Website yang digunakan sebagai sumber pengambilan data:

[https://books.toscrape.com/](https://books.toscrape.com/)

Books to Scrape merupakan website katalog buku yang digunakan sebagai sumber latihan web scraping.

---

## Penutup

Online Book Catalog Organizer dibuat sebagai penerapan materi Python yang mencakup web scraping, regular expression, pengolahan file, pengorganisasian direktori, command line interface, dan error handling.

Untuk menjalankan program, pastikan dependency sudah terpasang, terminal berada di direktori utama proyek, dan koneksi internet tersedia. Setelah itu, program dapat dijalankan menggunakan `main.py` dengan argumen sesuai kebutuhan.
