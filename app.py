from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
from urllib.parse import unquote, urlparse
from application_pages import application_page


ROOT = Path(__file__).resolve().parent
STATIC_ROOT = ROOT / "static"

PROFILE = {
    "name": "Tong(Stone)Shi",
    "title": "Transportation engineering, GIS, and multi-agent mobility research",
    "email": "tongshi@berkeley.edu",
    "phone": "(+1) 805-280-6424",
    "linkedin": "https://linkedin.com/in/stoneshiucb",
    "github": "https://github.com/camel-ai/oasis",
    "summary": (
        "I build GIS-centered transportation models, airport sustainability analyses, "
        "and LLM multi-agent simulations for mobility systems under stress."
    ),
}

WORK_SAMPLES = [
    {
        "slug": "transit-disruptions",
        "title": "Modeling Transit Decisions Under Network Disruptions",
        "tag": "LLM multi-agent simulation",
        "period": "2024 - ongoing",
        "summary": "A large-scale multi-agent transit simulator for testing how passengers and operators respond to sudden rail and bus disruptions.",
        "details": [
            "Built a million-agent simulation concept around realistic passenger decision-making, network disruptions, congestion, and multimodal alternatives.",
            "Integrated GIS layers, Chicago demographic context, route-choice logic, and forecasting workflows using NetworkX, OSMnx, PyMATSim, and OASIS.",
            "Designed coordination agents that adjust scheduling and assignments to reduce crowding and improve disruption resilience.",
        ],
        "methods": ["Python", "OASIS", "NetworkX", "OSMnx", "PyMATSim", "LLM agents"],
    },
    {
        "slug": "airport-emissions",
        "title": "California Airport Emissions and Environmental Justice",
        "tag": "Airport sustainability",
        "period": "2024 - 2025",
        "summary": "A spatiotemporal analysis of emissions from California airports and the socioeconomic exposure of nearby communities.",
        "details": [
            "Analyzed emission exposure around 66 California airports with GIS-based spatial overlays and temporal distribution logic.",
            "Connected aviation network dynamics, emission impacts, and environmental justice questions for a paper preparing for submission.",
            "Developed sustainability and mitigation framing for airport operations, safety-zone analysis, and community risk management.",
        ],
        "methods": ["ArcGIS", "QGIS", "scikit-learn", "spatial analysis", "environmental justice"],
    },
    {
        "slug": "airport-safety",
        "title": "Spatial Distribution of Aircraft Accidents in Airport Safety Zones",
        "tag": "FAA NEXTOR III",
        "period": "2024",
        "summary": "A California airport safety-zone study using accident records, runway geometries, clustering, and relative-distance analysis.",
        "details": [
            "Mapped accidents across 259 airports and compared observed risk patterns against safety-zone thresholds.",
            "Used NTSB accident records, digitized runway boundaries, triangulation, and point-pattern analysis to locate critical safety areas.",
            "Produced statistical and spatial evidence for updated safety-zone dimensions and risk-management decisions.",
        ],
        "methods": ["GIS", "NTSB records", "point-pattern analysis", "airport planning"],
    },
    {
        "slug": "urban-perception",
        "title": "Urban Perception in Human Biking Mobility: Bogota",
        "tag": "Street-view cognition",
        "period": "2023 - 2024",
        "summary": "A citywide street-view and mobility analysis of how perceived urban environments affect cycling experience.",
        "details": [
            "Optimized urban perception models using Google Street View imagery and PyTorch-based sensing workflows.",
            "Built perception layers across more than 90,000 road segments to evaluate infrastructure experience at network scale.",
            "Presented the research at the 2024 American Association of Geographers Annual Meeting.",
        ],
        "methods": ["PyTorch", "Google Street View", "mobility networks", "urban perception"],
    },
    {
        "slug": "tikal-milpa",
        "title": "Modeling the Milpa Cycle and Labor Density at Tikal",
        "tag": "Archaeological GIS",
        "period": "2021 - 2023",
        "summary": "A geospatial reconstruction of sustainable land use, hydrology, and labor density in the Maya lowlands.",
        "details": [
            "Managed a nine-person GIS team digitizing hydrological networks and validating more than 300 well locations.",
            "Combined archaeological records, DEM data, field observations, and watershed modeling to estimate settlement water supply and crop yield.",
            "Presented at the 2023 SAA and AAG meetings; the work placed second in the AAG GISS Student Honor Paper Competition.",
        ],
        "methods": ["ArcGIS", "DEM analysis", "hydrology", "archaeological mapping"],
    },
    {
        "slug": "streamflow-flood",
        "title": "Predicting Flood Likelihood of U.S. Major Streamflow",
        "tag": "Hydrology and forecasting",
        "period": "2020 - 2021",
        "summary": "A national streamflow recurrence and flood likelihood model using historic USGS monitoring data.",
        "details": [
            "Built a recurrence-interval dataset with 169,776 observations across USGS monitoring sites.",
            "Modeled future flood trends across two-to-one-hundred-year horizons and published interactive results through Tableau and RMarkdown.",
            "Connected hydrologic time intervals, statistical learning, and public-facing data visualization.",
        ],
        "methods": ["R", "RShiny", "Tableau", "USGS data", "scikit-learn"],
    },
]


