from openai import OpenAI
import time
import yaml

class robot:

    def __init__(self,type,system_prompt=""):
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
        api_key = config.get("OPENAI_API_KEY")
        base_url = config.get("BASE_URL")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.tot = []
        self.type = type
        self.str = ""
        if system_prompt != "":
            self.tot.append({"role": "system", "content": system_prompt})
    
    def clear(self):
        self.tot = []
        self.str = ""

    def listen(self,s):
        self.str+=s

    def construct_assistant_message(self,completion):
        content = completion.choices[0].message.content
        # content = self.remove_think_tags(content)
        return content,{"role": "assistant", "content": content}

    def speak(self):
        self.tot.append({"role": "user", "content": self.str})
        self.str = ""
        while True:  
            try:
                response = self.client.chat.completions.create(
                model=self.type,
                messages=self.tot,
                stream=False
            )
            except Exception as e:
                time.sleep(1)
                print(f"error:{e}")
                continue
            break        

        speak,add = self.construct_assistant_message(response)
        self.tot.append(add)
        return speak

if __name__ == '__main__':
    pass


