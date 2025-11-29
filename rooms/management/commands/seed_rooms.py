from django.core.management.base import BaseCommand
from rooms.models import Room, Amenity
from random import randint, choice, sample

class Command(BaseCommand):
    help = "Seed amenities and many rooms"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding amenities..."))
        amenity_names = [
            "와이파이","TV","욕조","샤워부스","에어컨","난방","주차장",
            "수영장","피트니스","사우나","조식","바다뷰","도시뷰","책상","헤어드라이어"
        ]
        amenities = []
        for n in amenity_names:
            a, _ = Amenity.objects.get_or_create(name=n)
            amenities.append(a)
        self.stdout.write(self.style.SUCCESS(f"Amenities ready: {len(amenities)}"))

        self.stdout.write(self.style.WARNING("Seeding rooms (300)..."))
        categories = [c[0] for c in Room.CATEGORY_CHOICES]
        created = 0
        for i in range(1, 301):
            number = f"{i:04d}"  # 0001 ~ 0300
            name = f"객실 {number}"
            category = choice(categories)
            capacity = {
                "single": 1, "double": 2, "twin": 2, "family": randint(3,5), "suite": randint(2,4)
            }[category]
            price = {
                "single": randint(60000,90000),
                "double": randint(80000,130000),
                "twin": randint(90000,140000),
                "family": randint(120000,200000),
                "suite": randint(180000,350000),
            }[category]
            desc_tokens = [
                "조용한","채광 좋은","방음 우수","업무용 책상","오션뷰","도시뷰",
                "넓은 욕조","청결한 침구","무료 주차","지하철 인접","고속 와이파이"
            ]
            desc = " ".join(sample(desc_tokens, k=3))

            room, created_flag = Room.objects.get_or_create(
                number=number,
                defaults={
                    "name": name,
                    "category": category,
                    "capacity": capacity,
                    "price_per_night": price,
                    "description": desc,
                    "is_available": choice([True, True, True, False]),  # 대체로 가능
                }
            )
            # 편의시설 3~6개 랜덤 연결
            room.amenities.set(sample(amenities, k=randint(3,6)))
            if created_flag:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Rooms created: {created}"))
        self.stdout.write(self.style.SUCCESS("Seeding complete."))