def link(label, href, css_class=""):
    class_attr = f' class="{css_class}"' if css_class else ""
    return f'<a{class_attr} href="{escape(href, quote=True)}">{escape(label)}</a>'


def base(title, body, language="en", nav_items=None):
    nav = (
        f'{link("CV", "/")} '
        f'{link("Cover Letter", "/cover-letter")} '
        f'{link("Research Proposal", "/research-proposal")} '
        f'{link("Statement of Purpose", "/statement-of-purpose")} '
        f'{link("Personal Statement", "/personal-statement")}'
    ) if nav_items is None else nav_items
    en_current = ' aria-current="true"' if language == "en" else ""
    zh_current = ' aria-current="true"' if language == "zh" else ""
    language_picker = (
        '<div class="language-switch" aria-label="Language">'
        f'<a href="/" lang="en"{en_current}>English</a>'
        f'<a href="/zh/" lang="zh-Hans"{zh_current}>简体中文</a>'
        '</div>'
    )
    footer = (
        f"<span>{PROFILE['email']}</span>"
        f"<span>{PROFILE['phone']}</span>"
        f'{link("LinkedIn", PROFILE["linkedin"])}'
        f'{link("OASIS", PROFILE["github"])}'
    )
    return f"""<!doctype html>
<html lang="{'zh-Hans' if language == 'zh' else 'en'}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <meta name="description" content="CV homepage for Tong (Stone) Shi, transportation engineering, GIS, and multi-agent mobility research.">
    <link rel="stylesheet" href="/static/styles.css?v=fall2027">
  </head>
<body{' class="zh-home"' if language == 'zh' else ''}>
    <header class="site-header">
      <a class="brand name-mark" href="/">{'史桐' if language == 'zh' else 'Tong(Stone)Shi'}</a>
      <div class="header-actions">
        <nav aria-label="Primary navigation">{nav}</nav>
        {language_picker}
      </div>
    </header>
    <main>{body}</main>
    <footer class="site-footer">{footer}</footer>
    <script>
      const currentPath = window.location.pathname.replace(/\/$/, "") || "/";
      document.querySelectorAll("nav a").forEach((item) => {{
        const itemPath = new URL(item.href).pathname.replace(/\/$/, "") || "/";
        if (itemPath === currentPath) item.setAttribute("aria-current", "page");
      }});

      const revealItems = document.querySelectorAll("main > section, .sample-card");
      revealItems.forEach((item) => item.classList.add("reveal-target"));
      const revealObserver = new IntersectionObserver((entries) => {{
        entries.forEach((entry) => {{
          if (entry.isIntersecting) {{
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }}
        }});
      }}, {{ threshold: 0.08, rootMargin: "0px 0px -40px" }});
      revealItems.forEach((item) => revealObserver.observe(item));

      const identity = document.querySelector(".identity-heading");
      if (identity && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
        const characters = [];
        identity.querySelectorAll("[data-type]").forEach((part) => {{
          const text = part.textContent;
          part.textContent = "";
          for (const character of Array.from(text)) {{
            const span = document.createElement("span");
            span.className = "typed-character";
            span.textContent = character;
            part.appendChild(span);
            characters.push(span);
          }}
        }});
        let index = 0;
        const typeNext = () => {{
          if (index > 0) characters[index - 1].classList.remove("typing-cursor");
          if (index < characters.length) {{
            characters[index].classList.add("is-typed", "typing-cursor");
            index += 1;
            window.setTimeout(typeNext, 45);
          }} else {{
            identity.classList.add("typing-complete");
          }}
        }};
        typeNext();
      }}
    </script>
  </body>
</html>"""


