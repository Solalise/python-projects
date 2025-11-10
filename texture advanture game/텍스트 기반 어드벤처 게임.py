import random
import sys
import copy

# 갈 수 있는 지역들
rooms = {
    '마을': {'east': '숲속', 'south': '해변가', 'west': '협곡', 'north': '미지의 안개숲'},
    '숲속': {'west': '마을', 'east': '동굴', 'north': '낭떠러지', 'south': '오크 부락'},
    '해변가': {'north': '마을', 'south': '심해', 'east': '보물방', 'west': '용의 둥지'},
    '협곡': {'east': '마을', 'north': '괴조 서식지', 'south': '동굴 거미 서식지', 'west': '돌풍 절벽'},
    '미지의 안개숲': {'south': '마을', 'east': '비밀의 숲', 'north': '엘프들의 마을', 'west': '정령 서식지'},
    '동굴': {'east': '마법사의동굴', 'west': '숲속', 'south': ' 무너진 동굴', 'north': '막다른 길'},
    '막다른 길': {'east': '동굴', 'west' :'동굴', 'north': '동굴', 'south': '동굴'},
    '마법사의 동굴': {'east': '동굴', 'west' :'동굴', 'north': '동굴', 'south': '동굴'},
    '무너진 동굴':{'east': '동굴', 'west' :'동굴', 'north': '동굴', 'south': '동굴'},
    '낭떠러지': {'east': '숲속', 'west' :'숲속', 'north': '숲속', 'south': '숲속'},
    '오크 부락': {'east': '태산 지대', 'west' :'해변가', 'north': '숲속', 'south': '보물방'},
    '태산 지대': {'east': '숲속', 'west' :'오크 부락', 'north': '동굴', 'south': '오크 부락'},
    '심해': {'east': '해안가', 'west' :'해안가', 'north': '해변가', 'south': '용궁'},
    '용의 둥지': {'east': '해변가', 'west' :'동굴 거미 서식지', 'north': '협곡', 'south': '해안가'},
    '해안가':{'east': '심해', 'west' :'해변가', 'north': '해변가', 'south': '해변가'},
    '용궁':{'east': '심연의 공포', 'west' :'심해', 'north': '심해', 'south': '심해'},
    '심연의 공포': {'east': '용궁', 'west' :'용궁', 'north': '용궁', 'south': '용궁'},
    '괴조 서식지': {'east': '정령 서식지', 'west' :'돌풍 절벽', 'north': '천역', 'south': '협곡'},
    '동굴 거미 서식지': {'east': '용의 둥지', 'west' :'깊은 심연', 'north': '협곡', 'south': '깊은 심연'},
    '깊은 심연': {'east': '동굴 거미 서식지', 'west' :'동굴 거미 서식지', 'north': '동굴 거미 서식지', 'south': '동굴 거미 서식지'},
    '돌풍 절벽': {'east': '협곡', 'west' :'협곡', 'north': '협곡', 'south': '협곡'},
    '천역': {'east': '천역', 'west' :'천역', 'north': '천역', 'south': '괴조 서식지'},
    '비밀의 숲': {'east': '비밀의 숲', 'west' :'미지의 안개숲', 'north': '비밀의 숲', 'south': '미지의 심연'},
    '미지의 심연' : {'east': '비밀의 숲', 'west' :'비밀의 숲', 'north': '비밀의 숲', 'south': '비밀의 숲'},
    '엘프들의 마을': {'east': '비밀의 숲', 'west' :'엘프들의 마을', 'north': '낭떠러지', 'south': '미지의 안개숲'},
    '정령 서식지': {'east': '미지의 안개숲', 'west' :'괴조 서식지', 'north': '정령 서식지', 'south': '정령 서식지'},
    '보물방': {'east': '오크 부락', 'west' :'해변가', 'north': '오크 부락', 'south': '심해'},
}

# 플레이어 정보
player = {
    'level': 1, 'exp': 0, 'gold': 30,
    'base_hp': 100, 'hp': 100, 'max_hp': 100,
    'base_mp': 50, 'mp': 50, 'max_mp': 50,
    'base_atk': 10000, 'base_def': 5,
    'atk': 10, 'def': 5,
    'inventory': ['낡은 검'],
    'equip': {'무기': None, '갑옷': None, '신발': None, '목걸이': None, '반지1': None, '반지2': None},
    'skills': [],
    'status': [],
    'current_room': '마을'
}
#아이템 성능
item_stats = {
    '낡은 검': {'atk': 7, 'def': 0, 'max_hp': 20, 'mp': 0, 'slot': '무기'},
    '녹슨 철검': {'atk': 15, 'def': 0, 'max_hp': 50, 'mp': 0, 'slot': '무기'},
    '철검': {'atk': 28, 'def': 0, 'max_hp': 80, 'mp': 0, 'slot': '무기'},
    '가죽 갑옷': {'atk': 0, 'def': 7, 'max_hp': 150, 'mp': 0, 'slot': '갑옷'},
    '강철 갑옷': {'atk': 0, 'def': 25, 'max_hp': 300, 'mp': 0, 'slot': '갑옷'},
    '가죽 장화': {'atk': 0, 'def': 3, 'max_hp': 0, 'mp': 10, 'slot': '신발'},
    '신속의 장화': {'atk': 0, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '신발'},
    '늑대 이빨 목걸이': {'atk': 0, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '목걸이'},
    '코볼트의 단검': {'atk': 22, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '무기'},
    '오크 갑옷': {'atk': 0, 'def': 35, 'max_hp': 400, 'mp': 30, 'slot': '갑옷'},
    '주술사의 반지': {'atk': 0, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '반지1'},
    '돌돌이 반지': {'atk': 0, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '반지2'},
    '딱딱이 갑옷': {'atk': 0, 'def': 50, 'max_hp': 100, 'mp': 30, 'slot': '갑옷'},
    '엘프의 활': {'atk': 90, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '무기'},
    '상어 이빨 검': {'atk': 120, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '무기'},
    '태산 부츠': {'atk': 0, 'def': 20, 'max_hp': 0, 'mp': 50, 'slot': '신발'},
    '바람 갑옷': {'atk': 0, 'def': 50, 'max_hp': 500, 'mp': 30, 'slot': '갑옷'},
    '정령의 반지': {'atk': 0, 'def': 15, 'max_hp': 0, 'mp': 40, 'slot': '반지1'},
    '폭풍의 가호': {'atk': 0, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '목걸이'},
    '용살검': {'atk': 200, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '무기'},
    '해신의 가호': {'atk': 0, 'def': 25, 'max_hp': 0, 'mp': 60, 'slot': '반지2'},
    '질투': {'atk': 0, 'def': 40, 'max_hp': 0, 'mp': 80, 'slot': '반지1'},
    '심해의 공포': {'atk': 300, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '무기'},
    '심연의 갑옷': {'atk': 0, 'def': 80, 'max_hp': 800, 'mp': 30, 'slot': '갑옷'},
    '안개 걸음': {'atk': 0, 'def': 30, 'max_hp': 0, 'mp': 80, 'slot': '신발'},
    '용살검 발뭉': {'atk': 450, 'def': 10, 'max_hp': 0, 'mp': 30, 'slot': '무기'},
    '전투의 각인 1단계': {'atk': 10, 'def': 10, 'max_hp': 10, 'mp': 10, 'slot': '각인'},
    '전투의 각인 2단계': {'atk': 50, 'def': 20, 'max_hp': 20, 'mp': 30, 'slot': '각인'},
    '전투의 각인 3단계': {'atk': 80, 'def': 30, 'max_hp': 40, 'mp': 50, 'slot': '각인'},
    '전투의 각인 4단계': {'atk': 100, 'def': 40, 'max_hp': 80, 'mp': 80, 'slot': '각인'},
    '전투의 각인 5단계': {'atk': 180, 'def': 45, 'max_hp': 100, 'mp': 90, 'slot': '각인'},
    '전투의 각인 6단계': {'atk': 250, 'def': 50, 'max_hp': 110, 'mp': 100, 'slot': '각인'},
    '전투의 각인 7단계': {'atk': 300, 'def': 55, 'max_hp': 130, 'mp': 110, 'slot': '각인'},
}
# 소비 아이템 성능
consumables = {
    'hp 포션': {'heal': 50},
    'mp 포션': {'mp_restore': 30},
    '상태이상 약': {'cleanse': True},
    '상급 포션' : {'heal': 200}
}

