# Please install OpenAI SDK first: `pip3 install openai`
import streamlit as st  
import time  
from openai import OpenAI




st.set_page_config(page_title="DeepSeek Online - Private", layout="wide")  
st.title(f"Let's Explore...")  
# Function to save session state data to a file
def save_session_state_to_file(data_messages, data_prompt_messages, file_name):
    # Define the file path where you want to save the data
    file_path = f"{file_name}.json"

    # Create a dictionary to store the session state data
    session_data = {
        "messages": data_messages,
        "prompt_messages": data_prompt_messages
    }

    # Write the session state data to a JSON file
    with open(file_path, "w") as file:
        json.dump(session_data, file, indent=4)

def open_session():
    #Create instance of tkinter 
    tk_win = tk.Tk()
    tk_win.withdraw()
    saved_file = filedialog.askopenfilename()

    if saved_file:
        with open(saved_file,'r') as file:
            data = json.load(file)
            data_messages = data['messages']
            data_prompt_messages = data['prompt_messages']
            print(f"Messages: \n{data_messages}\n\n prompt_messages: \n{data_prompt_messages}\n\n")
            return data_messages, data_prompt_messages

if "messages" not in st.session_state:  
    st.session_state.messages = []  
if "prompt_messages" not in st.session_state:
    st.session_state.prompt_messages = [{"role": "system", "content": "You are a helpful assistant"},]
if "file_name" not in st.session_state:
    st.session_state.file_name=''

def clear_filename():
    st.session_state.file_name=None

with st.sidebar:
    # Input field for file name
    file_name = st.text_input("Enter file name (without extension):", value=st.session_state['file_name'])
    if st.button("Save Session", icon="💾", disabled=not file_name):
        save_session_state_to_file(st.session_state.messages, st.session_state.prompt_messages, file_name)
        st.success("Session state saved to file!")
        print(f"File name before clearing: {st.session_state['file_name']}")
        clear_filename()
        print(f"File name after clearing: {st.session_state.file_name}")
        st.rerun()
    if st.button("Open Session", icon="📂"):
        st.session_state.messages, st.session_state.prompt_messages = open_session()  

for msg in st.session_state.messages:  
    with st.chat_message(msg["role"]):  
        st.write(msg["content"])  

prompt = st.chat_input("What to explore today...")  
client = OpenAI(api_key="sk-3e42a614dec94b0092b80d4b3c3a3c07", base_url="https://api.deepseek.com")

if prompt:  

    st.session_state.prompt_messages.append({"role": "user", "content": str(prompt)})
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.write(prompt)  

    time.sleep(1)  
    bot_response = f"You said: {prompt}"  # You can keep this for reference if needed

    print(f"Before Sending \n : {st.session_state.prompt_messages}\n\n\n")
    try:
        #print(f"Messages passed to Deepseek: {messages}\n\n")
        response = client.chat.completions.create(
            model="deepseek-chat",  # Updated to use the selected model
            messages=st.session_state.prompt_messages,
            stream=False
        )

        bot_response = response.choices[0].message.content
        st.session_state.prompt_messages.append({'role': 'assistant', 'content': bot_response})

    except Exception as e:
        st.error(f"Model selection error: {e}")
        bot_response = f"An error occurred while selecting the model."

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    with st.chat_message("assistant"):  
        st.write(bot_response)
    print(f"Ater receiving\n : {st.session_state.prompt_messages}\n\n\n")