def cv_page():
    cards = "\n".join(
        f"""<article class="sample-card">
    <div class="sample-card-summary">
      <span>{escape(sample['tag'])}</span>
      <h3>{escape(sample['title'])}</h3>
      <p>{escape(sample['summary'])}</p>
      <small>{escape(sample['period'])}</small>
    </div>
    <div class="sample-card-details">
      <div class="sample-card-slide">
        <span>{escape(sample['tag'])} | {escape(sample['period'])}</span>
        <h3>{escape(sample['title'])}</h3>
        <ul>{''.join(f'<li>{escape(detail)}</li>' for detail in sample['details'])}</ul>
        <div class="sample-methods">{''.join(f'<b>{escape(method)}</b>' for method in sample['methods'])}</div>
      </div>
    </div>
  </article>"""
        for sample in WORK_SAMPLES
    )
    body = f"""
<section class="hero">
  <div class="hero-copy">
    <h1 class="identity-heading" aria-label="Tong Shi. I go by Stone Shi. My Chinese name is 史桐.">
      <span class="identity-line" aria-hidden="true"><span class="identity-name" data-type>Tong Shi</span></span>
      <span class="identity-line" aria-hidden="true"><span class="identity-label" data-type>I go by </span><strong class="identity-name preferred-name" data-type>Stone Shi</strong></span>
      <span class="identity-line mother-tongue" aria-hidden="true"><span data-type>My Chinese name is </span><strong lang="zh" data-type>史桐</strong></span>
    </h1>
    <p class="lead">I study mobility, accessibility, and travel behavior through GIS, airport sustainability research, and multi-agent simulation.</p>
    <div class="research-availability">
      <p class="availability-label">Looking for <strong class="opportunity-role">PhD</strong> opportunities</p>
      <p class="availability-term">Fall 2027<span> entry</span></p>
      <p class="availability-note">Also open to <strong class="opportunity-role">Research Assistant</strong> roles<br>aligned with my research.</p>
    </div>
    <div class="button-row">
      <a class="button primary" href="/static/documents/research-cv.pdf" download>Download research CV</a>
      <a class="button secondary" href="/static/documents/transportation-gis-resume.pdf" download>Download transportation/GIS resume</a>
      <a class="button secondary" href="/statement-of-purpose">Statement of purpose</a>
      <a class="button secondary" href="/personal-statement">Personal statement</a>
    </div>
  </div>
  <aside class="profile-panel" aria-label="Profile">
    <div class="portrait">
      <img src="/static/images/profile-photo.jpg" alt="Portrait of Tong(Stone)Shi">
    </div>
    <p class="profile-education"><strong>UC Berkeley</strong> M.S., Transportation Engineering<br><strong>UC Santa Barbara</strong> B.A., GIS</p>
    <div class="profile-links">
      <a href="mailto:{PROFILE['email']}"><img src="/static/icons/envelope.svg" alt="" width="20" height="20"><span>{PROFILE['email']}</span></a>
      <a href="tel:+18052806424"><img src="/static/icons/telephone.svg" alt="" width="20" height="20"><span>Phone <small>{PROFILE['phone']}</small></span></a>
      <a href="{PROFILE['linkedin']}"><img src="/static/icons/linkedin.svg" alt="" width="20" height="20"><span>LinkedIn</span></a>
      <a href="{PROFILE['github']}"><img src="/static/icons/github.svg" alt="" width="20" height="20"><span>GitHub</span></a>
    </div>
  </aside>
</section>
<section class="cv-intro">
  <h2><span>Research, education,</span><br>and applied experience</h2>
</section>
{latex_cv_section()}
<section class="section-grid single-column">
  <div>
    <p class="eyebrow">Selected work</p>
    <h2>Research and applied mobility samples</h2>
  </div>
</section>
<section class="sample-grid" aria-label="Work samples">{cards}</section>
<section class="section-grid single-column">
  <div>
    <h2>Publications and presentations</h2>
    <ul class="tight-list">
      <li>Assessing Flight Network Dynamics and Emission Impacts of California's Intra-State Aviation.</li>
      <li>Spatial Distribution Analysis of Aircraft Accident in Airport Safety Zones, FAA NEXTOR III.</li>
      <li>Using street-view imagery to assess urban perception in daily mobility, AAG 2024.</li>
      <li>Modeling the Milpa at Tikal, SAA 2023.</li>
    </ul>
  </div>
</section>
<section class="core-methods" aria-labelledby="core-methods-title">
  <h2 id="core-methods-title">Core methods</h2>
  <div class="skill-cloud">
    <span>ArcGIS</span><span>QGIS</span><span>OSMnx</span><span>NetworkX</span><span>PyTorch</span><span>scikit-learn</span><span>MATSim</span><span>Python</span><span>R</span><span>SQL</span>
  </div>
</section>"""
    return base("Tong(Stone)Shi | CV", body)


def home_page():
    return cv_page()


