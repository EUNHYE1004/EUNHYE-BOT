import asyncio, discord, time, schedule, openpyxl, logging, time, datetime
import os
import json
from game import *
from user import *
from discord.ext import commands
from datetime import datetime, timedelta
from PointManager import PointManager

client = commands.Bot(command_prefix="!")

token = "ODU2Njc2MTQ0MTYxODgyMTcz.YNEf1Q.M1pXYg3_HYW4YYtTg08vzsPEoVY"

@client.event
async def on_ready(): # do action 1 time when ready

    # discord.Status.online -> dnd : "다른 용무 중", idle : "자리 비움"
    await client.change_presence(status=discord.Status.online, activity=discord.Game("꿀벌코인 채집")) # print status at right of discord UI
    print("꿀벌 on") # print state


@client.command()
async def 주인님(ctx):

    await ctx.send("절 만드신 분은 은혜#1004 님이에여!! 주인님 욕하면 꿀벌이 화낼꾸야")
@client.command()
async def 출첵(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    now = time.localtime()
    user, row = checkUser(ctx.author.name, ctx.author.id)
    _check = getcheck(ctx.author.name, userRow)
    if _check == 1:
        if userExistance:
            addMoney(row, int(10000))
            addChk(row, int(1))
            st()
            await ctx.send(f'⏰{now.tm_year}년 {now.tm_mon}월 {now.tm_mday}일 {now.tm_hour}시 {now.tm_min}분⏰')
            await ctx.send(str(ctx.author.name) + "님이 출석체크 하였습니다")
            await ctx.send("🎁일일보상🎁 지급완료")

        else:
            await ctx.send("출석체크는 회원가입 후 이용 가능합니다.")
    else:
        await ctx.send("출석체크는 하루에 한 번만 가능합니다.")
@client.command()
async def 들어와(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()  # PyNaCl 라이브러리 필요

@client.command()
async def 나가(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def 청소(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.send("삭제완료!")

@client.command()
async def 핑(ctx):
    await ctx.send(f'꿀벌 로딩속도 {round(round(client.latency, 4)*1000)}ms') # 봇의 핑을 pong! 이라는 메세지와 함께 전송한다
@client.command()
async def 도움(ctx):
    embed = discord.Embed(title="꿀벌 사용법", description="계속 추가 중", color=0x6E17E3)
    embed.add_field(name=client.command_prefix + "도움", value="도움말을 봅니다", inline=False)
    embed.add_field(name=client.command_prefix + "출첵", value="하루에 한 번 출석체크를 합니다/ 출첵시 10000코인 지급", inline=False)
    embed.add_field(name=client.command_prefix + "회원가입", value="각종 컨텐츠를 즐기기 위한 회원가입을 합니다 가입시/ 10000코인 지급", inline=False)
    embed.add_field(name=client.command_prefix + "주사위 [승,패,무] [코인]", value="[돈]을 걸고 주사위게임을 합니다/ 2.5배 무로 이길 시 6배", inline=False)
    embed.add_field(name=client.command_prefix + "홀짝 [홀,짝] [코인]", value="[돈]을 걸고 홀짝게임을 합니다/ 2배", inline=False)
    embed.add_field(name=client.command_prefix + "랭킹", value="꿀벌랭킹을 보여줍니다", inline=False)
    embed.add_field(name=client.command_prefix + "내정보", value="자신의 정보를 확인합니다", inline=False)
    embed.add_field(name=client.command_prefix + "정보 [대상]", value="멘션한 [대상]의 정보를 확인합니다", inline=False)
    embed.add_field(name=client.command_prefix + "송금 [대상] [코인]", value="멘션한 [대상]에게 [코인]을 보냅니다", inline=False)
    embed.add_field(name=client.command_prefix + "돈줘", value="꿀벌한테 불쌍한 척 하며 구걸합니다...", inline=False)
    embed.add_field(name=client.command_prefix + "청소 [숫자]", value="숫자만큼 채널의 채팅을 지웁니다", inline=False)
    embed.add_field(name=client.command_prefix + "내전 [시간]", value="내전할 사람을 모집 합니다", inline=False)
    embed.add_field(name=client.command_prefix + "투표 [선택지1] [선택지2]...", value="투표장이 투표 세팅을 한 후 투표를 진행합니다 선택지가 없으면 찬반투표로 진행", inline=False)
    embed.add_field(name=client.command_prefix + "핑", value="봇의 신호상태를 확인합니다", inline=False)
    embed.add_field(name=client.command_prefix + "주인님", value="은혜#1004 DM or @꿀벌 언급", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def 투표(ctx, title, *choice):
    '''
    투표
    :param title: 투표 제목
    :param choice: 선택지 (최대 9개)
    '''
    # TODO 웹
    # TODO 중복투표 불가능하게
    # TODO 익명투표 만들기
    # 투표 도움말
    if title is None and choice == ():
        embed = discord.Embed(title=f'투표 도움말', description=f'개발자: 은혜#1004')
        embed.add_field(name=f'좋아요/싫어요', value=f'!투표 제목')
        embed.add_field(name=f'복수응답(1-9)', value=f'!투표 제목 내용1 내용2 ...')
        await ctx.send(embed=embed)

    # 투표 진행
    else:
        embed = discord.Embed(title=title)
        if choice == ():
            # 좋아요/싫어요
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
            await message.add_reaction('👎')
        else:
            # 복수응답(1-10)
            emoji_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']  # 선택지 번호 라벨

            s = ''
            emoji = iter(emoji_list)
            for cont in choice:
                try:
                    s += f'{next(emoji)} {cont}\n'
                except ValueError:
                    await ctx.sent('투표 선택지는 9개까지만 가능합니다.')
                    return

            # 디스코드에 제목 출력
            embed.add_field(name=s, value='1은 기본적으로 있음, 중복투표 가능')
            message = await ctx.send(embed=embed)

            # 디스코드에 선택지 출력
            for i in range(len(choice)):
                await message.add_reaction(emoji_list[i])


"""@client.command()
async def 롤전적(ctx, id):
    
    op.gg에서 가져온 해당 유저의 롤 전적 조회
    :param id: 조회할 유저 id
    
    import requests
    from bs4 import BeautifulSoup
    import re

    url = f'http://www.op.gg/summoner/userName={id}'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, features='html.parser')

    # 태그 안에서 텍스트 추출
    def get_data(info):
        if info is not None:
            if re.search(r"\<.*\>", str(info)) is None:  # 태그가 있는지 확인
                return info
            else:
                return info.get_text().strip()  # 텍스트 추출
        else:
            return 'None'

    # 데이터 출력
    def print_data(info_type):
        result = ''
        # 해당 데이터가 존재하지 않는다면
        if len(info_type) == 1:
            return '해당 정보가 존재하지 않습니다.'
        else:
            for row in info_type[1:]:  # 데이터
                count = 0
                for data in info_type[0]:  # 해더
                    result += data + ': ' + row[count] + '\n'
                    count += 1
                if row is not info_type[-1]:
                    result += '-' * 10 + '\n'
            return result

    # 해당아이디가 존재하지 않는 경우
    if soup.find('div', class_='SummonerNotFoundLayout'):
        await ctx.send("해당 아이디가 존재하지 않네요. 혹시 오타는 아니시죠?")
        return

    # 소환사 정보
    user_info = [['소환사 이름', '티어', '리그 포인트', '승리', '패배', '승률']]
    name = id  # id 추가
    rank_info = soup.find('div', class_='TierRankInfo')
    tier = get_data(rank_info.find('div', class_='TierRank'))  # 솔로랭크 티어 추가
    if tier != 'Unranked':
        lp = get_data(rank_info.find('div', class_='TierInfo').find('span', 'LeaguePoints'))  # 리그 포인트 추가
        win = get_data(rank_info.find('span', class_='wins'))  # 승리 수 추가
        lose = get_data(rank_info.find('span', class_='losses'))  # 패배 수 추가
        winratio = get_data(rank_info.find('span', class_='winratio'))  # 승률 추가
    else:  # 언랭일 시
        lp, win, lose, winratio = 'None', 'None', 'None', 'None'
    user_info.append([name, tier, lp, win, lose, winratio])

    # 모스트 추가
    most_champ_lst = [['챔피언', 'kda', '승률']]
    if soup.find('div', class_='MostChampionContent') is not None:
        most_champ = soup.find('div', class_='MostChampionContent').find_all('div', 'ChampionBox Ranked')
        # 모스트 3 추출
        for champ in most_champ[: min(3, len(most_champ))]:
            champ_name = get_data(champ.find('div', class_='Face')['title'])  # 챔피언 이름 추가
            kda = get_data(champ.find('span', class_='KDA'))  # KDA
            champ_winratio = get_data(champ.find('div', class_='WinRatio normal tip'))  # 승률
            most_champ_lst.append([champ_name, kda, champ_winratio])

    # 최근 7일간 랭크 승률
    last_7 = [['챔피언 이름', '승률', '승리', '패배']]
    if soup.find('div', class_='Content') is not None:
        for champ in soup.find('div', class_='Content').find_all('div', class_='ChampionWinRatioBox'):
            champ_name = get_data(champ.find('div', class_='ChampionName')['title'])
            champ_winratio = get_data(champ.find('div', class_='WinRatio'))
            champ_win = get_data(champ.find('div', class_='Text Left'))
            champ_lose = get_data(champ.find('div', class_='Text Right'))
            last_7.append([champ_name, champ_winratio, champ_win, champ_lose])

    # TODO 데이터 전처리

    # TODO 디자인 고안
    embed = discord.Embed(title=f"{id}님 전적", description=f'디버그용')
    embed.add_field(name=f"Tire info", value=print_data(user_info))
    embed.add_field(name=f"모스트 챔프", value=print_data(most_champ_lst))
    embed.add_field(name=f"최근 전적", value=print_data(last_7))
    await ctx.send(embed=embed)
"""

@client.command()
async def 주사위(ctx, face, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    result, _color, bot1, bot2, user1, user2, a, b = dice()
    forecast =  result
    await ctx.send("주사위 굴리는 중..")
    await asyncio.sleep(1)
    betting = 0
    _color = 0x000000
    if userExistance:
        cur_money = getMoney(ctx.author.name, userRow)
        if int(money) >= 10:
            if cur_money >= int(money):
                if face == "승" or face == "패" or face == "무":
                    if forecast == face:
                        if face == "무":
                            result = "성공"
                            _color = 0x00ff56

                            betting = int(money)

                            modifyMoney(ctx.author.name, userRow, 5 * betting)
                        else:
                            result = "성공"
                            _color = 0x00ff56

                            betting = int(money)

                            modifyMoney(ctx.author.name, userRow, 1.5 * betting)
                    else:
                        result = "실패"
                        _color = 0xFF0000

                        betting = int(money)

                        modifyMoney(ctx.author.name, userRow, -int(betting))
                        addLoss(ctx.author.name, userRow, int(betting))

                    embed = discord.Embed(title="주사위 게임 결과", description= result,color=_color)
                    embed.add_field(name=ctx.author.name + "의 숫자 " + user1 + "+" + user2, value=":game_die: " + b,
                                    inline=False)
                    embed.add_field(name="꿀벌이 숫자 " + bot1 + "+" + bot2, value=":game_die: " + a, inline=False)
                    embed.add_field(name="배팅금액", value=betting, inline=False)
                    embed.add_field(name="현재 자산", value=getMoney(ctx.author.name, userRow), inline=False)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send("승 또는 패 또는 무를 입력하세요")
            else:
                await ctx.send("코인이 부족합니다. 현재자산: " + str(cur_money))
        else:
            await ctx.send("10개 이상만 배팅 가능합니다.")
    else:
        await ctx.send("주사위게임은 회원가입 후 이용 가능합니다.")
@client.command()
async def 홀짝(ctx, face, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    forecast = coin()
    await ctx.send("홀짝 확인 중..")
    await asyncio.sleep(1)
    result = ""
    betting = 0
    _color = 0x000000
    if userExistance:
        cur_money = getMoney(ctx.author.name, userRow)
        if int(money) >= 10:
            if cur_money >= int(money):
                if face == "홀" or face == "짝":
                    if forecast == face:
                        result = "성공"
                        _color = 0x00ff56

                        betting = int(money)

                        modifyMoney(ctx.author.name, userRow, 1 * betting)
                    else:
                        result = "실패"
                        _color = 0xFF0000

                        betting = int(money)

                        modifyMoney(ctx.author.name, userRow, -int(betting))
                        addLoss(ctx.author.name, userRow, int(betting))

                    embed = discord.Embed(title="📍홀짝게임 결과📍", description= result, color=_color)
                    embed.add_field(name=ctx.author.name +"의 결과", value=forecast, inline=False)
                    embed.add_field(name="배팅금액", value=betting, inline=False)
                    embed.add_field(name="현재 자산", value=getMoney(ctx.author.name, userRow), inline=False)

                    await ctx.send(embed=embed)

                else:
                    await ctx.send("홀 또는 짝을 입력하세요")
            else:
                await ctx.send("코인이 부족합니다. 현재자산: " + str(cur_money))
        else:
            await ctx.send("10개 이상만 배팅 가능합니다.")
    else:
        await ctx.send("홀짝게임은 회원가입 후 이용 가능합니다.")



@client.command()
async def 랭킹(ctx):
    rank = ranking()
    embed = discord.Embed(title="꿀벌 랭킹", color=0x4A44FF)
    for i in range(0, len(rank)):
        if i % 2 == 0:
            name = rank[i]
            lvl = rank[i + 1]
            embed.add_field(name=str(int(i / 2 + 1)) + "위 " + name, value="꿀벌코인: " + str(lvl), inline=False)
    await ctx.send(embed=embed)


@client.command()
async def 회원가입(ctx):
    print("회원가입이 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        await ctx.send("이미 가입하셨습니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("")
        Signup(ctx.author.name, ctx.author.id)
        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("회원가입이 완료되었습니다.",tts=True)


@client.command()
@commands.is_owner()
async def 탈퇴(ctx):
    print("탈퇴가 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        DeleteAccount(userRow)
        print("탈퇴가 완료되었습니다.")
        print("------------------------------\n")
        await ctx.send("주인님한테 문의주세용 위이잉")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("등록되지 않은 사용자입니다.")


@client.command()
async def 내정보(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 자신의 정보를 확인할 수 있습니다.")
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        boxes = int(exp / (level * level + 6 * level) * 20)
        expToUP = level * level + 6 * level
        boxes = int(exp / expToUP * 20)
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description=ctx.author.name, color=0x62D0F6)
        embed.add_field(name="레벨", value=level)
        embed.add_field(name="순위", value=str(rank) + "/" + str(userNum))
        embed.add_field(name="XP: " + str(exp) + "/" + str(level * level + 6 * level),
                        value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
        embed.add_field(name="XP: " + str(exp) + "/" + str(expToUP),
                        value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
        embed.add_field(name="보유 자산", value=money, inline=False)
        embed.add_field(name="도박으로 날린 코인", value=loss, inline=False)

        await ctx.send(embed=embed)


@client.command()
async def 정보(ctx, user: discord.User):
    userExistance, userRow = checkUser(user.name, user.id)
    if not userExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description=user.name, color=0x62D0F6)
        embed.add_field(name="레벨", value=level)
        embed.add_field(name="경험치", value=str(exp) + "/" + str(level * level + 6 * level))
        embed.add_field(name="순위", value=str(rank) + "/" + str(userNum))
        embed.add_field(name="보유 자산", value=money, inline=False)
        embed.add_field(name="도박으로 날린 코인", value=loss, inline=False)
        await ctx.send(embed=embed)


@client.command()
async def 송금(ctx, user: discord.User, money):
    print("송금이 가능한지 확인합니다.")
    senderExistance, senderRow = checkUser(ctx.author.name, ctx.author.id)
    receiverExistance, receiverRow = checkUser(user.name, user.id)
    if not senderExistance:
        print("DB에서", ctx.author.name, "을 찾을수 없습니다")
        print("------------------------------\n")
        await ctx.send("회원가입 후 송금이 가능합니다.")
    elif not receiverExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        print("송금하려는 코인: ", money)
        s_money = getMoney(ctx.author.name, senderRow)
        r_money = getMoney(user.name, receiverRow)
        if s_money >= int(money) and int(money) != 0:
            print("코인이 충분하므로 송금을 진행합니다.")
            print("")
            remit(ctx.author.name, senderRow, user.name, receiverRow, money)
            print("송금이 완료되었습니다. 결과를 전송합니다.")
            embed = discord.Embed(title="송금 완료", description="송금된 코인: " + money, color=0x77ff00)
            embed.add_field(name="보낸 사람: " + ctx.author.name,
                            value="현재 자산: " + str(getMoney(ctx.author.name, senderRow)))
            embed.add_field(name="→", value=":moneybag:")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(getMoney(user.name, receiverRow)))

            await ctx.send(embed=embed)
        elif int(money) == 0:
            await ctx.send("0코인이 보내지겠냐 멍청행")
        else:
            print("코인이 충분하지 않습니다.")
            print("송금하려는 코인: ", money)
            print("현재 자산: ", s_money)
            await ctx.send("코인이 충분하지 않습니다. 현재 자산: " + str(s_money))
        print("------------------------------\n")
@client.command()
async def 내전(ctx, amount : str):
    embed = discord.Embed(title="🛡️내전🛡️", description="선착순 모집 10명", color=0x6E17E3)
    embed.add_field(name="소환사의협곡 5대5", value="방제:0412 / 비번:1234", inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("⚔")
    await ctx.send("내전 시작은 "+ amount)
    await ctx.send("참여자는 ⚔ 눌러주세요")



@client.command()
async def 돈줘(ctx):
        user, row = checkUser(ctx.author.name, ctx.author.id)
        addMoney(row, int(100))
        print("money")
        await ctx.send("100원 줄테니 가라..")

@client.command()
@commands.is_owner()
async def reset(ctx):
    resetData()

@client.command()
@commands.is_owner()
async def 날짜(ctx):
    날짜reset()


@client.command()
@commands.is_owner()
async def 돈내놔(ctx, money):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addMoney(row, int(money))
    print("money")
    await ctx.send("주인님 확인완료")

@client.command()
async def exp(ctx, exp):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addExp(row, int(exp))
    print("exp")


@client.command()
@commands.is_owner()
async def lvl(ctx, lvl):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    adjustlvl(row, int(lvl))
    print("lvl")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!reset":
        await client.process_commands(message)
        return
    else:
        userExistance, userRow = checkUser(message.author.name, message.author.id)
        channel = message.channel
        if userExistance:
            levelUp, lvl = levelupCheck(userRow)
            if levelUp:
                print(message.author, "가 레벨업 했습니다")
                print("")
                embed = discord.Embed(title="레벨업", color=0x00A260)
                embed.set_footer(text=message.author.name + "님" + str(lvl) + "레벨 달성!")
                await channel.send(embed=embed)
            else:
                modifyExp(userRow, 1)
                print("------------------------------\n")
        await client.process_commands(message)


@client.event
async def on_member_remove(ctx, member):
    channel = member.server.get_channel('872066332861038594')
    fmt = (f'{ctx.author.mention}님이 서버에서 나가셨습니다!')
    await ctx.send(channel, fmt.format(member, member.server))

"""@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("!도움이라고 쳐바")
"""
client.run(token)
