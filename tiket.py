from abc import ABC, abstractmethod

from film import Film


class Tiket(ABC):  # ABSTRACT CLASS: menyimpan data dan kontrak umum semua tiket.
    jenis = "Tiket"

    def __init__(self, film: Film, kursi: str):
        # CONSTRUCTOR: menyimpan atribut film dan kursi pada object tiket.
        self._film = film
        self._kursi = kursi

    # ENCAPSULATION: properti hanya menyediakan akses baca ke data tiket.
    @property
    def film(self) -> Film:
        return self._film

    @property
    def kursi(self) -> str:
        return self._kursi

    @abstractmethod
    def harga(self) -> int:
        ...

    # METHOD: menyiapkan informasi dasar tiket.
    def info(self) -> str:
        return f"{self.jenis} - {self.film.judul}, kursi {self.kursi}"


class Reguler(Tiket):  # INHERITANCE: tiket reguler mewarisi struktur dari Tiket.
    jenis = "Reguler"

    def harga(self) -> int:
        return self.film.harga


class VIP(Tiket):  # INHERITANCE: tiket VIP mewarisi struktur dari Tiket.
    jenis = "VIP"
    TAMBAHAN_HARGA = 25000

    def harga(self) -> int:
        return self.film.harga + self.TAMBAHAN_HARGA

    def info(self) -> str:  # OVERRIDING: mengganti info() untuk menandai tiket VIP.
        return "[VIP] " + super().info()
