import random

def generate_data(n,selected_jurusan):

    data = []

    jurusan_kode = {
        "Informatika": "16",
        "Sistem Informasi": "17",
        "Teknik Elektro": "18",
        "Teknik Sipil": "19"
    }

    nomor_urut = {
        "Informatika": 1,
        "Sistem Informasi": 1,
        "Teknik Elektro": 1,
        "Teknik Sipil": 1
    }

    for _ in range(n):

        jurusan = random.choice(
            selected_jurusan
        )

        nim = (
            f"32025"
            f"{jurusan_kode[jurusan]}"
            f"{nomor_urut[jurusan]:03d}"
        )

        nomor_urut[jurusan] += 1

        data.append({
            "NIM": nim,
            "Nama": f"Mahasiswa {random.randint(1,100000)}",
            "IPK": round(random.uniform(2.0,4.0),2),
            "Jurusan": jurusan
        })

    random.shuffle(data)

    return data