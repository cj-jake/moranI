# MoranI
计算莫兰指数  
## 环境安装
使用conda管理环境版本，Python版本3.8.18，PyQt5版本5.15.10，pandas版本2.0.3，imageio版本2.31.4。  
```bash
 conda create --name   you_env_name   python=3.8，    &emsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#创建命为you_env_name的conda 环境
 conda activate you_env_name   &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;     #激活创建的环境
 conda install pyqt=5.15.1                    &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;    #安装 PyQT5 5.15.1
 conda install pandas=2.0.3                   &emsp;&nbsp; &nbsp;&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;#安装 Pandas 2.0.3
 conda install imagetio=2.31.4               &emsp; &nbsp;&nbsp;&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; #安装 ImageTIO 2.31.4
```
## conda基本使用
### 创建一个名为 "myenv" 的新环境
```bash
conda create --name myenv
```
### 创建一个名为 "myenv" 的新环境，并指定使用 Python 3.8 版本
```bash
conda create --name myenv python=3.8
```
### 激活名为 "myenv" 的 Conda 环境
```bash
conda activate myenv
```
### 查看当前环境的已安装包及其版本
```bash
conda list
```
### 安装特定版本（1.2.3）的包
```bash
conda install package_name=1.2.3
```
### 安装最新版本的指定包
```bash
conda install package_name
```
### 卸载指定包
```bash
conda remove package_name
```
### 更新 Conda 到最新版本
```bash
conda update conda
```
### 更新所有已安装的包到它们的最新版本
```bash
conda update --all
```
### 导出当前环境的配置到 environment.yml 文件
```bash
conda env export > environment.yml
```
### 根据环境配置文件创建一个新的 Conda 环境
```bash
conda env create -f environment.yml
```