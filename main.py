from selenium import webdriver
from selenium.webdriver.common.by import By
from robot import robot
import pickle
import yaml
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import ast
from OperateWeb import OperateWeb   

edge_options = EdgeOptions()
edge_options.add_argument('--ignore-certificate-errors')
edge_options.add_argument('--ignore-ssl-errors')
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(service=EdgeService("edgedriver_win64/msedgedriver.exe"), options=edge_options)
driver.implicitly_wait(0.1)


# 加载cookies
def load_cookies(driver, cookies_file):
    try:
        with open(cookies_file, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except (FileNotFoundError, EOFError):
        print("Cookies文件未找到或内容为空，跳过加载cookies步骤。")

# 保存cookies
def save_cookies(driver, cookies_file):
    with open(cookies_file, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

with open("summariser_prompt.txt", "r", encoding="utf-8") as file:
    summariser_prompt = file.read()

def trans_answer(answer):
    summariser = robot("deepseek-chat",system_prompt=summariser_prompt)
    summariser.listen(answer)
    response = summariser.speak()
    return ast.literal_eval(response)

# 打开目标网站
driver.get("https://www.saikr.com/")

# 加载cookies并刷新页面
load_cookies(driver, "cookies.pkl")
driver.refresh()

# 等待用户登录账号密码   一般是手动登录
print("请手动登录账号密码，并进入比赛界面。完成后输入（yes）任意字符回车开始自动做题。")
while True:
    if input() == "yes":
        break
    else:
        print("完成后输入（yes）任意字符回车开始自动做题。")
        continue


# 保存cookies
save_cookies(driver, "cookies.pkl")

# 切换到当前浏览器真正访问的窗口
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "testpaper" in driver.current_url:
        break
driver.switch_to.window(driver.current_window_handle)



# 创建一个锁对象
lock = Lock()

# 处理多个个题目的函数
def process_problems(problems):
    try:
        bot = robot("deepseek-reasoner")
        user_ask = ""
        for problem in problems:
            user_ask += problem.text + "\n\n"
        bot.listen(user_ask)
        response = bot.speak()
        tot = f"题目：{user_ask}\n\n答案：{response}"
        answer_list = trans_answer(tot)
        assert(len(answer_list) == len(problems)), "The number of answers is not equal to the number of problems."
        
        with lock:
            for i, problem in enumerate(problems):
                answer = answer_list[i]
                op = OperateWeb(driver,problem)
                op.handle_all(answer)

    except Exception as e:
        print(f"function error:{e}")

def process_reading(problem):
    try:
        bot = robot("deepseek-reasoner")
        user_ask = problem.text
        bot.listen(user_ask)
        response = bot.speak()
        tot = f"题目：{user_ask}\n\n答案：{response}"
        answer = trans_answer(tot)
        op = OperateWeb(driver,problem)
        op.handle_all(answer)

    except Exception as e:
        print(f"function error:{e}")

is_reading = driver.find_elements(By.XPATH, '//div[@class="material-detail"]')

if len(is_reading) == 0:
    problems = driver.find_elements(By.XPATH, '//div[@class="paper-detail-item"]')
    print(f"读取到{len(problems)}道题目，请稍等，正在完成中...")
    # 选择填空
    # 将题目分成每组problem_num道题目
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    problem_num = api_key = config.get("PROBLEM_NUM")
    problem_groups = [problems[i:i + problem_num] for i in range(0, len(problems), problem_num)]
    # 使用多线程处理题目
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_problems, group) for group in problem_groups]
        for future in futures:
            future.result()
else :
    # 阅读题
    problems = driver.find_elements(By.XPATH, '//div[@class="paper-detail-item"]')
    print(f"读取到{len(problems)}道题目，请稍等，正在完成中...")
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    problem_num = config.get("PROBLEM_NUM")
    # process_reading(problems[0])
    # 使用多线程处理每道题目
    with ThreadPoolExecutor(max_workers=problem_num) as executor:
        futures = [executor.submit(process_reading, problem) for problem in problems]
        for future in futures:
            future.result()


# 用户自己关闭浏览器，才结束程序
print("程序结束，请手动关闭浏览器以结束程序。")
while len(driver.window_handles) > 0:    
    pass
driver.quit()