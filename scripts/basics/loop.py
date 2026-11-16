nums=[3,7,2,9,5]
max_val=nums[0]
for i in nums:
    if i>=max_val:
        max_val=i
    else:
        max_val=max_val
print(max_val)

