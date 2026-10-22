from abc import ABC, abstractmethod
from functools import singledispatchmethod

# INTERFACE: Kontrak dasar metode pembayaran
class Pembayaran(ABC):
    @abstractmethod
    def bayar(self, j): ...

# METODE PEMBAYARAN: Implementasi biaya transaksi per metode
class Tunai(Pembayaran):
    def bayar(self, j): return j

class Debit(Pembayaran):
    def bayar(self, j): return j + 2500  # + admin Rp2.500

class QRIS(Pembayaran):
    def bayar(self, j): return j + 1000  # + admin Rp1.000

# ABSTRACT CLASS: Aturan dasar tiket bioskop
class Tiket(ABC):
    def __init__(self, f, k): self.film, self.kursi = f, k
    @abstractmethod
    def harga(self): ...
    def info(self): return f"{self.film.judul} kursi {self.kursi}"

# JENIS TIKET: Penentuan harga tiket Reguler & VIP
class Reguler(Tiket):
    def harga(self): return self.film.harga

class VIP(Tiket):
    def harga(self): return self.film.harga + 25000
    def info(self): return "[VIP] " + super().info()

# DATA FILM: Menyimpan data judul dan harga dasar film
class Film:
    def __init__(self, j, h): self.judul, self.harga = j, h

# STUDIO: Kelola denah & ketersediaan kursi (Agregasi Film)
class Studio:
    def __init__(self, film, j=10):
        self.film, self.total, self.kosong = film, j, set(range(1, j + 1))

    # Menampilkan denah visual kursi ([01] = kosong, [X] = terisi)
    def denah(self):
        print(f"\n--- Denah {self.film.judul} ---")
        d = [f"[{i:02d}]" if i in self.kosong else " [X] " for i in range(1, self.total + 1)]
        for i in range(0, len(d), 5): print(" ".join(d[i:i+5]))

# BIOSKOP: Kelola daftar studio (Komposisi) & Overloading Pencarian
class Bioskop:
    def __init__(self, films): self.studios = [Studio(f) for f in films]

    @singledispatchmethod
    def cari(self, x): raise TypeError  # Method overloading berdasarkan tipe input

    @cari.register  # Cari studio berdasarkan nomor indeks (int)
    def _(self, x: int): return self.studios[x] if 0 <= x < len(self.studios) else None

    @cari.register  # Cari studio berdasarkan judul film (str)
    def _(self, x: str): return next((s for s in self.studios if s.film.judul.lower() == x.lower()), None)

# KASIR: Mengendalikan seluruh alur transaksi pemesanan
class Kasir:
    def __init__(self, bioskop): self.bioskop = bioskop

    # Jalankan alur pilih film -> denah -> pilih kursi -> pembayaran -> detail tiket
    def transaksi(self, jenis=Reguler):
        print("\n=== DAFTAR FILM ===")
        for i, s in enumerate(self.bioskop.studios, 1):
            print(f"{i}. {s.film.judul} (Rp{s.film.harga:,})")
        
        # 1. Pilih film (bisa angka indeks atau string judul)
        p = input("Pilih film (nomor/judul, '0' keluar): ").strip()
        if p == "0": return False
        
        studio = self.bioskop.cari(int(p) - 1) if p.isdigit() else self.bioskop.cari(p)
        if not studio: print("Film tidak ditemukan!"); return True

        # 2. Tampilkan denah kursi
        studio.denah()
        if not studio.kosong: print("Studio Penuh!"); return True

        # 3. Input & validasi pilihan nomor kursi
        while True:
            try:
                k = int(input(f"Pilih kursi (1-{studio.total}): "))
                if k in studio.kosong: break
                print("Kursi tidak valid / terisi!")
            except ValueError: pass

        # 4. Pilih metode pembayaran
        metode = {"1": (Tunai(), "Cash"), "2": (Debit(), "Debit"), "3": (QRIS(), "QRIS")}
        print("1. Cash | 2. Debit (+2.5k) | 3. QRIS (+1k)")
        m_pilihan = input("Pilih Pembayaran (1/2/3): ").strip()
        pembayaran, nama_m = metode.get(m_pilihan, (Tunai(), "Cash"))

        # 5. Cetak ringkasan detail tiket & total pembayaran
        studio.kosong.remove(k)
        tiket = jenis(studio.film, k)
        print(f"\n=== DETAIL TIKET ===\nTiket  : {tiket.info()}\nBayar  : {nama_m}\nTotal  : Rp{pembayaran.bayar(tiket.harga()):,}\n====================\n")
        return True

    # Memulai loop utama aplikasi bioskop
    def jalan(self):
        while self.transaksi(): pass
        print("Terima Kasih!")

# MENJALANKAN PROGRAM
Kasir(Bioskop([Film("Avengers", 50000), Film("Frozen", 40000)])).jalan()
