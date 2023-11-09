from tkinter import Tk, Label, Entry, Button, Text, messagebox
from Crypto.Cipher import DES

# Fungsi untuk menambahkan padding PKCS#7
def add_padding(data):
    padding_length = 8 - (len(data) % 8)
    padded_data = data + bytes([padding_length] * padding_length)
    return padded_data

# Fungsi untuk mengenkripsi pesan menggunakan DES
def encrypt_message():
    sender_name = sender_name_entry.get()
    message = message_entry.get()
    key = key_entry.get()

    # Cek jika ada form yang kosong
    if not sender_name or not message or not key:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")
        return

    sender_name = sender_name.encode()
    message = message.encode()

    # Pastikan key memiliki panjang 8 byte
    key = key.ljust(8)[:8].encode()  # Mengambil 8 karakter pertama dari key dan menambahkan padding jika kurang dari 8 karakter
    
    # Menambahkan padding ke sender_name dan message
    padded_sender_name = add_padding(sender_name)
    padded_message = add_padding(message)
    
    # Mengenkripsi data yang telah dipadding menggunakan DES
    des = DES.new(key, DES.MODE_ECB)
    encrypted_sender_name = des.encrypt(padded_sender_name)
    encrypted_message = des.encrypt(padded_message)
    
    # Menampilkan hasil enkripsi
    result_text.config(state='normal')  # Membuka widget untuk diedit
    result_text.delete('1.0', 'end')  # Menghapus teks yang ada
    result_text.insert('end', f"Sender : {encrypted_sender_name.hex()}\nMessage : {encrypted_message.hex()}")
    result_text.config(state='disabled')  # Menutup widget agar tidak bisa diedit lagi

# Membuat jendela aplikasi
root = Tk()
root.title("Enkripsi DES")

# Label dan input untuk nama pengirim
sender_name_label = Label(root, text="Pengirim:")
sender_name_label.pack()
sender_name_entry = Entry(root)
sender_name_entry.pack()

# Label dan input untuk pesan
message_label = Label(root, text="Pesan:")
message_label.pack()
message_entry = Entry(root)
message_entry.pack()

# Label dan input untuk key
key_label = Label(root, text="Key (min. 8 chart) :")
key_label.pack()
key_entry = Entry(root, show="*")
key_entry.pack()

# Tombol untuk melakukan enkripsi
encrypt_button = Button(root, text="Enkripsi", command=encrypt_message)
encrypt_button.pack()

# Widget Text untuk menampilkan hasil enkripsi
result_text = Text(root, height=10, width=50)
result_text.config(state='disabled')  # Awalnya menutup widget agar tidak bisa diedit
result_text.pack()

# Menjalankan aplikasi
root.mainloop()