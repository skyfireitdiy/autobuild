# autobuild

适合中小项目的 python 自动化编译工具

## 依赖安装

```bash
pip install -r requirements.txt --user
```

在 windows 环境下使用还需要安装 pywin32

```bash
pip install pywin32 --user
```

## 模块划分

- 主模块（`autobuild.py`）

  程序入口，驱动其他模块。

- 配置模块（`build_config.py`）

  用于加载编译配置

- 版本控制模块（`vcs.py`）
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
  
 ## 配置示例
 
```json5
// 将此文件重命名为config.json
{
  // 全局环境变量，可选，可以在build、before、after、scp配置中使用，使用方法{{key}}，如{{VS2017_DIR}}
  env: {
    VS2017_DIR: "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Enterprise"
  },
  build: [
    // 这里可以指定编译的列表，不在此列表的项目将被忽略
  ],
  // 发生错误时是否立即停止编译，可选，默认为true
  stop_on_error: false,
  // 工程列表，必需，每个元素表示一个工程配置
  project: {
    // 工程名称对应工程配置
    Example1: {
      // 本工程的环境变量，可选
      env: {
        PATH: "{{PATH}};C:\\msys64\\mingw32\\bin"
      },
      // 跳过本工程编译
      skip: 0,
      // 工程类型，必需，值可以是local或者remote，分别代表在本地编译和在远程主机编译，当配置为remote时，需要配置ssh和scp
      type: "remote",
      // 编译机类型，可配置为Windows或Linux，当type为remote时，必需
      os: "Windows",
      // 版本控制系统配置，必需
      vcs: {
        // 跳过代码拉取，可选，某些工程可能不需要从VCS拉取代码，可以添加此项配置
        skip: 0,
        // 版本控制系统，必需，可选git和svn
        type: "svn",
        // 版本控制系统用户名，当选择svn时，必需
        username: "test",
        // 版本控制系统密码，当选择svn时，必需
        password: "password",
        // 代码地址，必需
        addr: "https://192.168.1.1:1443/svn/Example1",
        // 在拉取代码前需要执行的命令行、可选
        before: ["echo before get code", "echo prepare get code"],
        // 在拉取代码后需要执行的命令行、可选
        after: ["echo after get code", "echo get code finished"]
      },
      // 编译命令，可选，没有此字段则默认此过程成功
      build: [
        "cd Example1",
        "cmake .",
        "mingw32-make",
        "md {{_SLN_DIR}}\\Example1",
        "copy bin\\* {{_SLN_DIR}}\\Example1\\"
      ],
      // 在构建项目前执行的命令
      before: ["echo before build Example1"],
      // 构建命令后执行的命令
      after: ["echo after build Example1"],
      // ssh配置，当type为remote时，必需
      ssh: {
        host: "192.168.1.2",
        port: "22",
        username: "root",
        password: "password"
      },
      // 远程构建结束后，需要拉取的文件列表，当type为remote时，必需
      scp: {
        // 远程路径:本地路径
        "{{_PROJECT_DIR}}/RemoteControl/bin": "{{_SLN_DIR}}/RemoteControl"
      }
    }
    // 其他工程
  },
  // 所有工程构建前执行的命令
  before: ["echo before build solution"],
  // 所有工程构建完成后执行的命令
  after: ["echo after build solution"]
}

```
