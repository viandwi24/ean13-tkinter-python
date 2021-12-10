from tkinter import *
from tkinter import messagebox
from lib import Ean13, Ean13Canvas
    
def generate(input_code: str, save_name: str, canvas: Ean13Canvas, txt_checksum: Entry, txt_encoded: Entry, opt_txt_color: StringVar) -> None:
    """GENERATE BARCODE
    
    Fungsi ini akan membuat barcode dari inputan user

    Args:
        input_code (str): code yang akan dibuat barcode
        save_name (str): nama file yang akan disimpan
        canvas (Ean13Canvas): instance dari canvas
        txt_checksum (Entry): widget text untuk meletakan checksum
        txt_encoded (Entry): widget text untuk meletakan hasil encoded
        opt_txt_color (StringVar): instance dari widget option menu
    """    
    # check input digit muse be 12
    if len(input_code) != 12:
        # show error message
        return messagebox.showerror('Error', 'Input Code Must Be 12 Digits')
    # check input must be number
    if not input_code.isdigit():
        # show error message
        return messagebox.showerror('Error', 'Input Code Must Be Number')
    
    # create instance
    ean13: Ean13 = canvas.generate_barcode(input_code)
    
    # draw barcode
    canvas.draw_barcode(
        ean13.codeStr,
        ean13.encodedCode,
        opt_txt_color.get(),
    )
    canvas.save_barcode(
        ean13.codeStr,
        ean13.encodedCode,
        opt_txt_color.get(),
        save_name,
        460,
        520
    )
    txt_checksum.configure(state='normal')
    txt_checksum.delete(0, END)
    txt_checksum.insert(0, ean13.calculate_checksum())
    txt_checksum.configure(state='disabled')
    txt_encoded.configure(state='normal')
    txt_encoded.delete(0, END)
    txt_encoded.insert(0, ean13.encodedCode)
    txt_encoded.configure(state='disabled')

def main() -> None:
    """MAIN
    
    Fungsi main akan membuat window dan widget
    """    
    # membuat window dengan tkinter
    window = Tk()
    window.geometry("460x550")
    window.title('EAN-13')

    # membuat widget
    canvas = Ean13Canvas(window, background='white', height=280)
    lbl_save = Label(window, text="File Name To Save : ", font=("bold", 12), justify=LEFT, anchor='w')
    lbl_input = Label(window, text="Input Code (12 digits) : ", font=("bold", 12), justify=LEFT, anchor='w')
    txt_save = Entry(window, width=30)
    txt_input = Entry(window, width=30)
    lbl_color = Label(window, text="Bar Color : ", font=("bold", 12), justify=LEFT, anchor='w')
    opt_txt_color = StringVar(window)
    opt_txt_color.set("colorfull")
    txt_color = OptionMenu(
        window,
        opt_txt_color,
        "colorfull",
        "black"
    )
    lbl_check = Label(window, text="Checksum Digit : ", font=("bold", 12), justify=CENTER, anchor='w')
    txt_checksum = Entry(window, width=47, justify=CENTER)
    lbl_encoded = Label(window, text="Encoded : ", font=("bold", 12), justify=CENTER, anchor='w')
    txt_encoded = Entry(window, width=47)
    btn_generate = Button(
        window,
        text="Generate",
        command=lambda: generate(
            txt_input.get(),
            txt_save.get(),
            canvas,
            txt_checksum,
            txt_encoded,
            opt_txt_color
        )
    )
    
    # meletakan widget
    lbl_save.grid(sticky=W, row=0, column=0, padx=10, pady=5)
    lbl_input.grid(sticky=W, row=1, column=0, padx=10, pady=5)
    txt_save.grid(row=0, column=1, padx=10)
    txt_input.grid(row=1, column=1, padx=10)
    txt_color.grid(row=2, column=1, padx=10, sticky=N+S+E+W)
    lbl_color.grid(sticky=W, row=2, column=0, padx=10, pady=5)
    btn_generate.grid(row=3, column=1, sticky=N+S+E+W, ipady=2, padx=10)
    canvas.grid(row=4, column=0, columnspan=2, sticky=N+S+E+W, pady=5, padx=10)
    lbl_check.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
    txt_checksum.grid(row=6, column=0, columnspan=2, padx=10)
    lbl_encoded.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
    txt_encoded.grid(row=8, column=0, columnspan=2, padx=10)
    
    # membuat nilai awal untuk widget
    txt_save.insert(0, 'EAN13.eps')
    txt_input.insert(0, '899702980997')
    generate(txt_input.get(), txt_save.get(), canvas, txt_checksum, txt_encoded, opt_txt_color)

    # looping window agar tetap terbuka
    window.mainloop()

if __name__ == "__main__":
    main()