# 상점 아이템
shop_items = {
    '녹슨 철검': 25,
    '가죽 갑옷': 15,
    '가죽 장화': 50,
    '철검': 100,
    '강철 갑옷': 150,
    '신속의 장화': 80,
    '상태이상 약': 5,
    'hp 포션': 5,
    'mp 포션': 5,
    '상급 포션': 25,
    '전투의 각인 1단계' : 100,
    '전투의 각인 2단계' : 200,
    '전투의 각인 3단계' : 400,
    '전투의 각인 4단계' : 800,
    '전투의 각인 5단계' : 1200,
    '전투의 각인 6단계' : 1600,
    '전투의 각인 7단계' : 2000,
}



#몬스터
monsters = {
     #숲속 몬스터
    '슬라임[LV 1]': {
        'hp': 50, 'atk': 5, 'gold': 2, 'exp': 10,
        'drops': [('hp 포션', 0.2)],
        'skills': []
    },
    '늑대[LV 4]': {
        'hp': 100, 'atk': 10, 'gold': 4, 'exp': 20,
        'drops': [('늑대 이빨 목걸이', 0.3)],
        'skills': [
            {'name': '할퀴기', 'chance': 0.25, 'type': 'attack', 'power': 1.2} 
        ]
    },
    '코볼트[LV 6]': {
        'hp': 140, 'atk': 13, 'gold': 6, 'exp': 35,
        'drops': [('코볼트의 단검', 0.6)],
        'skills': [
            {'name': '돌 던지기', 'chance': 0.2, 'type': 'attack', 'power': 1.3}
        ]
    },
    '흡혈 박쥐[LV 8]': {
        'hp': 160, 'atk': 16, 'gold': 8, 'exp': 50,
        'drops': [('스킬북: 흡혈', 0.15)],
        'skills': [
            {
                'name': '흡혈', 'chance': 0.25,
                'type': 'lifesteal',
                'power': 1.0,        
                'heal_ratio': 0.5    
            }
        ]
    },
    '독 도마뱀[LV 9]': {
        'hp': 180, 'atk': 18, 'gold': 9, 'exp': 55,
        'drops': [('스킬북: 탈피', 0.05)],
        'skills': [
            {
                'name': '독침', 'chance': 0.25,
                'type': 'status',
                'status': {'name': '중독', 'duration': 4, 'dmg_per_turn': 5}
            }
        ]
    },
    '오크 전사[LV 16]': {
        'hp': 320, 'atk': 28, 'gold': 15, 'exp': 120,
        'drops': [('오크 갑옷', 0.1)],
        'skills': [
            {'name': '분노의 일격', 'chance': 0.3, 'type': 'attack', 'power': 1.5}
        ]
    },
    '오크 주술사[LV 20]': {
        'hp': 280, 'atk': 30, 'gold': 20, 'exp': 150,
        'drops': [('주술사의 반지', 0.2)],
        'skills': [
            {
                'name': '저주', 'chance': 0.2, 'type': 'debuff',
                'effect': {'atk_down': 3, 'duration': 3}
            }
        ]
    },
    '스톤 보어[LV 33]': {
        'hp': 600, 'atk': 42, 'gold': 23, 'exp': 220,
        'drops': [('hp 포션', 0.15)],
        'skills': [
            {'name': '돌진', 'chance': 0.25, 'type': 'attack', 'power': 1.4}
        ]
    },
    '태산의 지배자 트리톤[LV 40]': {
        'hp': 850, 'atk': 55, 'gold': 90, 'exp': 400,
        'drops': [('스킬북:지진', 1),('태산 부츠', 1) ],
        'skills': [
            {
                'name': '지진', 'chance': 0.2, 'type': 'aoe',
                'power': 1.3
            }
        ]
    },
    #해변 몬스터
    '모래게[LV 13]': {
        'hp': 250, 'atk': 20, 'gold': 12, 'exp': 80,
        'drops': [('hp 포션', 0.15)],
        'skills': []
    },
    '바다 갈매기[LV 10]': {
        'hp': 200, 'atk': 15, 'gold': 8, 'exp': 60,
        'drops': [],
        'skills': [{'name': '급강하', 'chance': 0.2, 'type': 'attack', 'power': 1.4}]
    },
    '용감한 용인 전사[LV 58]': {
        'hp': 1500, 'atk': 90, 'gold': 400, 'exp': 1000,
        'drops': [('용살검', 0.05)],
        'skills': [
            {'name': '전투의 포효', 'chance': 0.2, 'type': 'buff', 'effect': {'atk_up': 10, 'duration': 3}}
        ]
    },
    '매혹적인 인어[LV 62]': {
        'hp': 1700, 'atk': 94, 'gold': 450, 'exp': 1150,
        'drops': [('해신의 가호', 0.2)],
        'skills': [
            {'name': '매혹의 노래', 'chance': 0.15, 'type': 'status',
             'status': {'name': '매혹', 'duration': 2, 'dmg_per_turn': 0}}
        ]
    },
    '바다의 악몽 세이렌[LV 70]': {
        'hp': 2500, 'atk': 120, 'gold': 1000, 'exp': 2200,
        'drops': [('질투', 1)],
        'skills': [
            {'name': '절규', 'chance': 0.3, 'type': 'status',
             'status': {'name': '공포', 'duration': 2, 'dmg_per_turn': 0}}
        ]
    },
    '천공의 지배자인 바다용 아퀼로[LV ???]': {
        'hp': 10000, 'atk': 150, 'gold': 10000, 'exp': 20000,
        'drops': [('스킬북:수룡탄', 1), ('용살검 발뭉', 1)],
        'skills': [
            {
                'name': '브레스', 'chance': 0.5, 'type': 'aoe_status',
                'status': {'name': '화상', 'duration': 3, 'dmg_per_turn': 15},
                'power': 1.5
            }
        ]
    },
    '미믹[LV 14]': {
        'hp': 10, 'atk': 300, 'gold': 500, 'exp': 300,
        'drops': [],
        'skills': []
    },
    '턱상어[LV 37]': {
        'hp': 750, 'atk': 60, 'gold': 42, 'exp': 300,
        'drops': [('상어 이빨 검', 0.4)],
        'skills': [{'name': '물어뜯기', 'chance': 0.3, 'type': 'lifesteal', 'power': 1.2, 'heal_ratio': 0.3}]
    },
    '물총새[LV 39]': {
        'hp': 830, 'atk': 68, 'gold': 63, 'exp': 330,
        'drops': [('스킬북: 마나의 가호', 0.15)],
        'skills': [{'name': '돌풍 베기', 'chance': 0.25, 'type': 'attack', 'power': 1.4}]
    },
    '심연의 공포 메갈로돈[LV 80]': {
        'hp': 3300, 'atk': 135, 'gold': 2500, 'exp': 3500,
        'drops': [('심해의 조각', 1)],
        'skills': [
            {
                'name': '타이푼', 'chance': 0.5, 'type': 'aoe_status',
                'status': {'name': '기절', 'duration': 1, 'dmg_per_turn': 0},
                'power': 1.4
            }
        ]
        },
    #협곡 몬스터
    '돌돌이[LV 21]': {
    'hp': 260, 'atk': 22, 'gold': 25, 'exp': 90,
    'drops': [('돌돌이 반지', 0.15)],
    'skills': [
        {'name': '몸통 박치기', 'chance': 0.2, 'type': 'attack', 'power': 1.2}
    ]
},
'딱딱이[LV 24]': {
    'hp': 320, 'atk': 25, 'gold': 30, 'exp': 110,
    'drops': [('딱딱이 갑옷', 0.05)],
    'skills': [
        {'name': '단단해지기', 'chance': 0.25, 'type': 'buff', 'effect': {'def_up': 5, 'duration': 3}}
    ]
},
'괴조[LV 48]': {
    'hp': 950, 'atk': 60, 'gold': 70, 'exp': 250,
    'drops': [('스킬북: 울부짖기', 0.2)],
    'skills': [
        {'name': '날개 베기', 'chance': 0.25, 'type': 'attack', 'power': 1.3}
    ]
},
'괴조들의 왕 쿠퍼[LV 53]': {
    'hp': 1300, 'atk': 78, 'gold': 160, 'exp': 400,
    'drops': [('스킬북: 폭풍참', 1),('폭풍의 가호', 1)],
    'skills': [
        {'name': '폭풍참', 'chance': 0.3, 'type': 'aoe', 'power': 1.4},
        {'name': '분노의 울음', 'chance': 0.2, 'type': 'buff', 'effect': {'atk_up': 8, 'duration': 3}}
    ]
},
'동굴 거미[LV 51]': {
    'hp': 1000, 'atk': 65, 'gold': 80, 'exp': 300,
    'drops': [('스킬북: 맹독', 0.05)],
    'skills': [
        {'name': '독액', 'chance': 0.3, 'type': 'status',
         'status': {'name': '중독', 'duration': 3, 'dmg_per_turn': 8}},
        {'name': '거미줄 덫', 'chance': 0.25, 'type': 'status',
         'status': {'name': '속박', 'duration': 2, 'dmg_per_turn': 0}}
    ]
},
'거미들의 여왕 베로니카[LV 60]': {
    'hp': 1600, 'atk': 95, 'gold': 300, 'exp': 600,
    'drops': [('스킬북: 맹독 폭발', 1)],
    'skills': [
        {'name': '독폭발', 'chance': 0.4, 'type': 'status',
         'status': {'name': '중독', 'duration': 4, 'dmg_per_turn': 12}},
        {'name': '거미줄 폭풍', 'chance': 0.3, 'type': 'aoe_status',
         'status': {'name': '속박', 'duration': 2, 'dmg_per_turn': 0}, 'power': 1.2}
    ]
},
'깊은 그림자 어둑시니[LV 90]': {
    'hp': 2800, 'atk': 140, 'gold': 1000, 'exp': 2000,
    'drops': [('심연의 조각', 1), ('스킬북: 그림자 베기')],
    'skills': [
        {'name': '그림자 베기', 'chance': 0.3, 'type': 'attack', 'power': 1.5},
        {'name': '어둠의 장막', 'chance': 0.25, 'type': 'debuff', 'effect': {'acc_down': 20, 'duration': 3}}
    ]
},

    '하급 정령[LV 22]': {
    'hp': 250, 'atk': 20, 'gold': 22, 'exp': 70,
    'drops': [('mp 포션', 0.1)],
    'skills': [
        {'name': '바람의 돌진', 'chance': 0.25, 'type': 'attack', 'power': 1.3}
    ]
},
'중급 정령[LV 43]': {
    'hp': 750, 'atk': 50, 'gold': 55, 'exp': 200,
    'drops': [('정령의 반지', 0.15)],
    'skills': [
        {'name': '바람의 칼날', 'chance': 0.3, 'type': 'attack', 'power': 1.4}
    ]
},
'상급 정령 리베라[LV 48]': {
    'hp': 1000, 'atk': 68, 'gold': 180, 'exp': 350,
    'drops': [('스킬북:바람', 0.05)],
    'skills': [
        {'name': '폭풍의 포효', 'chance': 0.3, 'type': 'aoe', 'power': 1.5},
        {'name': '회오리', 'chance': 0.25, 'type': 'status',
         'status': {'name': '기절', 'duration': 1, 'dmg_per_turn': 0}}
    ]
},
'엘프 궁수[LV 36]': {
    'hp': 600, 'atk': 40, 'gold': 45, 'exp': 160,
    'drops': [('엘프의 활', 0.15)],
    'skills': [
        {'name': '더블 샷', 'chance': 0.3, 'type': 'attack', 'power': 1.5}
    ]
},
'엘프 대전사 티타니아[LV 42]': {
    'hp': 850, 'atk': 55, 'gold': 120, 'exp': 260,
    'drops': [('바람 갑옷', 1)],
    'skills': [
        {'name': '정의의 일격', 'chance': 0.3, 'type': 'attack', 'power': 1.6},
        {'name': '자연의 가호', 'chance': 0.2, 'type': 'buff', 'effect': {'def_up': 10, 'duration': 3}}
    ]
},
'안개 돌연변이[LV 28]': {
    'hp': 400, 'atk': 28, 'gold': 32, 'exp': 100,
    'drops': [],
    'skills': [
        {'name': '안개 베기', 'chance': 0.25, 'type': 'attack', 'power': 1.3}
    ]
},
'안개 속의 심연 트레스티안[LV 95]': {
    'hp': 3500, 'atk': 150, 'gold': 1200, 'exp': 2500,
    'drops': [('안개걸음', 1)],
    'skills': [
        {'name': '어둠의 숨결', 'chance': 0.3, 'type': 'aoe_status',
         'status': {'name': '저주', 'duration': 3, 'dmg_per_turn': 10}, 'power': 1.3},
        {'name': '그림자 폭풍', 'chance': 0.25, 'type': 'lifesteal', 'power': 1.3, 'heal_ratio': 0.4}
    ]
},
    }
