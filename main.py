import customtkinter
import tkinter
from tkinter import filedialog
import module

filePath = None
encryptFile = None
decryptFile = None
KprivateFile = None


def createButton(app, x, y, text, command):
    button = customtkinter.CTkButton(
        master=app, text=text, command=command, corner_radius=30)
    button.place(relx=x, rely=y, anchor=tkinter.CENTER)


def createLabel(app, x, y, text):
    label = customtkinter.CTkLabel(master=app, text=text, wraplength=400)
    label.place(relx=x, rely=y, anchor=tkinter.CENTER)
    return label


def readFile(filePath):
    with open(filePath, "r", encoding="utf-8") as f:
        return f.read()


def printDecryptResult(window):
    global KprivateFile
    global decryptFile
    filePath = filedialog.askopenfilename()
    if filePath:
        print('File path: ', filePath)

    KprivateFile = filePath
    createLabel(window, 0.5, 0.8, f'File Kprivate là {KprivateFile}')

    result_label = createLabel(window, 0.5, 0.9, '')
    module.decrypt_module(
        decryptFile, KprivateFile, result_label)
    # status, resultPath = module.decrypt_module(
    #     decryptFile, KprivateFile, result_label)
    # if status is None or resultPath is None:
    #     result_label.configure(text="Lỗi: Không thể giải mã file.")
    # elif status == 1:
    #     result_label.configure(
    #         text=f'Nội dung file sau khi Decrypt: \n {readFile(resultPath)}')
    # else:
    #     result_label.configure(text=resultPath)


def selectFile(fileType, window):

    global encryptFile
    global decryptFile
    global KprivateFile

    filePath = filedialog.askopenfilename()
    if filePath:
        print('File path: ', filePath)

    result_label = createLabel(window, 0.5, 0.7, '')

    if fileType == 0:
        encryptFile = filePath
        createLabel(window, 0.5, 0.6, f'File Encrypt là {encryptFile}')
        module.encrypt_module(filepath=filePath, result_label=result_label)

    elif fileType == 1:
        decryptFile = filePath
        createLabel(window, 0.5, 0.6, f'File Decrypt là {decryptFile}')
        createButton(window, 0.5, 0.7, 'Chọn file Kprivate',
                     command=lambda: printDecryptResult(window))


def createModesWindow(mode, app):
    modeWindow = customtkinter.CTkToplevel()
    modeWindow.title(mode + ' mode')
    modeWindow.geometry("1000x550")

    label = customtkinter.CTkLabel(
        master=modeWindow, text='Đây là chức năng ' + mode)
    label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    # Withdraw the main window
    app.withdraw()

    def disable_close():
        pass

    modeWindow.protocol("WM_DELETE_WINDOW", disable_close)

    return modeWindow


def goBackFunc(app, window):
    window.destroy()
    app.deiconify()
    choose_encrypt_decrypt(app)


def encrypt(app):
    print('Encrypt function')
    window = createModesWindow('Encrypt', app)

    createButton(window, 0.5, 0.5, 'Chọn 1 file để Encrypt',
                 command=lambda: selectFile(0, window))
    createButton(window, 0.1, 0.05, 'Quay lại',
                 command=lambda: goBackFunc(app, window))


def decrypt(app):
    print('Decrypt function')
    window = createModesWindow('Decrypt', app)

    createButton(window, 0.5, 0.5, 'Chọn 1 file để Decrypt',
                 command=lambda: selectFile(1, window))

    createButton(window, 0.1, 0.05, 'Quay lại',
                 command=lambda: goBackFunc(app, window))


def choose_encrypt_decrypt(app):
    createLabel(app, 0.5, 0.35, 'Chọn chức năng mong muốn')

    createButton(app, 0.5, 0.45, 'Encrypt', command=lambda: encrypt(app))
    createButton(app, 0.5, 0.55, 'Decrypt', command=lambda: decrypt(app))


def main():
    customtkinter.set_appearance_mode("dark")

    app = customtkinter.CTk()

    app.title("Project 1 - Encryption")
    app.geometry("1000x550")

    choose_encrypt_decrypt(app)

    app.mainloop()


if __name__ == "__main__":
    main()
