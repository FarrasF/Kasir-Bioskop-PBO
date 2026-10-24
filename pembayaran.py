from abc import ABC, abstractmethod


class Pembayaran(ABC):  # INTERFACE: menetapkan kontrak untuk semua metode pembayaran.
    @property
    @abstractmethod
    def nama(self) -> str:
        ...

    @abstractmethod
    def bayar(self, jumlah: int) -> int:
        ...


class Tunai(Pembayaran):  # INHERITANCE: Tunai mengimplementasikan kontrak Pembayaran.
    @property
    def nama(self) -> str:
        return "Tunai"

    def bayar(self, jumlah: int) -> int:
        return jumlah


class QRIS(Pembayaran):  # INHERITANCE: QRIS mengimplementasikan kontrak Pembayaran.
    BIAYA_ADMIN = 1000

    @property
    def nama(self) -> str:
        return "QRIS"

    def bayar(self, jumlah: int) -> int:
        return jumlah + self.BIAYA_ADMIN


class Debit(Pembayaran):  # INHERITANCE: Debit mengimplementasikan kontrak Pembayaran.
    @property
    def nama(self) -> str:
        return "Debit"

    def bayar(self, jumlah: int) -> int:
        return jumlah