region_monsters = {
    '숲속': ['슬라임[LV 1]', '늑대[LV 4]'],
    '동굴': ['독 도마뱀[LV 9]', '코볼트[LV 6]', '흡혈 박쥐[LV 8]'],
    '오크 부락': ['오크 전사[LV 16]', '오크 주술사[LV 20]'],
    '태산 지대': ['태산의 지배자 트리톤[LV 40]', '스톤 보어[LV 33]'],
    '해변가': ['모래게[LV 13]', '바다 갈매기[LV 10]'],
    '해안가': ['물총새[LV 39]', '턱상어[LV 37]'],
    '심해': ['바다의 악몽 세이렌[LV 70]', '매혹적인 인어[LV 62]'],
    '심연의 공포': ['심연의 공포 메갈로돈[LV 80]'],
    '용의 둥지': ['용감한 용인 전사[LV 58]', '천공의 지배자인 바다용 아퀼로[LV ???]'],
    '협곡': ['딱딱이[LV 24]', '돌돌이[LV 21]'],
    '괴조 서식지': ['괴조들의 왕 쿠퍼[LV 53]', '괴조[LV 48]'],
    '동굴 거미 서식지': ['거미들의 여왕 베로니카[LV 60]', '동굴 거미[LV 51]'],
    '깊은 심연': ['깊은 그림자 어둑시니[LV 90]'],
    '비밀의 숲': [],
    '엘프들의 마을': ['엘프 대전사 티타니아[LV 42]', '엘프 궁수[LV 36]'],
    '정령 서식지': ['상급 정령 리베라[LV 48]', '중급 정령[LV 43]', '하급 정령[LV 22]'],
    '미지의 안개숲' : ['안개 돌연변이[LV 28]'],
    '미지의 심연': ['안개 속의 심연 트레스티안[LV 95]'],
    '보물방': ['미믹[LV 14]'],

}

