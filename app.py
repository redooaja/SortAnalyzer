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

# --- CONFIG WARNA SOLID ---
BG_COLOR_SOLID = "#263238"   # Warna background utama
SIDEBAR_COLOR = "#1E272C"    # Warna background sidebar
TEXT_COLOR_SIDEBAR = "#FFFFFF" # Warna teks utama di sidebar
# ---------------------------

# INJEKSI CSS KUSTOM UNTUK WARNA SOLID & SIDEBAR
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
           2. PERBAIKAN DAN KUSTOMISASI PANEL KIRI (SIDEBAR)
           ===================================================== */
        section[data-testid="stSidebar"] {{
            background-color: {SIDEBAR_COLOR} !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }}

        /* Memaksa semua teks standar di sidebar berwarna putih */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] span {{
            color: {TEXT_COLOR_SIDEBAR} !important;
        }}
        
        /* 🔥 FIX INFO BOX SIDEBAR (Dataset aktif: 1,000 record) 🔥 */
        /* Memaksa background box sedikit transparan terang dan teks di dalamnya putih bersih */
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
# DATASET AWAL
# =====================================================

st.subheader(f"Dataset Mentah ({len(st.session_state.dataset)} Data)")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Jumlah Record",
        f"{len(st.session_state.dataset):,}"
    )

with col2:
    st.metric(
        "Jumlah Jurusan",
        4
    )

st.dataframe(
    pd.DataFrame(st.session_state.dataset).head(10),
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
    tracemalloc.start()
    start_time = time.perf_counter()

    sorted_result, comps, swaps = sorting_function(
        st.session_state.dataset,
        "NIM"
    )

    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    st.session_state.sorted_data = sorted_result
    st.success(
        f"{selected_algorithm} berhasil dijalankan."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Waktu Eksekusi",
            f"{end_time-start_time:.6f} detik"
        )

    with col2:
        st.metric(
            "Perbandingan",
            comps
        )

    with col3:
        st.metric(
            "Swap",
            swaps
        )

    st.info(
        f"""
        Algoritma: {selected_algorithm}

        Kompleksitas Waktu:
        {complexities[selected_algorithm]}
        """
    )

    st.info(
        f"Peak Memory: {peak_memory/1024:.2f} KB"
    )

    st.subheader("Hasil Sorting")

    st.dataframe(
        pd.DataFrame(sorted_result).head(20),
        use_container_width=True
    )

if (
    selected_algorithm in [
        "Bubble Sort",
        "Selection Sort"
    ]
    and len(st.session_state.dataset) > 10000
):
    st.error(
        "Dataset terlalu besar untuk "
        f"{selected_algorithm}. "
        "Gunakan Merge Sort atau Quick Sort."
    )
    st.stop()


# =====================================================
# BENCHMARK SORTING
# =====================================================

st.divider()
st.subheader("📊 Benchmark Semua Algoritma")

if st.button("Jalankan Semua Algoritma"):
    results = []
    progress = st.progress(0)
    total_algorithms = len(algorithms)

    for index, (name, func) in enumerate(algorithms.items()):
        if (
            len(st.session_state.dataset) >= 50000
            and name in [
                "Bubble Sort",
                "Selection Sort"
            ]
        ):
            continue

        tracemalloc.start()
        start_time = time.perf_counter()

        sorted_res, comps, swaps = func(
            st.session_state.dataset,
            "NIM"
        )

        end_time = time.perf_counter()
        duration = end_time - start_time
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results.append({
            "Algoritma": name,
            "Waktu (detik)": round(duration, 6),
            "Perbandingan": comps,
            "Swaps": swaps,
            "Peak Memory (KB)": round(peak_memory/1024, 2),
            "Kompleksitas": complexities[name]
        })

        if len(st.session_state.dataset) >= 50000:
            st.warning(
                "Bubble Sort dan Selection Sort "
                "akan membutuhkan waktu sangat lama "
                "untuk dataset besar."
            )

        if name == "Quick Sort":
            st.session_state.sorted_data = sorted_res

        progress.progress((index + 1) / total_algorithms)

    st.success("Benchmark selesai!")
    result_df = pd.DataFrame(results)

    st.dataframe(
        result_df,
        use_container_width=True
    )

    st.subheader("Grafik Perbandingan Waktu")

    fig = px.bar(
        result_df,
        x="Algoritma",
        y="Waktu (detik)",
        color="Algoritma",
        text="Waktu (detik)",
        labels={"Waktu (detik)": "Waktu Proses (Detik)"},
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_traces(
        texttemplate='%{text:.5f} s', 
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5, 
        opacity=0.85
    )
    
    fig.update_layout(
        yaxis=dict(range=[0, result_df["Waktu (detik)"].max() * 1.2]),
        showlegend=False,
        font=dict(family="Segoe UI, sans-serif", size=13),
        margin=dict(l=20, r=20, t=20, b=20),
        transition_duration=500  
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Merge Sort dan Quick Sort umumnya lebih efisien "
        "dibandingkan Bubble Sort dan Selection Sort "
        "untuk dataset berukuran besar."
    )

    fastest = result_df.loc[
        result_df["Waktu (detik)"].astype(float).idxmin()
    ]

    slowest = result_df.loc[
        result_df["Waktu (detik)"].astype(float).idxmax()
    ]

    st.subheader("📌 Kesimpulan ")

    st.success(
        f"Algoritma tercepat adalah "
        f"{fastest['Algoritma']} "
        f"dengan waktu "
        f"{fastest['Waktu (detik)']} detik."
    )

    st.warning(
        f"Algoritma terlambat adalah "
        f"{slowest['Algoritma']} "
        f"dengan waktu "
        f"{slowest['Waktu (detik)']} detik."
    )

# =====================================================
# DATA HASIL SORTING
# =====================================================

if st.session_state.sorted_data is not None:
    st.divider()
    st.subheader("📑 Hasil Sorting (10 Data Pertama)")
    st.dataframe(
        pd.DataFrame(st.session_state.sorted_data).head(10),
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