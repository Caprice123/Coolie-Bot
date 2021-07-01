from tkinter import *
import tkinter as tk
import time
from package.mqtt import MQTT
import os
import names

# mosquitto_pub -h test.mosquitto.org -t Line_Follower_Python -m "ESP32 Ready to Go"
# mosquitto_pub -h test.mosquitto.org -t Line_Follower_Python -m "Reach Destination"
# mosquitto_pub -h test.mosquitto.org -t Line_Follower_Python -m "Task Finished"

# setting ganti nama & tombol informasi
# tombol return manual & kalau sudah sampai ke next page buat kasih tau dah kelar
class GUI:
    def __init__(self, width, height):
        name = self.get_random_names()
        self.mqtt = MQTT(name)

        self.mqtt.start_connection()
        self.root = Tk()
        self.root.title("Coolie Bot")
        self.width = width
        self.height = height

        self.press = 0
        self.cnt = 0
        self.status = 0  # status connected
        self.font = ("Gotham", 24)
        self.warehouse = PhotoImage(file=os.path.join(os.getcwd(), "images/warehouse.png"))
        self.panah = PhotoImage(file=os.path.join(os.getcwd(), "images/right arrow.png"))
        self.panahkiri = PhotoImage(file=os.path.join(os.getcwd(), "images/left arrow.png"))
        self.root.geometry(f"{self.width}x{self.height}+300+150")
        #self.root.minsize(self.width, self.height)
        #self.root.maxsize(self.width, self.height)
        self.root.resizable(0,0)

        self.pageconnecting()

        self.root.mainloop()

    def get_random_names(self):
        return names.get_full_name()

    def pageconnecting(self):
        self.frame = Frame(self.root, bg="#333652", width=1000, height=500)
        self.frame.place(x=0, y=0)
        self.connecting = Text(self.frame, width=25, height=1)
        self.connecting.place(x=self.width // 2 - 90, y=self.height // 2 - 50)
        self.connecting.insert(tk.END, "CONNECTING...")  # textnya dari connection
        self.connecting.config(state=DISABLED)
        self.connected()

    def connected(self):
        while self.mqtt.status_ESP() == 0:
            self.connecting.update()
            self.mqtt.check_esp_ready()
            time.sleep(0.25)
            self.connecting.update()

        self.connecting.config(state=NORMAL)
        self.connecting.delete("1.0", "end")
        self.connecting.insert(tk.END, "CONNECTED")
        self.connecting.config(state=DISABLED)
        self.connecting.update()
        time.sleep(1)
        self.connecting.update()
        self.connecting.destroy()
        self.tomboltujuan()

    def tomboltujuan(self):  # kirim destination & Tombol A, B, & C

        self.frame = Frame(self.root, bg="#333652", width=1000, height=500)
        self.frame.place(x=0, y=0)

        self.text1 = Label(self.frame, relief=FLAT, bg="#333652", text="Where Would You Like Coolie Bot to Go?",
                           fg='white', font=self.font)
        self.text1.place(x=self.width - 800, y=self.height - 450)

        self.tombolA = Button(self.frame, text="A",bg ='#FAD02C', width=7, height=3, font=self.font,
                              command=lambda: self.pagedestination("A"))
        self.tombolA.place(x=self.width - 900, y=self.height - 320)
        self.tombolB = Button(self.frame, text="B",bg ='#E9EAEC', width=7, height=3, font=self.font,
                              command=lambda: self.pagedestination("B"))
        self.tombolB.place(x=self.width - 570, y=self.height - 320)
        self.tombolC = Button(self.frame, text="C",bg ='#90ADC6', width=7, height=3, font=self.font,
                              command=lambda: self.pagedestination("C"))
        self.tombolC.place(x=self.width - 250, y=self.height - 320)

    def pagedestination(self, DESTINATION):  # SETELAH DIKLIK TOMBOL A
        self.tombolA.destroy()
        self.tombolB.destroy()
        self.tombolC.destroy()

        self.press = 0
        self.cnt = 0

        self.mqtt.send_destination(DESTINATION)



        print("Here")

        self.fotowarehouse = Label(self.frame, image=self.warehouse)
        self.fotowarehouse.place(x=10, y=self.height // 3.5 - 20)
        self.fotopanah = Label(self.frame, image=self.panah)
        self.fotopanah.place(x=350, y=self.height // 3 - 20)
        if DESTINATION == "A":
            self.tombolA = Button(self.frame, text=DESTINATION,bg ='#FAD02C', width=7, height=3, relief=FLAT, font=self.font)
            self.tombolA.place(x=820, y=self.height // 2 - 100)
        elif DESTINATION == "B":
            self.tombolB= Button(self.frame, text=DESTINATION, bg='#E9EAEC', width=7, height=3, relief=FLAT, font=self.font)
            self.tombolB.place(x=820, y=self.height // 2 - 100)
        elif DESTINATION == "C":
            self.tombolC = Button(self.frame, text=DESTINATION, bg='#90ADC6', width=7, height=3, relief=FLAT, font=self.font)
            self.tombolC.place(x=820, y=self.height // 2 - 100)


        self.forceback = Button(self.frame, text="Force Back", width=10, height=5, state=DISABLED)
        self.forceback.place(x=self.width - 200, y=self.height - 100)

        while self.mqtt.status_ESP()!= 0.5:
            self.frame.update()
            time.sleep(0.5)
            self.frame.update()

        self.forceback.config(state=NORMAL)
        self.forceback.config(command = self.Forceback)

        while self.press ==0:
            if self.cnt >= 5:
                self.cnt = 0
                self.Forceback()
                break

            print(self.cnt)
            self.cnt += 0.5
            time.sleep(0.5)
            self.forceback.update()


    def Forceback(self):
        print("done 5 second")
        self.press =1
        #self.tombolA.destroy()
        self.forceback.destroy()
        #self.fotowarehouse.destroy()
        self.fotopanah.destroy()
        self.text1.destroy()
        self.PageOTWwarehouse()

    def PageOTWwarehouse(self):
        self.mqtt.send_signal_back()
        #self.fotowarehouse = Label(self.frame, image=self.warehouse)
        #self.fotowarehouse.place(x=10, y=self.height // 3.5 - 20)
        self.fotopanahkiri = Label(self.frame, image=self.panahkiri)
        self.fotopanahkiri.place(x=350, y=self.height // 3 - 20)
        self.tombolhome = Button(self.frame, text="Homepage", width=8, height=3, relief=FLAT,font = 20)
        self.tombolhome.place(x=850, y=self.height - 100 )
        self.tombolhome.config(state=DISABLED)


        while self.mqtt.status_ESP() != 0.25:
              self.tombolhome.update()
              time.sleep(0.25)
              self.tombolhome.update()

        self.tombolhome.config(state=NORMAL)
        self.tombolhome.config(command=self.tomboltujuan)


if __name__ == "__main__":
    GUI(1000, 500)