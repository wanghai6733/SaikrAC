# **赛氪自动做题机**

## **项目简介**

SaikrAC 是一款专为 [**赛氪竞赛网**](https://www.saikr.com) 设计的智能答题助手。  

借助先进的 **Deepseek-R1 推理模型**，SaikeAC 能够高效地完成各类客观题（如选择题、填空题等）的自动解答。

**正确率在 95% 左右！**  

## **安装与运行**

### 1. 克隆项目到本地
（或直接下载项目到本地解压）：  
```bash
git clone https://github.com/wanghai6733/SaikeAC.git
```

### 2. 进入项目目录  
```bash
cd SaikeAC
```

### 3. 安装依赖  
```bash
pip install -r requirements.txt
```

### 4. 配置 Deepseek API  
- 前往 [Deepseek 平台](https://platform.deepseek.com/api_keys) 申请 API Key。  
- 将申请到的 API Key 填写到本地 `config.yaml` 文件中的 `OPENAI_API_KEY` 字段，如：  

  ```yaml
  OPENAI_API_KEY: "your_api_key"
  ```

### 5. 启动项目* 
```bash
python main.py
```

---

## **使用步骤**

### 第一步，切换到代码路径，并运行
![第一步，切换到代码路径，并运行](/img/1.png)

### 第二步，自动跳出浏览器，自行登录
![第二步，自动跳出浏览器，自行登录](/img/2.png)

### 第三步，进入你想完成的比赛界面
![第三步，进入你想完成的比赛界面](/img/3.png)

### 第四步，在终端输出yes并回车，将自动开始做题，预计5分钟左右
![第四步，在终端输出yes并回车，将自动开始做题，预计5分钟左右](/img/4.png)

### 第五步，题目完成后，自行交卷
![第五步，题目完成后，自行交卷](/img/5.png)