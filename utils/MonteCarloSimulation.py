import random
import math

# 生成100个随机点
points = [(random.uniform(0, 40), random.uniform(0, 40), random.uniform(0, 100), random.uniform(-10, 10)) for _ in
          range(100)]


# 蒙特卡罗模拟过程
def monte_carlo_simulation(data, target_correlation):
    current_correlation = 0
    while abs(current_correlation - target_correlation) > 0.01:  # 设置目标水平精度为0.01
        # 选择两个点进行属性值交换
        idx1, idx2 = random.sample(range(len(data)), 2)
        data[idx1], data[idx2] = data[idx2], data[idx1]

        # 计算当前的相关性
        current_correlation = calculate_correlation(data)

        # 比较并更新相关性
        if abs(current_correlation - target_correlation) < abs(
                calculate_correlation([data[idx1], data[idx2]]) - target_correlation):
            # 如果当前值更接近目标值，则保留交换后的值
            continue
        else:
            # 否则交换回原始值
            data[idx1], data[idx2] = data[idx2], data[idx1]

    return data


# 计算相关性的函数，这里使用简单的相关性计算方法
def calculate_correlation(data):
    # 假设这里是相关性的计算方式
    # 这里使用了一个简化的相关性计算方法，实际应用中可能需要更复杂的方法
    values = [point[3] for point in data]  # 获取属性值
    distances = [math.sqrt((point[0] - data[0][0]) ** 2 + (point[1] - data[0][1]) ** 2) for point in data]  # 计算距离
    correlation = sum(values) / sum(distances)  # 计算相关性，这里仅作演示用

    return correlation


# 生成7个数据集，模拟空间自相关
space_correlation_levels = [-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
datasets = [monte_carlo_simulation(points.copy(), level) for level in space_correlation_levels]
print(datasets)