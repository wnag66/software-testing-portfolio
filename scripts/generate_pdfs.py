import re
import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = REPO_ROOT.parent
REPORT_DIR = REPO_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

RESUME_PATH = OUTPUT_ROOT / "刘亚-软件测试实习生-通用版.pdf"
REPORT_PATH = OUTPUT_ROOT / "软件测试实践项目综合报告.pdf"
REPORT_COPY_PATH = REPORT_DIR / "软件测试实践项目综合报告.pdf"

NAVY = colors.HexColor("#203247")
TEAL = colors.HexColor("#287D8E")
TEXT = colors.HexColor("#334054")
SECONDARY = colors.HexColor("#667487")
LIGHT = colors.HexColor("#DDE5EC")
PALE = colors.HexColor("#F4F7F9")
WHITE = colors.white


def register_fonts():
    regular = Path(r"C:\Windows\Fonts\Deng.ttf")
    bold = Path(r"C:\Windows\Fonts\Dengb.ttf")
    if not regular.exists() or not bold.exists():
        raise FileNotFoundError("DengXian fonts are required: C:\\Windows\\Fonts\\Deng.ttf and Dengb.ttf")
    pdfmetrics.registerFont(TTFont("DengXian", regular))
    pdfmetrics.registerFont(TTFont("DengXian-Bold", bold))


def text_width(text, font_name, font_size):
    return pdfmetrics.stringWidth(text, font_name, font_size)


