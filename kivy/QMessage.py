'''
QMessage
Author: Jihyun, Nam
'''

import argparse
import random
import time
import socket

from pythonosc import osc_message_builder
from pythonosc import udp_client


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string('''
<QMessage>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'TD Remote'
            font_size: '60sp'
            halign: 'left'
            valign: 'middle'

        TextInput:
            height: "200dp"
            size_hint_y: None
            size_hint_x: 30
            id: text_input          
            text: "Hello, world!"
            multiline: True

        BoxLayout:
            height: "40dp"
            size_hint_y: None
            Button:
                text: 'Send Message'
                on_press: root.send("text:"+text_input.text+":")
            Button:
                text: 'Clear Message'
                on_press: text_input.text = ''        
        
        BoxLayout:
            Label:
                text: 'Font Scale'
                size_hint_x: 30
            Slider:                
                id:s1
                size_hint_x: 70
                min: 0
                max: 1
                value: 0.5
                on_value: root.send("scale:"+str(s1.value)+":")
        BoxLayout:
            Label:
                text: 'Brightness'
                size_hint_x: 30
            Slider:
                id:s2
                size_hint_x: 70
                min: 0
                max: 1
                value: 0.5
                on_value: root.send("brightness:"+str(s2.value)+":")
        BoxLayout:
            Label:
                text: 'Screen Active'
                size_hint_x: 30
            Switch:
                size_hint_x: 70
                active: True
''')


class QMessage(BoxLayout):

    def send(self, message):
        server_ip = socket.gethostbyname(socket.gethostname())
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default='192.168.0.100', help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=7001, help="The port the OSC server is listening on")      

        args = parser.parse_args()
        client = udp_client.UDPClient(args.ip, args.port)

        msg = osc_message_builder.OscMessageBuilder(message)
        msg = msg.build() 
        client.send(msg)
        print(message)
        #time.sleep(1)


class QMessageApp(App):
    def build(self):
        return QMessage()

QMessageApp().run()