def chinese_home_page():
    nav = ''.join(
        f'<a href="#{section_id}">{label}</a>'
        for section_id, label in [
            ("about", "研究方向"), ("education", "教育背景"), ("research", "科研经历"),
            ("experience", "项目实践"), ("honors", "成果与荣誉"),
        ]
    )
    body = f'''
<section class="hero zh-hero" id="about">
  <div class="hero-copy">
    <p class="eyebrow">交通工程 · 城市计算 · 人工智能</p>
    <h1 class="zh-title">史桐 <span>Tong (Stone) Shi</span></h1>
    <p class="lead">我关注人工智能如何帮助理解和提升城市交通系统的韧性、可达性与公平性，致力于将交通工程、地理空间分析与以人为本的计算方法结合起来。</p>
    <div class="research-availability zh-availability">
      <p class="availability-label">计划申请</p>
      <p class="availability-term">2027 年秋季博士项目</p>
      <p class="availability-note">研究方向：城市交通韧性、交通网络中的 AI 应用、多模式可达性与空间公平。</p>
    </div>
    <div class="button-row">
      <a class="button primary" href="/static/documents/史桐_高校申请学术简历_简体中文.pdf" download>下载中文学术简历（PDF）</a>
      <a class="button secondary" href="/static/documents/史桐_高校申请学术简历_简体中文.docx" download>下载可编辑简历（Word）</a>
      <a class="button secondary" href="mailto:{PROFILE['email']}">联系我</a>
    </div>
  </div>
  <aside class="profile-panel" aria-label="个人资料">
    <div class="portrait"><img src="/static/images/profile-photo.jpg" alt="史桐毕业照"></div>
    <p class="profile-education"><strong>加州大学伯克利分校</strong> 土木与环境工程硕士（交通工程）<br><strong>加州大学圣巴巴拉分校</strong> 地理信息科学学士</p>
    <div class="profile-links">
      <a href="mailto:{PROFILE['email']}"><img src="/static/icons/envelope.svg" alt="" width="20" height="20"><span>{PROFILE['email']}</span></a>
      <a href="{PROFILE['linkedin']}"><img src="/static/icons/linkedin.svg" alt="" width="20" height="20"><span>LinkedIn</span></a>
      <a href="https://mycraysh.github.io/StoneShiWebsite/"><img src="/static/icons/github.svg" alt="" width="20" height="20"><span>个人主页</span></a>
    </div>
  </aside>
</section>
<section class="section-grid single-column" id="education">
  <div><p class="eyebrow">教育背景</p><h2>以交通工程与空间分析为基础</h2>
  <div class="zh-timeline">
    <article><div><h3>加州大学伯克利分校</h3><p>土木与环境工程理学硕士，交通工程方向</p></div><span>2023.08—2024.05 · GPA 3.2/4.0</span></article>
    <article><div><h3>加州大学圣巴巴拉分校</h3><p>地理信息科学文学学士；辅修建筑与城市史</p></div><span>2019.08—2022.06 · GPA 3.9/4.0</span></article>
  </div></div>
</section>
<section class="section-grid single-column" id="research">
  <div><p class="eyebrow">科研经历</p><h2>从交通网络到社区体验</h2>
  <div class="zh-project-grid">
    <article><span>环境公平 · 加州大学伯克利分校 · 2024—2025</span><h3>加州机场排放与社区社会经济暴露</h3><p>分析 66 座加州机场周边排放的时空分布，结合 GIS、EPA 数据与 CalEnviroScreen 指标，研究航空活动、环境暴露和社区公平问题。</p></article>
    <article><span>交通安全 · Caltrans / NEXTOR III · 2024</span><h3>机场安全区事故空间分布</h3><p>整合 259 座机场的事故记录、跑道与安全区空间数据，运用相对距离和点模式分析，为风险评估与安全区规划提供证据。</p></article>
    <article><span>城市感知 · HuMNet 实验室 · 2023—2024</span><h3>波哥大骑行出行中的城市感知</h3><p>结合街景影像和 PyTorch 感知模型，构建覆盖 9 万余条道路路段的城市环境感知图层，并在 2024 年 AAG 年会上报告相关研究。</p></article>
    <article><span>水文与考古 GIS · UCSB · 2020—2023</span><h3>玛雅低地土地利用与洪水风险</h3><p>带领 9 人 GIS 团队开展蒂卡尔农业周期研究，核验 300 余处水井；另整理 169,776 条 USGS 水文观测，分析河流流量与洪水可能性。</p></article>
  </div></div>
</section>
<section class="section-grid single-column" id="experience">
  <div><p class="eyebrow">项目实践</p><h2>把空间数据与 AI 转化为可用的决策支持</h2>
  <div class="zh-project-grid">
    <article><span>Ditto · 产品经理与提示工程师 · 2025—至今</span><h3>基于 GIS 的地点推荐</h3><p>运用 Python、GeoPandas、GIS 数据和路线 API，设计结合用户偏好、公共交通可达性与无障碍区域信息的推荐流程。</p></article>
    <article><span>Emuser · 产品策略与用户体验 · 项目贡献 · 2025—2026</span><h3>AI 求职经历档案与申请辅助</h3><p>参与规划以个人经历档案为基础的职业智能体，梳理网页应用与浏览器扩展的交互流程、用户控制模式、匹配透明度及资料一致性要求。</p></article>
    <article><span>交通韧性与多智能体研究</span><h3>模拟网络中断下的出行决策</h3><p>结合 GIS、网络科学与大语言模型智能体，探索乘客和运营方如何应对交通中断，为城市多模式交通系统的韧性评估建立可解释的分析框架。</p></article>
  </div></div>
</section>
<section class="section-grid single-column" id="honors">
  <div><p class="eyebrow">成果与荣誉</p><h2>学术报告、研究成果与奖项</h2>
  <ul class="tight-list zh-honors">
    <li>加州大学伯克利分校院系奖学金（2024，25,000 美元）及 Student Opportunity Fund（2023）。</li>
    <li>AAG GISS 学生荣誉论文竞赛二等奖（2023）；研究成果发表于 SAA、AAG 年会报告。</li>
    <li>加州大学圣巴巴拉分校地理专业优秀成就奖、学院荣誉奖（2022）。</li>
    <li>研究方法：ArcGIS、QGIS、Python、GeoPandas、OSMnx、NetworkX、PyTorch、MATSim、R、SQL。</li>
  </ul></div>
</section>'''
    return base("史桐｜交通工程与城市计算", body, language="zh", nav_items=nav)


