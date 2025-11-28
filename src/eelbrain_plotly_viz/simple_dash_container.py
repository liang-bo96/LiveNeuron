"""简单的 Dash 容器测试类，用于测试 Jupyter cell 大小控制。"""

import random
from typing import Optional

import dash
from dash import html


# Check if we're running in a Jupyter environment
def _is_jupyter_environment():
    """检查是否在 Jupyter notebook 环境中运行。"""
    try:
        from IPython import get_ipython

        return get_ipython() is not None
    except ImportError:
        return False


JUPYTER_AVAILABLE = _is_jupyter_environment()


class SimpleDashContainer:
    """简单的 Dash 测试类，仅包含一个空容器，用于测试 Jupyter cell 大小控制。

    Parameters
    ----------
    width
        容器宽度（像素）。默认为 800。
    height
        容器高度（像素）。默认为 600。
    background_color
        容器背景颜色。默认为 '#f0f0f0'（浅灰色）。
    """

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        background_color: str = "#f0f0f0",
    ):
        self.width = width
        self.height = height
        self.background_color = background_color

        # 创建 Dash 应用
        self.app = dash.Dash(__name__)

        # 设置布局 - 仅包含一个空容器
        self.app.layout = html.Div(
            [
                html.Div(
                    id="empty-container",
                    style={
                        "width": f"{width}px",
                        "height": f"{height}px",
                        "background-color": background_color,
                        "border": "2px solid #333",
                        "border-radius": "8px",
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "margin": "10px auto",
                    },
                    children=[
                        html.P(
                            f"空容器 ({width} × {height}px)",
                            style={
                                "color": "#666",
                                "font-size": "16px",
                                "font-family": "Arial, sans-serif",
                            },
                        )
                    ],
                )
            ],
            style={
                "width": "100%",
                "display": "flex",
                "justify-content": "center",
            },
        )

    def run(
        self,
        port: Optional[int] = None,
        debug: bool = False,
        mode: str = "inline",
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """运行 Dash 应用。

        Parameters
        ----------
        port
            服务器端口号。如果为 None，使用随机端口。
        debug
            是否启用调试模式。默认为 False。
        mode
            显示模式。选项：
            - 'inline': 直接在 Jupyter notebook 中嵌入（默认）
            - 'jupyterlab': 在 JupyterLab 标签页中打开
            - 'external': 在单独的浏览器窗口中打开
        width
            显示宽度（像素）。如果为 None，使用初始化时的宽度。
        height
            显示高度（像素）。如果为 None，使用初始化时的高度。
        """
        if port is None:
            port = random.randint(8001, 9001)

        display_width = width if width is not None else self.width
        display_height = height if height is not None else self.height

        if JUPYTER_AVAILABLE and mode in ["inline", "jupyterlab"]:
            print(f"\n启动简单 Dash 容器测试...")
            print(f"模式: {mode}, 尺寸: {display_width}×{display_height}px")

            self.app.run(
                debug=debug,
                port=port,
                mode=mode,
                width=display_width,
                height=display_height,
            )
        else:
            print(f"\n启动简单 Dash 容器测试，端口: {port}")
            print(f"在浏览器中打开 http://127.0.0.1:{port}/")
            if not JUPYTER_AVAILABLE and mode != "external":
                print("注意: 未检测到 Jupyter 环境，使用外部浏览器模式")
            print()

            self.app.run(debug=debug, port=port)

    def show_in_jupyter(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        debug: bool = False,
    ) -> None:
        """在 Jupyter notebook 中显示容器。

        Parameters
        ----------
        width
            显示宽度（像素）。如果为 None，使用初始化时的宽度。
        height
            显示高度（像素）。如果为 None，使用初始化时的高度。
        debug
            是否启用调试模式。默认为 False。
        """
        if not JUPYTER_AVAILABLE:
            print("警告: 未检测到 Jupyter 环境。")
            print("回退到外部浏览器模式...")
            self.run(debug=debug)
            return

        display_width = width if width is not None else self.width
        display_height = height if height is not None else self.height

        self.run(mode="inline", width=display_width, height=display_height, debug=debug)


# 测试代码
if __name__ == "__main__":
    # 创建简单容器
    container = SimpleDashContainer(width=1000, height=700, background_color="#e8f4f8")

    # 在 Jupyter 中显示（如果在 Jupyter 环境中）
    # container.show_in_jupyter(width=1200, height=800)

    # 或者在外部浏览器中运行
    container.run()