defeat_once_targets = ['태산의 지배자 트리톤[LV 40]', '바다의 악몽 세이렌[LV 70]', '심연의 공포 메갈로돈[LV 80]', '천공의 지배자인 바다용 아퀼로[LV ???]', '괴조들의 왕 쿠퍼[LV 53]', '거미들의 여왕 베로니카[LV 60]', '깊은 그림자 어둑시니[LV 90]', '엘프 대전사 티타니아[LV 42]', '상급 정령 리베라[LV 48]', '안개 속의 심연 트레스티안[LV 95]']


defeated_once = set()

#배울 수 있는 스킬 종류
skill_templates = {
    '파이어볼': {
        'mp_cost': 12,
        'desc': '적에게 불덩이를 날려 화상과 함께 강한 피해를 준다',
        'action': lambda user, target: target.update({
            'hp': target['hp'] - 70 
        })
    },
    '돌풍 베기': {
        'mp_cost': 15,
        'desc': '빠른 회전 공격으로 강력한 물리 피해를 준다',
        'action': lambda user, target: target.update({
            'hp': target['hp'] - 90  
        })
    },
    '지진': {
        'mp_cost': 20,
        'desc': '대지를 뒤흔들어 전체 적에게 피해와 기절을 입힌다',
        'action': lambda user, target: target.update({
            'hp': target['hp'] - 80,
            'status': {'name': '기절', 'duration': 1}
        })
    },
    '수룡탄': {
        'mp_cost': 25,
        'desc': '물의 정령이 담긴 탄환을 발사해 강력한 피해를 준다',
        'action': lambda user, target: target.update({
            'hp': target['hp'] - 150  
        })
    },
    '그림자베기': {
        'mp_cost': 30,
        'desc': '그림자의 힘으로 적을 벤다. 체력, 방어력, 공격력을 흡수한다',
        'action': lambda user, target: (
            target.update({'hp': target['hp'] - 120}),
            user.update({
                'hp': min(user['hp'] + 30, user['base_hp']),
                'base_atk': user['base_atk'] + 1,
                'base_def': user['base_def'] + 1
            })
        )
    },
    '흡혈': {
        'mp_cost': 12,
        'desc': '적에게 피해를 주며 입힌 피해의 절반만큼 체력을 회복한다',
        'action': lambda user, target: (
            target.update({'hp': target['hp'] - 60}),
            user.update({'hp': min(user['hp'] + 30, user['base_hp'])})
        )
    },
    '힐': {
        'mp_cost': 10,
        'desc': '자신의 체력을 회복한다',
        'action': lambda user, target: user.update({
            'hp': min(user['hp'] + 100, user['base_hp'])
        })
    },
    '탈피': {
        'mp_cost': 20,
        'desc': '자신의 체력과 마나를 일정량 회복한다',
        'action': lambda user, target: user.update({
            'hp': min(user['hp'] + 150, user['base_hp']),
            'mp': min(user['mp'] + 30, user['base_mp'])
        })
    },
    '바람': {
        'mp_cost': 12,
        'desc': '바람의 힘을 빌려 3턴 동안 방어력을 30% 증가시킨다',
        'action': lambda user, target: user.update({
            'status': {'name': '방어력 증가', 'duration': 3, 'buff_def': 1.3}
        })
    },
    '마나의 가호': {
        'mp_cost': 0,
        'desc': '자신의 마나를 40 회복한다',
        'action': lambda user, target: user.update({
            'mp': min(user['mp'] + 40, user['base_mp'])
        })
    },
    '맹독': {
        'mp_cost': 10,
        'desc': '적에게 독을 부여해 3턴 동안 지속 피해를 준다',
        'action': lambda user, target: target.update({
            'status': {'name': '중독', 'duration': 3, 'dmg_per_turn': 20}
        })
    },
    '맹독폭발': {
        'mp_cost': 20,
        'desc': '적을 독으로 오염시킨 후 폭발시켜 큰 피해를 준다',
        'action': lambda user, target: (
            target.update({'hp': target['hp'] - 80}),
            target.update({'status': {'name': '중독', 'duration': 4, 'dmg_per_turn': 25}})
        )
    },
    '울부짖기': {
        'mp_cost': 15,
        'desc': '적을 위협해 1턴 동안 기절시킨다',
        'action': lambda user, target: target.update({
            'status': {'name': '기절', 'duration': 1}
        })
    },
    '폭풍참': {
        'mp_cost': 18,
        'desc': '연속적인 바람 공격으로 3턴 동안 지속 피해를 준다',
        'action': lambda user, target: target.update({
            'status': {'name': '출혈', 'duration': 3, 'dmg_per_turn': 40}
        })
    }
}
#레벨업 + 스텟 상승
def exp_to_next(level):
    return 50 + (level - 1) * 25

