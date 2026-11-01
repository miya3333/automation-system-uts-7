
import argparse
import csv
import re
import zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. KONFIGURASI
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

START_URL = "https://books.toscrape.com/"
DEFAULT_LIMIT = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}

CSV_FIELDS = [
    "judul",
    "harga",
    "rating",
    "ketersediaan",
    "kategori",
    "url",
]


# =========================================================
# 2. PEMBERSIHAN DATA MENGGUNAKAN REGEX
# =========================================================

def clean_text(text):
    """Menghapus spasi berlebih dan karakter whitespace."""
    return re.sub(r"\s+", " ", text).strip()


def clean_price(price):
    """Mengambil angka dan titik desimal dari harga."""
    return re.sub(r"[^0-9.]", "", price)


def is_valid_price(price):
    """Memeriksa format harga, misalnya 51.77."""
    return bool(re.fullmatch(r"\d+\.\d{2}", price))


# =========================================================
# 3. EKSTRAKSI RATING
# =========================================================

def get_rating(product):
    """Mengubah class rating menjadi angka bintang."""
    rating_element = product.select_one("p.star-rating")

    if not rating_element:
        return "Tidak diketahui"

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    for class_name in rating_element.get("class", []):
        if class_name in rating_map:
            return rating_map[class_name]

    return "Tidak diketahui"


# =========================================================
# 4. MENGAMBIL KATEGORI DARI HALAMAN DETAIL
# =========================================================

