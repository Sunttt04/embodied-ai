filename = "numbers.txt"

nums = []
skipped = 0

# 1. 打开并逐行解析
try:
    with open(filename) as f:
        for line in f:
            text = line.strip()
            if text == "":
                continue
            try:
                nums.append(float(text))
            except ValueError:
                skipped += 1
except FileNotFoundError:
    print(f"文件不存在：{filename}")
    exit()

# 2. 没有有效数据就提前结束
if not nums:
    print("没有有效数据（文件为空或全是非法行）")
    exit()

# 3. 统计
count = len(nums)
mean = sum(nums) / count

print(f"有效数据 {count} 个")
print(f"平均值 {mean:.2f}")
print(f"最小值 {min(nums):.2f}")
print(f"最大值 {max(nums):.2f}")
print(f"跳过 {skipped} 行非法数据")
