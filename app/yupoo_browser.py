from pathlib import Path
from playwright.sync_api import sync_playwright

class YupooBrowser:
    """
    Browser session controller.

    We intentionally use a visible browser login instead of asking the app
    to store a Yupoo password. Page selectors are kept in one place so they
    can be updated if Yupoo changes its UI.
    """
    def __init__(self):
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.page.goto("https://www.yupoo.com/", wait_until="domcontentloaded")

    def close(self):
        for obj in (self.context, self.browser, self.pw):
            try:
                if obj: obj.close() if hasattr(obj, "close") else obj.stop()
            except Exception:
                pass
        self.page = self.context = self.browser = self.pw = None

    def is_ready(self):
        return self.page is not None

    def upload_album(self, title, description, files, cover=None):
        """
        Upload entry point. Because Yupoo's current authenticated upload
        controls can change, this method deliberately fails loudly rather
        than pretending a simulated upload succeeded.
        """
        if not self.page:
            raise RuntimeError("请先点击“登录又拍”并完成网页登录。")
        raise NotImplementedError(
            "当前 Yupoo 页面上传接口需要在 Windows 实机登录后校准一次。"
            "请不要把账号密码发给任何人。"
        )
