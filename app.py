import pandas as pd
import time
import streamlit as st
import tracemalloc
from data.generator import generate_data
import plotly.express as px

from algorithms.searching import binary_search

from config.settings import (
    algorithms,
    complexities
)

from utils.benchmark import (
    benchmark_algorithm
)

# =====================================================
# 4. STREAMLIT APP
# =====================================================

st.set_page_config(
    page_title="SortAnalyzer",
    layout="wide"
)

# --- CONFIG WARNA ---
BG_COLOR_SOLID = "#263238"   # Warna background utama
SIDEBAR_COLOR = "#1E272C"    # Warna background sidebar
TEXT_COLOR_SIDEBAR = "#FFFFFF" # Warna teks utama di sidebar
# ---------------------------

# INJEKSI CSS KUSTOM UNTUK WARNA SOLID & sidebar
st.markdown(f"""
    <style>
        /* Mengatur font global agar seragam dan jelas */
        html, body, [class*="css"] {{
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        
        /* 1. MENGUBAH LATAR BELAKANG UTAMA */
        .stApp {{
            background-color: {BG_COLOR_SOLID} !important;
        }}

        /* Container utama (area konten) */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.04);
            padding: 3rem;
            border-radius: 12px;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        
        /* =====================================================
        2. KUSTOMISASI PANEL KIRI (SIDEBAR)
           ===================================================== */
        section[data-testid="stSidebar"] {{
            background-color: {SIDEBAR_COLOR} !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /*semua teks standar di sidebar berwarna putih */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] span {{
            color: {TEXT_COLOR_SIDEBAR} !important;
        }}
        
        
        /*background box sedikit transparan terang dan teks di dalamnya putih bersih */
        section[data-testid="stSidebar"] div[data-testid="stAlert"] {{
            background-color: rgba(255, 255, 255, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
        }}
        
        section[data-testid="stSidebar"] div[data-testid="stAlert"] p,
        section[data-testid="stSidebar"] div[data-testid="stAlert"] div {{
            color: #FFFFFF !important;
            font-weight: 500 !important;
        }}
        /* ===================================================== */
        
        /* Desain Metric Box yang lebih soft dan interaktif */
        div[data-testid="stMetricBlock"] {{
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        div[data-testid="stMetricBlock"]:hover {{
            transform: translateY(-4px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            border-color: #1E88E5;
        }}
        
        /* Animasi dan Styling untuk Semua Tombol */
        .stButton > button {{
            background-color: #1E88E5;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.25s ease-in-out;
            box-shadow: 0 2px 5px rgba(30,136,229,0.2);
        }}
        .stButton > button:hover {{
            background-color: #1565C0;
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(21,101,192,0.4);
        }}
        .stButton > button:active {{
            transform: scale(0.98);
        }}
        
        /* Efek Transisi Halus pada Input Form */
        div[data-baseweb="select"], div[data-baseweb="input"] {{
            transition: border-color 0.2s ease;
        }}
        div[data-baseweb="select"]:hover, div[data-baseweb="input"]:hover {{
            border-color: #1E88E5 !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("📊 SortAnalyzer")
st.subheader("Studi Komparatif Algoritma Sorting dan Binary Search")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Konfigurasi Dataset")

# MODE DATASET
pilihan = st.sidebar.radio(
    "Mode Dataset",
    [
        "Semua Jurusan",
        "Pilih Jurusan"
    ]
)

jurusan_options = [
    "Informatika",
    "Sistem Informasi",
    "Teknik Elektro",
    "Teknik Sipil"
]

if pilihan == "Semua Jurusan":
    selected_jurusan = jurusan_options
else:
    selected_jurusan = st.sidebar.multiselect(
        "Pilih Jurusan",
        jurusan_options,
        default=["Informatika"]
    )

# Validasi
if len(selected_jurusan) == 0:
    st.sidebar.error(
        "Pilih minimal satu jurusan!"
    )
    st.stop()

# Jumlah data
data_size = st.sidebar.selectbox(
    "Jumlah Data Mahasiswa",
    [1000, 10000, 50000, 100000]
)

generate_btn = st.sidebar.button(
    "Generate Data Baru"
)

st.sidebar.info(
    f"Dataset aktif: {data_size:,} record"
)
# =====================================================
# SESSION STATE
# =====================================================

if "dataset" not in st.session_state:
    st.session_state.dataset = generate_data(
        data_size,
        selected_jurusan
    )

if "sorted_data" not in st.session_state:
    st.session_state.sorted_data = None

if "current_size" not in st.session_state:
    st.session_state.current_size = data_size

# Jika ukuran dataset berubah
if st.session_state.current_size != data_size:
    st.session_state.dataset = generate_data(
        data_size,
        selected_jurusan
    )
    st.session_state.sorted_data = None
    st.session_state.current_size = data_size

# Jika tombol generate ditekan
if generate_btn:
    st.session_state.dataset = generate_data(
        data_size,
        selected_jurusan
    )
    st.session_state.sorted_data = None

# =====================================================
# DISPLAY DATASET MENTAH
# =====================================================
st.subheader(f"Dataset Mentah ({len(st.session_state.dataset)} Data)")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Jumlah Record",
        f"{len(st.session_state.dataset):,}"
    )

with col2:
    # Menggunakan len() agar jumlahnya dinamis mengikuti pilihan user
    st.metric(
        "Jumlah Jurusan",
        len(selected_jurusan)
    )

st.dataframe(
    pd.DataFrame(st.session_state.dataset),
    use_container_width=True
)

st.divider()

st.subheader("⚙️ Sorting Individual")

if len(st.session_state.dataset) >= 50000:
    st.warning(
        "Dataset besar terdeteksi. "
        "Disarankan menggunakan "
        "Merge Sort atau Quick Sort."
    )

selected_algorithm = st.selectbox(
    "Pilih Algoritma Sorting",
    list(algorithms.keys())
)

if st.button("Jalankan Sorting Terpilih"):

    sorting_function = algorithms[selected_algorithm]

    # Progress Bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.info(
        f"⏳ Menjalankan {selected_algorithm}..."
    )

    # Animasi loading
    for i in range(100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)

    tracemalloc.start()

    start_time = time.perf_counter()

    sorted_result, comps, swaps = sorting_function(
        st.session_state.dataset,
        "NIM"
    )

    end_time = time.perf_counter()

    current_memory, peak_memory = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    # Hapus progress
    progress_bar.empty()

    status_text.success(
        f"✅ {selected_algorithm} berhasil dijalankan."
    )

    st.session_state.sorted_data = sorted_result

    # ==========================
    # HASIL METRIK
    # ==========================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "⏱️ Waktu Eksekusi",
            f"{end_time-start_time:.6f} detik"
        )

    with col2:
        st.metric(
            "🔍 Perbandingan",
            f"{comps:,}"
        )

    with col3:
        st.metric(
            "🔄 Swap",
            f"{swaps:,}"
        )

    st.info(
        f"""
        **Algoritma:** {selected_algorithm}

        **Kompleksitas Waktu:** {complexities[selected_algorithm]}
        """
    )

    st.info(
        f"💾 Peak Memory: {peak_memory/1024:.2f} KB"
    )

    # ==========================
    # TABEL HASIL SORTING
    # ==========================

    st.subheader(
        "📋 Hasil Sorting Dataset Mahasiswa"
    )

    st.dataframe(
        pd.DataFrame(sorted_result),
        use_container_width=True
    )

if (
    selected_algorithm in [
        "Bubble Sort",
        "Selection Sort"
    ]
    and len(st.session_state.dataset) >= 50000
):
    st.warning(
        "Proses dapat memakan waktu sangat lama."
    )


# =====================================================
# BENCHMARK ALL ALGORITHMS (DENGAN ESTIMASI AUTOMATIS)
# =====================================================
st.divider()
st.subheader("📊 Benchmark Semua Algoritma")

if st.button("Jalankan Semua Algoritma"):
    results = []
    progress = st.progress(0)
    total_algorithms = len(algorithms)
    
    n_data = len(st.session_state.dataset)

    for index, (name, func) in enumerate(algorithms.items()):
        
        # JIKA DATA BESAR DAN ALGORITMA LAMBAT -> GUNAKAN SIMULASI/ESTIMASI
        if n_data >= 50000 and name in ["Bubble Sort", "Selection Sort"]:
            
            # Notifikasi ke user bahwa kita memakai estimasi demi keamanan runtime
            st.caption(f"ℹ️ {name} dilewati (Menggunakan estimasi berbasis kompleksitas $O(n^2)$)")
            
            # Rumus perkiraan waktu empiris (konstanta berbasis performa rata-rata CPU)
            # Nilai ini disesuaikan agar grafiknya tetap realistis di Streamlit
            if name == "Bubble Sort":
                estimated_time = (n_data ** 2) * 0.00000006  # Est sekitar 150 detik untuk 50k
                comps = (n_data * (n_data - 1)) // 2          # Rumus pasti perbandingan Bubble
                swaps = int(comps * 0.5)                      # Estimasi rata-rata pertukaran acak
                peak_mem = 150.0                              # Estimasi memori overhead ringan
            else:  # Selection Sort
                estimated_time = (n_data ** 2) * 0.00000005  # Sedikit lebih cepat dari bubble
                comps = (n_data * (n_data - 1)) // 2          # Rumus pasti perbandingan Selection
                swaps = n_data - 1                            # Maksimal swap selection sort
                peak_mem = 120.0
                
            results.append({
                "Algoritma": name,
                "Waktu (detik)": round(estimated_time, 6),
                "Perbandingan": comps,
                "Swaps": swaps,
                "Peak Memory (KB)": peak_mem,
                "Kompleksitas": complexities[name]
            })
            
        else:
            # JIKA DATA KECIL ATAU ALGORITMA CEPAT (MERGE/QUICK) -> JALANKAN ASLI
            res = benchmark_algorithm(func, st.session_state.dataset, "NIM")

            results.append({
            "Algoritma": name,
            "Waktu (detik)": round(res["time"], 6),
            "Perbandingan": res["comparisons"],
            "Swaps": res["swaps"],
            "Peak Memory (KB)": round(res["peak_memory"], 2),
            "Kompleksitas": complexities[name]
        })



            if name == "Quick Sort":
                st.session_state.sorted_data = res["sorted_data"]

        progress.progress((index + 1) / total_algorithms)

    st.success("Benchmark selesai (dengan optimasi keamanan data besar)!")
    result_df = pd.DataFrame(results)
    st.dataframe(result_df, use_container_width=True)

    # =====================================================
    # TABEL HASIL BENCHMARK
    # =====================================================
    
    chart_df = result_df.set_index("Algoritma")
    
    # =====================================================
    # VISUALISASI BENCHMARK PROFESIONAL
    # =====================================================
    
    st.subheader("📈 Analisis Perbandingan Algoritma")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "⏱ Waktu",
        "🔄 Comparison",
        "🔁 Swap",
        "💾 Memory"
    ])
    
    with tab1:
    
        fig_time = px.bar(
            result_df,
            x="Algoritma",
            y="Waktu (detik)",
            text="Waktu (detik)",
            color="Algoritma"
        )
    
        fig_time.update_layout(
            title="Perbandingan Waktu Eksekusi",
            showlegend=False
        )
    
        st.plotly_chart(
            fig_time,
            use_container_width=True
        )
    
    with tab2:
    
        fig_comp = px.bar(
            result_df,
            x="Algoritma",
            y="Perbandingan",
            text="Perbandingan",
            color="Algoritma"
        )
    
        fig_comp.update_layout(
            title="Jumlah Comparison",
            showlegend=False
        )
    
        st.plotly_chart(
            fig_comp,
            use_container_width=True
        )
    
    with tab3:
    
        fig_swap = px.bar(
            result_df,
            x="Algoritma",
            y="Swaps",
            text="Swaps",
            color="Algoritma"
        )
    
        fig_swap.update_layout(
            title="Jumlah Swap",
            showlegend=False
        )
    
        st.plotly_chart(
            fig_swap,
            use_container_width=True
        )
    
    with tab4:
    
        fig_mem = px.bar(
            result_df,
            x="Algoritma",
            y="Peak Memory (KB)",
            text="Peak Memory (KB)",
            color="Algoritma"
        )
    
        fig_mem.update_layout(
            title="Peak Memory Usage",
            showlegend=False
        )
    
        st.plotly_chart(
            fig_mem,
            use_container_width=True
        )
    
    # =====================================================
    # KESIMPULAN OTOMATIS
    # =====================================================
    
    fastest = result_df.loc[
        result_df["Waktu (detik)"].astype(float).idxmin()
    ]
    
    slowest = result_df.loc[
        result_df["Waktu (detik)"].astype(float).idxmax()
    ]
    
    st.subheader("📌 Kesimpulan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(
            f"""
            🚀 Algoritma Tercepat
    
            {fastest['Algoritma']}
    
            Waktu:
            {fastest['Waktu (detik)']} detik
            """
        )
    
    with col2:
        st.error(
            f"""
            🐢 Algoritma Terlambat
    
            {slowest['Algoritma']}
    
            Waktu:
            {slowest['Waktu (detik)']} detik
            """
        )

# =====================================================
# DATA HASIL SORTING
# =====================================================

if st.session_state.sorted_data is not None:
    st.divider()
    st.subheader("📑 Hasil Sorting Dataset Mahasiswa")
    st.dataframe(
        pd.DataFrame(st.session_state.sorted_data),
        use_container_width=True
    )

# =====================================================
# BINARY SEARCH
# =====================================================

st.divider()
st.subheader("🔍 Binary Search")

if st.session_state.sorted_data is not None:
    nim_query = st.text_input(
        "Masukkan NIM yang dicari"
    )

    if st.button("Cari dengan Binary Search"):
        result = binary_search(
            st.session_state.sorted_data,
            nim_query
        )

        if result:
            st.success("Data ditemukan!")
            st.json(result)
        else:
            st.error("Data tidak ditemukan.")
else:
    st.warning(
        "Jalankan proses sorting terlebih dahulu "
        "agar Binary Search dapat digunakan."
    )