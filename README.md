# autobuild

适合中小项目的 python 自动化编译工具

## 模块划分

- 主模块（`autobuild.py`）

  程序入口，驱动其他模块。

- 配置模块（`build_config.py`）

  用于加载编译配置

- 版本控制模块（`cvs.py`）
  用于版本控制，拉取代码
- 环境变量控制系统 （`env.py`）

  用于环境变量、运行目录的设置、恢复等

- 本地构建模块（`local_build.py`）

  用于在本地构建的执行

- 远程构建模块（`remote_build.py`）

  用于远程构建执行

- 日志模块（`logger.py`）

  用于打印日志

- 脚本生成模块（`script_gen.py`）

  用于生成编译脚本

- ssh 连接模块（`ssh.py`）

  ssh 远程执行命令，并且提供`scp`文件下载功能

- 本地命令执行模块（`local_command.py`）

  执行本地命令模块
