from pathlib import Path
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QTableWidget,QTableWidgetItem,
    QPushButton,QLabel,QComboBox,QSpinBox,QFileDialog,QMessageBox,QDialog,
    QCheckBox,QLineEdit,QPlainTextEdit,QHeaderView
)
from .scanner import scan_root
from .settings import load, save
from .yupoo_browser import YupooBrowser

class SettingsDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent); self.setWindowTitle("软件设置"); self.data=data.copy()
        lay=QVBoxLayout(self)
        self.checks={}
        labels=[
            ("upload_video","上传视频"),("no_title_number","不上传标题编号"),
            ("upload_description","上传描述"),("remove_description_links","不上传描述中的链接"),
            ("zt_cover","将图片名带有：ZT 的图片设为封面主图")
        ]
        for key,text in labels:
            c=QCheckBox(text); c.setChecked(bool(self.data[key])); lay.addWidget(c); self.checks[key]=c
        for key,text in [
            ("title_prefix","添加标题前缀"),("title_suffix","添加标题后缀"),
            ("description_prefix","添加描述前缀"),("description_suffix","添加描述后缀"),
            ("description_filename","描述文件名称")
        ]:
            row=QHBoxLayout(); row.addWidget(QLabel(text))
            e=QLineEdit(str(self.data[key])); row.addWidget(e); lay.addLayout(row); self.checks[key]=e
        row=QHBoxLayout(); row.addWidget(QLabel("使用固定描述"))
        self.fixed=QPlainTextEdit(str(self.data["fixed_description"])); self.fixed.setMaximumHeight(90)
        row.addWidget(self.fixed); lay.addLayout(row)
        btn=QPushButton("保存设置"); btn.clicked.connect(self.accept); lay.addWidget(btn)
    def accept(self):
        for k,w in self.checks.items():
            self.data[k]=w.isChecked() if isinstance(w,QCheckBox) else w.text()
        self.data["fixed_description"]=self.fixed.toPlainText()
        save(self.data); super().accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("又拍相册助手 V2.0"); self.resize(1100,680)
        self.cfg=load(); self.albums=[]; self.browser=YupooBrowser()
        root=QWidget(); self.setCentralWidget(root); outer=QVBoxLayout(root)

        menu=QHBoxLayout()
        for text,slot in [("软件设置",self.settings),("卡密",self.show_license),
                          ("列表跟随",lambda:None),("图片压缩",lambda:None),
                          ("又拍批量下载",self.download),("复制克隆相册",self.clone)]:
            b=QPushButton(text); b.clicked.connect(slot); menu.addWidget(b)
        menu.addStretch(); outer.addLayout(menu)

        self.table=QTableWidget(0,6)
        self.table.setHorizontalHeaderLabels(["ID","相册标题","图片","视频","相册描述","上传状态"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        outer.addWidget(self.table)

        controls=QHBoxLayout()
        controls.addWidget(QLabel("本地目录"))
        self.path=QLineEdit(); controls.addWidget(self.path)
        b=QPushButton("选择"); b.clicked.connect(self.choose); controls.addWidget(b)
        b=QPushButton("扫描"); b.clicked.connect(self.scan); controls.addWidget(b)
        outer.addLayout(controls)

        controls=QHBoxLayout()
        self.reverse=QCheckBox("相册倒序上传"); controls.addWidget(self.reverse)
        controls.addWidget(QLabel("每上传一个相册等待"))
        self.wait=QSpinBox(); self.wait.setRange(0,999); self.wait.setValue(int(self.cfg["wait_seconds"]))
        controls.addWidget(self.wait); controls.addWidget(QLabel("秒"))
        controls.addStretch()
        controls.addWidget(QLabel("又拍水印"))
        self.water=QComboBox(); self.water.addItems(["不添加水印"]); controls.addWidget(self.water)
        controls.addWidget(QLabel("*又拍分类"))
        self.category=QComboBox(); self.category.addItems(["请选择分类"]); controls.addWidget(self.category)
        outer.addLayout(controls)

        actions=QHBoxLayout()
        login=QPushButton("登录又拍"); login.clicked.connect(self.login); actions.addWidget(login)
        start=QPushButton("开始上传"); start.clicked.connect(self.start_upload); actions.addWidget(start)
        self.status=QLabel("就绪"); actions.addWidget(self.status); actions.addStretch()
        outer.addLayout(actions)

    def choose(self):
        p=QFileDialog.getExistingDirectory(self,"选择相册根目录")
        if p: self.path.setText(p); self.scan()

    def scan(self):
        if not self.path.text(): return
        try: self.albums=scan_root(self.path.text())
        except Exception as e:
            QMessageBox.critical(self,"扫描失败",str(e)); return
        self.table.setRowCount(len(self.albums))
        for i,a in enumerate(self.albums):
            vals=[str(i+1),a.title,str(len(a.images)),str(len(a.videos)),a.description,"待上传"]
            for j,v in enumerate(vals): self.table.setItem(i,j,QTableWidgetItem(v))
        self.status.setText(f"已读取 {len(self.albums)} 个相册")

    def settings(self):
        SettingsDialog(self,self.cfg).exec(); self.cfg=load()

    def login(self):
        try:
            self.browser.start()
            self.status.setText("请在浏览器窗口完成又拍登录，完成后返回本软件。")
        except Exception as e: QMessageBox.critical(self,"登录失败",str(e))

    def start_upload(self):
        if not self.albums:
            QMessageBox.warning(self,"提示","请先选择根目录并扫描。"); return
        if not self.browser.is_ready():
            QMessageBox.warning(self,"提示","请先点击“登录又拍”。"); return
        QMessageBox.information(
            self,"当前版本说明",
            "浏览器登录模块已经准备好。\n"
            "真实上传按钮需要根据你当前 Yupoo 账号页面校准一次上传控件，"
            "否则程序不会伪造“上传成功”。"
        )

    def show_license(self): QMessageBox.information(self,"卡密","当前版本采用本地授权接口预留。")
    def download(self): QMessageBox.information(self,"又拍批量下载","下载模块已预留，下一步接入当前 Yupoo 页面。")
    def clone(self): QMessageBox.information(self,"复制克隆相册","克隆模块已预留，下一步接入当前 Yupoo 页面。")
