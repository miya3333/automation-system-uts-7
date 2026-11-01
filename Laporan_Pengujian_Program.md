# LAPORAN PENGUJIAN PROGRAM

## Online Book Catalog Organizer

### 1. Pendahuluan

Program **Online Book Catalog Organizer** merupakan aplikasi berbasis Python yang digunakan untuk mengambil dan mengorganisasi data buku dari situs [Books to Scrape](https://books.toscrape.com/). Data yang diperoleh mencakup judul buku, harga, rating, ketersediaan, kategori, dan URL halaman buku.

Program memanfaatkan teknik web scraping untuk membaca informasi dari halaman web, kemudian menyimpan hasilnya ke dalam berkas TXT dan CSV. Program juga menyediakan pembuatan laporan ringkas, pengarsipan hasil ke dalam ZIP, serta sejumlah argumen Command Line Interface (CLI) agar proses pengambilan data dapat diatur melalui terminal.

### 2. Tujuan

Pengujian dilakukan untuk memastikan bahwa program dapat:

1. Mengambil data buku dari situs Books to Scrape.
2. Menelusuri beberapa halaman melalui mekanisme pagination.
3. Membersihkan dan memvalidasi teks serta harga menggunakan regular expression.
4. Menyimpan data hasil scraping ke dalam berkas TXT dan CSV.
5. Membuat direktori keluaran secara otomatis.
6. Membuat arsip ZIP dari berkas hasil scraping.
7. Menjalankan program melalui argumen CLI, termasuk pencarian berdasarkan keyword.
8. Menangani masukan tidak valid dan kegagalan koneksi dengan pesan kesalahan.

### 3. Lingkungan dan Persiapan

Program dijalankan pada Windows melalui terminal PowerShell. Bahasa pemrograman yang digunakan adalah Python. Pustaka eksternal yang dibutuhkan dicantumkan dalam `requirements.txt`, yaitu:

- `requests` untuk mengirim permintaan HTTP ke situs sumber.
- `beautifulsoup4` untuk membaca dan mengambil elemen HTML.

Instalasi dependency dilakukan dari direktori utama proyek menggunakan perintah:

```powershell
python -m pip install -r requirements.txt
```

**Dokumentasi instalasi dependency:**

![Instalasi dependency](dokumentasi/1.%20Instalasi%20dependency.png)

### 4. Alur Kerja Program

Secara umum, proses program berlangsung melalui tahapan berikut:

1. Program membaca argumen yang diberikan melalui CLI, seperti URL, keyword, jumlah data, direktori hasil, dan opsi backup.
2. Program mengirim permintaan HTTP ke halaman sumber.
3. HTML halaman diproses menggunakan BeautifulSoup untuk mengambil informasi buku.
4. Regular expression digunakan untuk membersihkan teks dan harga serta memvalidasi format harga.
5. Program mengikuti tautan halaman berikutnya apabila jumlah data yang diminta belum terpenuhi.
6. Informasi buku disimpan ke dalam berkas TXT dan CSV.
7. Program membuat laporan berisi ringkasan hasil scraping.
8. Jika opsi backup digunakan, berkas hasil disalin ke dalam arsip ZIP.

### 5. Pengujian Program

Pengujian dilakukan melalui terminal. Setiap pengujian menggunakan direktori keluaran tersendiri di dalam folder `hasil_uji` agar hasil dari satu pengujian tidak bercampur dengan hasil pengujian lainnya.

#### 5.1 Pengujian 1 — Pengambilan Data

Pengujian pertama dilakukan untuk memastikan program dapat mengambil data sebanyak 30 buku dari situs Books to Scrape. Hasil pengujian menunjukkan bahwa program berhasil memperoleh 30 data buku dan menyimpan hasilnya ke dalam direktori pengujian.

![Pengujian 1 — Pengambilan data 30 buku](dokumentasi/2.%20Pengujian%201%20%E2%80%94%20Pengambilan%20data%20%2830%20buku%29.png)

#### 5.2 Pengujian 2 — Pagination

Pengujian pagination dilakukan dengan meminta 30 data buku. Karena satu halaman katalog memuat 20 buku, program perlu melanjutkan proses ke halaman berikutnya untuk memenuhi jumlah data yang diminta. Berdasarkan keluaran terminal, program memproses halaman pertama dan halaman kedua hingga memperoleh 30 buku.

![Pengujian 2 — Pagination 30 buku](dokumentasi/3.%20Pengujian%202%20%E2%80%94%20Pagination%20%2830%20buku%29.png)

#### 5.3 Pengujian 3 — Regular Expression

Pengujian ini memeriksa proses pembersihan dan validasi teks menggunakan regular expression. Simbol mata uang dihapus dari nilai harga sehingga tersisa format numerik, sedangkan spasi berlebih pada judul dirapikan. Validasi dilakukan untuk memastikan harga mengikuti pola angka dengan dua digit desimal.

![Pengujian 3 — Regex](dokumentasi/4.%20Pengujian%203%20%E2%80%94%20Regex.png)

#### 5.4 Pengujian 4 — Penyimpanan TXT

Pengujian ini memastikan data hasil scraping dapat ditulis ke dalam berkas teks `raw_data.txt`. Berkas tersebut disimpan di dalam direktori `data` pada folder pengujian.

![Pengujian 4 — Penyimpanan TXT](dokumentasi/5.%20Pengujian%204%20%E2%80%94%20Penyimpanan%20TXT.png)

#### 5.5 Pengujian 5 — Penyimpanan CSV

Pengujian ini memastikan data buku dapat disimpan dalam format CSV dengan kolom yang telah ditentukan, yaitu judul, harga, rating, ketersediaan, kategori, dan URL. Berkas CSV disimpan sebagai `hasil_scraping.csv` di dalam direktori `output`.

![Pengujian 5 — Penyimpanan CSV](dokumentasi/6.%20Pengujian%205%20%E2%80%94%20Penyimpanan%20CSV.png)

#### 5.6 Pengujian 6 — Pembuatan Folder Otomatis

Pengujian ini memeriksa kemampuan program dalam membuat struktur direktori keluaran secara otomatis. Program menyiapkan direktori `data` dan `output` sebelum menyimpan hasil scraping.

![Pengujian 6 — Pembuatan folder otomatis](dokumentasi/7.%20Pengujian%206%20%E2%80%94%20Pembuatan%20folder%20otomatis.png)

#### 5.7 Pengujian 7 — Backup ZIP

Pengujian backup dilakukan dengan mengaktifkan argumen `--backup`. Program kemudian membuat arsip `backup_data.zip` yang berisi berkas hasil scraping dan laporan sesuai implementasi program.

![Pengujian 7 — Backup ZIP](dokumentasi/8.%20Pengujian%207%20%E2%80%94%20Backup%20ZIP.png)

#### 5.8 Pengujian 8 — Command Line Interface

Pengujian CLI terdiri dari dua bagian:

1. **Melihat daftar argumen.** Perintah bantuan `--help` digunakan untuk menampilkan argumen yang tersedia, seperti `--url`, `--keyword`, `--limit`, `--run-dir`, dan `--backup`.
2. **Pencarian berdasarkan keyword.** Argumen `--keyword` digunakan untuk membatasi hasil berdasarkan kata kunci yang cocok dengan judul atau kategori buku.

![Pengujian 8 — Daftar argumen CLI](dokumentasi/9.%20Pengujian%208%20%E2%80%94%20Command%20Line%20Interface%20-%201.%20Lihat%20daftar%20argumen.png)

![Pengujian 8 — Pencarian berdasarkan keyword](dokumentasi/9.%20Pengujian%208%20%E2%80%94%20Command%20Line%20Interface%20-%202.%20Uji%20pencarian%20berdasarkan%20keyword.png)

#### 5.9 Pengujian 9 — Error Handling

Pengujian error handling dilakukan untuk memeriksa respons program terhadap kondisi yang tidak valid atau kegagalan saat mengakses situs.

**a. Uji limit tidak valid**

Program dijalankan dengan nilai `--limit` sebesar `0`. Program menolak nilai tersebut dan menampilkan pesan bahwa limit harus lebih besar dari 0.

![Pengujian 9 — Limit tidak valid](dokumentasi/10.%20Pengujian%209%20%E2%80%94%20Error%20handling%20-%201.%20Uji%20limit%20tidak%20valid.png)

**b. Uji kegagalan koneksi**

Program dijalankan menggunakan alamat yang tidak dapat diakses. Kegagalan permintaan ditangani dan ditampilkan sebagai pesan kesalahan, sehingga proses tidak berhenti dengan traceback yang tidak tertangani.

![Pengujian 9 — Kegagalan koneksi](dokumentasi/10.%20Pengujian%209%20%E2%80%94%20Error%20handling%20-%202.%20Uji%20kegagalan%20koneksi.png)

### 6. Struktur Hasil Pengujian

Hasil setiap pengujian disimpan pada direktori terpisah di dalam `hasil_uji`. Struktur umumnya adalah:

```text
hasil_uji/
├── 01_pengambilan_data/
│   ├── data/
│   │   └── raw_data.txt
│   └── output/
│       ├── hasil_scraping.csv
│       └── laporan.txt
├── 02_pagination/
├── 03_regex/
├── 04_penyimpanan_txt/
├── 05_penyimpanan_csv/
├── 06_pembuatan_folder/
├── 07_backup_zip/
│   ├── backup/
│   │   └── backup_data.zip
│   ├── data/
│   └── output/
├── 08_cli/
└── 09_error_handling/
```

Setiap direktori pengujian dapat memiliki berkas keluaran sesuai proses yang dijalankan. Pengujian regex menghasilkan keluaran langsung pada terminal, sehingga direktori `03_regex` tidak harus berisi berkas hasil.

### 7. Kesimpulan

Berdasarkan dokumentasi keluaran terminal, program berhasil menjalankan pengambilan data buku, pagination, pembersihan dan validasi teks menggunakan regular expression, penyimpanan hasil ke TXT dan CSV, pembuatan direktori keluaran, pembuatan backup ZIP, penggunaan argumen CLI, serta penanganan input limit tidak valid dan kegagalan koneksi.

Pengujian menunjukkan bahwa fungsi-fungsi utama program dapat dijalankan sesuai skenario yang telah disiapkan. Pemeriksaan isi berkas CSV, TXT, laporan, dan hasil ekstraksi ZIP tetap perlu dilakukan untuk memastikan bahwa konten yang tersimpan sesuai dengan data yang diharapkan.
