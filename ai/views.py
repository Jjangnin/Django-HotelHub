from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rooms.models import Room
from openai import OpenAI

# OpenAI 클라이언트 생성 (settings에 저장한 키 사용)
client = OpenAI(api_key=getattr(settings, "OPENAI_API_KEY", None))


@login_required
def recommend(request):
    """
    인원 / 예산 / 분위기를 입력받아서
    1) DB에서 조건에 맞는 객실 필터링
    2) OpenAI로 추천 문구 생성
    -> 모두 ai/recommend.html 템플릿에서 보여줌
    """
    suggestion_text = None
    recommended_rooms = []

    if request.method == "POST":
        # 폼 값 읽기
        guests_raw = request.POST.get("guests") or "1"
        budget_raw = request.POST.get("budget") or ""
        mood = (request.POST.get("mood") or "").strip()

        # 숫자 변환 (예외 처리)
        try:
            guests = int(guests_raw)
        except ValueError:
            guests = 1

        try:
            budget = int(budget_raw) if budget_raw else 0
        except ValueError:
            budget = 0

        # 1) DB에서 조건 맞는 객실 필터링
        qs = Room.objects.filter(is_available=True, capacity__gte=guests)
        if budget > 0:
            qs = qs.filter(price_per_night__lte=budget)

        recommended_rooms = list(qs.order_by("price_per_night"))

        if not recommended_rooms:
            # 조건에 맞는 방이 없을 때
            suggestion_text = "조건에 맞는 예약 가능한 객실이 없습니다. 인원이나 예산 조건을 조정해 보세요."
        else:
            # AI에게 보낼 객실 리스트 문자열로 만들기
            room_lines = []
            for r in recommended_rooms:
                line = (
                    f"- 방번호 {r.number}: {r.name}, "
                    f"정원 {r.capacity}명, 1박 {r.price_per_night}원, "
                    f"카테고리 {r.get_category_display()}"
                )
                room_lines.append(line)
            room_desc = "\n".join(room_lines)

            prompt = f"""
다음은 한 호텔의 객실 목록입니다:

{room_desc}

고객 조건:
- 인원: {guests}명
- 1박 예산: {"제한 없음" if budget == 0 else str(budget) + "원 이하"}
- 원하는 분위기: {mood or "특별히 없음"}

위 조건에 가장 잘 맞는 객실 1~3개를 골라서,
고객에게 이해하기 쉬운 한국어로 추천해 주세요.

형식:
1. 어떤 방이 왜 좋은지 간단 설명
2. 예산/인원/분위기 측면에서 장점
3. 필요하면 대안 방도 1~2개 정도 제안
"""

            try:
                if client.api_key:
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "너는 호텔 객실을 추천해주는 한국어 상담원이다.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                    )
                    suggestion_text = resp.choices[0].message.content.strip()
                else:
                    suggestion_text = (
                        "AI API 키가 설정되어 있지 않아 기본 추천만 표시합니다."
                    )
            except Exception as e:
                suggestion_text = f"AI 추천 중 오류가 발생했습니다: {e}"

    return render(
        request,
        "ai/recommend.html",   
        {
            "suggestion_text": suggestion_text,
            "recommended_rooms": recommended_rooms,
        },
    )