def recalc_stats():
    # --- 기본 능력치 초기화 ---
    player['base_atk'] = player.get('base_atk', 10)
    player['base_def'] = player.get('base_def', 5)
    player['atk'] = player['base_atk']
    player['def'] = player['base_def']

    old_max_hp = player.get('max_hp', player.get('base_hp', 100))
    old_max_mp = player.get('max_mp', player.get('base_mp', 50))

    player['max_hp'] = player.get('base_hp', player.get('hp', 100))
    player['max_mp'] = player.get('base_mp', player.get('mp', 50))

    # --- 장비 확인 ---
    equip_dict = player.get('equip', {})
    if not isinstance(equip_dict, dict):
        equip_dict = {'무기': None, '갑옷': None, '신발': None}
        player['equip'] = equip_dict

    # --- 장비 효과 적용 ---
    for slot, item_name in equip_dict.items():
        if not item_name:
            continue
        stats = item_stats.get(item_name)
        if not stats:
            continue
        player['atk'] += stats.get('atk', 0)
        player['def'] += stats.get('def', 0)
        player['max_hp'] += stats.get('max_hp', 0)
        player['max_mp'] += stats.get('max_mp', 0)

    # --- ✅ HP/MP 보정 ---
    # 체력 및 마나 최대치가 변동되었을 때 조정
    if 'hp' not in player:
        player['hp'] = player['max_hp']
    if 'mp' not in player:
        player['mp'] = player['max_mp']

    # HP가 최대 체력을 초과하지 않게 제한
    if player['hp'] > player['max_hp']:
        player['hp'] = player['max_hp']
    # HP 상승 반영 (장비로 HP가 늘어나면 회복)
    elif player['max_hp'] > old_max_hp:
        diff = player['max_hp'] - old_max_hp
        player['hp'] += diff
        if player['hp'] > player['max_hp']:
            player['hp'] = player['max_hp']

    # MP도 동일하게 처리
    if player['mp'] > player['max_mp']:
        player['mp'] = player['max_mp']
    elif player['max_mp'] > old_max_mp:
        diff = player['max_mp'] - old_max_mp
        player['mp'] += diff
        if player['mp'] > player['max_mp']:
            player['mp'] = player['max_mp']

def gain_exp(amount):
    """경험치 획득 및 자동 레벨업 처리"""
    player['exp'] += amount
    print(f"✨ {amount} 경험치를 획득했습니다!")

    while player['exp'] >= exp_to_next(player['level']):
        player['exp'] -= exp_to_next(player['level'])
        player['level'] += 1
        player['base_hp'] += 10
        player['base_mp'] += 5
        player['base_atk'] += 2
        player['base_def'] += 1
        player['hp'] = player['base_hp']
        player['mp'] = player['base_mp']
        print(f"🎉 레벨 업! 현재 레벨: {player['level']} (HP/MP/능력치 상승)")

#몬스터 드랍 템

def handle_drops(monster_name, monster):
    drops = monster.get('drops', [])
    for drop in drops:
        # 1️⃣ 드랍 데이터 형태가 (아이템, 확률)인 경우
        if isinstance(drop, tuple):
            item, chance = drop
            if random.random() >= chance:
                continue  # 확률 미달 시 스킵
        else:
            # 2️⃣ 문자열만 있는 경우 (확정 드랍)
            item = drop

        print(f"🎁 {monster_name}이(가) '{item}'을(를) 드랍했습니다!")

        # 3️⃣ 스킬북 처리
        if item.startswith('스킬북: '):
            skill_name = item.replace('스킬북: ', '').strip()
            if skill_name not in player['skills']:
                player['skills'].append(skill_name)
                print(f"📘 '{skill_name}' 스킬북을 사용했습니다! 새로운 스킬 '{skill_name}'을(를) 배웠습니다.")
            else:
                print(f"이미 '{skill_name}' 스킬을 알고 있어서 스킬북은 사라졌습니다.")
        else:
            player['inventory'].append(item)
            print(f"🎒 '{item}'이(가) 인벤토리에 추가되었습니다.")
