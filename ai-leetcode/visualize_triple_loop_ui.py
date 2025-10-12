import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider
import numpy as np
from typing import List, Tuple, Optional
import time

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "sans-serif"]

class TripleLoopVisualizer:
    def __init__(self):
        # 初始化数据
        self.points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        self.n = len(self.points)
        
        # 初始化循环状态
        self.i = 0
        self.j = 1
        self.k = 2
        self.animation_running = False
        self.animation_speed = 1.0  # 动画速度因子
        
        # 创建图形和子图
        self.fig, (self.ax_plot, self.ax_info) = plt.subplots(1, 2, figsize=(12, 6))
        self.fig.subplots_adjust(bottom=0.2, right=0.75)
        
        # 设置绘图区域
        self.setup_plot_area()
        
        # 添加按钮和滑块
        self.setup_controls()
        
        # 初始化绘制
        self.update_plot()
        
        # 创建动画对象
        self.anim = None
    
    def setup_plot_area(self):
        """设置绘图区域"""
        self.ax_plot.set_title('三点组合选取可视化')
        self.ax_plot.set_xlabel('X坐标')
        self.ax_plot.set_ylabel('Y坐标')
        
        # 设置坐标轴范围，留出一些边距
        x_min, x_max = min(self.points[:, 0]) - 0.5, max(self.points[:, 0]) + 0.5
        y_min, y_max = min(self.points[:, 1]) - 0.5, max(self.points[:, 1]) + 0.5
        self.ax_plot.set_xlim(x_min, x_max)
        self.ax_plot.set_ylim(y_min, y_max)
        self.ax_plot.grid(True)
    
    def setup_controls(self):
        """设置控件：按钮和滑块"""
        # 播放/暂停按钮
        ax_play = plt.axes([0.81, 0.7, 0.15, 0.075])
        self.btn_play = Button(ax_play, '播放')
        self.btn_play.on_clicked(self.toggle_animation)
        
        # 下一步按钮
        ax_next = plt.axes([0.81, 0.6, 0.15, 0.075])
        self.btn_next = Button(ax_next, '下一步')
        self.btn_next.on_clicked(self.next_step)
        
        # 重置按钮
        ax_reset = plt.axes([0.81, 0.5, 0.15, 0.075])
        self.btn_reset = Button(ax_reset, '重置')
        self.btn_reset.on_clicked(self.reset_animation)
        
        # 速度滑块
        ax_speed = plt.axes([0.2, 0.1, 0.65, 0.03])
        self.slider_speed = Slider(ax_speed, '速度', 0.1, 3.0, valinit=1.0)
        self.slider_speed.on_changed(self.update_speed)
    
    def update_plot(self):
        """更新绘图"""
        self.ax_plot.clear()
        self.ax_info.clear()
        
        self.setup_plot_area()
        
        # 绘制所有点
        self.ax_plot.scatter(self.points[:, 0], self.points[:, 1], c='gray', s=100, alpha=0.5)
        
        # 为每个点添加标签
        for idx, (x, y) in enumerate(self.points):
            self.ax_plot.annotate(f'P{idx}', (x, y), xytext=(5, 5), textcoords='offset points')
        
        # 高亮显示当前选中的三个点
        colors = ['green', 'blue', 'red']
        labels = ['i', 'j', 'k']
        selected_indices = [self.i, self.j, self.k]
        
        # 检查索引是否有效
        valid_indices = []
        for idx in selected_indices:
            if 0 <= idx < self.n:
                valid_indices.append(idx)
        
        # 绘制选中的点和连接线
        for i, idx in enumerate(valid_indices):
            x, y = self.points[idx]
            self.ax_plot.scatter(x, y, c=colors[i], s=150, label=f'{labels[i]} = {idx}')
            
        # 如果有三个有效的点，绘制三角形
        if len(valid_indices) == 3:
            triangle_points = self.points[valid_indices]
            # 闭合三角形
            triangle_points = np.vstack([triangle_points, triangle_points[0]])
            self.ax_plot.plot(triangle_points[:, 0], triangle_points[:, 1], 'k-', alpha=0.5)
        
        # 添加图例
        self.ax_plot.legend(loc='upper right')
        
        # 在信息区域显示当前状态
        self.ax_info.axis('off')
        info_text = []
        info_text.append(f'总点数: {self.n}')
        info_text.append(f'总组合数: {self.n * (self.n - 1) * (self.n - 2) // 6}')
        info_text.append('')
        info_text.append(f'当前循环状态:')
        info_text.append(f'  i = {self.i}, 点 = {self.points[self.i]} (绿色)')
        info_text.append(f'  j = {self.j}, 点 = {self.points[self.j]} (蓝色)')
        info_text.append(f'  k = {self.k}, 点 = {self.points[self.k]} (红色)')
        
        # 显示当前组合是否有效
        if self.is_valid_combination():
            info_text.append('')
            info_text.append(f'当前组合: [i={self.i}, j={self.j}, k={self.k}]')
            info_text.append('这是一个有效的三点组合')
        else:
            info_text.append('')
            info_text.append('当前索引组合无效，请继续')
        
        self.ax_info.text(0.05, 0.95, '\n'.join(info_text), 
                          verticalalignment='top', 
                          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        self.fig.canvas.draw_idle()
    
    def is_valid_combination(self):
        """检查当前的i, j, k是否构成有效的三点组合"""
        return (0 <= self.i < self.n and 
                0 <= self.j < self.n and 
                0 <= self.k < self.n and 
                self.i < self.j < self.k)
    
    def next_step(self, event=None):
        """执行下一步循环"""
        # 按照三层循环的逻辑更新索引
        if self.k < self.n - 1:
            self.k += 1
        elif self.j < self.n - 2:
            self.j += 1
            self.k = self.j + 1
        elif self.i < self.n - 3:
            self.i += 1
            self.j = self.i + 1
            self.k = self.j + 1
        else:
            # 循环结束，重置到开始
            self.reset_animation()
            return
        
        self.update_plot()
    
    def toggle_animation(self, event):
        """切换动画播放/暂停状态"""
        self.animation_running = not self.animation_running
        self.btn_play.label.set_text('暂停' if self.animation_running else '播放')
        
        if self.animation_running:
            self.start_animation()
        else:
            self.stop_animation()
    
    def animate(self, frame):
        """动画更新函数，用于matplotlib.animation"""
        if self.animation_running:
            self.next_step()
        return self.ax_plot, self.ax_info
    
    def start_animation(self):
        """启动动画"""
        if self.anim is None:
            # 根据速度计算间隔（毫秒）
            interval = int(1000 / self.animation_speed)
            self.anim = animation.FuncAnimation(
                self.fig, self.animate, interval=interval, blit=False
            )
        else:
            # 更新现有动画的间隔
            interval = int(1000 / self.animation_speed)
            self.anim.event_source.interval = interval
        self.fig.canvas.draw_idle()
    
    def stop_animation(self):
        """停止动画"""
        if self.anim is not None:
            self.anim.event_source.stop()
    
    def reset_animation(self, event=None):
        """重置动画到初始状态"""
        self.animation_running = False
        self.btn_play.label.set_text('播放')
        self.i = 0
        self.j = 1
        self.k = 2
        self.update_plot()
    
    def update_speed(self, val):
        """更新动画速度"""
        self.animation_speed = val
        # 如果动画正在运行，更新速度
        if self.animation_running:
            self.start_animation()
    
    def show(self):
        """显示UI界面"""
        plt.show()

# 主函数
if __name__ == "__main__":
    visualizer = TripleLoopVisualizer()
    visualizer.show()