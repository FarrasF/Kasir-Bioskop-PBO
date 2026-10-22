from abc import ABC, abstractmethod
from functools import singledispatchmethod

class Pembayaran(ABC):
    @abstractmethod
    def bayar(self, j): ...

class Tunai(Pembayaran):
    def bayar(self, j): return j
class Debit(Pembayaran):
    def bayar(self, j): return j + 2500
class QRIS(Pembayaran):
    def bayar(self, j): return j + 1000

class Tiket(ABC):
    def __init__(self, f, k): self.film, self.kursi = f, k
    @abstractmethod
    def harga(self): ...
    def info(self): return f"{self.film.judul} kursi {self.kursi}"

class Reguler(Tiket):
    def harga(self): return self.film.harga
class VIP(Tiket):
    def harga(self): return self.film.harga + 25000
    def info(self): return "[VIP] " + super().info()

class Film:
    def __init__(self, j, h): self.judul, self.harga = j, h

class Studio:
    def __init__(self, film, j=10):
        self.film, self.total, self.kosong = film, j, set(range(1, j + 1))

    def denah(self):
        print(f"\n--- Denah {self.film.judul} ---")
        d = [f"[{i:02d}]" if i in self.kosong else " [X] " for i in range(1, self.total + 1)]
        for i in range(0, len(d), 5): print(" ".join(d[i:i+5]))

class Bioskop:
    def __init__(self, films): self.studios = [Studio(f) for f in films]

    @singledispatchmethod
    def cari(self, x): raise TypeError
    @cari.register
    def _(self, x: int): return self.studios[x] if 0 <= x < len(self.studios) else None
    @cari.register
    def _(self, x: str): return next((s for s in self.studios if s.film.judul.lower() == x.lower()), None)

class Kasir:
    def __init__(self, bioskop): self.bioskop = bioskop

    def transaksi(self, jenis=Reguler):
        print("\n=== DAFTAR FILM ===")
        for i, s in enumerate(self.bioskop.studios, 1):
            print(f"{i}. {s.film.judul} (Rp{s.film.harga:,})")
        
        p = input("Pilih film (nomor/judul, '0' keluar): ").strip()
        if p == "0": return False
        
        studio = self.bioskop.cari(int(p) - 1) if p.isdigit() else self.bioskop.cari(p)
        if not studio: print("Film tidak ditemukan!"); return True

        studio.denah()
        if not studio.kosong: print("Studio Penuh!"); return True

        while True:
            try:
                k = int(input(f"Pilih kursi (1-{studio.total}): "))
                if k in studio.kosong: break
                print("Kursi tidak valid / terisi!")
            except ValueError: pass

        metode = {"1": (Tunai(), "Cash"), "2": (Debit(), "Debit"), "3": (QRIS(), "QRIS")}
        print("1. Cash | 2. Debit (+2.5k) | 3. QRIS (+1k)")
        m_pilihan = input("Pilih Pembayaran (1/2/3): ").strip()
        pembayaran, nama_m = metode.get(m_pilihan, (Tunai(), "Cash"))

        studio.kosong.remove(k)
        tiket = jenis(studio.film, k)
        
        print(f"\n=== DETAIL TIKET ===\nTiket  : {tiket.info()}\nBayar  : {nama_m}\nTotal  : Rp{pembayaran.bayar(tiket.harga()):,}\n====================\n")
        return True

    def jalan(self):
        while self.transaksi(): pass
        print("Terima Kasih!")

# RUN PROGRAM
Bioskop([Film("Avengers", 50000), Film("Frozen", 40000)]).studios
Kasir(Bioskop([Film("Avengers", 50000), Film("Frozen", 40000)])).jalan()
