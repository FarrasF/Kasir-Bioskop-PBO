class Film:  # CLASS: cetak biru untuk membuat object film.
    def __init__(self, judul: str, harga: int):
        # CONSTRUCTOR: memvalidasi input lalu mengisi atribut object.
        if not judul.strip():
            raise ValueError("Judul film tidak boleh kosong.")
        if harga <= 0:
            raise ValueError("Harga film harus lebih dari nol.")

        # ATTRIBUTE: menyimpan data film; underscore menandai data internal.
        self._judul = judul.strip()
        self._harga = harga

    # ENCAPSULATION: property menyediakan akses baca untuk atribut internal.
    @property
    def judul(self) -> str:
        return self._judul

    @property
    def harga(self) -> int:
        return self._harga
