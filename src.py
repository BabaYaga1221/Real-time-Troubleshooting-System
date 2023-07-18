from customtkinter import CTk, CTkTextbox, CTkEntry, CTkButton, CTkComboBox
import bardapi
import psutil
import os
import customtkinter 
import requests
import threading as th
from PIL import Image,ImageTk, ImageFilter
from tkinter import simpledialog
import tkinter as tk
from tkinter import colorchooser, filedialog
from fpdf import FPDF
import platform
import sys
import subprocess


chatbotChecker = 0

chatgpt_4_url = "https://chatgpt-gpt4-ai-chatbot.p.rapidapi.com/ask"

chatgpt_4_payload = { "query": "Are you a ChatGPT-4?" }
chatgpt_4_headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "...........Enter you API key............",
	"X-RapidAPI-Host": "chatgpt-gpt4-ai-chatbot.p.rapidapi.com"
}

os.environ['_BARD_API_KEY']="............Enter you API Key(__Secure_1PSID).................."
pdf_data = []

url = "https://openai80.p.rapidapi.com/chat/completions"

bingURL = "https://chatgpt-bing-ai-chat-api.p.rapidapi.com/ask"

bing_token = "................Enter you Bing Token.................."

bing_payload = {
	"question": "Is Artificial Intelligence a threat to humans?",
	"bing_u_cookie": f"{bing_token}"
}

bing_headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "...............Enter you Rapid API key...............",
	"X-RapidAPI-Host": "chatgpt-bing-ai-chat-api.p.rapidapi.com"
}

payload = {
    "model": "gpt-3.5-turbo",
    "messages": []
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "a7f3acb712msha3f28e95023e89bp1eeb1djsn02828ef9e5c8",
    "X-RapidAPI-Host": "openai80.p.rapidapi.com"
}

background_image_path = "images/435.png"


class CustomTextArea:
    def __init__(self, text_widget, root):
        self.text_widget = text_widget
        self.background_label = tk.Label(root)
        self.background_label.place(in_=root, anchor="nw", relwidth=1, relheight=1)
        self.one_time_background_image(background_image_path)
        
        # Bind the resize event to the update_background_image function

    def set_background_image(self, image_path, width, height):
        image = Image.open(image_path)
        image = image.resize((1920, 1080), Image.LANCZOS)
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=8))  # Apply blur filter

        self.background_image = ImageTk.PhotoImage(blurred_image)
        self.background_label.configure(image=self.background_image)
        self.background_label.image = self.background_image  # Avoid garbage collection
        self.background_label.place(in_=self.text_widget, anchor="nw", relwidth=1, relheight=1)
        self.text_widget.bind("<Configure>", background_image_path)
    
    def one_time_background_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((1920,1080), Image.LANCZOS)
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=8))  # Apply blur filter

        self.background_image = ImageTk.PhotoImage(blurred_image)
        self.background_label.configure(image=self.background_image)
        self.background_label.image = self.background_image  # Avoid garbage collection
        self.background_label.place(in_=self.text_widget, anchor="nw", relwidth=1, relheight=1)
        self.text_widget.bind("<Configure>", background_image_path)

# Create the main window
window = CTk()
window.title("Chat UI")
window.geometry("900x400")
customtkinter.set_appearance_mode("System")
window.pack_propagate(0)

window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=0)
window.grid_rowconfigure(2, weight=0)
window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(1, weight=0)
window.grid_columnconfigure(2, weight=0)
text_widget = tk.Text(window, state='disabled', wrap='word', font=("Helvetica", 16), bg='black')
text_widget.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

text_box = CustomTextArea(window,window)
# Create a custom text area
text_area = CTkTextbox(window, state='disabled',border_width=2, font=("Helvetica", 16))
# text_area.configure(corner_radius=100,border_width=0, font=("Helvetica", 16))
text_area.grid(row=0, column=0,columnspan=1, padx=10, pady=10, sticky='nsew')
# Create an entry field for user input
entry = CTkEntry(window)
entry.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

text_box.one_time_background_image(background_image_path)



