from bioskop import Bioskop
from pembayaran import Pembayaran
from tiket import Reguler, Tiket


class Kasir:  # CLASS: mengatur transaksi penjualan tiket.
    def __init__(self, bioskop: Bioskop, pembayaran: Pembayaran):
        # CONSTRUCTOR: menerima layanan yang dipakai object Kasir.
        # ASSOCIATION: Bioskop dan Pembayaran dibuat di luar lalu digunakan Kasir.
        self._bioskop = bioskop
        self._pembayaran = pembayaran

    # ENCAPSULATION: expose metode pembayaran sebagai akses baca.
    @property
    def pembayaran(self) -> Pembayaran:
        return self._pembayaran

    def jual(
        self,
        film: int | str,
        kursi: str,
        jenis: type[Tiket] = Reguler,
    ) -> tuple[Tiket, int]:
        # METHOD: membuat tiket, memproses pembayaran, dan memesan kursi.
        studio = self._bioskop.cari(film)
        if not studio.kursi_bisa_dipesan(kursi):
            raise ValueError("Kursi tidak tersedia!")

        # POLYMORPHISM: class tiket dan object pembayaran menentukan perilakunya.
        tiket = jenis(studio.film, kursi)
        total = self._pembayaran.bayar(tiket.harga())
        studio.pesan_kursi(kursi)
        return tiket, total
