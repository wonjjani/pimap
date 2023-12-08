import matplotlib.pyplot as plt
from pykis import PyKis
from prettytable import PrettyTable
from infor import *

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False


# PyKis 객체 생성
kis = PyKis(
    appkey= apkey(),
    appsecret= apsecre(),
    virtual_account=True,
    realtime=False
)

# 계좌 및 잔고 정보 조회
account = kis.account(kacc())
balance = account.balance_all()

# PrettyTable을 사용하여 표 생성
table = PrettyTable(field_names=[
    '상품명',
    '평가액',
    '투자 성장률',
],
align='r',
)

# 파이 차트에 사용할 데이터
evaluation_amounts = []  # 평가액 리스트를 저장할 리스트
growth_rates = []  # 투자 성장률 리스트를 저장할 리스트

for stock in balance.stocks:
    table.add_row([
        stock.prdt_name,
        f'{stock.evlu_amt:,}원',
        f'{stock.evlu_pfls_rt:.2f}%',
    ])

    # 평가액 및 투자 성장률을 리스트에 추가
    evaluation_amounts.append(stock.evlu_amt)
    growth_rates.append(stock.evlu_pfls_rt)

# PrettyTable을 사용하여 테이블 출력
print(table)

# 파이 차트 그리기
fig, ax = plt.subplots()


outer_wedges, outer_texts, outer_autotexts = ax.pie(growth_rates, labels=[f'{stock.evlu_pfls_rt:.2f}%(투자 성장률)' for stock in balance.stocks],
                                                    autopct='', startangle=90,
                                                    radius=1, wedgeprops=dict(width=0.3, edgecolor='w', linewidth=2),
                                                    colors=plt.cm.viridis(growth_rates))

# 내부 원: 평가액
inner_wedges, inner_texts, inner_autotexts = ax.pie(evaluation_amounts, labels=[f'{stock.evlu_amt:,}원(평가액)' for stock in balance.stocks],
                                                    autopct='', startangle=90,
                                                    radius=0.7, wedgeprops=dict(width=0.3, edgecolor='w', linewidth=2),
                                                    colors=plt.cm.viridis(growth_rates))

# 도넛 차트를 표현하기 위해 중심에 원 추가
centre_circle = plt.Circle((0, 0), 0.5, color='white', linewidth=0.5)
ax.add_patch(centre_circle)

# 그래프 제목 설정
ax.set_title('주식 포트폴리오')

# 그래프 표시
plt.show()