def get_system_info():
    # Retrieve system information
    os_info = f"Operating System: {platform.system()} {platform.release()}"
    architecture = f"Architecture: {platform.machine()}"
    processor = f"Processor: {platform.processor()}"
    
    # Retrieve CPU utilization
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_utilization = f"CPU Utilization: {cpu_percent}%"
    
    # Retrieve memory usage
    memory = psutil.virtual_memory()
    memory_usage = f"RAM Consumption: {memory.percent}%"
    
    # Retrieve storage information
    disk_usage = psutil.disk_usage("/")
    storage_level = f"Storage Level: {disk_usage.percent}%"
    io_rate = f"IO Rate: {psutil.disk_io_counters().read_bytes / 1024 / 1024} MB/s"
    
    # Retrieve running processes
    processes = psutil.process_iter()
    running_processes = [process.name() for process in processes]
    running_processes_info = f"Running Processes: {', '.join(running_processes)}"
    
    # Retrieve available updates (example command for Linux system)
    updates_available = subprocess.check_output(["powershell", "Get-Hotfix"])
    updates_info = f"Updates Available:\n{updates_available.decode('utf-8')}"
    
    # Retrieve bug logs (example command for Windows system)
    bug_logs = subprocess.check_output(["powershell", "Get-EventLog", "-LogName", "Application", "-Newest", "10"])
    bug_logs_info = f"Bug Logs:\n{bug_logs.decode('utf-8')}"
    
    # Combine all information into a single string
    system_info = f"{os_info}\n{architecture}\n{processor}\n{cpu_utilization}\n{memory_usage}\n{storage_level}\n{io_rate}\n{running_processes_info}\n{updates_info}\n{bug_logs_info}"
    
    return system_info

def on_entry_click(event):
    if entry.get() == "Enter your text here":
        entry.delete(0, "end")
        entry.configure(text_color='white')

def on_entry_leave(event):
    if entry.get() == "":
        entry.insert(0, "Enter your text here")
        entry.configure(text_color='grey')

def clear_chat():
    text_area.configure(state='normal')
    text_area.delete('1.0', 'end')
    text_area.configure(state='disabled')

