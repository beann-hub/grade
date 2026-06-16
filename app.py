# app.py -- 우리 반 성적 분석 대시보드 (화면)
import streamlit as st
from utils import (total_score, average_score, to_grade, grade_to_gpa,
                   subject_average, subject_top, grade_distribution,
                   rank_list, pass_rate)

st.set_page_config(page_title="성적 분석 대시보드", layout="wide")

# 프리미엄 디자인을 위한 Custom CSS
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 폰트 설정 */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 메트릭 카드 디자인 */
    div[data-testid="metric-container"] {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px;
        padding: 20px;
        background: rgba(128, 128, 128, 0.03);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease-in-out;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        border-color: #6366f1;
        background: rgba(99, 102, 241, 0.02);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.08);
    }
    
    div[data-testid="stMetricValue"] > div {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    div[data-testid="stMetricLabel"] > div {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
    }
    
    /* 추가 버튼 디자인 */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #2563eb 100%);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
        transform: translateY(-2px);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* 테이블 디자인 */
    .stTable table {
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(128, 128, 128, 0.15) !important;
    }
    
    /* 서브헤더 그라데이션 */
    .gradient-header {
        font-weight: 800;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 상단 배너 이미지 (파이썬 상단 배너 이미지.png 파일을 함께 둘 것)
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
banner_path = os.path.join(current_dir, "파이썬 상단 배너 이미지.png")
if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)
else:
    st.warning("배너 이미지(파이썬 상단 배너 이미지.png) 파일을 찾을 수 없습니다. 스크립트와 동일한 폴더에 위치시켜 주세요.")
st.title("우리 반 성적 분석 대시보드")

SUBJECTS = ["국어", "영어", "수학"]

# 파일 입출력을 통한 데이터 영구 보존
import json
students_file = os.path.join(current_dir, "students.json")
DEFAULT_STUDENTS = [
    {"이름": "김민준", "국어": 92,  "영어": 85, "수학": 78},
    {"이름": "이서연", "국어": 88,  "영어": 90, "수학": 95},
    {"이름": "박도윤", "국어": 60,  "영어": 55, "수학": 72},
    {"이름": "최지우", "국어": 100, "영어": 80, "수학": 90},
    {"이름": "정하준", "국어": 45,  "영어": 60, "수학": 58},
]

def load_students():
    if os.path.exists(students_file):
        try:
            with open(students_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_STUDENTS.copy()
    else:
        save_students(DEFAULT_STUDENTS)
        return DEFAULT_STUDENTS.copy()

def save_students(data):
    try:
        with open(students_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"데이터 저장 중 오류 발생: {e}")

if "students" not in st.session_state:
    st.session_state.students = load_students()

students = st.session_state.students

# --- 상단 요약 지표 ---
col1, col2, col3 = st.columns(3)
col1.metric("응시 인원", f"{len(students)}명")

if students:
    avgs = [average_score(stu) for stu in students]
    overall = sum(avgs) / len(avgs)
    col2.metric("전체 평균", f"{overall:.2f}점")
    col3.metric("합격률", f"{pass_rate(students):.1f}%")
else:
    col2.metric("전체 평균", "0.00점")
    col3.metric("합격률", "0.0%")

# --- 텝 4개 구성 ---
tab1, tab2, tab3, tab4 = st.tabs(["학생 입력", "학생별 성적표", "과목별 통계", "석차학점 분포"])

# --- Tab 1 : 학생 입력 ---
with tab1:
    st.header("학생 추가")
    name = st.text_input("이름", placeholder="예: 홍길동")
    kor = st.number_input("국어", 0, 100, 0, step=5)
    eng = st.number_input("영어", 0, 100, 0, step=5)
    mat = st.number_input("수학", 0, 100, 0, step=5)
    if st.button("추가"):
        if name.strip():
            if any(stu["이름"] == name.strip() for stu in students):
                st.error("이미 존재하는 이름입니다. 다른 이름을 입력해주세요.")
            else:
                new_student = {"이름": name.strip(), "국어": kor, "영어": eng, "수학": mat}
                st.session_state.students.append(new_student)
                save_students(st.session_state.students)
                st.success(f"{name} 학생을 추가했습니다.")
                st.rerun()
        else:
            st.warning("이름을 입력해주세요.")

# --- Tab 2 : 학생별 성적표 ---
with tab2:
    st.header("학생별 성적표")
    if students:
        table = []
        for stu in students:
            avg = average_score(stu)
            grade = to_grade(avg)
            table.append({
                "이름": stu["이름"],
                "국어": stu["국어"], 
                "영어": stu["영어"], 
                "수학": stu["수학"],
                "총점": total_score(stu),
                "평균": round(avg, 2),
                "학점": grade,
                "평점": grade_to_gpa(grade),
            })
        st.table(table)
    else:
        st.info("등록된 학생이 없습니다. 학생 입력 탭에서 학생을 추가해주세요.")

# --- Tab 3 : 과목별 통계 ---
with tab3:
    st.header("과목별 통계")
    if students:
        cols = st.columns(3)
        for i in range(len(SUBJECTS)):
            subject = SUBJECTS[i]
            with cols[i]:
                st.subheader(subject)
                avg = subject_average(students, subject)
                st.write(f"평균: {avg:.2f}점")
                st.write(f"최고: {subject_top(students, subject)}점")

        st.markdown("---")
        st.subheader("과목 평균 막대 그래프")
        chart_data = []
        for subject in SUBJECTS:
            chart_data.append({"과목": subject, "평균": subject_average(students, subject)})
        st.bar_chart(chart_data, x="과목", y="평균", horizontal=True, height=300)
    else:
        st.info("등록된 학생이 없습니다.")

# --- Tab 4 : 석차학점 분포 ---
with tab4:
    if students:
        st.header("석차")
        ranked = rank_list(students)
        rank_table = []
        rank = 1
        for stu in ranked:
            rank_table.append({"석차": rank, "이름": stu["이름"], "총점": total_score(stu)})
            rank = rank + 1
        st.table(rank_table)

        st.markdown("---")
        st.header("학점 분포")
        dist = grade_distribution(students)
        dist_data = [{"학점": g, "인원": dist[g]} for g in ["A", "B", "C", "D", "F"]]
        st.bar_chart(dist_data, x="학점", y="인원", horizontal=True, height=300)
    else:
        st.info("등록된 학생이 없습니다.")