def wrap_cjk(text, font_name, font_size, max_width):
    lines = []
    current = ""
    tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9./#+:_%()\-]*|.", text)
    for token in tokens:
        candidate = current + token
        if current and text_width(candidate, font_name, font_size) > max_width:
            lines.append(current)
            current = token
        else:
            current = candidate
        if text_width(current, font_name, font_size) > max_width:
            split_at = max(1, len(current) // 2)
            lines.append(current[:split_at])
            current = current[split_at:]
    if current:
        lines.append(current)
    return lines


def draw_text(c, text, x, top, font_name, font_size, color=TEXT):
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    c.drawString(x, A4[1] - top, text)


def draw_paragraph(c, text, x, top, width, font_name, font_size, leading, color=TEXT):
    lines = wrap_cjk(text, font_name, font_size, width)
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    for index, line in enumerate(lines):
        c.drawString(x, A4[1] - (top + index * leading), line)
    return top + len(lines) * leading


def draw_labeled_paragraph(c, label, text, x, top, width, font_size=8.9, leading=11.8):
    label_width = text_width(label, "DengXian-Bold", font_size)
    draw_text(c, label, x, top, "DengXian-Bold", font_size, NAVY)
    return draw_paragraph(
        c,
        text,
        x + label_width,
        top,
        width - label_width,
        "DengXian",
        font_size,
        leading,
    )


def draw_bullet(c, text, x, top, width, font_size=8.9, leading=11.8):
    draw_text(c, "•", x, top, "DengXian-Bold", font_size, TEAL)
    return draw_paragraph(c, text, x + 10, top, width - 10, "DengXian", font_size, leading)


def start_section(c, title, top):
    rule_y = A4[1] - (top + 5)
    draw_text(c, title, 42, top, "DengXian-Bold", 11.6, NAVY)
    c.setStrokeColor(LIGHT)
    c.setLineWidth(0.8)
    c.line(42, rule_y, A4[0] - 42, rule_y)
    return top + 17


def create_resume():
    register_fonts()
    c = canvas.Canvas(str(RESUME_PATH), pagesize=A4)
    c.setTitle("刘亚 - 软件测试实习生")
    c.setAuthor("刘亚")
    c.setSubject("通用软件测试实习简历")

    top = 54
    draw_text(c, "刘亚", 42, top, "DengXian-Bold", 23, NAVY)
    draw_text(c, "求职意向：软件测试实习生（2027 届）", 42, top + 27, "DengXian-Bold", 11.5, TEAL)
    draw_text(
        c,
        "电话：17280984481  |  邮箱：18883314058@163.com",
        42,
        top + 46,
        "DengXian",
        8.7,
        TEXT,
    )
    draw_text(
        c,
        "可实习：每周 5 天，稳定实习 5-6 个月，一周内到岗",
        42,
        top + 59,
        "DengXian",
        8.7,
        TEXT,
    )
    drawer_y = A4[1] - 122
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.2)
    c.line(42, drawer_y, A4[0] - 42, drawer_y)

    top = 142
    top = start_section(c, "教育背景", top)
    draw_text(c, "浙江师范大学", 42, top + 1, "DengXian-Bold", 9.6, TEXT)
    draw_text(c, "计算机科学与技术 | 本科", 118, top + 1, "DengXian", 9.4, TEXT)
    draw_text(c, "2023.09-2027.06", 485, top + 1, "DengXian", 8.8, TEXT)
    top += 14
    top = draw_labeled_paragraph(
        c,
        "相关课程：",
        "数据库、数据结构、Java 程序设计、操作系统、软件工程",
        42,
        top,
        511,
    )

    top += 7
    top = start_section(c, "专业技能", top)
    top = draw_labeled_paragraph(
        c,
        "测试基础：",
        "黑盒测试、等价类、边界值、场景法、冒烟测试、回归测试、缺陷生命周期、测试用例与测试报告编写。",
        42,
        top,
        511,
    )
    top += 1
    top = draw_labeled_paragraph(
        c,
        "接口与数据：",
        "Postman、REST Assured、HTTP/JSON、状态码、参数校验；MySQL/H2、SQL 查询、数据一致性校验。",
        42,
        top,
        511,
    )
    top += 1
    top = draw_labeled_paragraph(
        c,
        "UI 自动化：",
        "Selenium、JUnit 5、Page Object Model、显式等待、异常截图、Allure 测试报告。",
        42,
        top,
        511,
    )
    top = draw_labeled_paragraph(
        c,
        "工程工具：",
        "Git、GitHub Actions、Linux、Docker、JMeter；Java、Spring Boot、接口设计与异常处理。",
        42,
        top,
        511,
    )

    top += 7
    top = start_section(c, "测试实践项目", top)
    draw_text(c, "设备与订单管理 API 功能及性能测试", 42, top + 1, "DengXian-Bold", 10.2, NAVY)
    draw_text(c, "个人测试实践项目", 430, top + 1, "DengXian", 8.5, SECONDARY)
    top += 14
    top = draw_paragraph(
        c,
        "技术栈：Java / Spring Boot / JUnit 5 / REST Assured / Postman / JMeter / Allure / GitHub Actions",
        52,
        top,
        501,
        "DengXian",
        8.2,
        10.7,
        SECONDARY,
    )
    top = draw_bullet(
        c,
        "搭建 4 个接口的测试靶场，设计 20 条手工用例与 8 条 REST Assured 自动化用例，覆盖参数校验、重复请求、过期边界和分页边界。",
        42,
        top,
        511,
    )
    top = draw_bullet(
        c,
        "在缺陷版本复现 5 个有效问题并记录复现步骤，修复后自动化回归 8/8 通过。",
        42,
        top,
        511,
    )
    top = draw_bullet(
        c,
        "使用 JMeter 完成 50 并发负载测试，共 396,024 次请求，平均响应 13.83 ms，P95 70 ms，错误率 0%。",
        42,
        top,
        511,
    )
    top = draw_bullet(
        c,
        "使用 Postman 进行接口探索，通过 SQL 校验测试数据，并使用 GitHub Actions 自动执行 API 回归。",
        42,
        top,
        511,
    )
    link_y = A4[1] - top
    c.setFont("DengXian", 8.1)
    c.setFillColor(TEAL)
    c.drawString(52, link_y, "项目链接：github.com/wnag66/software-testing-portfolio")
    c.linkURL(
        "https://github.com/wnag66/software-testing-portfolio",
        (52, link_y - 2, 345, link_y + 9),
        relative=0,
    )
    top += 13

    draw_text(c, "SauceDemo 电商流程 UI 自动化测试", 42, top + 1, "DengXian-Bold", 10.2, NAVY)
    draw_text(c, "个人测试实践项目", 430, top + 1, "DengXian", 8.5, SECONDARY)
    top += 14
    top = draw_paragraph(
        c,
        "技术栈：Java / Selenium / JUnit 5 / Page Object Model / Allure / GitHub Actions",
        52,
        top,
        501,
        "DengXian",
        8.2,
        10.7,
        SECONDARY,
    )
    top = draw_bullet(
        c,
        "基于 Page Object Model 编写 10 条 UI 自动化用例，覆盖登录、锁定用户、商品排序、购物车、结算校验和退出登录。",
        42,
        top,
        511,
    )
    top = draw_bullet(
        c,
        "使用显式等待和稳定 data-test 定位器，失败时自动附加截图与页面源码；Chrome Headless 回归 10/10 通过。",
        42,
        top,
        511,
    )
    top = draw_bullet(
        c,
        "使用 GitHub Actions 持续执行 UI 回归，Allure 记录用例步骤、执行结果和失败证据。",
        42,
        top,
        511,
    )

    top += 7
    top = start_section(c, "测试交付", top)
    top = draw_paragraph(
        c,
        "公开仓库包含测试计划、20 条手工用例、5 份缺陷报告、8 条 API 自动化用例、10 条 UI 自动化用例、"
        "Allure 报告、Postman Collection 和 JMeter HTML Dashboard，测试结果和缺陷编号可相互追溯。",
        42,
        top,
        511,
        "DengXian",
        8.9,
        11.8,
    )

    top += 7
    top = start_section(c, "开发项目与实习", top)
    top = draw_labeled_paragraph(
        c,
        "商品秒杀系统：",
        "Java/Spring Boot/Redis/RabbitMQ 后端项目；实现库存原子扣减、异步削峰和幂等处理，参与接口自测、异常校验和回归验证。",
        42,
        top,
        511,
    )
    top += 1
    top = draw_labeled_paragraph(
        c,
        "DocMind：",
        "RAG 知识库问答系统；完成 RESTful API、参数校验、异常处理与 Docker/Linux 部署，关注接口和数据链路一致性。",
        42,
        top,
        511,
    )
    top += 1
    top = draw_labeled_paragraph(
        c,
        "中国移动营业厅实习：",
        "参与前台业务受理、客户信息核验与订单查询，熟悉需求受理、处理、回访的状态流转，具备客户沟通和任务闭环意识。",
        42,
        top,
        511,
    )

    top += 7
    top = start_section(c, "自我评价", top)
    top = draw_paragraph(
        c,
        "做事认真细致，能够按测试流程完成任务闭环；具备 Java 开发和接口调试基础，能够快速理解软件逻辑与测试要求。"
        "沟通配合意识较强，希望在软件测试方向持续积累，并对自动化测试、接口测试和性能测试保持持续学习。",
        42,
        top,
        511,
        "DengXian",
        8.6,
        11.3,
    )

    if top > 810:
        raise RuntimeError(f"Resume content overflows page: bottom={top:.1f}")
    c.showPage()
    c.save()


