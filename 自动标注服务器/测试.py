import os
class BrowserManager:
    @staticmethod
    def switch_directory():
        """切换工作目录到脚本所在位置"""
        current_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(current_path)
        os.chdir(script_dir)
        print(f'Directory changed to: {script_dir}')
        return script_dir

    @classmethod
    def configure_browser(cls):
        """配置并返回浏览器实例"""
        cls.switch_directory()
        co = ChromiumOptions().set_local_port(8077).set_timeouts(base=5)
        page = ChromiumPage(addr_or_opts=co)
        print(f"Browser started on port: {page.address}")
        return page

