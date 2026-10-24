from functools import singledispatchmethod

from film import Film
from studio import Studio


class Bioskop:  # CLASS: mengelola koleksi film beserta studio pemutarannya.
    def __init__(self, films: list[Film]):
        # CONSTRUCTOR: menerima film dan menyiapkan studio untuk masing-masing.
        if not films:
            raise ValueError("Bioskop harus memiliki setidaknya satu film.")

        # COMPOSITION: Bioskop membuat dan memiliki objek Studio.
        self._studios = tuple(Studio(film) for film in films)

    # ENCAPSULATION: daftar film diberikan sebagai tuple, bukan koleksi internal.
    @property
    def films(self) -> tuple[Film, ...]:
        return tuple(studio.film for studio in self._studios)

    @singledispatchmethod  # OVERLOADING: cari() memilih implementasi sesuai tipe kunci.
    def cari(self, kunci: int | str) -> Studio:
        raise TypeError("Gunakan nomor film (int) atau judul film (str).")

    @cari.register  # METHOD: mencari studio dengan nomor urut film.
    def _(self, kunci: int) -> Studio:
        if not 1 <= kunci <= len(self._studios):
            raise IndexError("Nomor film tidak ditemukan.")
        return self._studios[kunci - 1]

    @cari.register  # METHOD: mencari studio dengan judul film.
    def _(self, kunci: str) -> Studio:
        for studio in self._studios:
            if studio.film.judul.casefold() == kunci.strip().casefold():
                return studio
        raise LookupError(f"Film '{kunci}' tidak ditemukan.")
