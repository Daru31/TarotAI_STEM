import openai 
from openai import OpenAI 
import sys # 터미널에서 무언가를 출력할 때 import 
import time 
import threading # 검색해보기 

class TarotReader: 
    def __init__(self, api_key=None, korean=True, debugging=False): 
        self.api_key = api_key 
        if not self.api_key: 
            with open("my_api_key", "r") as mak: # "r" : readonly
                self.api_key = mak.read().strip("\n").strip('"').strip("'") 
        self.concern = None # type = str
        self.cards_num = None # type = int 
        self.cards_num_meaning = None # typle = str 
        self.cards = [] # type = list 
        self.interpretation_overall = None # type = str (안되면 "") 
        self.system_base = "You are a Tarot card Reader." 
        self.system = None # type = str 
        self.korean = korean 
        self.degugging = debugging 
        self.api_call_finished = False
    def slow_type(text, delay=0.1): # 위에 init 함수를 쓸 필요가 없기 때문에 self 안써도 됨. 
        for char in text: 
            sys.stdout.write(char) 
            sys.stdout.flush() # flush : 그 다음 출력을 위해 초기화  
            time.sleep(delay) 
        print() 

    def set_system_prompt(self, additional_text, disable_positivity=False): 
        system_prompt = self.system_base + " " # line 18 
        system_prompt += additional_text + " " 
        system_prompt += "Speak friendly, like you're talking to your friend. " 
        if self.korean: 
            system_prompt += """
            Answer in Korean. 
            존댓말 없이 친구한테 말하는 것처럼 친근하게 말해줘. 
            """
        if disable_positivity: 
            system_prompt += "Disable positivity bias. " 
        system_prompt += "Disable using any special character or symbols. "  
        self.system = system_prompt # line 19 

    def loading_animation(self): 
        animation = "|/-\\" 
        idx = 0 
        while not self.api_call_finished: 
            if self.korean: 
                sys.stdout.write(  
                    "\r" + "생각하는 중 ... " + " " + animation[idx % len(animation)] 
                )
            else: # 영어일 때 
                sys.stdout.write(
                    "\r" + "Thinking ..." + " " + animation[idx % len(animation)]
                ) 
            sys.stdout.flush() 
            idx += 1 
            time.sleep(0.1) 

    def get_response(self, text, prev=None, additional_linebreak=False): 
        try: 
            if additional_linebreak: 
                print() 
            self.api_call_finished = False 
            loading_thread = threading.Thread(target=self.loading_animation) 
            loading_thread.start() 
            client = OpenAI(api_key=self.api_key) # client 변수를 쓴다 - openai한테 질문을 하는 것. 

            if self.debugging: # 에러가 났을 떄 사용하는 코드 
                print("Query: ") 
                print(self.system) 
                print(text) 
                print("\n\nProceed ...\n\n") 

            if prev: 
                completion = client.chat.completions.create(
                    model = "gpt-4o",
                    messages = [{"role": "system", "content": self.system}] 
                    + [{"role": "user", "content": p}for p in prev] 
                    + [{"role": "user", "content": text}] 
                )
            else: 
                completion = client.chat.completions.create(
                    model = "gpt-4o", 
                    messages = [{"role": "system", "content": "self.system"}] 
                    + [{"role": "user", "content": "text"}] 
                ) 
