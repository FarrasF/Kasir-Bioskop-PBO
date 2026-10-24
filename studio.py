from film import Film


class Studio:  # CLASS: mengelola denah studio dan ketersediaan kursi.
    def __init__(self, film: Film, baris: str = "ABCDEF", jumlah_kolom: int = 5):
        # CONSTRUCTOR: menerima film dan membuat atribut awal studio.
        if not baris or jumlah_kolom < 1:
            raise ValueError("Denah studio harus memiliki baris dan kolom.")

        # AGGREGATION: Studio memakai Film yang dibuat di luar kelas Studio.
        # ATTRIBUTE: data internal setiap object Studio.
        self._film = film
        self._baris = baris
        self._jumlah_kolom = jumlah_kolom
        self._kursi_tersedia = {
            f"{huruf}{nomor}"
            for huruf in baris
            for nomor in range(1, jumlah_kolom + 1)
        }

    # ENCAPSULATION: property memberi akses baca tanpa membuka atribut internal.
    @property
    def film(self) -> Film:
        return self._film

    @property
    def baris(self) -> str:
        return self._baris

    @property
    def jumlah_kolom(self) -> int:
        return self._jumlah_kolom

    @property
    def kursi_tersedia(self) -> frozenset[str]:
        return frozenset(self._kursi_tersedia)

    def kursi_valid(self, kode: str) -> bool:  # METHOD: memeriksa kode di dalam denah.
        semua_kursi = {
            f"{huruf}{nomor}"
            for huruf in self._baris
            for nomor in range(1, self._jumlah_kolom + 1)
        }
        return kode in semua_kursi

    def kursi_bisa_dipesan(self, kode: str) -> bool:  # METHOD: memeriksa kursi kosong.
        return kode in self._kursi_tersedia

    def pesan_kursi(self, kode: str) -> None:  # METHOD: menandai kursi sebagai terisi.
        if not self.kursi_bisa_dipesan(kode):
            raise ValueError("Kursi tidak tersedia!")
        self._kursi_tersedia.remove(kode)
