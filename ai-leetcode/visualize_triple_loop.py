import time
from typing import List

class SolutionVisualizer:
    def __init__(self):
        self.delay = 1  # 每次循环的延迟时间（秒）
    
    def visualize_triple_loop(self, points: List[List[int]]):
        """可视化三层循环选取三点组合的过程"""
        n = len(points)
        print(f"总共有 {n} 个点: {points}")
        print(f"将遍历所有可能的三点组合，总共有 C({n},3) = {n*(n-1)*(n-2)//6} 种组合\n")
        
        # 遍历所有可能的三点组合
        for i in range(n):
            print(f"\033[1;32m=== 第一层循环 i = {i}, 选择点 {points[i]} ===\033[0m")
            time.sleep(self.delay)
            
            for j in range(i + 1, n):
                print(f"  \033[1;34m--- 第二层循环 j = {j}, 选择点 {points[j]} ---\033[0m")
                time.sleep(self.delay)
                
                for k in range(j + 1, n):
                    # 创建当前状态的可视化表示
                    visualization = []
                    for idx, point in enumerate(points):
                        if idx == i:
                            visualization.append(f"\033[1;32m{i}:{point}\033[0m")  # 绿色高亮第一个点
                        elif idx == j:
                            visualization.append(f"\033[1;34m{j}:{point}\033[0m")  # 蓝色高亮第二个点
                        elif idx == k:
                            visualization.append(f"\033[1;31m{k}:{point}\033[0m")  # 红色高亮第三个点
                        else:
                            visualization.append(f"{idx}:{point}")
                    
                    # 打印当前选择的三个点
                    print(f"    第三层循环 k = {k}, 选择点 {points[k]}")
                    print(f"    当前选择: [i={i},j={j},k={k}] = [{points[i]}, {points[j]}, {points[k]}]")
                    print(f"    点列表: [" + ", ".join(visualization) + "]")
                    print("    " + "-" * 60)
                    time.sleep(self.delay * 0.5)  # 第三层循环延迟短一些

# 主函数
if __name__ == "__main__":
    visualizer = SolutionVisualizer()
    
    # 使用一个简单的例子来可视化
    example_points = [[0,0], [0,1], [1,0], [1,1]]
    print("=== 三点组合选取动画演示 ===")
    print("这个动画展示了如何使用三层循环从点列表中选择所有可能的三点组合")
    print("每层循环用不同颜色高亮显示当前选择的点:")
    print("  - 绿色: 第一层循环选择的点")
    print("  - 蓝色: 第二层循环选择的点")
    print("  - 红色: 第三层循环选择的点")
    print("\n按 Ctrl+C 可以随时停止演示\n")
    
    try:
        visualizer.visualize_triple_loop(example_points)
        print("\n=== 动画演示结束 ===")
    except KeyboardInterrupt:
        print("\n=== 动画演示已停止 ===")