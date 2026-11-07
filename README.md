# multidbms-ecommerce-dashboard
Interactive Multi-DBMS Executive Dashboard (PostgreSQL &amp; MongoDB) for Olist E-Commerce Dataset using Streamlit and Plotly.
# 🛒 Multi-DBMS E-Commerce Analytics Dashboard

**Tugas Mandiri Terstruktur / UTS: Visualisasi Data dan Informasi**  
*Program Studi Informatika - Universitas Sebelas April (UNSAP)*  

**Disusun Oleh:**  
- **Nama:** Gina Vio Amelina  
- **NIM:** 230660121085  

---

## 📌 Ringkasan Arsitektur & Multi-DBMS

Proyek ini mengintegrasikan data dari dua sistem basis data heterogen berbasis Cloud secara *real-time*:
1. **PostgreSQL (Neon Cloud - Relational/SQL):** Menyimpan data utama transaksi pesanan pada tabel `orders` (`order_id`, `order_status`).
2. **MongoDB Atlas (Cloud NoSQL Document):** Menyimpan data ulasan & rating pelanggan pada koleksi `order_reviews` (`order_id`, `review_score`).

### 🔄 Alur Integrasi Data (Data Pipeline)
Data dari kedua DBMS diambil melalui konektor Python (`psycopg2`/`SQLAlchemy` untuk PostgreSQL dan `pymongo` untuk MongoDB). Di tingkat aplikasi, data digabungkan secara langsung (*on-the-fly*) menggunakan metode **Inner Join** pada objek `Pandas Dataframe` berdasarkan parameter `order_id`. Data hasil penggabungan disajikan dalam bentuk dashboard visualisasi interaktif menggunakan **Streamlit** dan **Plotly**.

---

## 🔗 Tautan Pengumpulan (Submission Links)

- **🌐 Live Web Application:** https://multidbms-ecommerce-dashboard-dvzaapub4pbd7kxrpwcibb.streamlit.app
- **📂 Repositori GitHub:** https://github.com/ginavioamelina/multidbms-ecommerce-dashboard
- **🗃️ Sumber Data Asli:** [Kaggle - Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **💡 Referensi Kode/Proyek:** [Streamlit Official Documentation](https://docs.streamlit.io) & [Plotly Python Open Source Graphing Library](https://plotly.com/python/)

---

## 📊 Fitur Interaktivitas Dashboard

- **Filter Control:** Filter interaktif berdasarkan `order_status` pada sidebar.
- **Executive Metrics (KPI Cards):** Menampilkan Total Pesanan, Rata-rata Rating, Jumlah Ulasan Bintang 5, dan Total Pesanan Terkirim.
- **Visualisasi Grafik Interaktif:**
  - Bar Chart Distribusi Rating Pelanggan (MongoDB).
  - Donut Chart Proporsi Status Pesanan (PostgreSQL).
  - Performa Rating per Status Pesanan & Treemap Komposisi Status Pesanan.
- **Data Preview Table:** Tabel sampel data hasil *join real-time* kedua DBMS.

---

## ⚙️ Cara Menjalankan Aplikasi Secara Lokal

1. **Clone Repositori:**
   ```bash
   git clone [https://github.com/ginavioamelina/multidbms-ecommerce-dashboard.git](https://github.com/ginavioamelina/multidbms-ecommerce-dashboard.git)
   cd multidbms-ecommerce-dashboard
