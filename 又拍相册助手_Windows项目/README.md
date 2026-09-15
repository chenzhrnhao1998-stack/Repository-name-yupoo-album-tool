# 又拍相册助手

Windows 桌面工具项目。目标：批量整理本地相册并通过浏览器登录会话操作 Yupoo。

## 当前版本

- PySide6 桌面 GUI
- 本地文件夹扫描
- 图片/视频任务列表
- 标题、描述、前后缀设置
- 图片排序
- `ZT` 文件名自动作为主图候选
- 任务暂停/继续/重试
- Playwright 浏览器登录会话
- Windows GitHub Actions 自动打包 EXE

> 注意：Yupoo 页面结构和登录状态可能变化，因此真实账号上传流程需要在 Windows 环境用实际账号测试一次。项目不会保存明文密码。

## Windows 本地运行

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python main.py
```

## 打包

```bat
build.bat
```

生成：`dist\YupooAlbumAssistant.exe`

## GitHub Actions

把项目上传到 GitHub 后，进入 Actions，运行 `Build Windows EXE`。
