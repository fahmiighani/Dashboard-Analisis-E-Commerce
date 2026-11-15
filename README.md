# Dashboard Analisis E-Commerce Olist 2017

Dashboard interaktif ini dibuat untuk menganalisis dataset publik E-Commerce pada pesanan berstatus *delivered* di tahun 2017. Proyek ini merupakan submission kelas **Belajar Fundamental Analisis Data** di Dicoding.

- **Nama:** Fahmi Irfan Ghani
- **ID Dicoding:** ds001b6y0543

## Pertanyaan Bisnis
1. Kategori produk apa saja yang menyumbang lebih dari 10% total pendapatan (revenue) platform selama tahun 2017?
2. Seberapa signifikan keterlambatan pengiriman memengaruhi rata-rata skor ulasan pelanggan hingga turun di bawah 2,5 bintang pada pesanan *delivered* tahun 2017?

## Dataset
Dashboard menggunakan lima file berikut:

| File | Kegunaan |
|---|---|
| `orders_dataset.csv` | Status pesanan serta tanggal beli, tiba, dan estimasi tiba |
| `order_items_dataset.csv` | Harga item, dasar perhitungan revenue |
| `products_dataset.csv` | Relasi produk ke kategori |
| `product_category_name_translation.csv` | Terjemahan nama kategori ke bahasa Inggris |
| `order_reviews_dataset.csv` | Skor ulasan pelanggan (1-5) |

## Teknik Analisis
- **Data Wrangling:** memuat data, memfilter pesanan *delivered* tahun 2017, menangani *missing value* (tanggal tiba kosong, kategori kosong), menghapus ulasan ganda per pesanan, dan mengonversi kolom tanggal ke tipe datetime.
- **Exploratory Data Analysis (EDA):** agregasi revenue per kategori beserta persentase kontribusinya, serta perbandingan rata-rata skor ulasan pesanan tepat waktu vs terlambat.
- **Visualization & Explanatory Analysis:** *bar chart* kontribusi revenue per kategori dan *bar chart* skor ulasan berdasarkan status dan lama keterlambatan.

## Fitur Dashboard
- **Ringkasan metrik:** total revenue, jumlah pesanan, rata-rata skor ulasan, dan persentase pesanan terlambat.
- **Tab Pertanyaan 1:** kontribusi revenue per kategori, dengan ambang yang dapat diatur.
- **Tab Pertanyaan 2:** skor ulasan pesanan tepat waktu vs terlambat, serta per kelompok lama keterlambatan.
- **Filter sidebar:** rentang bulan, ambang revenue (%), jumlah kategori, dan ambang skor ulasan.

## Ringkasan Insight
- Tidak ada kategori yang melampaui 10% total revenue pada 2017. Kategori tertinggi adalah `bed_bath_table` (sekitar 8,4%), kedua `watches_gifts` dan ketiga `health_beauty` (sekitar 8,1%), sehingga pendapatan tersebar cukup merata.
- Rata-rata skor ulasan pesanan terlambat sekitar 2,55, jauh di bawah pesanan tepat waktu yang sekitar 4,29. Keterlambatan menurunkan kepuasan secara signifikan, meskipun rata-ratanya belum turun di bawah ambang 2,5.

## Struktur Folder
```text
submission
├── dashboard
│   └── dashboard.py
├── data
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt   (opsional, jika dashboard di-deploy)
```

## Persiapan Environment

Buka terminal lalu pindah ke **direktori utama proyek**, yaitu folder `submission` yang berisi folder `dashboard`, `data`, dan file `requirements.txt`.

```bash
cd path/ke/submission
```

Pastikan posisi sudah benar dengan memeriksa isi folder:

```bash
# Windows
dir dashboard

# Mac / Linux
ls dashboard
```

File `dashboard.py` harus tampil. Jika tidak, pindah ke folder yang benar sebelum melanjutkan.

## Instalasi Dependensi

Pilih salah satu opsi berikut dari direktori utama proyek.

### Opsi 1: Menggunakan Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
python -m pip install -r requirements.txt
```

### Opsi 2: Menggunakan Python (virtual environment)
```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

python -m pip install -r requirements.txt
```

## Menjalankan Dashboard secara Lokal

Pastikan terminal masih berada di direktori utama proyek (`submission`), kemudian jalankan:

```bash
python -m streamlit run dashboard/dashboard.py
```

Browser akan terbuka otomatis di `http://localhost:8501`. Jika tidak, buka alamat tersebut secara manual. Untuk menghentikan dashboard, tekan `Ctrl + C` di terminal.

> **Catatan:** jalankan perintah dari folder `submission`, bukan dari dalam folder `dashboard`, karena dashboard membaca data dari folder `data` yang berada sejajar dengan folder `dashboard`.

