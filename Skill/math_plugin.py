# import math
# from semantic_kernel.functions import kernel_function
#
# class MathPlugin:
#     """
#     这是一个数学技能包，包含原生计算和语义理解
#     """
#
#     # --- 1. Native Function (原生函数：处理硬计算) ---
#     @kernel_function(
#         description="计算数字的平方根",
#         name="Sqrt"
#     )
#     def sqrt(self, number: float) -> float:
#         return math.sqrt(number)
#
#     # --- 2. Native Function (原生函数：加法) ---
#     @kernel_function(
#         description="计算两个数字的和",
#         name="Add"
#     )
#     def add(self, number1: float, number2: float) -> float:
#         return number1 + number2