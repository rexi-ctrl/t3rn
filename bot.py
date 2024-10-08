from web3 import Web3
from eth_account import Account
import time
import sys
import os

# Fungsi untuk menampilkan teks di tengah layar
def center_text(text):
    terminal_width = os.get_terminal_size().columns
    lines = text.splitlines()
    centered_lines = [line.center(terminal_width) for line in lines]
    return "\n".join(centered_lines)


ascii_art = """
                                         CT IS CONTOL
"""

# Deskripsi teks
description = """
Bot Auto Bridge  https://bridge.t1rn.io/
"""


print("\033[92m" + center_text(ascii_art) + "\033[0m")
print(center_text(description))

# Tambahkan jarak dua paragraf setelah deskripsi teks
print("\n\n")

# Detail jaringan
private_key = 'PK'
rpc_url = 'https://sepolia.optimism.io'
chain_id = 11155420
contract_address = '0xF221750e52aA080835d2957F2Eed0d5d7dDD8C38' #JANGAN DIGANTI
w3 = Web3()
non_checksum_address = "ADDRESS"
my_address = w3.to_checksum_address(non_checksum_address)


# Koneksi ke jaringan
web3 = Web3(Web3.HTTPProvider(rpc_url))
if not web3.is_connected():
    raise Exception("Tidak dapat terhubung ke jaringan")

# Buat akun dari private key
account = Account.from_key(private_key)

# Data transaksi untuk bridge
data = '0x56591d5962737370000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d360f8df9604efa1de0e8e70fa3a7023b966053200000000000000000000000000000000000000000000000000238644b463d65700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002386f26fc10000'

# Fungsi untuk membuat dan mengirim transaksi
def send_bridge_transaction():
    # Ambil nonce untuk alamat pengirim
    nonce = web3.eth.get_transaction_count(my_address)

    # Estimasi gas
    try:
        gas_estimate = web3.eth.estimate_gas({
            'to': contract_address,
            'from': my_address,
            'data': data,
            'value': web3.to_wei(0.01, 'ether')  # Mengirim 0.01 ETH
        })
        gas_limit = gas_estimate + 10000  # Tambahkan buffer gas
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return None

    # Buat transaksi
    transaction = {
        'nonce': nonce,
        'to': contract_address,
        'value': web3.to_wei(0.01, 'ether'),  # Mengirim 0.01 ETH
        'gas': gas_limit,  # Gunakan gas limit yang diestimasi
        'gasPrice': web3.eth.gas_price,
        'chainId': chain_id,
        'data': data
    }

    # Tanda tangani transaksi dengan private key
    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

    # Kirim transaksi
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None

# Jalankan script sampai dihentikan secara manual
successful_txs = 0

try:
    while True:
        tx_hash = send_bridge_transaction()
        if tx_hash:
            successful_txs += 1
            print(f"Tx Hash: {tx_hash} | Total Tx Sukses: {successful_txs}")
        time.sleep(25)  # Delay 25 detik setiap transaksi
except KeyboardInterrupt:
    print("\nScript dihentikan oleh pengguna.")
    print(f"Total transaksi sukses: {successful_txs}")
    sys.exit(0)