#상태이상
def apply_status_effects(entity, name_for_print=""):
    """매 턴 상태이상 처리: entity는 dict, 상태 리스트는 [{'name','duration','dmg_per_turn' optional}]"""
    new_status = []
    if 'status' not in entity:
        entity['status'] = []

    for s in entity['status']:
        effect_name = s['name']
        duration = s['duration']
        dmg = s.get('dmg_per_turn', 0)

        if effect_name == '화상':
            entity['hp'] -= dmg
            print(f"{name_for_print}이(가) 🔥화상으로 {dmg}의 피해를 입었습니다! (남은 지속: {duration-1})")

        elif effect_name == '중독':
            entity['hp'] -= dmg
            print(f"{name_for_print}이(가) ☠중독으로 {dmg}의 피해를 입었습니다! (남은 지속: {duration-1})")

        elif effect_name == '저주':
            entity['hp'] -= dmg
            print(f"{name_for_print}이(가) 💀저주로 {dmg}의 피해를 입었습니다! (남은 지속: {duration-1})")

        elif effect_name == '출혈':
            entity['hp'] -= dmg
            print(f"{name_for_print}이(가) 💢출혈로 {dmg}의 피해를 입었습니다! (남은 지속: {duration-1})")

        elif effect_name == '기절':
            entity['can_act'] = False
            print(f"{name_for_print}이(가) 😵기절하여 이번 턴 행동할 수 없습니다! (남은 지속: {duration-1})")

        elif effect_name == '매혹':
            entity['can_act'] = False
            print(f"{name_for_print}이(가) 💫매혹 상태로 정신을 잃었습니다! (남은 지속: {duration-1})")

        elif effect_name == '방어력 증가':
            if not s.get('applied', False):
                entity['base_def'] = int(entity.get('base_def', 0) * s.get('buff_def', 1.3))
                s['applied'] = True
                print(f"{name_for_print}의 🛡방어력이 상승했습니다! (지속: {duration})")

        elif effect_name == '공격력 증가':
            if not s.get('applied', False):
                entity['base_atk'] = int(entity.get('base_atk', 0) * s.get('buff_atk', 1.3))
                s['applied'] = True
                print(f"{name_for_print}의 ⚡공격력이 상승했습니다! (지속: {duration})")

        elif effect_name == '방어력 감소':
            if not s.get('applied', False):
                entity['base_def'] = int(entity.get('base_def', 0) * 0.8)
                s['applied'] = True
                print(f"{name_for_print}의 🧩방어력이 감소했습니다! (지속: {duration})")

        elif effect_name == '공격력 감소':
            if not s.get('applied', False):
                entity['base_atk'] = int(entity.get('base_atk', 0) * 0.8)
                s['applied'] = True
                print(f"{name_for_print}의 🧨공격력이 감소했습니다! (지속: {duration})")

        s['duration'] -= 1
        if s['duration'] > 0:
            new_status.append(s)
        else:
            print(f"➡ {effect_name} 효과가 사라졌습니다.")

            if effect_name == '방어력 증가' and s.get('applied', False):
                entity['base_def'] = int(entity.get('base_def', 0) / s.get('buff_def', 1.3))
            elif effect_name == '공격력 증가' and s.get('applied', False):
                entity['base_atk'] = int(entity.get('base_atk', 0) / s.get('buff_atk', 1.3))
            elif effect_name == '방어력 감소' and s.get('applied', False):
                entity['base_def'] = int(entity.get('base_def', 0) / 0.8)
            elif effect_name == '공격력 감소' and s.get('applied', False):
                entity['base_atk'] = int(entity.get('base_atk', 0) / 0.8)

    # 결과 반영
    entity['status'] = new_status
    if not any(s['name'] == '기절' for s in new_status) and not any(s['name'] == '매혹' for s in new_status):
        entity['can_act'] = True

#인벤토리, 휴식, 상점
def show_inventory():
    print("\n🎒 [인벤토리]")
    print(f"레벨: {player.get('level',1)} | EXP: {player.get('exp',0)}/{exp_to_next(player.get('level',1))}")
    # 착용 중 장비 표시
    equip_lines = []
    for slot, itm in player.get('equip', {}).items():
        equip_lines.append(f"{slot}: {itm or '없음'}")
    print("착용 중 장비: " + ", ".join(equip_lines))
    print(f"보유 장비 및 소비품: {', '.join(player.get('inventory', []))}")
    print(f"HP: {player['hp']} / {player['max_hp']} | MP: {player['mp']} / {player['max_mp']}")
    print(f"공격력: {player.get('atk',0)}, 방어력: {player.get('def',0)}")
    print(f"골드: {player.get('gold',0)} G\n")
    if player.get('skills'):
        print("배운 스킬:", ", ".join(player['skills']))
    if player.get('status'):
        print("상태이상:", ", ".join([s['name'] for s in player['status']]))

def rest():
     if player['current_room'] == '마을':
        player['hp'] = player['base_hp']
        player['mp'] = player['base_mp']
        player['status'] = []
        print("\n🏡 마을에서 충분히 휴식했습니다. HP/MP 완전 회복 및 상태이상 해제!\n")
     else:
        healed_hp = min(player['base_hp'] - player['hp'], 40)
        healed_mp = min(player['base_mp'] - player['mp'], 20)
        player['hp'] += healed_hp
        player['mp'] += healed_mp
        player['status'] = []
        print(f"\n🛏️ 휴식을 취했습니다. HP {healed_hp} / MP {healed_mp} 회복, 상태이상 해제!\n")

def shop():
    print("\n💰 상점에 오신 것을 환영합니다!\n")
    for item, price in shop_items.items():
        print(f"- {item}: {price} G")
    choice = input("\n구매할 아이템 이름을 입력하거나 '나가기'를 입력하세요: ")
    if choice == '나가기':
        print("상점을 나갑니다.\n")
        return
    if choice in shop_items:
        price = shop_items[choice]
        if player['gold'] >= price:
            player['gold'] -= price
            player['inventory'].append(choice)
            print(f"{choice}을(를) 구매했습니다! 남은 골드: {player['gold']} G\n")
        else:
            print("골드가 부족합니다!\n")
    else:
        print("존재하지 않는 아이템입니다.\n")

#아이템 착용

def equip_item():
    if not player.get('inventory'):
        print("🎒 보유한 아이템이 없습니다.")
        return

    print("\n⚔️ 착용할 아이템을 입력하세요 (보유 장비 목록):")
    print("보유 장비:", ", ".join(player['inventory']))
    choice = input(">>> ").strip()

    if choice not in player['inventory']:
        print("❌ 해당 아이템을 보유하고 있지 않습니다.")
        return

    stats = item_stats.get(choice)
    if not stats:
        print("❌ 이 아이템은 착용 가능한 장비가 아닙니다. (소비품일 수 있음)")
        return

    slot = stats.get('slot')
    if not slot:
        print("❌ 이 아이템에 slot 정보가 없습니다.")
        return

    # 같은 슬롯 장비가 이미 있으면 인벤토리로 환원
    prev_item = player['equip'].get(slot)
    if prev_item:
        print(f"기존 {slot} 장비 '{prev_item}'을(를) 벗겼습니다. 인벤토리에 반환됩니다.")
        player['inventory'].append(prev_item)

    # 선택 장비를 슬롯에 장착, 인벤토리에서 제거
    player['equip'][slot] = choice
    player['inventory'].remove(choice)
    recalc_stats()
    print(f"✅ {choice}을(를) [{slot}]에 착용했습니다.")