def get_category(session, book_url):
    response = session.get(book_url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    breadcrumb = soup.select("ul.breadcrumb li a")

    # Urutan breadcrumb umumnya:
    # Home > Books > Category
    if len(breadcrumb) >= 3:
        return clean_text(breadcrumb[-1].get_text())

    return "Tidak diketahui"


# =========================================================
# 5. PROSES WEB SCRAPING DAN PAGINATION
# =========================================================

def scrape_books(session, start_url, limit, keyword=None):
    data_books = []
    total_pages = 0
    current_url = start_url

    while current_url and len(data_books) < limit:
        print(f"Mengakses halaman: {current_url}")

        response = session.get(current_url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")

        total_pages += 1

        if not products:
            print("Tidak ditemukan produk pada halaman ini.")
            break

        for product in products:
            if len(data_books) >= limit:
                break

            # Mengambil judul dan URL buku
            title_element = product.select_one("h3 a")

            if not title_element:
                continue

            title = clean_text(title_element.get("title", ""))
            relative_url = title_element.get("href", "")
            book_url = urljoin(current_url, relative_url)

            # Mengambil harga
            price_element = product.select_one(".price_color")

            if not price_element:
                continue

            raw_price = price_element.get_text()
            price = clean_price(raw_price)

            if not is_valid_price(price):
                continue

            # Mengambil ketersediaan
            availability_element = product.select_one(
                ".instock.availability"
            )

            availability = (
                clean_text(availability_element.get_text())
                if availability_element
                else "Tidak diketahui"
            )

            # Mengambil rating
            rating = get_rating(product)

            # Mengambil kategori dari halaman detail
            category = get_category(session, book_url)

            # Filter keyword berdasarkan judul atau kategori
            if keyword:
                search_text = f"{title} {category}".lower()

                if keyword.lower() not in search_text:
                    continue

            # Menyimpan data yang sudah dibersihkan
            data_books.append({
                "judul": title,
                "harga": price,
                "rating": rating,
                "ketersediaan": availability,
                "kategori": category,
                "url": book_url,
            })

        print(
            f"Halaman {total_pages} selesai. "
            f"Total data terkumpul: {len(data_books)}"
        )

        # Mengambil link halaman berikutnya
        next_element = soup.select_one("li.next a")

        if next_element and len(data_books) < limit:
            current_url = urljoin(
                current_url,
                next_element.get("href", "")
            )
        else:
            current_url = None

    return data_books, total_pages


# =========================================================
# 6. MENYIMPAN DATA MENTAH KE FILE TXT
# =========================================================

def save_raw_data(data, file_path):
    with file_path.open("w", encoding="utf-8") as file:
        file.write("HASIL WEB SCRAPING - RAW DATA\n")
        file.write("=" * 60 + "\n\n")

        for index, book in enumerate(data, start=1):
            file.write(f"Data Buku ke-{index}\n")
            file.write(f"Judul        : {book['judul']}\n")
            file.write(f"Harga        : £{book['harga']}\n")
            file.write(f"Rating       : {book['rating']}\n")
            file.write(f"Ketersediaan : {book['ketersediaan']}\n")
            file.write(f"Kategori     : {book['kategori']}\n")
            file.write(f"URL          : {book['url']}\n")
            file.write("-" * 60 + "\n")

    print(f"File TXT berhasil disimpan: {file_path}")


# =========================================================
# 7. MENYIMPAN DATA KE FILE CSV
# =========================================================

def save_csv(data, file_path):
    with file_path.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS
        )

        writer.writeheader()
        writer.writerows(data)

    print(f"File CSV berhasil disimpan: {file_path}")


# =========================================================
# 8. MEMBUAT LAPORAN HASIL SCRAPING
# =========================================================

def create_report(data, total_pages, keyword, start_url, file_path):
    category_counts = Counter(
        book["kategori"] for book in data
    )

    with file_path.open("w", encoding="utf-8") as file:
        file.write("LAPORAN HASIL WEB SCRAPING\n")
        file.write("=" * 45 + "\n\n")

        file.write(f"Website          : {start_url}\n")
        file.write(f"Jumlah buku      : {len(data)}\n")
        file.write(f"Jumlah halaman   : {total_pages}\n")
        file.write(f"Keyword          : {keyword or '-'}\n\n")

        file.write("JUMLAH BUKU BERDASARKAN KATEGORI\n")
        file.write("-" * 45 + "\n")

        if category_counts:
            for category, count in category_counts.most_common():
                file.write(f"{category}: {count} buku\n")
        else:
            file.write("Tidak ada data kategori.\n")

        file.write("\n")
        file.write("Catatan:\n")
        file.write(
            "Data diperoleh melalui proses web scraping "
            "pada website Books to Scrape.\n"
        )

    print(f"Laporan berhasil disimpan: {file_path}")


# =========================================================
# 9. MEMBUAT BACKUP ZIP
# =========================================================

def create_backup(run_dir, backup_file):
    files_to_backup = [
        run_dir / "data" / "raw_data.txt",
        run_dir / "output" / "hasil_scraping.csv",
        run_dir / "output" / "laporan.txt",
    ]

    with zipfile.ZipFile(
        backup_file,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        for file_path in files_to_backup:
            if file_path.exists():
                # Menyimpan struktur folder relatif terhadap run_dir
                zip_file.write(
                    file_path,
                    arcname=file_path.relative_to(run_dir)
                )

    print(f"Backup ZIP berhasil dibuat: {backup_file}")


# =========================================================
# 10. ARGUMENT COMMAND LINE INTERFACE (CLI)
# =========================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Online Book Catalog Organizer"
    )

    parser.add_argument(
        "--url",
        type=str,
        default=START_URL,
        help="URL Books to Scrape yang kompatibel"
    )

    parser.add_argument(
        "--keyword",
        type=str,
        default=None,
        help="Filter berdasarkan judul atau kategori buku"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Jumlah maksimum buku yang diambil"
    )

    parser.add_argument(
        "--run-dir",
        type=Path,
        default=Path("hasil_utama"),
        help="Folder khusus untuk menyimpan hasil eksekusi"
    )

    parser.add_argument(
        "--backup",
        action="store_true",
        help="Membuat backup hasil scraping dalam ZIP"
    )

    args = parser.parse_args()

    if args.limit <= 0:
        parser.error("--limit harus lebih besar dari 0.")

    # Memastikan URL menggunakan HTTP atau HTTPS
    parsed_url = urlparse(args.url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        parser.error("--url harus berupa URL HTTP atau HTTPS yang valid.")

    return args


# =========================================================
# 11. FUNGSI UTAMA PROGRAM
# =========================================================

def main():
    args = parse_arguments()

    # Menentukan folder penyimpanan eksekusi
    run_dir = args.run_dir

    if not run_dir.is_absolute():
        run_dir = BASE_DIR / run_dir

    # Menentukan lokasi masing-masing file
    data_dir = run_dir / "data"
    output_dir = run_dir / "output"
    backup_dir = run_dir / "backup"

    raw_file = data_dir / "raw_data.txt"
    csv_file = output_dir / "hasil_scraping.csv"
    report_file = output_dir / "laporan.txt"
    zip_file = backup_dir / "backup_data.zip"

    # Membuat folder secara otomatis
    data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.backup:
        backup_dir.mkdir(parents=True, exist_ok=True)

    print("\nONLINE BOOK CATALOG ORGANIZER")
    print("=" * 45)
    print(f"URL       : {args.url}")
    print(f"Limit     : {args.limit}")
    print(f"Keyword   : {args.keyword or '-'}")
    print(f"Folder    : {run_dir}")
    print("=" * 45)

    try:
        with requests.Session() as session:
            session.headers.update(HEADERS)

            # Menjalankan scraping
            data, total_pages = scrape_books(
                session=session,
                start_url=args.url,
                limit=args.limit,
                keyword=args.keyword
            )

        if not data:
            print("\nTidak ada buku yang memenuhi kriteria.")
            return

        # Menyimpan hasil scraping
        save_raw_data(data, raw_file)
        save_csv(data, csv_file)

        # Membuat laporan
        create_report(
            data=data,
            total_pages=total_pages,
            keyword=args.keyword,
            start_url=args.url,
            file_path=report_file
        )

        # Membuat backup jika diminta
        if args.backup:
            create_backup(run_dir, zip_file)

        print("\n" + "=" * 45)
        print("PROSES SCRAPING SELESAI")
        print("=" * 45)
        print(f"Total buku       : {len(data)}")
        print(f"Total halaman    : {total_pages}")
        print(f"Lokasi hasil     : {run_dir}")

        if args.backup:
            print(f"Lokasi backup    : {zip_file}")

    except requests.RequestException as error:
        print("\nTerjadi kesalahan koneksi atau HTTP.")
        print(f"Detail: {error}")

    except (OSError, csv.Error, zipfile.BadZipFile) as error:
        print("\nTerjadi kesalahan saat mengelola file.")
        print(f"Detail: {error}")


# =========================================================
# 12. MENJALANKAN PROGRAM
# =========================================================

if __name__ == "__main__":
    main()
