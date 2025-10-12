from typing import List

class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        # 对数组进行排序
        nums.sort(reverse=True)  # 降序排序
        
        # 从最大的数开始，检查三个连续的数是否能组成三角形
        for i in range(len(nums) - 2):
            # 假设三个数为a >= b >= c，如果a < b + c，则可以组成三角形
            if nums[i] < nums[i+1] + nums[i+2]:
                # 返回这三个数的和（周长）
                return nums[i] + nums[i+1] + nums[i+2]
        
        # 如果不能形成任何面积不为零的三角形，返回0
        return 0

# 测试代码
if __name__ == "__main__":
    solution = Solution()
    
    # 测试用例1: [2,1,2] - 预期输出: 5
    print(solution.largestPerimeter([2,1,2]))
    
    # 测试用例2: [1,2,1,10] - 预期输出: 0
    print(solution.largestPerimeter([1,2,1,10]))
    
    # 测试用例3: [3,2,3,4] - 预期输出: 10
    print(solution.largestPerimeter([3,2,3,4]))