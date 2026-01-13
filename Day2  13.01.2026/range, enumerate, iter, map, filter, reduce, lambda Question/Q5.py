# 5. Uses enumerate() to print the index and value of the final result list

squares = list(map(lambda x: pow(x, 2), filter(lambda x: not x % 2, range(1, 21))))

for count, item in enumerate(squares):
    print(f"[{count}] -> {item}")