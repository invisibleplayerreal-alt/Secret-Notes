from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import base64

# --- Encrype function ---
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

# --- File write and encrype ---
def save_and_encrypt_notes():
    title = entry.get("1.0", "end-1c")
    message = entry2.get("1.0", "end-1c")
    master_secret = entry3.get("1.0", "end-1c")

    if len(title) == 0 or len(message) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Xəta!", message="Bütün sahələri doldurun!")
    else:
        message_encrypted = encode(master_secret, message)
        try:
            with open("mysecret.txt", "a") as data_file:
                data_file.write(f'\n{title}\n{message_encrypted}')
            messagebox.showinfo(title="Uğur!", message="Qeyd yadda saxlanıldı və şifrələndi!")
        except Exception as e:
            messagebox.showinfo(title="Xəta!", message=f"Yazılamadı: {e}")
        finally:
            entry.delete("1.0", END)
            entry2.delete("1.0", END)
            entry3.delete("1.0", END)

# --- File decrypt ---
def decrypt_notes():
    message_encrypted = entry2.get("1.0", "end-1c")
    master_secret = entry3.get("1.0", "end-1c")

    if len(message_encrypted) == 0 or len(master_secret) == 0:
        messagebox.showinfo(title="Xəta!", message="Şifrələnmiş mesaj və açarı daxil edin!")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            entry2.delete("1.0", END)
            entry2.insert("1.0", decrypted_message)
        except Exception as e:
            messagebox.showinfo(title="Xəta!", message="Şifrələnmiş məlumat düzgün deyil!")

# --- Tkinter interface ---
root = Tk()
root.title("Secret Notes")
root.geometry("450x800")

# Imagine
image1 = Image.open("secret.webp")
image1 = image1.resize((250, 150))
photo = ImageTk.PhotoImage(image1)
img_label = Label(root, image=photo)
img_label.pack(pady=10)
root.photo = photo

# Entry
Label(root, text="Secret File Name : ").pack(pady=5)
entry = Text(root, width=15, height=1)
entry.pack()

Label(root, text="Secret Word : ").pack(pady=5)
entry2 = Text(root, width=43, height=23)
entry2.pack(pady=5)

Label(root, text="Key Word: ").pack(pady=5)
entry3 = Text(root, width=15, height=1)
entry3.pack(pady=5)

# Button
Button(root, text="Save and Encrypt", command=save_and_encrypt_notes).pack(pady=1)
Button(root, text="Decrypt", command=decrypt_notes).pack(pady=1)

# Tab and enter function
def focus_next1(event):
    entry2.focus_set()
    return "break"

def focus_next2(event):
    entry3.focus_set()
    return "break"

entry.bind("<Return>", focus_next1)
entry2.bind("<Return>", focus_next2)
entry.bind("<Tab>", focus_next1)
entry2.bind("<Tab>", focus_next2)

root.mainloop()