def latex_cv_section():
    return (ROOT / "cv_fragment.html").read_text(encoding="utf-8")


def legacy_latex_cv_section():
    return """
<section class="latex-cv" aria-label="LaTeX formatted CV">
  <div class="latex-paper">
    <header class="latex-header">
      <h2>Tong (Stone) Shi</h2>
      <p>(+1) 805-280-6424 | <a href="mailto:tongshi@berkeley.edu">tongshi@berkeley.edu</a> | <a href="https://linkedin.com/in/stoneshiucb">linkedin.com/in/stoneshiucb</a> | <a href="https://github.com/camel-ai/oasis">github.com/camel-ai/oasis</a></p>
    </header>

    <section>
      <h3>Research Profile</h3>
      <p>Transportation engineering and GIS researcher focused on transportation accessibility, travel behavior, environmental justice, airport systems, and multi-agent simulation. My work connects spatial data science, human mobility, network resilience, and AI-based behavioral modeling to study how people experience, adapt to, and are affected by transportation systems.</p>
    </section>

    <section>
      <h3>Education</h3>
      <p><strong>University of California, Berkeley</strong><span>Aug 2023 - May 2024</span><br>M.S. in Civil and Environmental Engineering, Transportation Engineering | GPA: 3.2/4.0</p>
      <p><strong>University of California, Santa Barbara</strong><span>Aug 2019 - Jun 2022</span><br>B.A. in Geographical Information Science | Minor in Architecture and Urban History | GPA: 3.9/4.0</p>
    </section>

    <section>
      <h3>Publications and Presentations</h3>
      <ul>
        <li>Kondo, G., <strong>Shi, S.</strong>, Anfaresi, N., and Rakas, J. (2025). Assessing Flight Network Dynamics and Emission Impacts of California's Intra-State Aviation: A Study on Environmental Justice and Air Traffic Network. Preparing for submission.</li>
        <li>Lindbergh, S., <strong>Shi, S.</strong>, and Rakas, J. (2024). Spatial Distribution Analysis of Aircraft Accident in Airport Safety Zones. FAA NEXTOR III, UC Berkeley.</li>
        <li><strong>Shi, S.</strong>, Wang, R., and Gonzalez, M. (2024). How does my cognition change on the roadway? Using street view imageries to assess urban perception in human daily mobility. 2024 AAG Annual Meeting.</li>
        <li><strong>Shi, S.</strong>, Kresse, M., Moran, T., Ford, A., and Carr, R. (2023). Modeling the Milpa at Tikal: New dimensions of the Carr and Hazard map. 88th SAA Annual Meeting.</li>
        <li><strong>Shi, S.</strong>, Ramirez, A., and Ford, A. (2023). Visualize Sustainable Land Use in the Tropical Maya Forest: Revitalizing the Old Tikal Map for New Geospatial Analyses. 2023 AAG Annual Meeting.</li>
      </ul>
    </section>

    <section>
      <h3>Honors and Awards</h3>
      <ul>
        <li>Departmental Fellowship, UC Berkeley ($25,000), 2024</li>
        <li>Student Opportunity Fund, UC Berkeley ($1,350), 2023</li>
        <li>Second Place, AAG GISS Student Honor Paper Competition, 2023</li>
        <li>Academic Excellence Award, UCSB College of Letters and Science, 2022</li>
        <li>Outstanding Achievement in Geography Major, 2022</li>
        <li>High Honors, UCSB College of Letters and Science, 2022</li>
        <li>Dean's Honors, UCSB, five semesters</li>
      </ul>
    </section>

    <section>
      <h3>Skills</h3>
      <p><strong>GIS:</strong> ArcGIS Suite, QGIS, ENVI, Google Earth Engine, OpenStreetMap, AutoCAD, Civil3D</p>
      <p><strong>Transportation and Network Modeling:</strong> MATSim, SUMO, NetworkX, OSMnx, PyTorch, scikit-learn, SimPy, route-choice optimization, agent-based modeling</p>
      <p><strong>Accessibility and Behavior Analysis:</strong> travel behavior modeling, multimodal accessibility, urban perception, spatial equity, safety-zone analysis, emission exposure mapping</p>
      <p><strong>Coding and Data:</strong> Python, JavaScript, R, SQL, GeoPandas, pandas, spatial statistics, machine-learning workflows</p>
      <p><strong>Cloud and Visualization:</strong> AWS, Azure, Google Cloud, Git, Tableau</p>
      <p><strong>Languages:</strong> English, Chinese, Spanish, German</p>
    </section>

    <section>
      <h3>Research Experience</h3>
      <p><strong>Modeling Transit Decision Under Network Disruptions by LLM Multi-Agent</strong><span>Nov 2024 - ongoing</span><br>Lead Scientist | CAMEL-AI</p>
      <ul>
        <li>Built a large-scale LLM-driven multi-agent system with up to one million agents to evaluate multimodal transit resilience under sudden rail and bus disruptions.</li>
        <li>Designed GIS-based transportation models integrating Chicago demographic context, congestion metrics, transit hubs, and route-choice optimization.</li>
        <li>Implemented traffic coordination agents that adjust schedules, assignments, and traveler alternatives to study crowding, delay, and accessibility impacts.</li>
        <li>Integrated PyMATSim, NetworkX, and OSMnx for forecasting and compared LLM decision-making with traditional agent-based simulation behavior.</li>
        <li>Positioned the project as a behavioral analysis framework for understanding how travelers respond to uncertainty, service loss, and network stress.</li>
      </ul>
      <p><strong>Assessing the Socioeconomic Exposure of Emissions at California Airports</strong><span>Jan 2024 - Oct 2025</span><br>Project Leader | Institute of Transportation Studies, UC Berkeley</p>
      <ul>
        <li>Conducted comprehensive spatiotemporal distribution analysis of emissions from 66 California airports to evaluate exposure for nearby communities.</li>
        <li>Used GIS overlay, accessibility-style catchment analysis, and machine-learning workflows to examine emission diffusion trends and environmental justice impacts.</li>
        <li>Connected air traffic network dynamics with airport-adjacent socioeconomic conditions to identify where operational changes could reduce unequal burdens.</li>
        <li>Developed sustainable airport management strategies by integrating safety-zone analysis, emission exposure, and long-term planning considerations.</li>
      </ul>
      <p><strong>Enhancing Airport Safety through Spatial Distribution of Accidents</strong><span>Jan 2024 - Jul 2024</span><br>Research Assistant | Caltrans and NEXTOR III</p>
      <ul>
        <li>Conducted spatial analysis of accident locations across 259 California airports and evaluated risk patterns against airport safety-zone thresholds.</li>
        <li>Integrated National Transportation Safety Board accident records with digitized runway and safety-zone geometries.</li>
        <li>Applied relative-distance calculations, triangulation, and point-pattern analysis to identify clustering near runway lines and safety-zone boundaries.</li>
        <li>Produced statistical and geospatial evidence to support decisions on safety-zone dimensions, land-use compatibility, and airport risk management.</li>
      </ul>
      <p><strong>Discovering Urban Perception in Human Biking Mobility: Bogota</strong><span>Sep 2023 - Apr 2024</span><br>Project Leader | HuMNet Lab, UC Berkeley</p>
      <ul>
        <li>Used PyTorch and Google Street View imagery to improve urban perception sensing models for bicycle mobility and roadway cognition analysis.</li>
        <li>Led development of citywide perception layers across more than 90,000 road segments to evaluate comfort, safety, and behavioral response in cycling environments.</li>
        <li>Connected street-level visual features with human mobility data to understand how perceived urban form influences route experience.</li>
        <li>Presented the research at the 2024 American Association of Geographers Annual Meeting.</li>
      </ul>
      <p><strong>Modeling the Milpa Cycle and Labor Density at the Tikal Site</strong><span>Oct 2021 - Apr 2023</span><br>Laboratory Manager | MesoAmerican Research Center, UCSB</p>
      <ul>
        <li>Supervised a nine-person GIS team and digitized hydrological networks for the Tikal site in Guatemala.</li>
        <li>Created watershed models and verified more than 300 well locations using archaeological records and DEM data.</li>
        <li>Conducted field investigation of monuments and rotating cultivation practices across four Maya lowland settlements.</li>
        <li>Built local water-supply and crop-yield models to support population and labor-density estimates.</li>
        <li>Presented related work at the 2023 AAG Annual Meeting and received second place in the AAG GISS Student Honor Paper Competition.</li>
      </ul>
      <p><strong>Predicting Flood Likelihood of U.S. Major Streamflow by Time Intervals</strong><span>Nov 2020 - Apr 2021</span><br>Undergraduate Research Assistant | Hydro Research Group, UCSB</p>
      <ul>
        <li>Modeled flood likelihood for major streamflow in the contiguous United States and simulated future trends with machine-learning workflows.</li>
        <li>Built an RShiny dataset of historical streamflow records organized by recurrence intervals from 1 to 50 years.</li>
        <li>Compiled a recurrence-interval data frame with 169,776 observations across USGS monitoring sites.</li>
        <li>Generated a database to simulate nationwide flood trends over 2-to-100-year horizons and communicated results through Tableau and RMarkdown.</li>
      </ul>
    </section>

    <section>
      <h3>Work Experience</h3>
      <p><strong>Ditto</strong> | Product Manager, Prompt Engineer <span>Feb 2025 - ongoing</span></p>
      <ul>
        <li>Built a GIS-driven dating-location search system using Python, GeoPandas, ArcGIS, QGIS, and routing APIs to optimize suggestions by mobility patterns, transit access, and accessibility zones.</li>
        <li>Designed a preference-exclusion algorithm using multi-agent representations of deal-breakers and compatibility thresholds, reducing irrelevant suggestions by more than 40 percent.</li>
        <li>Engineered prompts to align AI agents with location-based user behavior, scenario planning, and real-time accessibility features for more than 20,000 California users.</li>
      </ul>
      <p><strong>TossTo.ai</strong> | Founder, Product Manager <span>Nov 2023 - Jan 2025</span></p>
      <ul>
        <li>Led product prototype design, beta rollout, early-user interviews, and investor-facing feedback cycles.</li>
        <li>Developed an LLM-agent concept for travel and dining experiences from more than 30 primary user interviews.</li>
        <li>Designed POI recommendation algorithms for real-time AI-enhanced user experiences, connecting location preference, context, and destination behavior.</li>
      </ul>
      <p><strong>YoMio BEYOUNG Co., Ltd.</strong> | Co-Founder, Product Manager <span>Jan 2024 - ongoing</span></p>
      <ul>
        <li>Led a four-person team building an end-to-end GenAI agent-based toy for the video game ZeroEra, scaling deployment to more than 6,000 users.</li>
        <li>Developed a retrieval-augmented generation framework for product definition using more than one million tokens of ACG brand and user-preference knowledge.</li>
        <li>Collected more than 50,000 user-preference signals from online forums and interest groups to define personas for ACG enthusiasts aged 14-30 in the Asia-Pacific region.</li>
      </ul>
    </section>

    <section>
      <h3>PhD Research Fit</h3>
      <p>I am seeking a transportation accessibility and behavior analysis PhD position where I can study how infrastructure, service disruptions, perception, and environmental exposure shape mobility decisions. My preparation combines civil and environmental engineering, GIS, human mobility analytics, and AI-based agent modeling, with an emphasis on producing interpretable tools for planning agencies and transportation researchers.</p>
    </section>
  </div>
</section>"""