#전투
def use_item_in_battle():
    print("사용 가능한 소비 아이템:", [i for i in player['inventory'] if i in consumables])
    it = input("사용할 아이템 입력 (취소: 나가기): ")
    if it == '나가기':
        return
    if it in player['inventory'] and it in consumables:
        if it == 'hp 포션':
            healed = min(50, player['base_hp'] - player['hp'])
            player['hp'] = min(player['hp'] + 50, player['base_hp'])
            player['inventory'].remove(it)
            print(f"HP를 {healed} 회복했습니다. (현재 HP: {player['hp']})")
        elif it == 'mp 포션':
            player['mp'] = min(player['mp'] + 30, player['base_mp'])
            player['inventory'].remove(it)
            print(f"MP를 30 회복했습니다. (현재 MP: {player['mp']})")
        elif it == '상태이상 약':
            player['status'] = []
            player['inventory'].remove(it)
            print("모든 상태이상 해제!")
    else:
        print("사용 불가하거나 인벤토리에 없습니다.")

def use_skill_in_battle(skill_name, monster):
    if skill_name not in player['skills']:
        print("해당 스킬을 배우지 않았습니다.")
        return False
    sk = skill_templates.get(skill_name)
    if not sk:
        print("스킬 템플릿이 없습니다.")
        return False
    if player['mp'] < sk['mp_cost']:
        print("MP가 부족합니다.")
        return False
    # 스킬 사용
    player['mp'] -= sk['mp_cost']
    sk['action'](player, monster)
    print(f"스킬 {skill_name} 사용! {sk['desc']}")
    return True
#전투 함수
def battle(monster_name, monster):
    monster = copy.deepcopy(monster)  # 원본 훼손 방지
    print(f"\n⚔️ {monster_name}이(가) 나타났다!\n")

    if 'status' not in monster:
        monster['status'] = []

    # 전투 루프
    while monster['hp'] > 0 and player['hp'] > 0:
        apply_status_effects(player, "당신")
        apply_status_effects(monster, monster_name)

        if player['hp'] <= 0 or monster['hp'] <= 0:
            break

        print(f"\n당신 HP: {player['hp']} | {monster_name} HP: {monster['hp']}")
        action = input("행동 선택 (공격 / 스킬 / 아이템 / 도망): ")

        if action == '공격':
            damage = max(1, player['atk'] - random.randint(0, 3))
            monster['hp'] -= damage
            print(f"{monster_name}에게 {damage}의 피해를 입혔습니다!")

        elif action == '스킬':
            if not player['skills']:
                print("배운 스킬이 없습니다.")
                continue
            print("사용 가능한 스킬:", ", ".join(player['skills']))
            s_choice = input("사용할 스킬 이름 입력: ")
            used = use_skill_in_battle(s_choice, monster)
            if not used:
                continue

        elif action == '아이템':
            use_item_in_battle()

        elif action == '도망':
            if random.random() < 0.5:
                print("🏃‍♂️ 도망쳤습니다!")
                return
            else:
                print("도망 실패!")

        else:
            print("잘못된 입력입니다.")
            continue

        # 몬스터 턴
        if monster['hp'] > 0:
            used_skill = False
            for sk in monster.get('skills', []):
                if random.random() < sk.get('chance', 0):
                    if sk['type'] == 'status':
                        player.setdefault('status', []).append(sk['status'].copy())
                        print(f"{monster_name}이(가) {sk['name']}을(를) 사용했습니다! ({sk['status']['name']} 상태)")
                    used_skill = True
                    break
            if not used_skill:
                m_damage = max(1, monster['atk'] - player['def'])
                player['hp'] -= m_damage
                print(f"{monster_name}이(가) 당신에게 {m_damage}의 피해를 입혔습니다!")

    # ===== 전투 종료 처리 =====
    if player['hp'] <= 0:
        print("💀 당신은 쓰러졌습니다... 게임 오버!")
        sys.exit()

    # 몬스터 처치 성공 시
    print(f"\n🎉 {monster_name}을(를) 물리쳤습니다!")
    print(f"💰 골드 +{monster.get('gold',0)} | 경험치 +{monster.get('exp',0)}")

    player['gold'] += monster.get('gold', 0)
    gain_exp(monster.get('exp', 0))
    handle_drops(monster_name, monster)

    # 1회성 몬스터 처리
    if monster_name in defeat_once_targets:
        defeated_once.add(monster_name)
