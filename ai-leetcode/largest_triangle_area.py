from typing import List

class Solution:
    def largestTriangleArea(self, points: List[List[int]]) -> float:
        # 获取点的数量
        n = len(points)
        max_area = 0
        
        # 遍历所有可能的三点组合
        for i in range(n):
            x1, y1 = points[i]
            for j in range(i + 1, n):
                x2, y2 = points[j]
                for k in range(j + 1, n):
                    x3, y3 = points[k]
                    
                    # 使用向量叉积计算三角形面积
                    # 面积 = 1/2 * |(x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)|
                    area = 0.5 * abs((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
                    
                    # 更新最大面积
                    max_area = max(max_area, area)
        
        return max_area

# 测试代码
if __name__ == "__main__":
    solution = Solution()
    
    # 测试用例1: [[0,0],[0,1],[1,0],[0,2],[2,0]] - 预期输出: 2.0
    print(solution.largestTriangleArea([[0,0],[0,1],[1,0],[0,2],[2,0]]))
    
    # 测试用例2: [[1,0],[0,0],[0,1]] - 预期输出: 0.5
    print(solution.largestTriangleArea([[1,0],[0,0],[0,1]]))
    
    # 测试用例3: [[3,4],[2,5],[1,6]] - 预期输出: 1.0
    print(solution.largestTriangleArea([[3,4],[2,5],[1,6]]))