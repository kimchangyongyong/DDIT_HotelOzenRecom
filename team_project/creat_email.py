from faker import Faker
fake = Faker('ko_KR') # locale 정보 설정
Faker.seed() # 초기 seed 설정

for i in range(4) :
    name = fake.free_email()
    print(name)
    