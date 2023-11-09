from tkinter import Tk, Label, Entry, Button, messagebox
from Crypto.Cipher import DES

# Fungsi untuk menghapus padding PKCS#7 dari data yang telah didekripsi
def remove_padding(data):
    padding_length = data[-1]
    if padding_length > 8:
        raise ValueError("Invalid padding length.")
    # Periksa bahwa semua byte padding memiliki nilai yang sama dengan panjang padding
    if data[-padding_length:] != bytes([padding_length] * padding_length):
        raise ValueError("Invalid padding.")
    return data[:-padding_length]

# Fungsi untuk mendekripsi pesan menggunakan DES
def decrypt_message():
    try:
        encrypted_sender_name = bytes.fromhex(sender_name_entry.get())
        encrypted_message = bytes.fromhex(message_entry.get())
        key = key_entry.get().encode()

        # Tambahkan padding pada key untuk mencapai 8 byte jika kurang
        key = key.ljust(8, b'\x00')[:8]

        # Mendekripsi data menggunakan DES
        des = DES.new(key, DES.MODE_ECB)
        decrypted_sender_name = remove_padding(des.decrypt(encrypted_sender_name)).decode('utf-8', errors='ignore')
        decrypted_message = remove_padding(des.decrypt(encrypted_message)).decode('utf-8', errors='ignore')
        
        # Menampilkan hasil dekripsi
        result_label.config(text="Nama Pengirim: " + decrypted_sender_name + "\nPesan: " + decrypted_message)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "Terjadi kesalahan saat mendekripsi: " + str(e))

# Membuat jendela aplikasi
root = Tk()
root.title("Dekripsi DES")

# Label dan input untuk ciphertext nama pengirim
sender_name_label = Label(root, text="Ciphertext (Pengirim):")
sender_name_label.pack()
sender_name_entry = Entry(root, width=30)
sender_name_entry.pack()

# Label dan input untuk ciphertext pesan
message_label = Label(root, text="Ciphertext (Pesan):")
message_label.pack()
message_entry = Entry(root, width=30)
message_entry.pack()

# Label dan input untuk key
key_label = Label(root, text="Key (min. 8 chart):")
key_label.pack()
key_entry = Entry(root, show="*", width=30)
key_entry.pack()

# Tombol untuk melakukan dekripsi
decrypt_button = Button(root, text="Dekripsi", command=decrypt_message)
decrypt_button.pack()

# Label untuk menampilkan hasil dekripsi
result_label = Label(root, text="")
result_label.pack()

# Menjalankan aplikasi
root.mainloop()
