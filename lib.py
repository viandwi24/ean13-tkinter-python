from tkinter import *
import os

class Ean13:
    """EAN13 Barcode Generator
    
    Class ini berfungsi untuk menghasilkan barcode EAN13. Ditulis oleh viandwi24
    
    codeStr - Code digit yang akan di encode
    """
    length = 13         # The length of the code
    
    # MAPPING TABLE UNTUK L CODE
    L_CODE = {
        0: "0001101", 1: "0011001", 2: "0010011",
        3: "0111101", 4: "0100011", 5: "0110001",
        6: "0101111", 7: "0111011", 8: "0110111",
        9: "0001011"
    }
    
    # MAPPING TABLE UNTUK R CODE
    R_CODE = {
        0: "1110010", 1: "1100110", 2: "1101100",
        3: "1000010", 4: "1011100", 5: "1001110",
        6: "1010000", 7: "1000100", 8: "1001000",
        9: "1110100"
    }
    
    # MAPPING TABLE UNTUK G CODE
    G_CODE = {
        0: "0100111", 1: "0110011", 2: "0011011",
        3: "0100001", 4: "0011101", 5: "0111001",
        6: "0000101", 7: "0010001", 8: "0001001",
        9: "0010111"
    }
    
    # STRUKTUR KODE EAN13 YANG SESUAI DENGAN DIGIT AWAL
    STRUCTURE_CODE = {
        0: (L_CODE, L_CODE, L_CODE, L_CODE, L_CODE, L_CODE),
        1: (L_CODE, L_CODE, G_CODE, L_CODE, G_CODE, G_CODE),
        2: (L_CODE, L_CODE, G_CODE, G_CODE, L_CODE, G_CODE),
        3: (L_CODE, L_CODE, G_CODE, G_CODE, G_CODE, L_CODE),
        4: (L_CODE, G_CODE, L_CODE, L_CODE, G_CODE, G_CODE),
        5: (L_CODE, G_CODE, G_CODE, L_CODE, L_CODE, G_CODE),
        6: (L_CODE, G_CODE, G_CODE, G_CODE, L_CODE, L_CODE),
        7: (L_CODE, G_CODE, L_CODE, G_CODE, L_CODE, G_CODE),
        8: (L_CODE, G_CODE, L_CODE, G_CODE, G_CODE, L_CODE),
        9: (L_CODE, G_CODE, G_CODE, L_CODE, G_CODE, L_CODE)
    }
    
    def __init__(self, codeStr: str) -> None:
        """Constructor
        
        Code digit akan di encode menjadi bit dan di buat juga checksumnya

        Args:
            codeStr (str): code digit yang akan di encode
        """
        self.codeStr = codeStr + str(0)
        self.codeNum = [int(x) for x in self.codeStr]
        checksum = self.calculate_checksum()
        self.codeStr = self.codeStr[:12] + str(checksum)
        self.codeNum = [int(x) for x in self.codeStr]
        self.calculate()
        
    def calculate(self):
        """Menghasilkan bit dari code digit

        Returns:
            encodedCode (str): deretan bit yang dihasilkan dari encode
        """        
        left = self.STRUCTURE_CODE[self.codeNum[0]]
        # membuat divider awal
        self.encodedCode = 'L0L'
        # menghasilkan bit dari code 6 digit pertama
        for i in range(0, 6):
            self.encodedCode += left[i][self.codeNum[i+1]]
        # membuat divider tengah
        self.encodedCode += '0L0L0'
        # menghasilkan bit dari code 6 digit terakhir
        for i in range(7, 13):
            self.encodedCode += self.R_CODE[self.codeNum[i]]
        # membuat divider akhir
        self.encodedCode += 'L0L'
        # return
        return self.encodedCode
    
    def calculate_checksum(self):
        """Menghitung checksum dari code digit

        Returns:
            code (int): nilai checksum dari code digit
        """        
        weight = [1, 3] * 6
        magic = 10
        sum = 0
        for i in range(12):
            sum = sum + self.codeNum[i] * weight[i]
        z = (magic - (sum % magic)) % magic
        if z < 0 or z >= magic:
            return None
        return z 

class Ean13Canvas(Canvas):
    """Ean13Canvas
    
    Class ini berfungsi mempermudah menggenerate barcode EAN13 dibantu dengan canvas tkinter

    Args:
        Canvas (Canvas): Instance Canvas dari tkinter
    """ 
    
    def generate_barcode(self, code: str) -> Ean13:
        """Membuat instance barcode EAN13

        Args:
            code (str): code digit yang akan di encode

        Returns:
            Ean13: instance barcode EAN13
        """        
        ean13 = Ean13(code)
        return ean13
        
    def draw_barcode(self, code: str, encodedCode: str, color: str):
        """Menggambar barcode EAN13 ke dalam canvas

        Args:
            code (str): code digit yang akan di encode
            encodedCode (str): code digit yang telah di encode menjadi bit
            color (str): warna bar yang dihasilkan di barcode
        """        
        height = 175
        width_per_bit = 4
        ml = 30
        mt = 40
        colorfull = True if color == 'colorfull' else False
        with_text = True
        font_size = 42
        
        # 
        self.delete("all")
        
        # first digit
        if with_text:
            self.create_text(
                0 + ml - (font_size / 1.5),
                0 + mt + height,
                text=code[:1],
                fill="black",
                font=("Arial", font_size),
                justify="left",
                anchor="nw"
            )
            self.create_text(
                0 + ml + ((font_size / 1.5)),
                0 + mt + height,
                text=code[1:7],
                fill="black",
                font=("Arial", font_size),
                justify="left",
                anchor="nw"
            )
            self.create_text(
                0 + ml + ((font_size / 1.5) * 8) - ((font_size / 1.5) / 2),
                0 + mt + height,
                text=code[7:13],
                fill="black",
                font=("Arial", font_size),
                justify="left",
                anchor="nw"
            )
        
        index = 0
        a = True
        for i in range(len(encodedCode)):
            bit = encodedCode[i]
            
            # Draw normal bar
            if bit == '1':
                self.create_rectangle(
                    ml + i * width_per_bit,
                    mt,
                    ml + i * width_per_bit + (1 * width_per_bit),
                    mt + height,
                    fill='green' if colorfull else 'black',
                    outline='green' if colorfull else 'black'
                )
            # Draw long bar
            elif bit == 'L':
                self.create_rectangle(
                    ml + i * width_per_bit,
                    mt,
                    ml + i * width_per_bit + (1 * width_per_bit),
                    mt + height + (height * 10 / 100),
                    fill = 'blue' if colorfull else 'black',
                    outline='blue' if colorfull else 'black'
                )
            index += 1
        
        # scale canvas before save
        # self.scale('all', 0, 0, 5, 5)
                
    def save_barcode(self, code: str, encodedCode: str, color: str, path: str, width: int, height: int):
        """Menyimpan barcode EAN13 ke dalam file

        Args:
            code (str): code digit yang akan di encode
            encodedCode (str): code digit yang telah di encode menjadi bit
            color (str): warna bar yang dihasilkan di barcode
            path (str): nama file yang akan disimpan
            width (int): ukuran panjang dari gambar
            height (int): ukuran lebar dari gambar
        """        
        self.draw_barcode(code, encodedCode, color)
        # check if exist delete
        if os.path.isfile(path):
            os.remove(path)
        
        # save
        self.postscript(
            file=path,
            colormode='color',
            width=width,
            height=height,
        )