def create_resume_star(headshot_path: str | Path | None = None):
    register_fonts()
    c = canvas.Canvas(str(RESUME_PATH), pagesize=A4)
    c.setTitle("刘亚 - AI 测试开发实习生")
    c.setAuthor("刘亚")
    c.setSubject("AI 测试开发实习简历")

    top = 52
    draw_text(c, "刘亚", 42, top, "DengXian-Bold", 22, NAVY)
    draw_text(c, "求职意向：AI 测试开发实习生（2027 届）", 42, top + 25, "DengXian-Bold", 11, TEAL)
    draw_text(c, "电话：17280984481  |  邮箱：18883314058@163.com", 42, top + 43, "DengXian", 8.4, TEXT)
    draw_text(c, "可实习：每周 5 天，稳定实习 5-6 个月，一周内到岗", 42, top + 56, "DengXian", 8.4, TEXT)
    if headshot_path:
        headshot = Path(headshot_path)
        if not headshot.exists():
            raise FileNotFoundError(f"Headshot not found: {headshot}")
        photo_x = 504.2756
        photo_top = 69.37856
        photo_width = 38.0
        photo_height = 53.24294
        c.drawImage(
            ImageReader(str(headshot)),
            photo_x,
            A4[1] - photo_top - photo_height,
            width=photo_width,
            height=photo_height,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )
    drawer_y = A4[1] - 116
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.2)
    c.line(42, drawer_y, A4[0] - 42, drawer_y)

    top = 136
    top = start_section(c, "教育背景", top)
    draw_text(c, "浙江师范大学", 42, top + 1, "DengXian-Bold", 9.3, TEXT)
    draw_text(c, "计算机科学与技术 | 本科", 118, top + 1, "DengXian", 9.1, TEXT)
    draw_text(c, "2023.09-2027.06", 485, top + 1, "DengXian", 8.6, TEXT)
    top += 13
    top = draw_labeled_paragraph(
        c,
        "相关课程：",
        "数据结构、数据库、Java 程序设计、操作系统、软件工程",
        42,
        top,
        511,
        8.4,
        10.8,
    )

    top += 4
    top = start_section(c, "专业技能", top)
    top = draw_labeled_paragraph(
        c,
        "AI 测试开发：",
        "LLM/Agent 评测、Prompt Injection 与安全拒答、工具调用正确性、幻觉防护、答案关键词校验、P95 延迟阈值。",
        42,
        top,
        511,
        8.2,
        10.7,
    )
    top = draw_labeled_paragraph(
        c,
        "Python 自动化：",
        "Python、Pytest、Dataclass、JSON 数据驱动、评测报告生成；Java、JUnit 5、REST Assured、Selenium。",
        42,
        top,
        511,
        8.2,
        10.7,
    )
    top = draw_labeled_paragraph(
        c,
        "测试与工具：",
        "黑盒测试、等价类、边界值、场景法、接口测试、UI 自动化、性能测试、Allure、Postman、JMeter、SQL。",
        42,
        top,
        511,
        8.2,
        10.7,
    )
    top = draw_labeled_paragraph(
        c,
        "工程与 CI：",
        "Git、GitHub Actions、Linux、Docker、Spring Boot；能够将测试框架接入持续集成流水线。",
        42,
        top,
        511,
        8.2,
        10.7,
    )

    top += 4
    top = start_section(c, "测试开发项目（STAR）", top)

    draw_text(c, "AgentEval - LLM/Agent 评测框架", 42, top + 1, "DengXian-Bold", 9.9, NAVY)
    draw_text(c, "个人测试开发项目", 430, top + 1, "DengXian", 8.2, SECONDARY)
    top += 12
    top = draw_paragraph(
        c,
        "技术栈：Python / Pytest / Dataclass / JSON / GitHub Actions",
        52,
        top,
        501,
        "DengXian",
        7.9,
        10.2,
        SECONDARY,
    )
    top = draw_labeled_paragraph(
        c,
        "背景：",
        "LLM/Agent 的输出具有不确定性，传统断言很难覆盖工具选择错误、Prompt 注入和幻觉风险。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "职责：",
        "负责评测框架与用例模型设计，定义任务成功、工具调用、安全拒答、幻觉防护和 P95 延迟指标。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "行动：",
        "实现规则 Agent、工具层、评测器和 JSON/Markdown 报告模块；构建 12 条评测样例与 10 条 Pytest 用例，校验工具调用顺序、答案关键词、禁用词、异常权限和响应时间。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "结果：",
        "12/12 评测通过，工具调用准确率 100%，安全通过率 100%，P95 0.3452 ms，并接入 GitHub Actions 持续回归。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    link_y = A4[1] - top
    c.setFont("DengXian", 7.8)
    c.setFillColor(TEAL)
    c.drawString(52, link_y, "项目仓库：github.com/wnag66/software-testing-portfolio")
    c.linkURL(
        "https://github.com/wnag66/software-testing-portfolio",
        (52, link_y - 2, 340, link_y + 9),
        relative=0,
    )
    top += 11

    top += 4
    draw_text(c, "设备与订单管理 API 功能及性能测试", 42, top + 1, "DengXian-Bold", 9.9, NAVY)
    draw_text(c, "个人测试项目", 450, top + 1, "DengXian", 8.2, SECONDARY)
    top += 12
    top = draw_paragraph(
        c,
        "技术栈：Java / Spring Boot / JUnit 5 / REST Assured / Postman / H2 / JMeter / Allure / GitHub Actions",
        52,
        top,
        501,
        "DengXian",
        7.9,
        10.2,
        SECONDARY,
    )
    top = draw_labeled_paragraph(
        c,
        "背景：",
        "设备与订单服务同时涉及状态流转、时间边界、重复请求、分页和数据一致性，质量问题会直接影响交付。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "职责：",
        "负责需求拆解、测试方案、接口自动化、缺陷复现、性能场景设计和回归验证。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "行动：",
        "自建 4 个接口的测试靶场，设计 20 条手工用例和 8 条 REST Assured 自动化用例；使用 Postman 探索接口，通过 H2 SQL 校验数据一致性，用 JMeter 编排 1/20/50 并发场景。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "结果：",
        "修复后 8/8 自动化通过，关闭 5 个缺陷；50 并发完成 396,024 次请求，平均 13.83 ms，P95 70 ms，错误率 0%。",
        42,
        top,
        511,
        8.1,
        10.6,
    )

    top += 4
    draw_text(c, "SauceDemo 电商流程 UI 自动化测试", 42, top + 1, "DengXian-Bold", 9.9, NAVY)
    draw_text(c, "个人测试项目", 450, top + 1, "DengXian", 8.2, SECONDARY)
    top += 12
    top = draw_paragraph(
        c,
        "技术栈：Java / Selenium / JUnit 5 / Page Object Model / Allure / GitHub Actions",
        52,
        top,
        501,
        "DengXian",
        7.9,
        10.2,
        SECONDARY,
    )
    top = draw_labeled_paragraph(
        c,
        "背景：",
        "电商用户流程跨多个页面，手工回归成本高，需要稳定、可重复且能保留失败证据的自动化方案。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "职责：",
        "负责页面对象分层、稳定定位器、显式等待策略和失败证据采集。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "行动：",
        "编写 10 条 UI 自动化用例，覆盖登录、锁定用户、商品排序、购物车、结算校验和退出；在 Chrome Headless 中执行并接入 Allure。",
        42,
        top,
        511,
        8.1,
        10.6,
    )
    top = draw_labeled_paragraph(
        c,
        "结果：",
        "自动化回归 10/10 通过，失败时自动记录截图和页面源码，GitHub Actions 持续执行回归。",
        42,
        top,
        511,
        8.1,
        10.6,
    )

    top += 4
    top = start_section(c, "相关开发与实习经历", top)
    top = draw_labeled_paragraph(
        c,
        "DocMind RAG：",
        "参与文档上传、切分、向量检索和 LLM 问答链路开发，理解 RAG 评测中的召回、上下文和幻觉风险。",
        42,
        top,
        511,
        8.2,
        10.7,
    )
    top = draw_labeled_paragraph(
        c,
        "商品秒杀系统：",
        "完成 Redis 原子扣减、RabbitMQ 异步削峰和幂等处理，参与接口自测、异常校验和回归验证。",
        42,
        top,
        511,
        8.2,
        10.7,
    )
    top = draw_labeled_paragraph(
        c,
        "中国移动营业厅实习：",
        "参与前台业务受理、客户信息核验和订单查询，熟悉需求受理、处理、回访的闭环流程。",
        42,
        top,
        511,
        8.2,
        10.7,
    )

    top += 4
    top = start_section(c, "自我评价", top)
    top = draw_paragraph(
        c,
        "以 Python 为主要测试开发语言，能够把测试需求沉淀为可执行框架并接入 CI；具备 Java/Spring Boot 和 RAG 开发基础，"
        "理解 AI 产品在工具调用、幻觉、安全和延迟方面的测试重点。认真细致，沟通配合意识强，希望在 AI 测试开发方向长期发展。",
        42,
        top,
        511,
        "DengXian",
        8.3,
        10.9,
    )

    if top > 812:
        raise RuntimeError(f"STAR resume content overflows page: bottom={top:.1f}")
    c.showPage()
    c.save()


def report_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ChineseTitle",
            parent=styles["Title"],
            fontName="DengXian-Bold",
            fontSize=25,
            leading=34,
            textColor=NAVY,
            alignment=TA_CENTER,
            wordWrap="CJK",
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "ChineseSubtitle",
            parent=styles["Normal"],
            fontName="DengXian",
            fontSize=11,
            leading=18,
            textColor=SECONDARY,
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "ChineseH1",
            parent=styles["Heading1"],
            fontName="DengXian-Bold",
            fontSize=16,
            leading=22,
            textColor=NAVY,
            wordWrap="CJK",
            spaceBefore=8,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "ChineseH2",
            parent=styles["Heading2"],
            fontName="DengXian-Bold",
            fontSize=12,
            leading=18,
            textColor=TEAL,
            wordWrap="CJK",
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "ChineseBody",
            parent=styles["BodyText"],
            fontName="DengXian",
            fontSize=9.5,
            leading=15,
            textColor=TEXT,
            alignment=TA_LEFT,
            wordWrap="CJK",
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "ChineseSmall",
            parent=styles["BodyText"],
            fontName="DengXian",
            fontSize=8.3,
            leading=12,
            textColor=SECONDARY,
            wordWrap="CJK",
        ),
    }