#지역별 진입 이벤트
def on_enter_room(room):
    """방 입장 시 발동 이벤트 (보물방, 낭떠러지, 절벽 NPC 등)"""
    if room == '보물방':
        print("✨ 보물방에 들어왔습니다. 희귀 스킬을 발견할 확률이 있습니다...")
        if random.random() < 0.4:
            if '힐' not in player['skills']:
                player['skills'].append('힐')
                print("🌿 신비한 힘이 몸을 감싸며, 스킬 '힐'을 얻었습니다!")
            else:
                print("이미 힐 스킬을 알고 있습니다.")
        else:
            print("아쉽게도 아무 일도 일어나지 않았습니다.")
    elif room == '낭떠러지':
        print("⚠️ 낭떠러지에 접근했습니다. 발을 헛디디면 큰일 날 수 있습니다...")
        if random.random() < 0.25:
            print("발을 헛디뎌 낭떠러지로 떨어졌습니다... 회생 불가.")
            sys.exit()
        else:
            print("간신히 균형을 잡고 지나갔습니다.")
    elif room == '돌풍 절벽':
        print("🌀 돌풍 절벽의 현자가 당신을 주시합니다...")
        if random.random() < 0.5:
            print("현자가 바람의 기술을 가르쳐줍니다! 스킬 '돌풍 베기'를 배웠습니다.")
            if '돌풍 베기' not in player['skills']:
                player['skills'].append('돌풍 베기')
        else:
            print("현자는 오늘은 가르쳐주지 않습니다.")
    elif room == '무너진 동굴':
        print("💀 무너진 동굴에 들어섰습니다. 공기가 탁하고 불안한 기운이 감돕니다...")
        if random.random() < 0.7:
            print("천장이 무너졌습니다! 돌더미에 깔려 사망했습니다...")
            sys.exit()
        else:
            print("간신히 무너진 틈새를 빠져나왔습니다. 당신은 살아남았습니다!")

    elif room == '마법사의 동굴':
        print("🔮 신비한 마법의 기운이 느껴집니다. 한 노마법사가 나타납니다.")
        print("마법사: '500G만 주면 강력한 화염 마법을 가르쳐주지.'")
        if player['gold'] >= 500:
            choice = input("500G를 지불하고 '파이어볼'을 배우겠습니까? (Y/N): ").strip().lower()
            if choice == 'y':
                player['gold'] -= 500
                if '파이어볼' not in player['skills']:
                    player['skills'].append('파이어볼')
                    print("🔥 파이어볼 스킬을 배웠습니다!")
                else:
                    print("이미 파이어볼 스킬을 알고 있습니다.")
            else:
                print("당신은 거래를 거절했습니다.")
        else:
            print("💸 골드가 부족합니다. (500G 필요)")
    elif room == '용궁':
        print("🐉 용궁에 들어섰습니다. 용왕이 당신을 맞이합니다.")
        if '심해의 조각' in player['inventory']:
            choice = input("용왕: '심해의 조각을 바치면 심해의 공포를 주마.' 바치겠습니까? (Y/N): ").strip().lower()
            if choice == 'y':
                player['inventory'].remove('심해의 조각')
                if '심해의 공포' not in player['inventory']:
                    player['inventory'].append('심해의 공포')
                    print("⚔️ '심해의 공포'를 획득했습니다!")
                else:
                    print("이미 '심해의 공포'를 보유 중입니다.")
            else:
                print("용왕은 고개를 끄덕이며 당신을 보냅니다.")
        else:
            print("용왕: '심해의 조각이 없구나... 돌아가거라.'")

    elif room == '천역':
        print("☁️ 천역에 도달했습니다. 천공의 수호자가 당신을 바라봅니다.")
        if '심연의 조각' in player['inventory']:
            choice = input("수호자: '심연의 조각을 바치면 심연의 갑옷을 주지.' 바치겠습니까? (Y/N): ").strip().lower()
            if choice == 'y':
                player['inventory'].remove('심연의 조각')
                if '심연의 갑옷' not in player['inventory']:
                    player['inventory'].append('심연의 갑옷')
                    print("🛡️ '심연의 갑옷'을 획득했습니다!")
                else:
                    print("이미 '심연의 갑옷'을 보유 중입니다.")
            else:
                print("수호자는 고요히 당신을 떠나보냅니다.")
        else:
            print("수호자: '심연의 조각이 없구나... 돌아가거라.'")

    else:
        print(f"📍 {room}에 입장했습니다.")

def explore():
    """탐험 로직 — 마을 제외, 지역 몬스터 조우"""
    global defeated_once
    current_room = player['current_room']

    if current_room == '마을':
        print("🏡 마을에서는 전투가 발생하지 않습니다.\n")
        return

    print(f"\n📍 현재 위치: {current_room}")
    candidates = region_monsters.get(current_room, [])

    # 1회성 몬스터 필터링
    available = [m for m in candidates if m not in defeated_once]

    if not available:
        print("이 지역의 모든 몬스터를 이미 정복했습니다.\n")
    elif random.random() < 0.6:  # 전투 확률
        monster_name = random.choice(available)
        monster = monsters[monster_name]
        battle(monster_name, monster)
    else:
        print("🌿 조용히 탐험을 마쳤습니다. 아무 일도 일어나지 않았습니다.\n")


# 이동 선택
    if current_room in rooms and rooms[current_room]:
        print("이동 가능한 방향:")
        for direction, room in rooms[current_room].items():
            print(f" - {direction} → {room}")
        move = input("이동할 방향을 입력하세요 (예: north, east, west, south / 취소: return): ")
        if move == 'return':
            return
        if move in rooms[current_room]:
            player['current_room'] = rooms[current_room][move]
            print(f"\n🚶‍♂️ {rooms[current_room][move]}(으)로 이동했습니다!\n")
            on_enter_room(player['current_room'])
        else:
            print("🚫 그 방향으로는 이동할 수 없습니다.\n")
    else:
        print("이 지역은 이동 가능한 방향이 없습니다.\n")

def area_menu():
    """마을 이외 지역용 메뉴"""
    while True:
        current_room = player['current_room']
        print(f"\n📍 현재 위치: {current_room}")
        print("무엇을 하시겠습니까?")
        print("① 탐험  ② 휴식  ③ 이동  ④ 인벤토리  ⑤ 마을로 귀환")

        choice = input("선택: ")
        if choice == '1' or choice == '탐험':
            explore()
        elif choice == '2' or choice == '휴식':
            rest()
        elif choice == '3' or choice == '이동':
            move_between_rooms()
        elif choice == '4' or choice == '인벤토리':
            show_inventory()
        elif choice == '5' or choice == '마을':
            player['current_room'] = '마을'
            print("\n🏡 마을로 귀환했습니다.\n")
            return
        else:
            print("잘못된 입력입니다.")
def move_between_rooms():
    """방 이동 로직"""
    current_room = player['current_room']
    if current_room in rooms and rooms[current_room]:
        print("이동 가능한 방향:")
        for direction, room in rooms[current_room].items():
            print(f" - {direction} → {room}")
        move = input("이동할 방향 입력 (return: 취소): ")
        if move == 'return':
            return
        if move in rooms[current_room]:
            player['current_room'] = rooms[current_room][move]
            print(f"\n🚶‍♂️ {rooms[current_room][move]}(으)로 이동했습니다!\n")
            on_enter_room(player['current_room'])
        else:
            print("🚫 그 방향으로는 이동할 수 없습니다.\n")





#메인 루프
recalc_stats()
print("🌍 어드벤처 RPG 시작합니다!")
print("명령어: [휴식], [탐험], [이동], [상점], [착용], [inventory], [skills], [quit]")

while True:
    current_room = player['current_room']

    # 🏡 마을일 때
    if current_room == '마을':
        action = input("\n무엇을 하시겠습니까? (휴식 / 탐험 / 이동 / 상점 / 착용 / inventory / skills / quit): ")
        if action == '휴식':
            rest()
        elif action == '탐험':
            explore()
        elif action == '이동': 
            move_between_rooms()
        elif action == '상점':
            shop()
        elif action == '착용':
            equip_item()
        elif action == 'inventory':
            show_inventory()
        elif action == 'skills':
            print("배운 스킬:", player.get('skills', []))
        elif action == 'quit':
            print("게임을 종료합니다.")
            sys.exit()
        else:
            print("잘못된 입력입니다.")
    
    else:
        area_menu()
