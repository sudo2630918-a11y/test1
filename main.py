import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬과 전력수요 분석", layout="wide")

st.title("🌆 서울·양평 열섬현상 및 전력수요 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")
power = pd.read_csv("전력수요.csv", encoding="cp949")

# 날짜형 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])
power["일시"] = pd.to_datetime(power["일시"])

# 열 이름 변경
seoul = seoul.rename(columns={"기온(°C)": "서울기온"})
yangpyeong = yangpyeong.rename(columns={"기온(°C)": "양평기온"})

# =====================================================
# 탭 생성
# =====================================================
tab1, tab2 = st.tabs(["🌆 열섬 분석", "⚡ 전력 연결"])

# =====================================================
# 탭1 : 열섬 분석
# =====================================================
with tab1:

    st.header("서울과 양평의 도시 열섬현상")

    # 데이터 병합
    temp = pd.merge(
        seoul[["일시", "서울기온"]],
        yangpyeong[["일시", "양평기온"]],
        on="일시"
    )

    temp["기온차"] = temp["서울기온"] - temp["양평기온"]
    temp["시"] = temp["일시"].dt.hour
    temp["월"] = temp["일시"].dt.month

    # ① 연간 기온 변화
    st.subheader("① 1년간 두 지역 기온 변화")
    st.line_chart(
        temp.set_index("일시")[["서울기온", "양평기온"]]
    )

    # ② 시각별 평균 기온차
    st.subheader("② 시각별 평균 기온차 (서울 - 양평)")
    hour_diff = temp.groupby("시")["기온차"].mean()
    st.bar_chart(hour_diff)

    # ③ 월별 평균 기온차
    st.subheader("③ 월별 평균 기온차 (서울 - 양평)")
    month_diff = temp.groupby("월")["기온차"].mean()
    st.bar_chart(month_diff)

# =====================================================
# 탭2 : 전력 연결
# =====================================================
with tab2:

    st.header("서울 기온과 전력수요의 관계")

    # 데이터 병합
    energy = pd.merge(
        seoul[["일시", "서울기온"]],
        power,
        on="일시"
    )

    energy["월"] = energy["일시"].dt.month

    # 기온 구간 생성 (5℃ 간격)
    bins = [-30, -20, -10, 0, 10, 20, 30, 40]
    labels = [
        "-20~-10",
        "-10~0",
        "0~10",
        "10~20",
        "20~30",
        "30~40",
        "40이상"
    ]

    energy["기온구간"] = pd.cut(
        energy["서울기온"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    # ① 산점도
    st.subheader("① 서울 기온과 전력수요 산점도")

    scatter = energy.rename(columns={
        "서울기온": "x",
        "전력수요(MWh)": "y"
    })

    st.scatter_chart(scatter, x="x", y="y")

    # ② 기온 구간별 평균 전력수요
    st.subheader("② 기온 구간별 평균 전력수요")

    temp_power = (
        energy.groupby("기온구간", observed=False)["전력수요(MWh)"]
        .mean()
    )

    st.bar_chart(temp_power)

    # ③ 월별 평균 전력수요
    st.subheader("③ 월별 평균 전력수요")

    month_power = (
        energy.groupby("월")["전력수요(MWh)"]
        .mean()
    )

    st.bar_chart(month_power)