def paragraph(text, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


def make_table(data, widths, header=True, style=None):
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("FONTNAME", (0, 0), (-1, -1), "DengXian"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.35, LIGHT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "DengXian-Bold"),
            ]
        )
    if style:
        commands.extend(style)
    table.setStyle(TableStyle(commands))
    return table


def add_page_footer(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(LIGHT)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
    canvas_obj.setFont("DengXian", 8)
    canvas_obj.setFillColor(SECONDARY)
    canvas_obj.drawString(20 * mm, 10 * mm, "软件测试实践项目综合报告")
    canvas_obj.drawRightString(A4[0] - 20 * mm, 10 * mm, f"第 {doc.page} 页")
    canvas_obj.restoreState()


def create_report():
    register_fonts()
    styles = report_styles()
    document = SimpleDocTemplate(
        str(REPORT_PATH),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title="软件测试实践项目综合报告",
        author="刘亚",
    )
    story = []

    story.append(Spacer(1, 85))
    story.append(paragraph("软件测试实践项目综合报告", styles["title"]))
    story.append(paragraph("设备与订单 API 功能及性能测试 / SauceDemo UI 自动化测试", styles["subtitle"]))
    story.append(Spacer(1, 22))
    story.append(
        make_table(
            [
                ["报告版本", "v1.0"],
                ["报告日期", "2026-09-30"],
                ["执行人", "刘亚"],
                ["项目性质", "个人测试实践项目，不包含真实企业生产数据"],
            ],
            [40 * mm, 110 * mm],
            header=False,
        )
    )
    story.append(PageBreak())

    story.append(paragraph("1. 管理摘要", styles["h1"]))
    story.append(
        paragraph(
            "本报告汇总两个测试实践项目的执行情况：设备与订单管理 API、SauceDemo 电商 Web 应用。"
            "API 项目完成 20 条手工用例设计、8 条自动化回归、5 个缺陷复现与修复，以及 3 组 JMeter 性能场景。"
            "UI 项目完成 10 条基于 Page Object Model 的 Selenium 自动化用例。"
            "所有修复版本的自动化用例均全部通过，JMeter 场景错误率为 0%。",
            styles["body"],
        )
    )
    story.append(paragraph("执行结论", styles["h2"]))
    story.append(
        make_table(
            [
                ["测试对象", "范围", "结果"],
                ["设备与订单 API", "8 条自动化用例", "8/8 通过"],
                ["SauceDemo Web", "10 条 UI 自动化用例", "10/10 通过"],
                ["缺陷生命周期", "5 个缺陷", "5/5 修复并回归"],
                ["性能测试", "冒烟 / 基线 / 负载", "0% 错误率"],
            ],
            [45 * mm, 65 * mm, 40 * mm],
        )
    )
    story.append(PageBreak())

    story.append(paragraph("2. 测试环境与方法", styles["h1"]))
    story.append(paragraph("测试环境", styles["h2"]))
    story.append(
        make_table(
            [
                ["类别", "版本/配置"],
                ["Java", "17.0.20"],
                ["Spring Boot", "3.5.16"],
                ["API 自动化", "JUnit 5.14.4 / REST Assured 5.5.7"],
                ["UI 自动化", "Selenium 4.49.0 / Chrome Headless"],
                ["性能测试", "JMeter 5.6.3"],
                ["报告", "Allure 2.35.5 结果 / Allure 2.46.1 生成器"],
                ["CI", "GitHub Actions / Java 17 / Ubuntu"],
            ],
            [40 * mm, 110 * mm],
        )
    )
    story.append(paragraph("测试方法", styles["h2"]))
    for item in [
        "等价类、边界值和场景法用于功能与接口用例设计。",
        "REST Assured 用于接口回归和响应字段、状态码、业务状态断言。",
        "Selenium 使用 Page Object Model、显式等待和稳定 data-test 定位器。",
        "缺陷版本用于复现问题，修复版本用于验证根因修复和回归。",
        "JMeter 使用参数化 JMX 执行 1、20、50 并发场景。",
    ]:
        story.append(paragraph(f"• {item}", styles["body"]))
    story.append(PageBreak())

    story.append(paragraph("3. API 功能测试", styles["h1"]))
    story.append(
        paragraph(
            "API 靶场包含设备状态、设备心跳、订单校验和事件查询四类接口。测试覆盖正常流程、异常参数、"
            "过期边界、重复请求、数据一致性、分页下界和分页上界。",
            styles["body"],
        )
    )
    story.append(paragraph("用例统计", styles["h2"]))
    story.append(
        make_table(
            [
                ["模块", "手工用例", "自动化用例", "覆盖重点"],
                ["设备状态", "4", "2", "存在、缺失、格式、字段"],
                ["设备心跳", "4", "1", "状态、负延迟、更新结果"],
                ["订单校验", "6", "3", "有效、过期、边界、重复"],
                ["事件查询", "6", "2", "筛选、分页 0/51/50"],
                ["合计", "20", "8", "缺陷与回归闭环"],
            ],
            [34 * mm, 27 * mm, 30 * mm, 59 * mm],
        )
    )
    story.append(paragraph("执行结果", styles["h2"]))
    story.append(
        paragraph(
            "缺陷版本执行结果为 8 条用例中 5 条失败，失败原因与 5 个已知缺陷一一对应。"
            "修复版本执行结果为 8 条用例全部通过，错误用例数和异常数为 0。",
            styles["body"],
        )
    )
    story.append(
        make_table(
            [
                ["版本", "执行", "失败", "结论"],
                ["v0.1-buggy", "8", "5", "稳定复现缺陷"],
                ["v1.0-fixed", "8", "0", "回归通过"],
            ],
            [38 * mm, 30 * mm, 30 * mm, 52 * mm],
        )
    )
    story.append(PageBreak())

    story.append(paragraph("4. UI 自动化测试", styles["h1"]))
    story.append(
        paragraph(
            "SauceDemo 是用于自动化练习的公开演示站点。测试使用 Selenium 和 Page Object Model，"
            "每条用例创建独立浏览器会话，通过显式等待处理页面加载，失败时记录截图和页面源码。",
            styles["body"],
        )
    )
    story.append(paragraph("测试覆盖", styles["h2"]))
    story.append(
        make_table(
            [
                ["编号", "场景", "断言"],
                ["TC-UI-001", "标准用户登录", "进入商品列表"],
                ["TC-UI-002", "锁定用户登录", "显示锁定提示"],
                ["TC-UI-003", "错误密码", "显示认证失败提示"],
                ["TC-UI-004", "商品名称降序", "首项排序正确"],
                ["TC-UI-005", "加入购物车", "购物车角标为 1"],
                ["TC-UI-006", "移除商品", "购物车角标消失"],
                ["TC-UI-007", "进入购物车", "商品名称正确"],
                ["TC-UI-008", "完成结算", "显示订单完成提示"],
                ["TC-UI-009", "缺少必填字段", "显示姓名必填提示"],
                ["TC-UI-010", "退出登录", "返回登录页"],
            ],
            [27 * mm, 65 * mm, 58 * mm],
        )
    )
    story.append(paragraph("执行结果", styles["h2"]))
    story.append(paragraph("Chrome Headless 环境下执行 10 条用例，10/10 通过，0 失败，0 异常。", styles["body"]))
    story.append(PageBreak())

    story.append(paragraph("5. 缺陷分析", styles["h1"]))
    story.append(
        make_table(
            [
                ["编号", "问题", "严重度", "根因与修复"],
                ["BUG-001", "负心跳延迟被接受", "High", "缺少下限校验，增加 latencyMs >= 0"],
                ["BUG-002", "过期边界被接受", "Critical", "边界比较错误，改为 validatedAt >= expiresAt 时拒绝"],
                ["BUG-003", "订单重复校验", "Critical", "缺少幂等检查，validated_count > 0 时返回 409"],
                ["BUG-004", "分页 size=0 返回 500", "High", "除零错误，增加 1-50 范围校验"],
                ["BUG-005", "分页 size>50 被接受", "Medium", "缺少上界校验，限制最大页大小"],
            ],
            [25 * mm, 46 * mm, 20 * mm, 79 * mm],
        )
    )
    story.append(paragraph("缺陷流程", styles["h2"]))
    story.append(
        paragraph(
            "每个缺陷均包含前置条件、复现步骤、预期结果、实际结果、根因、修复和回归映射。"
            "缺陷版本标签为 v0.1-buggy，修复版本标签为 v1.0-fixed。"
            "缺陷记录与 GitHub Issues、测试用例编号保持对应。",
            styles["body"],
        )
    )
    story.append(PageBreak())

    story.append(paragraph("6. 性能测试", styles["h1"]))
    story.append(
        paragraph(
            "性能测试在本地单节点 Spring Boot 和 H2 环境中执行，请求组合包含健康检查、设备状态、"
            "心跳上报和事件查询。结果用于验证 JMeter 方法和稳定性趋势，不代表生产容量。",
            styles["body"],
        )
    )
    story.append(
        make_table(
            [
                ["场景", "并发", "时长", "请求数", "吞吐量", "平均", "P95", "错误率"],
                ["冒烟", "1", "10 s", "5,083", "515.2/s", "1.81 ms", "4 ms", "0%"],
                ["基线", "20", "60 s", "235,271", "3,927.7/s", "4.62 ms", "23 ms", "0%"],
                ["负载", "50", "120 s", "396,024", "3,303.0/s", "13.83 ms", "70 ms", "0%"],
            ],
            [20 * mm, 15 * mm, 18 * mm, 25 * mm, 28 * mm, 22 * mm, 18 * mm, 18 * mm],
        )
    )
    story.append(paragraph("分析", styles["h2"]))
    story.append(
        paragraph(
            "服务在 1、20、50 并发场景下均保持 0% 错误率。并发从 20 提升到 50 后，总吞吐量从 "
            "3,927.7 降至 3,303.0 请求/秒，平均响应时间从 4.62 ms 上升至 13.83 ms，说明本地测试机、"
            "JVM 和 H2 写入开始出现资源竞争。后续可进行更长持续时间的稳定性测试、JVM 指标采集和数据库调优。",
            styles["body"],
        )
    )
    story.append(PageBreak())

    story.append(paragraph("7. 持续集成与复现", styles["h1"]))
    story.append(
        make_table(
            [
                ["任务", "命令", "产物"],
                ["API 回归", "mvn -pl api-testlab test", "Surefire / Allure"],
                ["UI 回归", "mvn -pl ui-automation test -Dheadless=true", "Surefire / 截图 / Allure"],
                ["性能测试", "api-testlab/scripts/run-performance.ps1", "JTL / HTML Dashboard"],
                ["完整构建", "mvn clean verify", "Maven 测试结果"],
            ],
            [30 * mm, 83 * mm, 57 * mm],
        )
    )
    story.append(paragraph("项目资产", styles["h2"]))
    for item in [
        "公开仓库：github.com/wnag66/software-testing-portfolio",
        "Postman Collection：postman/device-order-api.postman_collection.json",
        "手工测试用例：docs/test-cases.md",
        "缺陷报告：docs/bug-reports/",
        "性能明细：docs/performance-results.md",
        "Allure 报告：reports/allure-api/ 与 reports/allure-ui/",
    ]:
        story.append(paragraph(f"• {item}", styles["body"]))
    story.append(paragraph("最终结论", styles["h2"]))
    story.append(
        paragraph(
            "两个实践项目已完成计划范围内的设计、执行、缺陷修复、回归、性能验证和持续集成。"
            "仓库中的测试结果、缺陷编号、自动化代码和执行证据可以相互验证。"
            "该项目能够证明通用软件测试岗位所需的测试思维、接口测试、UI 自动化、性能测试和工程协作能力。",
            styles["body"],
        )
    )

    document.build(story, onFirstPage=add_page_footer, onLaterPages=add_page_footer)
    REPORT_COPY_PATH.write_bytes(REPORT_PATH.read_bytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate resume and project report PDFs")
    parser.add_argument("--headshot", default=None, help="Optional headshot image path")
    arguments = parser.parse_args()
    create_resume_star(arguments.headshot)
    create_report()
    print(f"Created: {RESUME_PATH}")
    print(f"Created: {REPORT_PATH}")
    print(f"Created: {REPORT_COPY_PATH}")
