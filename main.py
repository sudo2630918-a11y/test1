import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상 분석", layout="wide")

st.title("🌆 서울과 양평의 도시 열섬현상 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")

# 날짜형으로 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])

# 열 이름 변경
seoul = seoul.rename(columns={"기온(°C)": "서울기온"})
yangpyeong = yangpyeong.rename(columns={"기온(°C)": "양평기온"})

# 필요한 열만 선택 후 병합
df = pd.merge(
    seoul[["일시", "서울기온"]],
    yangpyeong[["일시", "양평기온"]],
    on="일시"
)

# 기온 차 계산
df["기온차"] = df["서울기온"] - df["양평기온"]

# 시간, 월 정보 추가
df["시"] = df["일시"].dt.hour
df["월"] = df["일시"].dt.month

# -----------------------------
# ① 연간 기온 변화
# -----------------------------
st.header("① 2025년 서울과 양평의 기온 변화")

line_data = df.set_index("일시")[["서울기온", "양평기온"]]
st.line_chart(line_data)

# -----------------------------
# ② 시각별 평균 기온차
# -----------------------------
st.header("② 시각별 평균 기온차 (서울 - 양평)")

hour_mean = (
    df.groupby("시")["기온차"]
    .mean()
    .sort_index()
)

st.bar_chart(hour_mean)

# -----------------------------
# ③ 월별 평균 기온차
# -----------------------------
st.header("③ 월별 평균 기온차 (서울 - 양평)")

month_mean = (
    df.groupby("월")["기온차"]
    .mean()
    .sort_index()
)

st.bar_chart(month_mean)

# -----------------------------
# 요약 통계
# -----------------------------
st.header("📊 요약")

st.write(f"연평균 기온차 (서울 - 양평): **{df['기온차'].mean():.2f}℃**")
st.write(f"최대 기온차: **{df['기온차'].max():.2f}℃**")
st.write(f"최소 기온차: **{df['기온차'].min():.2f}℃**")
