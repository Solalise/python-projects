import random

game = ["가위", "바위", "보"]
user_score = 0
computer_score = 0

print("게임을 시작합니다")
print("먼저 5점을 한쪽이 획득하면 끝이 납니다")

while True:
    user = input("가위, 바위, 보 중 한개를 입력해주세요 :")


    if user not in game:
        print("잘못된 입력입니다.")
        continue


    computer = random.choice(game)
    print(f"컴퓨터: {computer}")

    if user == computer:
        print("비겼습니다!")
    elif (user == "가위" and computer == "보") or \
         (user == "바위" and computer == "가위") or \
         (user == "보" and computer == "바위"):
        print("승리하셨습니다")
        user_score += 1
    else:
        print("패배하셨습니다")
        computer_score += 1

    game_score = user_score - computer_score
    print(f"현재 점수는 {game_score}점 입니다")


    if user_score == 5:
        print("당신이 게임에서 승리하셨습니다")
        break
    elif computer_score == 5:
        print("당신이 게임에서 패배하셨습니다")
        break
    
