import tkinter as tk



class Lampada:

    def __init__(self):

        self.x1 = 340
        self.y1 = 10
        self.x2 = 440
        self.y2 = 110


        self.outline = "black"

        self.color = "#ffffff" # Cor que será renderizada
        self.color_saved = "#ffffff" # Preciso disso para não perder a cor quando ajustar a luminosidade
        self.aux = "#000000" # Serve para salvar a cor anterior quando apagar

        self.luminosidade = 100 # Valor de 0 a 100 que só será chamado quando eu mudar a cor, para aplicar a luminosidade

        # Vou salvar qual função eu vou chamar, apagar ou acender, e intercambiar entre as duas funções
        self.on_off = self.apagar_lampada
        self.onoff_aux = self.acender_lampada

        self.state = "ON"





    # Renderização da lâmpada
    def renderizar_lampada(self, canvas):

        canvas.create_oval(self.x1,
                           self.y1,
                           self.x2,
                           self.y2,
                           outline = self.outline,
                           fill = self.color)
    
    def renderizar_ajuste_de_cor(self, nova_cor, canvas):
        # Renderiza só quando necessário, feita para
        # entender quando a lâmpada está ligada e desligada

        if self.state == "OFF": self.aux = nova_cor
        else:
            self.color = nova_cor
            self.renderizar_lampada(canvas)
    



    # Apagar e acender
    def apagar_lampada(self, canvas):

        canvas.delete("all") # Limpa o canvas

        self.aux = self.color
        self.color = "#000000"

        self.switch_on_off()
        self.state = "OFF"

        self.renderizar_lampada(canvas)
    
    def acender_lampada(self, canvas):

        self.color = self.aux # Quando acender eu recupero a cor guardada

        self.switch_on_off()
        self.state = "ON"
        
        self.renderizar_lampada(canvas)
    
    def switch_on_off(self):
        # Quando apagar a lampada ser chamado no on_off, eu troco
        # para a próxima funcionalidade ser acender
        self.on_off, self.onoff_aux = self.onoff_aux, self.on_off








    # Mudança na luminosidade
    # VOU CONVERTER O VALOR HEXADECIMAL PARA RGB
    # APLICAR O MULTIPLICADOR DA ESCALA PARA CADA VALOR DE RGB
    # E POR FIM ATUALIZAR O VALOR NO SELF.COLOR
    # E DAÍ RENDERIZAR NOVAMENTE
    # Converter para hexadecimal (Função do StackOverflow)
    def hex_to_rgb(self, hexa):

        hexa = hexa.strip("#")
        return list(int(hexa[i:i+2], 16)  for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return '%02x%02x%02x' % rgb
    
    def ajustar_rgb(self, lista, valor_da_intensidade):

        for n in range(len(lista)):

            lista[n] = int(lista[n] * (valor_da_intensidade / 100))
        
        return tuple(lista)
    
    def obter_cor_ajustada_luminosidade(self, valor):

        lista_rgb = self.hex_to_rgb(self.color_saved)

        rgb_ajustado = self.ajustar_rgb(lista_rgb, valor)

        string_hex = "#" + self.rgb_to_hex(rgb_ajustado)

        return string_hex





    def ajustar_luminosidade(self, valor, canvas):

        nova_cor = self.obter_cor_ajustada_luminosidade(valor)
        self.renderizar_ajuste_de_cor(nova_cor, canvas)

        self.luminosidade = valor

    def ajustar_cor(self, tupla_cor, canvas):

        nova_cor = "#" + self.rgb_to_hex(tupla_cor)
        self.color_saved = nova_cor
        self.ajustar_luminosidade(self.luminosidade, canvas) # Ajustar luminosidade já renderiza

    


    


# Eventos do Tkinter

def acender_apagar(event):

    global lampada_um
    global canvas

    global txt_on_off, aux_on_off

    txt_on_off, aux_on_off = aux_on_off, txt_on_off

    on_off.set(txt_on_off)
    lampada_um.on_off(canvas)


def ajustar_intensidade(event):

    global lampada_um
    global canvas

    lampada_um.ajustar_luminosidade(escala.get(), canvas)

def ajustar_cor(event):

    global lampada_um
    global canvas

    nova_cor_dicionario = {'R': int(255 * (Red.get() / 100)),
                           'G': int(255 * (Green.get() / 100)),
                           'B': int(255 * (Blue.get() / 100))}
    
    tupla_cor = (nova_cor_dicionario['R'],
                 nova_cor_dicionario['G'],
                 nova_cor_dicionario['B'])
    
    lampada_um.ajustar_cor(tupla_cor, canvas)









janela = tk.Tk()
janela.title("PY Lampadas")
janela.geometry("800x700")

lampada_um = Lampada()

canvas = tk.Canvas()
canvas.pack(fill = "x", expand = True)

lampada_um.renderizar_lampada(canvas)

txt_on_off = "Desligar"
aux_on_off = "Ligar"

on_off = tk.StringVar()
on_off.set(txt_on_off)
botao = tk.Button(janela, textvariable = on_off)
botao.pack(pady = 50)
botao.bind('<ButtonRelease-1>', acender_apagar)


intensidade_label = tk.Label(janela, text = "Intensidade", bg = "white")
intensidade_label.pack(fill = "x", expand = True)

escala = tk.Scale(janela, orient = "horizontal")
escala.pack(fill = "x", expand = True)
escala.set(100)
escala.bind('<ButtonRelease-1>', ajustar_intensidade)



Red_label = tk.Label(janela, text = "RED", bg = "red", fg = "white")
Red_label.pack(fill = "x", expand = True)

Red = tk.Scale(janela, orient = "horizontal")
Red.pack(fill = "x", expand = True)
Red.set(100)
Red.bind('<ButtonRelease-1>', ajustar_cor)



Green_label = tk.Label(janela, text = "GREEN", bg = "green", fg = "white")
Green_label.pack(fill = "x", expand = True)

Green = tk.Scale(janela, orient = "horizontal")
Green.pack(fill = "x", expand = True)
Green.set(100)
Green.bind('<ButtonRelease-1>', ajustar_cor)



Blue_label = tk.Label(janela, text = "BLUE", bg = "blue", fg = "white")
Blue_label.pack(fill = "x", expand = True)

Blue = tk.Scale(janela, orient = "horizontal")
Blue.pack(fill = "x", expand = True)
Blue.set(100)
Blue.bind('<ButtonRelease-1>', ajustar_cor)





janela.mainloop()