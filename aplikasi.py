from bioskop import Bioskop
from film import Film
from kasir import Kasir
from pembayaran import Debit, Pembayaran, QRIS, Tunai
from studio import Studio
from tiket import Reguler, Tiket, VIP


class AplikasiKasir:  # CLASS: mengatur antarmuka dan alur pemesanan.
    LEBAR = 52

    def __init__(self):
        # CONSTRUCTOR: membuat objek Film dan Bioskop untuk sesi aplikasi.
        judul = ("Spiderman", "The Odyssey", "Filosofi Teras", "Laut Bercerita", "Resident Evil")
        self._bioskop = Bioskop([Film(nama, 50000) for nama in judul])

    @staticmethod
    def rupiah(jumlah: int) -> str:
        return f"Rp{jumlah:,}".replace(",", ".")

    def judul(self, teks: str) -> None:  # METHOD: menampilkan judul bagian.
        print(f"\n{'=' * self.LEBAR}\n  {teks}\n{'=' * self.LEBAR}")

    @staticmethod
    def pilih_nomor(prompt: str, minimum: int, maksimum: int) -> int:
        while True:
            try:
                pilihan = int(input(prompt))
            except ValueError:
                print("  Masukkan angka yang valid.")
                continue
            if minimum <= pilihan <= maksimum:
                return pilihan
            print(f"  Pilihan harus antara {minimum} dan {maksimum}.")

    @staticmethod
    def tampilkan_denah(studio: Studio) -> None:
        lebar = 6
        garis = "    +" + "+".join("-" * lebar for _ in range(studio.jumlah_kolom)) + "+"
        batas_layar = "    +" + "-" * (len(garis) - 6) + "+"
        print(f"\n{batas_layar}\n    |{'LAYAR BIOSKOP'.center(len(garis) - 6)}|\n{batas_layar}\n{garis}")
        tersedia = studio.kursi_tersedia
        for baris in studio.baris:
            kursi = (f"{(kode if kode in tersedia else 'X'):^{lebar}}"
                     for kode in (f"{baris}{n}" for n in range(1, studio.jumlah_kolom + 1)))
            print(" " * 4 + "|" + "|".join(kursi) + "|\n" + garis)
        print("  Kode kursi ada di dalam kotak; X = kursi terisi")

    def pilih_film(self) -> tuple[Film, Studio]:
        films = self._bioskop.films
        self.judul("PILIH FILM")
        print(f"  {'NO.':<6}{'JUDUL FILM':<30}{'HARGA':>14}\n  {'-' * (self.LEBAR - 4)}")
        for nomor, film in enumerate(films, 1):
            print(f"  {nomor:<6}{film.judul:<30}{self.rupiah(film.harga):>14}")
        film = films[self.pilih_nomor("\n  Masukkan nomor film: ", 1, len(films)) - 1]
        return film, self._bioskop.cari(film.judul)

    def pilih_kursi(self, film: Film, studio: Studio) -> str:
        self.judul("PILIH KURSI")
        print(f"  Film: {film.judul}")
        self.tampilkan_denah(studio)
        while True:
            kursi = input("\n  Masukkan kode kursi (contoh A1): ").strip().upper()
            if studio.kursi_bisa_dipesan(kursi):
                print(f"  Kursi {kursi} dipilih.")
                return kursi
            status = "sudah terisi" if studio.kursi_valid(kursi) else "tidak valid"
            print(f"  Kursi {status}. Silakan pilih lagi.")

    def pilih_jenis_tiket(self, film: Film) -> type[Tiket]:
        self.judul("PILIH JENIS TIKET")
        print(f"  1. Reguler               {self.rupiah(film.harga)}")
        harga_vip = self.rupiah(film.harga + VIP.TAMBAHAN_HARGA)
        tambahan = self.rupiah(VIP.TAMBAHAN_HARGA)
        print(f"  2. VIP                   {harga_vip} (termasuk tambahan {tambahan})")
        return (Reguler, VIP)[self.pilih_nomor("\n  Masukkan pilihan: ", 1, 2) - 1]

    def pilih_pembayaran(self) -> Pembayaran:
        self.judul("PILIH PEMBAYARAN")
        print(f"  1. Tunai\n  2. QRIS (biaya admin {self.rupiah(QRIS.BIAYA_ADMIN)})\n  3. Debit")
        return (Tunai, QRIS, Debit)[self.pilih_nomor("\n  Masukkan pilihan: ", 1, 3) - 1]()

    def cetak_struk(self, tiket: Tiket, pembayaran: Pembayaran, total: int) -> None:
        self.judul("STRUK PEMESANAN")
        print("  +--------------------------------------------------+\n"
              "  |                 BIOSKOP - E-TIKET                |\n"
              "  +--------------------------------------------------+")
        for label, nilai in (("Film", tiket.film.judul), ("Kursi", tiket.kursi),
                             ("Jenis tiket", tiket.jenis)):
            print(f"  | {label:<16}: {nilai:<30} |")
        print("  |" + "-" * 50 + "|")
        for label, nilai in (("Harga tiket", self.rupiah(tiket.harga())),
                             ("Pembayaran", pembayaran.nama),
                             ("Biaya admin", self.rupiah(total - tiket.harga()))):
            print(f"  | {label:<16}: {nilai:<30} |")
        print(f"  +--------------------------------------------------+\n"
              f"  | {'TOTAL PEMBAYARAN':<20}{self.rupiah(total):>28} |\n"
              f"  +--------------------------------------------------+\n"
              f"  Terima kasih. Selamat menonton!\n{'=' * self.LEBAR}")

    def jalankan(self) -> None:  # METHOD: menjalankan seluruh alur pemesanan.
        print(f"\n{'=' * self.LEBAR}\n             PEMESANAN TIKET BIOSKOP\n{'=' * self.LEBAR}")
        film, studio = self.pilih_film()
        kursi = self.pilih_kursi(film, studio)
        jenis = self.pilih_jenis_tiket(film)
        pembayaran = self.pilih_pembayaran()
        tiket, total = Kasir(self._bioskop, pembayaran).jual(
            film.judul, kursi, jenis
        )
        self.cetak_struk(tiket, pembayaran, total)
