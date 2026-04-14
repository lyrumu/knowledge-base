import random
#python随机数生成
random_number = random.randint(1,100)#包括1和00
cnt = 0
while True:
    guess = int(input("请猜测一到一百的数字！"))
    if guess == random_number:
        cnt+=1
        print(f"猜对了！,共猜测了{cnt}次！太厉害了吧！")
        break
    elif guess > random_number:
        print("太大了！")
        cnt+=1
    elif guess < random_number:
        print("太小了！")
        cnt+=1