def work_page(slug):
    sample = next((item for item in WORK_SAMPLES if item["slug"] == slug), None)
    if sample is None:
        return None
    details = "".join(f"<li>{escape(item)}</li>" for item in sample["details"])
    methods = "".join(f"<span>{escape(item)}</span>" for item in sample["methods"])
    body = f"""
<article class="detail">
  <a class="back-link" href="/cv">Back to CV</a>
  <p class="eyebrow">{escape(sample['tag'])} · {escape(sample['period'])}</p>
  <h1>{escape(sample['title'])}</h1>
  <p class="lead">{escape(sample['summary'])}</p>
  <div class="paper-preview">
    <section>
      <h2>Paper Preview</h2>
      <p>This preview summarizes the research question, technical approach, and applied transportation or geospatial value of the work sample.</p>
      <ul>{details}</ul>
    </section>
    <aside>
      <h2>Methods</h2>
      <div class="skill-cloud">{methods}</div>
    </aside>
  </div>
</article>"""
    return base(f"{sample['title']} | Tong (Stone) Shi", body)


def cover_letter_page():
    body = """
<article class="document-page">
  <p class="eyebrow">General-use cover letter</p>
  <h1>Cover Letter</h1>
  <p class="lead">Adapted from the supplied cover-letter sample with firm-specific language removed.</p>
  <div class="letter">
    <p>Dear Hiring Committee,</p>
    <p>I am writing to express my interest in transportation, GIS, planning, and data-driven mobility roles where I can apply my background in geospatial analysis, airport systems, multimodal transportation, and AI-assisted modeling. My graduate training at UC Berkeley and research experience across aviation, urban mobility, hydrology, and archaeological GIS have prepared me to work across technical analysis, project coordination, and product-facing communication.</p>
    <p>At UC Berkeley, I studied transportation engineering and led research on California airport emissions, aircraft accident distributions in airport safety zones, and urban perception in cycling mobility. These projects required rigorous GIS workflows, data cleaning, spatial statistics, machine-learning support, and clear visual communication for technical and policy audiences. I also contribute to OASIS-based LLM multi-agent transportation simulation, where I model passenger decisions under network disruptions and connect demographic, congestion, and routing data into large-scale mobility experiments.</p>
    <p>In product and startup work, I have translated location intelligence into practical systems, including a GIS-driven dating-location search system, POI recommendation workflows, and prompt-engineered agent experiences. These roles strengthened my ability to define user needs, coordinate teams, and turn complex spatial data into tools that support decisions.</p>
    <p>I would bring strong GIS judgment, transportation-domain knowledge, Python-based analysis skills, and an interdisciplinary research perspective to your team. I would welcome the opportunity to discuss how my background can support your planning, analytics, product, or infrastructure work.</p>
    <p>Sincerely,<br>Tong (Stone) Shi</p>
  </div>
  <div class="embed-panel">
    <h2>Original reference PDF</h2>
    <object data="/static/documents/source-cover-letter-ferrovial.pdf" type="application/pdf">
      <a href="/static/documents/source-cover-letter-ferrovial.pdf">Open the source cover-letter PDF</a>
    </object>
  </div>
</article>"""
    return base("General Cover Letter | Tong (Stone) Shi", body)


