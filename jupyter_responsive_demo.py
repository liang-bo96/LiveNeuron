#!/usr/bin/env python3
"""
Jupyter动态尺寸检测演示

展示如何在Jupyter notebook中动态获取窗口尺寸并自适应调整可视化大小。
"""

from eelbrain_plotly_viz import EelbrainPlotly2DViz

def demo_responsive_sizing():
    """演示响应式尺寸检测功能"""
    
    print("🎯 Jupyter动态尺寸检测演示")
    print("=" * 50)
    
    # 创建可视化实例
    viz = EelbrainPlotly2DViz(
        cmap='Viridis',
        show_max_only=True
    )
    
    print("📱 可用的响应式显示方法：")
    print()
    print("1. 自动检测最优尺寸：")
    print("   viz.show_in_jupyter_auto()")
    print()
    print("2. 自定义响应式参数：")
    print("   viz.show_in_jupyter_responsive(")
    print("       aspect_ratio=1.6,    # 16:10 宽高比")
    print("       min_width=800,       # 最小宽度")
    print("       max_width=1800       # 最大宽度")
    print("   )")
    print()
    print("3. 传统固定尺寸：")
    print("   viz.show_in_jupyter(width=1200, height=900)")
    
    return viz

def create_jupyter_demo_notebook():
    """创建演示notebook单元格内容"""
    
    notebook_content = '''
# Jupyter动态尺寸检测演示

## 方法1: 自动检测最优尺寸
```python
from eelbrain_plotly_viz import EelbrainPlotly2DViz

# 创建可视化
viz = EelbrainPlotly2DViz()

# 一键自动检测并显示
viz.show_in_jupyter_auto()
```

## 方法2: 自定义响应式参数
```python
# 自定义宽高比和尺寸范围
viz.show_in_jupyter_responsive(
    aspect_ratio=1.6,     # 16:10 宽高比，适合宽屏
    min_width=900,        # 最小宽度
    max_width=1800,       # 最大宽度
    min_height=600,       # 最小高度
    max_height=1200       # 最大高度
)
```

## 方法3: JavaScript直接检测
```python
from IPython.display import HTML, Javascript

# 直接使用JavaScript获取尺寸
js_code = """
<script>
function detectCellSize() {
    var cell = document.querySelector('.output_area') || 
               document.querySelector('.jp-OutputArea');
    if (cell) {
        var width = cell.clientWidth;
        var height = window.innerHeight * 0.6;  // 60% of viewport height
        console.log('Detected cell dimensions:', width, 'x', height);
        window.cellDimensions = {width: width, height: height};
        
        // 显示检测结果
        document.write('<div style="background: #e8f4fd; padding: 10px; border-left: 4px solid #2196F3;">');
        document.write('<strong>🔍 尺寸检测结果:</strong><br/>');
        document.write('Cell宽度: ' + width + 'px<br/>');
        document.write('建议高度: ' + Math.round(height) + 'px');
        document.write('</div>');
    }
}
detectCellSize();
</script>
"""

HTML(js_code)
```

## 技术原理

### 1. JavaScript检测
- 使用`document.querySelector()`查找输出区域
- 通过`clientWidth`获取实际可用宽度
- 兼容不同Jupyter版本的选择器

### 2. Python端处理
- 接收JavaScript检测的尺寸数据
- 应用最小/最大尺寸约束
- 根据宽高比计算最优高度

### 3. 响应式策略
- **小屏幕**: 使用最小尺寸，确保可读性
- **中等屏幕**: 按比例缩放，保持最佳体验
- **大屏幕**: 限制最大尺寸，避免过度拉伸

### 4. 适配不同环境
- **Jupyter Notebook**: 使用`.output_area`选择器
- **JupyterLab**: 使用`.jp-OutputArea`选择器
- **其他环境**: 降级到智能默认值
'''
    
    return notebook_content

if __name__ == "__main__":
    # 运行演示
    viz = demo_responsive_sizing()
    
    print("\n" + "="*50)
    print("💡 在Jupyter notebook中运行以下代码测试:")
    print()
    print("viz = EelbrainPlotly2DViz()")
    print("viz.show_in_jupyter_auto()  # 自动检测最优尺寸")
    print()
    print("或者:")
    print("viz.show_in_jupyter_responsive(aspect_ratio=1.6)")


