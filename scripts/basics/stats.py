"""统计数字文件：个数、平均值、最小值、最大值。"""


def load_numbers(filename):
    """读取文件，返回 (有效数字列表, 跳过的行数)。"""
    nums = []
    skipped = 0

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
        return [], 0

    return nums, skipped


def summarize(nums):
    """返回 (个数, 平均值, 最小值, 最大值)。"""
    count = len(nums)
    mean = sum(nums) / count
    return count, mean, min(nums), max(nums)


def main():
    filename = "numbers.txt"

    nums, skipped = load_numbers(filename)

    if not nums:
        print("没有有效数据（文件为空或全是非法行）")
        return

    count, mean, lo, hi = summarize(nums)

    print(f"有效数据 {count} 个")
    print(f"平均值 {mean:.2f}")
    print(f"最小值 {lo:.2f}")
    print(f"最大值 {hi:.2f}")
    print(f"跳过 {skipped} 行非法数据")


if __name__ == "__main__":
    main()