def research_proposal_page():
    body = """
<article class="document-page">
  <p class="eyebrow">Research interest proposal</p>
  <h1>Mobility Resilience, Environmental Justice, and Human-Centered Transportation AI</h1>
  <p class="lead">A concise research agenda connecting transportation networks, GIS, environmental exposure, and multi-agent simulation.</p>
  <div class="proposal-grid">
    <section>
      <h2>Research Direction</h2>
      <p>My research interest focuses on how transportation systems behave under disruption and how their impacts are distributed across communities. I am especially interested in linking GIS, aviation and transit networks, environmental justice, and LLM-driven multi-agent simulation to evaluate decisions before they become real-world consequences.</p>
    </section>
    <section>
      <h2>Core Questions</h2>
      <ul>
        <li>How do travelers adjust route, mode, timing, and destination choices when networks are disrupted?</li>
        <li>How can airport and transit operations reduce unequal exposure to emissions, congestion, and safety risks?</li>
        <li>How can LLM agents be benchmarked against traditional agent-based models for credible transportation planning?</li>
      </ul>
    </section>
    <section>
      <h2>Methods</h2>
      <p>The proposal combines spatial statistics, network science, geospatial machine learning, street-view perception modeling, emission exposure analysis, and large-scale agent simulation. Python, GIS, OSMnx, NetworkX, PyTorch, and MATSim-style workflows form the technical backbone.</p>
    </section>
    <section>
      <h2>Expected Contribution</h2>
      <p>This agenda aims to produce decision-support models for resilient multimodal systems, sustainable airport planning, and equitable infrastructure investment. The practical goal is to help agencies and researchers test policy alternatives with transparent assumptions and community-centered metrics.</p>
    </section>
  </div>
  <div class="embed-panel">
    <h2>Research statement PDF</h2>
    <object data="/static/documents/research-statement.pdf" type="application/pdf">
      <a href="/static/documents/research-statement.pdf">Open the research statement PDF</a>
    </object>
  </div>
</article>"""
    return base("Research Interest Proposal | Tong (Stone) Shi", body)


class PortfolioHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        parsed = urlparse(path)
        clean_path = unquote(parsed.path)
        if clean_path.startswith("/static/"):
            relative = clean_path.removeprefix("/static/")
            return str((STATIC_ROOT / relative).resolve())
        return str(ROOT / "index.html")

    def send_html(self, html, status=200):
        encoded = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/") or "/"
        if path.startswith("/static/"):
            return super().do_GET()
        if path == "/":
            return self.send_html(home_page())
        if path == "/zh":
            return self.send_html(chinese_home_page())
        if path == "/cv":
            return self.send_html(cv_page())
        if path == "/cover-letter":
            return self.send_html(cover_letter_page())
        if path == "/research-proposal":
            return self.send_html(research_proposal_page())
        if path == "/statement-of-purpose":
            return self.send_html(application_page("sop", base))
        if path == "/personal-statement":
            return self.send_html(application_page("personal", base))
        if path.startswith("/work/"):
            html = work_page(path.removeprefix("/work/"))
            if html:
                return self.send_html(html)
        return self.send_html(base("Page not found", "<h1>Page not found</h1>"), status=404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), PortfolioHandler)
    print(f"Serving Tong(Stone)Shi CV website at http://127.0.0.1:{port}")
    server.serve_forever()
