#!/usr/bin/env python3
"""
LiveNeuron Display Mode 演示

展示新增的display_mode参数功能，支持多种解剖视图布局模式。
类似于Eelbrain GlassBrain的display_mode功能。
"""

from eelbrain_plotly_viz import EelbrainPlotly2DViz

def demo_display_modes():
    """演示所有可用的display_mode选项"""
    
    print("🧠 LiveNeuron Display Mode 功能演示")
    print("=" * 60)
    
    # 定义所有可用的显示模式
    display_modes = {
        "单视图模式": {
            'x': "矢状面 (Sagittal) - X轴方向切片",
            'y': "冠状面 (Coronal) - Y轴方向切片", 
            'z': "轴向面 (Axial) - Z轴方向切片",
            'l': "左半球矢状面 - 仅显示左半球",
            'r': "右半球矢状面 - 仅显示右半球"
        },
        "双视图模式": {
            'xz': "矢状面 + 轴向面 - 经典组合",
            'yx': "冠状面 + 矢状面 - 前后+左右视角",
            'yz': "冠状面 + 轴向面 - 前后+上下视角", 
            'lr': "左半球 + 右半球 - 半球对比"
        },
        "三视图模式": {
            'ortho': "正交视图 (矢状+冠状+轴向) - 标准三维视角",
            'lzr': "左半球 + 轴向 + 右半球 - 半球对称视图",
            'lyr': "左半球 + 冠状 + 右半球 - 半球功能对比"
        },
        "四视图模式": {
            'lzry': "左半球 + 轴向 + 右半球 + 冠状 - 全方位视角",
            'lyrz': "左半球 + 冠状 + 右半球 + 轴向 - 功能导向布局"
        }
    }
    
    print("📋 所有可用的Display Mode选项:\n")
    
    for category, modes in display_modes.items():
        print(f"🔸 {category}:")
        for mode, description in modes.items():
            print(f"   • '{mode}': {description}")
        print()
    
    print("🧪 功能测试:")
    print("-" * 40)
    
    # 测试每种模式
    for category, modes in display_modes.items():
        print(f"\n{category}:")
        for mode in modes.keys():
            try:
                viz = EelbrainPlotly2DViz(display_mode=mode, show_max_only=True)
                views = viz._parse_display_mode()
                print(f"   ✅ '{mode}' → 视图: {views}")
            except Exception as e:
                print(f"   ❌ '{mode}' → 错误: {e}")

def demo_practical_usage():
    """演示实际使用案例"""
    
    print("\n\n🎯 实际使用案例演示")
    print("=" * 60)
    
    print("\n📊 案例1: 功能性脑网络分析")
    print("使用三视图模式查看整体激活模式")
    viz_networks = EelbrainPlotly2DViz(
        display_mode='ortho',
        cmap='Hot',
        show_max_only=True
    )
    print("🔧 配置: display_mode='ortho', cmap='Hot'")
    print("📐 视图:", viz_networks._parse_display_mode())
    
    print("\n📊 案例2: 半球功能不对称性研究") 
    print("使用左右半球对比模式")
    viz_asymmetry = EelbrainPlotly2DViz(
        display_mode='lr',
        cmap='Viridis',
        arrow_threshold='auto'
    )
    print("🔧 配置: display_mode='lr', cmap='Viridis'")
    print("📐 视图:", viz_asymmetry._parse_display_mode())
    
    print("\n📊 案例3: 单一平面详细分析")
    print("聚焦于轴向平面的高分辨率分析")
    viz_focused = EelbrainPlotly2DViz(
        display_mode='z',
        cmap='Plasma',
        show_max_only=False
    )
    print("🔧 配置: display_mode='z', cmap='Plasma'")
    print("📐 视图:", viz_focused._parse_display_mode())
    
    print("\n📊 案例4: 复合视图全景分析")
    print("使用四视图获得最全面的视角")
    viz_comprehensive = EelbrainPlotly2DViz(
        display_mode='lzry',
        cmap='Cividis',
        arrow_threshold=0.01
    )
    print("🔧 配置: display_mode='lzry', cmap='Cividis'")
    print("📐 视图:", viz_comprehensive._parse_display_mode())

def demo_jupyter_integration():
    """演示Jupyter集成功能"""
    
    print("\n\n💻 Jupyter集成演示")
    print("=" * 60)
    
    print("🎯 响应式尺寸检测 + Display Mode组合使用:\n")
    
    example_code = '''
# 在Jupyter notebook中的使用示例:

# 1. 自动检测尺寸 + 单视图模式
viz_auto = EelbrainPlotly2DViz(display_mode='z')
viz_auto.show_in_jupyter_auto()

# 2. 自定义尺寸 + 双视图模式  
viz_custom = EelbrainPlotly2DViz(display_mode='lr')
viz_custom.show_in_jupyter_responsive(aspect_ratio=2.0, max_width=1600)

# 3. 静态显示 + 三视图模式
viz_static = EelbrainPlotly2DViz(display_mode='ortho')
viz_static.show_in_jupyter_static(time_idx=30, width=1400, height=800)

# 4. 复杂布局 + 完全交互
viz_interactive = EelbrainPlotly2DViz(display_mode='lzry')
viz_interactive.show_in_jupyter(width=1600, height=1000)
'''
    
    print(example_code)
    
    print("\n🎨 Display Mode与Jupyter显示方法的最佳搭配:")
    recommendations = {
        "单视图模式 ('x', 'y', 'z')": "show_in_jupyter_static() - 静态显示，完美尺寸控制",
        "双视图模式 ('xz', 'lr', 等)": "show_in_jupyter_responsive() - 响应式布局",
        "三视图模式 ('ortho', 'lyr')": "show_in_jupyter_auto() - 自动优化尺寸",
        "四视图模式 ('lzry', 等)": "show_in_jupyter() - 固定大尺寸显示"
    }
    
    for mode_type, recommendation in recommendations.items():
        print(f"  • {mode_type}: {recommendation}")

if __name__ == "__main__":
    # 运行所有演示
    demo_display_modes()
    demo_practical_usage() 
    demo_jupyter_integration()
    
    print("\n\n🎉 Display Mode功能演示完成!")
    print("💡 现在您可以:")
    print("   • 选择最适合您研究问题的视图布局")
    print("   • 组合使用动态尺寸检测和display_mode")
    print("   • 在Jupyter中获得最佳的可视化体验")
    print("   • 导出高质量的科研图片")


