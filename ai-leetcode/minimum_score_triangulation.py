class Solution:
    def minScoreTriangulation(self, values):
        """
        计算凸多边形三角剖分后的最低分
        
        参数:
        values: List[int] - 多边形每个顶点的值（顺时针顺序）
        
        返回:
        int - 三角剖分后的最低分
        """
        n = len(values)
        # dp[i][j] 表示从顶点i到顶点j的多边形三角剖分的最低分
        dp = [[0] * n for _ in range(n)]
        
        # 按区间长度从小到大计算
        # 长度为2表示两点之间没有三角形，需要至少3个点才能形成三角形
        for length in range(3, n + 1):
            # 遍历所有可能的起始顶点i
            for i in range(n - length + 1):
                # 计算结束顶点j
                j = i + length - 1
                # 初始化为一个很大的值
                dp[i][j] = float('inf')
                # 遍历i和j之间的所有可能的中间顶点k
                for k in range(i + 1, j):
                    # 状态转移方程：dp[i][j] = min(dp[i][k] + dp[k][j] + values[i]*values[j]*values[k])
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + values[i] * values[j] * values[k])
        
        # 返回整个多边形的结果
        return dp[0][n - 1]

# 测试用例
if __name__ == "__main__":
    solution = Solution()
    
    # 测试用例1: [1,2,3] - 一个三角形，只能有一种剖分方式
    # 结果应该是1*2*3=6
    print(solution.minScoreTriangulation([1, 2, 3]))  # 预期输出: 6
    
    # 测试用例2: [3,7,4,5] - 四边形，有两种剖分方式
    # 方式1: 选择顶点0-1-2形成三角形，分数为3*7*4=84，剩下的四边形变成三角形0-2-3，分数为3*4*5=60，总分数84+60=144
    # 方式2: 选择顶点0-2-3形成三角形，分数为3*4*5=60，剩下的四边形变成三角形0-1-2，分数为3*7*4=84，总分数60+84=144
    # 方式3: 选择顶点1-2-3形成三角形，分数为7*4*5=140，剩下的四边形变成三角形0-1-3，分数为3*7*5=105，总分数140+105=245
    # 所以最低分数是144
    print(solution.minScoreTriangulation([3, 7, 4, 5]))  # 预期输出: 144
    
    # 测试用例3: [1,3,1,4,1,5] - 六边形
    # 最低分数为13
    print(solution.minScoreTriangulation([1, 3, 1, 4, 1, 5]))  # 预期输出: 13