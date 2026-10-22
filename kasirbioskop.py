from abc import ABC, abstractmethod
from functools import singledispatchmethod


# INTERFACE: hanya method abstrak, tanpa implementasi/atribut
class Pembayaran(ABC):
    @abstractmethod
    def bayar(self, jumlah): ...


class Tunai(Pembayaran):
    def bayar(self, jumlah): return jumlah


class EWallet(Pembayaran):
    def bayar(self, jumlah): return jumlah + 1000  # + biaya admin


# ABSTRACT CLASS: punya method konkret (info) + method abstrak (harga)
class Tiket(ABC):
    def __init__(self, film, kursi):
        self.film, self.kursi = film, kursi

    @abstractmethod
    def harga(self): ...

    def info(self):
        return f"{self.film.judul} kursi {self.kursi}"


# INHERITANCE + OVERRIDING
class Reguler(Tiket):
    def harga(self): return self.film.harga


class VIP(Tiket):
    def harga(self): return self.film.harga + 25000

    def info(self): return "[VIP] " + super().info()  # override method induk


class Film:
    def __init__(self, judul, harga): self.judul, self.harga = judul, harga


class Studio:  # AGREGASI: Film ada di luar Studio, hanya dipakai
    def __init__(self, film, jumlah=5):
        self.film, self.kosong = film, set(range(1, jumlah + 1))


class Bioskop:  # KOMPOSISI: Studio dibuat & dimiliki Bioskop
    def __init__(self, films): self.studios = [Studio(f) for f in films]

    @singledispatchmethod  # OVERLOADING: cari() beda perilaku sesuai tipe argumen
    def cari(self, x): raise TypeError("Gunakan nomor (int) atau judul (str)")

    @cari.register
    def _(self, x: int): return self.studios[x]

    @cari.register
    def _(self, x: str): return next(s for s in self.studios if s.film.judul == x)


class Kasir:  # ASOSIASI: Kasir memakai Bioskop & Pembayaran
    def __init__(self, bioskop, pembayaran): self.bioskop, self.pembayaran = bioskop, pembayaran

    def jual(self, film, kursi, jenis=Reguler):
        studio = self.bioskop.cari(film)
        if kursi not in studio.kosong:
            return print("Kursi tidak tersedia!")
        studio.kosong.remove(kursi)
        tiket = jenis(studio.film, kursi)
        print(f"{tiket.info()} = Rp{self.pembayaran.bayar(tiket.harga()):,}")


bioskop = Bioskop([Film("Avengers", 50000), Film("Frozen", 40000)])
for metode in (Tunai(), EWallet()):  # POLYMORPHISM: bayar() beda hasil per objek
    kasir = Kasir(bioskop, metode)
    kasir.jual("Avengers", 1 if isinstance(metode, Tunai) else 2)  # cari pakai str
    kasir.jual(1, 3 if isinstance(metode, Tunai) else 4, VIP)       # cari pakai int, tiket VIP
kasir.jual("Avengers", 1)  # kursi sudah terjual