def export_chat():
    global pdf_data,payload
    text_file = open("chat.txt", "w")  # Open a text file for writing

    messages = payload['messages']
    data = pdf_data

    for message, value in zip(messages, data):
        content_1 = message['role'] + ' : ' + message['content']
        content_2 = value['role'] + ' : ' + value['content']

        text_file.write(content_1 + '\n')
        text_file.write(content_2 + '\n')

    text_file.close()  # Close the text file

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=14)

    # Read the text file and add its contents to the PDF
    with open("chat.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            pdf.multi_cell(0, 10, txt=line, align='L')

    pdf.output("chat.pdf")
    os.remove("chat.txt")

def process_response(message):
    global chatbotChecker
    chatbot = chatgpt(message)
    if chatbotChecker == 0:
        display_Thinking("ChatGPT: " + chatbot+"\n")
    if chatbotChecker == 1:
        display_Thinking("BARD: " + chatbot+"\n")
    if chatbotChecker == 2:
        display_Thinking("BingAI: " + chatbot+"\n")
    if chatbotChecker == 3:
        display_Thinking("ChatGPT-4: " + chatbot+"\n")

def chatgpt(message):
    global pdf_data,chatbotChecker
    if chatbotChecker == 0:
        data = {
            'role': 'user',
            'content': f"{message}"
        }
        payload['messages'].append(data)
        display_message("ChatGPT: .... \n")
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        chatgpt = data['choices'][0]['message']['content']
        pdf_data.append({'role': 'ChatBot', 'content': f'{chatgpt}'})
        return chatgpt
    elif chatbotChecker == 1:
        display_message("BARD: ... \n")
        response = bardapi.core.Bard().get_answer(message)
        # print(response['content'])
        bard = response['content']
        pdf_data.append({'role': 'ChatBot', 'content': f'{bard}'})
        return bard
    elif chatbotChecker == 2:
        display_message("BingAI: ... \n")
        bing_payload={
            "question": f"{message}",
            "bing_u_cookie": f"{bing_token}"
        }
        response = requests.post(bingURL, json=bing_payload, headers=bing_headers)
        if response.status_code == 200:
            pdf_data.append({'role': 'ChatBot', 'content': f'{response.json()["text_response"]}'})
            return response.json()["text_response"]
        else:
            return "Error: " + str(response.status_code) + " " + response.reason
    elif chatbotChecker == 3:
        chatgpt_4_payload = {"query": f"{message}"}
        display_message("ChatGPT-4 : .... \n")
        response = requests.post(chatgpt_4_url, json=chatgpt_4_payload, headers=chatgpt_4_headers)
        data = response.json()
        chatgpt_4 = data['response'] 
        pdf_data.append({'role': 'ChatBot', 'content': f'{chatgpt_4}'})
        return chatgpt_4

def send_message():
    message = entry.get()
    display_message("User: " + message+"\n")
    entry.delete(0, 'end')
    th.Thread(target=process_response, args=(message,)).start()
    entry.delete(0, 'end')

def display_message(message):
    text_area.configure(state='normal')
    text_area.insert('end', message)
    text_area.configure(state='disabled')
    text_area.see('end')

def display_Thinking(message):
    text_area.configure(state='normal')
    
    # Delete the previous line
    text_area.delete("end-2l linestart", "end-2l lineend+1c")
    
    # Insert the new message at the end
    # text_area.insert('end', message + "\n")
    text_area.insert('end', message+"\n", 'right')  

    
    text_area.configure(state='disabled')
    text_area.see('end')

def choose_text_color():
    color = colorchooser.askcolor()
    if color:
        text_area.configure("text_color",text_color=color[1])

def choose_background_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        text_box.set_background_image(file_path,window.winfo_width(),window.winfo_height())
    else:
        text_box.set_background_image(background_image_path)

def chatbotOptions(event):
    global chatbotChecker
    if event == 'ChatGPT':
        chatbotChecker = 0
    elif event == 'Bard':
        chatbotChecker = 1
    elif event == 'BingAI':
        chatbotChecker = 2
    elif event == 'ChatGPT-4':
        chatbotChecker = 3

def display_system_info():
    system_info = get_system_info()
    system_info += '''\n Analyse the system info to get more information about the system and suggest the best solution for the problem.
    and provide video tutorials for the solution.'''
    th.Thread(target=process_response, args=(system_info,)).start()


def main():

    # Create a send button
    send_button = CTkButton(window, text="Send")
    send_button.grid(row=1, column=1, padx=10, pady=10, sticky='e')


    send_button.configure(command=send_message)

    clear_button = CTkButton(window, text="Clear Chat", command=clear_chat)
    clear_button.grid(row=1, column=2, padx=10, pady=10, sticky='w',)


    export_button = CTkButton(window, text="Export as PDF", command=export_chat)
    export_button.grid(row=2, column=1, padx=10, pady=10, sticky='e')

    color_button = CTkButton(window, text="Choose Text Color", command=choose_text_color)
    color_button.grid(row=2, column=2,padx=10, pady=10, sticky='w')
    # color_button.pack(side='left', padx=10, pady=10,expand=True)

    background_button = CTkButton(window, text="Choose Background Image", command=choose_background_image)
    background_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    # background_button.pack(side='right', padx=10, pady=10,expand=True)

    chatbot_options = CTkComboBox(window, values=['ChatGPT','Bard','BingAI','ChatGPT-4'],command=chatbotOptions,button_color='#256D9C',fg_color='#256D9C',dropdown_fg_color='#256D9C',border_color='#256D9C',dropdown_hover_color='#979A9A',corner_radius=5)
    chatbot_options.grid(row=2, column=0,padx=10, pady=10, sticky='e')
    chatbot_options.set('ChatGPT')

    system_info_button = CTkButton(window, text="Calibrate System Info", command=display_system_info)
    system_info_button.grid(row=2, column=0, padx=(200,200), pady=(10), sticky='w')

    entry.bind('<Return>', lambda event: send_message())
    entry.insert(0, "Enter your text here")
    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_entry_leave)

    # Start the main event loop
    window.mainloop()

if __name__ == '__main__':
    main()
