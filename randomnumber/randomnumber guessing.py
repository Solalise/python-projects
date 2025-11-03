import random

randomnumber = random.randint(1,100)
user = None
attempts = 0
score = 100

while user != randomnumber:
    user = int(input("숫자를 입력해주세요:"))
    attempts += 1
    score -= 10

    if user > randomnumber:
        print("너무 큽니다")
    elif  user < randomnumber:
        print("너무 작습니다")
    else:
        print("정답입니다!")
        print(f"시도  횟수: {attempts}번")
        print(f"최종 점수는 {max(score, 0)}점입니다")
        break


    if attempts == 2:
        if randomnumber %2 == 0:
            print("힌트:정답은 짝수입니다.")
        else:
            print("힌트:정답은 홀수입니다.")


    if attempts ==3:
        for i in range(2,10):
            if randomnumber % i == 0:
                print(f"힌트: 정답은 {i}의 배수입니다")
                break
