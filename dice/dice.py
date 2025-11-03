import random


while True:
    number = int(input("몇 개의 주사위를 굴리겠습니까? (1~5): "))

    print("결과")
    for i in range(number):
        randomdice = random.randint(1,6)
        print(f"주사위 {i+1}: {randomdice}")


      


    user = input("다시 굴리시겠습니까(Y,N)?").upper()
    if user == "Y":
        continue
    elif user == "N":
        print("프로그램이 종료합니다.")
        break
    else:
        print("잘못 입력하셨습니다")
        break

     

    
    
      
