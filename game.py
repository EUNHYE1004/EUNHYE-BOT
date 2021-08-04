import random


def dice():
    print("game.py - dice")
    bot1 = random.randrange(1, 7)
    bot2 = random.randrange(1, 7)
    user1 = random.randrange(1, 7)
    user2 = random.randrange(1, 7)

    a = bot1 + bot2
    b = user1 + user2

    if a > b:
        return "패", 0xFF0000, str(bot1), str(bot2), str(user1), str(user2), str(a), str(b)
    elif a == b:
        return "무", 0xFAFA00, str(bot1), str(bot2), str(user1), str(user2), str(a), str(b)
    elif a < b:
        return "승", 0x00ff56, str(bot1), str(bot2), str(user1), str(user2), str(a), str(b)

def coin():
    coin_face = random.randrange(0,2)
    if coin_face == 0:
        return "홀"
    elif coin_face == 1:
        return "짝"
