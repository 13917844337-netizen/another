import dash
from dash import dcc, html, Input, Output, State, ALL
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import os
import random
# ==================== 0. Base64 图片读取与统一居中排版函数 ====================
def get_image_base64(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'assets', filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
    print(f"⚠️ [未找到图片文件]: {filepath}")
    return ""
def make_img_html(filenames, max_height="220px"):
    if isinstance(filenames, str):
        filenames = [filenames]
    imgs_html = []
    for fn in filenames:
        b64_str = get_image_base64(fn)
        if b64_str:
            imgs_html.append(
                f'<img src="{b64_str}" style="max-width: 48%; max-height: {max_height}; object-fit: contain; border-radius: 6px; border: 1px solid #cbd5e1;" />'
            )
    if not imgs_html:
        return ""
    joined_imgs = "".join(imgs_html)
    return f'<div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-top: 20px; flex-wrap: wrap;">{joined_imgs}</div>'
# ==================== 1. 全球篮球传播数据源 ====================
start_pt = {"name": "Springfield College, USA", "lat": 42.1015, "lon": -72.5898, "year": 1891}
history_data = [
    {
        "id": 0, "country_code": "FRA", "name": "France", "display_name": "France", "lat": 48.8566, "lon": 2.3522,
        "color": "#d97706", "start_year": 1893,
        "leader": "Mel Rideout / Renato William Jones / Tony Parker / Victor Wembanyama",
        "photo": "tony_parker.png",
        "sections": {
            "origin": "<b>1. Origin & Early Introduction (1893):</b><br>"
                      "Basketball made its historic European debut in Paris, France, on December 27, 1893. Mel Rideout, an American graduate of Springfield College, introduced the game at the newly constructed Union Chrétienne de Jeunes Gens (YMCA) gymnasium located on Rue de Trévise in Paris.<br><br>"
                      "The gym featured wooden parquet floors and running tracks, mirroring Naismith's original indoor vision. Today, the court on Rue de Trévise stands as the world's oldest continuously operating indoor basketball venue, serving as a historic shrine for international basketball culture.",
            "leagues": "<b>2. Institutional Development & Professional Leagues:</b><br>"
                       "During World War I (1917–1919), Dr. James Naismith served in France as a YMCA war work secretary, organizing matches to promote physical welfare among Allied troops. In 1932, the International Basketball Federation (FIBA) was established, with French basketball leaders playing an instrumental founding role alongside Renato William Jones.<br><br>"
                       "The Fédération Française de Basketball (FFBB) was officially founded in 1932 to govern national competitions. In 1987, France modernized its elite structure by establishing LNB Pro A (now Élite), which grew into one of Europe's top professional basketball domestic leagues.",
            "culture": "<b>3. Local Culture & Grassroots Impact:</b><br>"
                       "France pioneered a world-class national sports development framework anchored by INSEP (Institut National du Sport, de l'Expertise et de la Performance) in Paris. This elite institute integrates education with top-tier athletic training, producing dozens of international pros.<br><br>"
                       "Urban basketball thrives across French cities, from famous playground courts in Paris (such as Pigalle Duperré) to thriving youth development academies in Lyon, Marseille, and Gravelines, bridging diverse multicultural communities through hoops.",
            "figures": "<b>4. Key Pioneers & Global Figures:</b><br>"
                       "• <b>Mel Rideout & R. William Jones:</b> Transatlantic pioneers and FIBA co-founders.<br>"
                       "• <b>Tony Parker:</b> Naismith Hall of Famer, 4-time NBA Champion, and 2007 Finals MVP with the San Antonio Spurs.<br>"
                       "• <b>Boris Diaw & Rudy Gobert:</b> Diaw (NBA Champion) and Gobert (4-time NBA Defensive Player of the Year).<br>"
                       "• <b>Victor Wembanyama:</b> Generational prodigy, #1 overall pick in the 2023 NBA Draft, and 2024 NBA Rookie of the Year."
                       + make_img_html("Wemby.png"),
            "modern": "<b>5. Modern Era & Contemporary Achievements:</b><br>"
                      "France has solidified its reputation as the chief international challenger to Team USA. The national team claimed Silver Medals at both the Tokyo 2020 and Paris 2024 Olympic Games.<br><br>"
                      "In the 2024 NBA Draft, French basketball made unprecedented history by capturing the top two overall draft picks: Zaccharie Risacher (#1) and Alexandre Sarr (#2), demonstrating France's dominant global talent pipeline."
                      + make_img_html("team_France.png")
        }
    },
    {
        "id": 1, "country_code": "GBR", "name": "United Kingdom", "display_name": "UK", "lat": 51.5074, "lon": -0.1278,
        "color": "#dc2626", "start_year": 1894,
        "leader": "Dr. James Naismith / Martina Bergman-Österberg / Luol Deng",
        "photo": "uk.png",
        "sections": {
            "origin": "<b>1. Origin & Early Introduction (1894):</b><br>"
                      "Basketball arrived in Great Britain in 1894, barely three years after its invention. American YMCA physical training instructors demonstrated the sport at physical education colleges in London and Birkenhead.<br><br>"
                      "The game gained rapid popularity among physical education instructors across Victorian England as an ideal structured indoor athletic activity for harsh British winters.",
            "leagues": "<b>2. Evolutionary Adaptation — The Birth of Netball:</b><br>"
                       "Due to strict Victorian social etiquette and restrictive clothing for women, physical educator Martina Bergman-Österberg and local instructors modified Naismith's original 13 rules in the late 1890s. Dribbling was eliminated, backboards were removed, and movement was restricted to designated court zones.<br><br>"
                       "This adaptation evolved into <i>Netball</i>, receiving its first official rulebook in 1901. Netball expanded across the British Empire and Commonwealth, becoming one of the most popular female team sports globally.",
            "culture": "<b>3. Institutionalization & Professional Leagues:</b><br>"
                       "The Basketball Association of Great Britain was established in 1936 ahead of the Berlin Olympics. The professional British Basketball League (BBL) ran from 1987 to 2024, providing structured professional competition.<br><br>"
                       "In 2024, British basketball underwent major structural reform, launching Premier Super League Basketball (SLB) to unify professional franchises, media distribution, and youth development infrastructure."
                       + make_img_html("BBL.png"),
            "figures": "<b>4. Key Pioneers & Global Figures:</b><br>"
                       "• <b>Martina Bergman-Österberg:</b> Pioneer who adapted basketball into Netball.<br>"
                       "• <b>Luol Deng:</b> Two-time NBA All-Star, Olympian, and leader of South Sudan Basketball Federation.<br>"
                       "• <b>Pops Mensah-Bonsu & Jeremy Sochan:</b> Mensah-Bonsu (NBA player and executive) and Sochan (San Antonio Spurs forward)."
                       + make_img_html("Luol_Deng.png"),
            "modern": "<b>5. Modern Era & Grassroots Expansion:</b><br>"
                      "While Netball remains dominant in female school curricula, men's basketball has built strong grassroots roots in London, Manchester, and Birmingham.<br><br>"
                      "British players increasingly secure Division I NCAA scholarships and EuroLeague roster spots, while Great Britain Basketball regularly competes in European Continental Championships (EuroBasket)."
        }
    },
    {
        "id": 3, "country_code": "CHN", "name": "China", "display_name": "China", "lat": 39.9042, "lon": 116.4074,
        "color": "#059669", "start_year": 1895,
        "leader": "David Willard Lyon / Dong Shouyi / Yao Ming / Zheng Haixia",
        "photo": "china.png",
        "sections": {
            "origin": "<b>1. Origin & Early Introduction (1895):</b><br>"
                      "David Willard Lyon, the first official representative of the International YMCA in China, introduced basketball to Tianjin in late 1895. The first public demonstration match in Asia took place in Tianjin on January 11, 1896.<br><br>"
                      "By 1910, basketball was featured as an exhibition event at the 1st Chinese National Games in Nanjing, quickly embedding itself in middle school and university physical education curricula across East Asia.",
            "leagues": "<b>2. Institutionalization & Elite League Structure:</b><br>"
                       "Pioneer educator Dong Shouyi published China's earliest basketball technical textbooks and coached the national squad at the 1936 Berlin Olympics.<br><br>"
                       "Following 1949, the Chinese Basketball Association (CBA) was formed. The professional Chinese Basketball Association Professional League (CBA League) launched in 1995, evolving alongside the WCBA (women's league) and CUBAL (university system)."
                       + make_img_html("CBA_allstar.png"),
            "culture": "<b>3. Local Culture & Grassroots Explosion:</b><br>"
                       "Basketball is one of the most played sports in China, boasting hundreds of millions of active participants and fans. Beyond top tier megacities like Shanghai and Beijing, basketball is deeply woven into rural culture.<br><br>"
                       "Events like the 'Village BA' (CunBA) in Taipan Village, Guizhou Province, attract tens of thousands of live rural spectators and multi‑million livestream views, celebrating grassroots sports passion."
                       + make_img_html("village.png"),
            "figures": "<b>4. Key Pioneers & Global Icons:</b><br>"
                       "• <b>Dong Shouyi:</b> Pioneer educator and Olympic delegate.<br>"
                       "• <b>Zheng Haixia:</b> WNBA pioneer, 1992 Olympic Silver Medalist, and FIBA Hall of Famer.<br>"
                       "• <b>Yao Ming:</b> #1 Overall NBA Draft Pick in 2002, 8‑time NBA All‑Star, Naismith Hall of Famer, and former CBA President who transformed basketball into a cultural bridge between China and the US.",
            "modern": "<b>5. Modern Era & Global Exchange:</b><br>"
                      "China hosted the 2019 FIBA Basketball World Cup across eight host cities. The national women's team achieved world prominence by claiming the Silver Medal at the 2022 FIBA Women's World Cup.<br><br>"
                      "Basketball remains a key engine of youth culture, digital sports media, and international athletic diplomacy across Asia."
                      + make_img_html("team_China.png")
        }
    },
    {
        "id": 2, "country_code": "DEU", "name": "Germany", "display_name": "Germany", "lat": 52.5200, "lon": 13.4050,
        "color": "#7c3aed", "start_year": 1896,
        "leader": "Dr. James Naismith / Dirk Nowitzki / Dennis Schröder",
        "photo": "Dirk.png",
        "sections": {
            "origin": "<b>1. Origin & Early Introduction (1896):</b><br>"
                      "Basketball reached Germany in the late 1890s through physical training educators returning from American YMCA conventions. Initial adoption was gradual as it competed with traditional German gymnastics (Turnen).<br><br>"
                      "However, university physical education departments recognized its tactical value, progressively incorporating indoor hoops into winter academic physical programs.",
            "leagues": "<b>2. 1936 Berlin Olympic Milestone & League Genesis:</b><br>"
                       "The 1936 Berlin Olympic Games marked the monumental debut of basketball as an official Olympic medal sport. Founder Dr. James Naismith personally tossed the ceremonial first tip‑off in outdoor rain.<br><br>"
                       "The Deutscher Basketball Bund (DBB) was founded in 1949, and the Basketball Bundesliga (BBL) was established in 1966, building professional club structures across West and East Germany.",
            "culture": "<b>3. Local Culture & Professional Academy System:</b><br>"
                       "Germany developed one of Europe's most efficient sports club models (such as ALBA Berlin, FC Bayern Munich, and Brose Bamberg).<br><br>"
                       "These multi‑sport clubs run accredited youth academies (NBBL/JBBL), pairing elite basketball coaching with formal academic education to produce well‑rounded professional athletes.",
            "figures": "<b>4. Key Pioneers & Global Legends:</b><br>"
                       "• <b>Dirk Nowitzki:</b> 2011 NBA Champion, 2007 NBA MVP, 14‑time NBA All‑Star, and Naismith Hall of Famer widely regarded as the greatest European player in NBA history.<br>"
                       "• <b>Dennis Schröder:</b> World Cup MVP and national team leader.<br>"
                       "• <b>Franz Wagner & Moritz Wagner:</b> Key contributors to Germany's international resurgence."
                       + make_img_html("Schröder.png"),
            "modern": "<b>5. Modern Era & World Championship Glory:</b><br>"
                      "German basketball reached its historical zenith in 2023 by capturing an undefeated Gold Medal at the 2023 FIBA Basketball World Cup in Manila, defeating the USA and Serbia.<br><br>"
                      "This historic victory, followed by a strong 4th‑place finish at the Paris 2024 Olympics, ushered in a golden era for German athletic culture."
                      + make_img_html("Germany2.png")
        }
    },
    {
        "id": 4, "country_code": "BRA", "name": "Brazil", "display_name": "Brazil", "lat": -23.5505, "lon": -46.6333,
        "color": "#2563eb", "start_year": 1900,
        "leader": "Augusto Shaw / Oscar Schmidt / Wlamir Marques",
        "photo": "brazil.png",
        "sections": {
            "origin": "<b>1. Origin & Early Introduction (1900):</b><br>"
                      "Augusto Shaw, an American professor and Yale University graduate, introduced basketball to Mackenzie College in São Paulo in 1896–1900. Brazil became the first nation in South America to embrace basketball.<br><br>"
                      "Despite initial resistance from football enthusiasts, Shaw organized collegiate matches, establishing a strong university basketball foundation.",
            "leagues": "<b>2. Institutional Development & Early World Dominance:</b><br>"
                       "The Confederação Brasileira de Basketball (CBB) was established in 1933. Brazil swiftly established itself as an early global giant, winning back‑to‑back FIBA World Championship Gold Medals in 1959 (Chile) and 1963 (Rio de Janeiro).<br><br>"
                       "In 2008, the modern Novo Basquete Brasil (NBB) was launched, revitalizing professional club competition across South America.",
            "culture": "<b>3. Local Culture & Historical Pan‑Am Victory:</b><br>"
                       "Basketball holds a revered status in Brazilian athletic history. In the 1987 Pan American Games Gold Medal match in Indianapolis, Brazil pulled off one of the greatest upsets in sports history.<br><br>"
                       "Led by Oscar Schmidt's 46 points, Brazil defeated Team USA 120–115, marking the first time the US men's national team lost on home soil.",
            "figures": "<b>4. Key Pioneers & Global Legends:</b><br>"
                       "• <b>Augusto Shaw:</b> South American basketball pioneer.<br>"
                       "• <b>Wlamir Marques:</b> Two‑time World Champion and FIBA Hall of Famer.<br>"
                       "• <b>Oscar Schmidt ('Mão Santa'):</b> The all‑time leading scorer in Olympic basketball history (1,093 points across 5 Olympics) and Naismith Hall of Famer.<br>"
                       "• <b>Tiago Splitter, Barbosa & Nenê:</b> Key NBA champions and veterans.",
            "modern": "<b>5. Modern Era & Regional Leadership:</b><br>"
                      "Brazil continues to serve as the dominant force in South American basketball, maintaining regular presence in FIBA World Championships and sending talent to top NBA and EuroLeague clubs."
                      + make_img_html("brazil_FIBA.png")
        }
    },
    {
        "id": 9, "country_code": "AUS", "name": "Australia", "display_name": "Australia", "lat": -37.8136, "lon": 144.9631,
        "color": "#16a34a", "start_year": 1905,
        "leader": "Andrew Gaze / Luc Longley / Patty Mills / Josh Giddey / Lauren Jackson",
        "photo": "australia.png",
        "sections": {
            "origin": "<b>1. Origin & Early Introduction (1905):</b><br>"
                      "Basketball reached Australia in February 1905 when YMCA physical directors introduced the sport in Melbourne and Sydney.<br><br>"
                      "It gained immediate traction across schools and local community clubs, providing a fast‑paced team activity during winter sports off‑seasons.",
            "leagues": "<b>2. Institutionalization & National Leagues (NBL / WNBL):</b><br>"
                       "The Australian Basketball Federation (now Basketball Australia) was formed in 1939. In 1979, the National Basketball League (NBL) was established, followed by the Women's National Basketball League (WNBL) in 1981.<br><br>"
                       "The NBL has since evolved into one of the highest quality professional domestic leagues outside North America, featuring the Next Stars player pathway program."
                       + make_img_html("NBL.png"),
            "culture": "<b>3. Australian Institute of Sport (AIS) & Grassroots Pipeline:</b><br>"
                       "Australia built one of the world's premier sports development models via the Australian Institute of Sport (AIS) Centre of Excellence in Canberra.<br><br>"
                       "The AIS system has systematically identified and trained top athletic talents, producing dozens of NBA and WNBA stars while fostering thriving participation at community centers statewide.",
            "figures": "<b>4. Key Pioneers & Global Legends:</b><br>"
                       "• <b>Andrew Gaze:</b> 5‑time Olympian, FIBA Hall of Famer, and legendary scorer.<br>"
                       "• <b>Luc Longley:</b> First Australian to play in the NBA, winning 3 consecutive championships with the Chicago Bulls (1996–1998).<br>"
                       "• <b>Josh Giddey:</b> Versatile young playmaker and elite NBA talent leading the next generation of Boomers.<br>"
                       "• <b>Lauren Jackson:</b> 3‑time WNBA MVP, 7‑time WNBA All‑Star, and Naismith Hall of Famer.<br>"
                       "• <b>Patty Mills & Joe Ingles:</b> Cultural leaders of the national squad ('Boomers')."
                       + make_img_html("Giddey.png"),
            "modern": "<b>5. Modern Era & Bronze Medal Milestone:</b><br>"
                      "Australian basketball hit a monumental milestone at the Tokyo 2020 Olympics, where the Boomers captured their historic first Olympic Bronze Medal.<br><br>"
                      "With elite young talent flourishing in both the NBA and WNBA, Australia stands firmly as an international basketball powerhouse."
                      + make_img_html("team_Aus.png")
        }
    },
    {
        "id": 5, "country_code": "PHL", "name": "Philippines", "display_name": "Philippines", "lat": 14.5995, "lon": 120.9842,
        "color": "#b45309", "start_year": 1898,
        "leader": "Dionisio Calvo / Carlos Loyzaga / Jordan Clarkson",
        "photo": "philippines.png",
        "sections": {
            "origin": "<b>1. Origin & Early Introduction (1898):</b><br>"
                      "Following the arrival of American administration in 1898, basketball was introduced into the Philippine public school system and YMCA athletic programs.<br><br>"
                      "Its fast pace, team dynamic, and minimal equipment requirements resonated immediately with local youth, quickly transforming into a national obsession across the archipelago.",
            "leagues": "<b>2. Asia's First Professional League (PBA):</b><br>"
                       "In 1975, the Philippine Basketball Association (PBA) was founded, becoming the first professional basketball league in Asia and the second oldest continuous professional league in the world after the NBA.<br><br>"
                       "The sport is today governed by the Samahang Basketbol ng Pilipinas (SBP), which manages collegiate leagues like UAAP and NCAA Philippines.",
            "culture": "<b>3. Unrivaled Grassroots Hoop Culture:</b><br>"
                       "Basketball is practically a religion in the Philippines. Makeshift hoops made of repurposed wood and metal hoops line narrow urban alleys (barangays) and rural coastal villages nationwide.<br><br>"
                       "Flip‑flop basketball (playing barefoot or in sandals) is iconic, demonstrating an unparalleled passion for the game across all economic strata.",
            "figures": "<b>4. Key Pioneers & Global Figures:</b><br>"
                       "• <b>Dionisio Calvo:</b> Coached the national team to a 5th‑place finish at the 1936 Berlin Olympics (highest Olympic finish by an Asian nation in history).<br>"
                       "• <b>Carlos Loyzaga ('The Great Difference'):</b> Led the Philippines to a historic Bronze Medal at the 1954 FIBA World Championship and FIBA Hall of Fame inductee.<br>"
                       "• <b>Jordan Clarkson:</b> NBA Sixth Man of the Year winner and Gilas Pilipinas star."
                       + make_img_html("Jordan_Clarkson.png"),
            "modern": "<b>5. Modern Era & Co‑Hosting 2023 FIBA World Cup:</b><br>"
                      "The Philippines co‑hosted the 2023 FIBA World Cup alongside Japan and Indonesia. During opening night at the Philippine Arena in Bulacan, a record‑breaking 38,115 spectators attended, setting the all‑time attendance record for an indoor FIBA World Cup match."
                      + make_img_html("team_Phi.png")
        }
    },
    {
        "id": 7, "country_code": "USA", "name": "United States", "display_name": "USA", "lat": 40.7128, "lon": -74.0060,
        "color": "#4f46e5", "start_year": 1947,
        "leader": "Wat Misaka / Michael Jordan / LeBron James / Steph Curry",
        "photo": "usa.png",
        "sections": {
            "origin": "<b>1. Invention & Racial Integration Breakthrough (1891 / 1947):</b><br>"
                      "Invented by Dr. James Naismith in Springfield, Massachusetts, in December 1891. In 1947, Japanese‑American WWII veteran Wataru 'Wat' Misaka was drafted by the New York Knicks.<br><br>"
                      "Misaka broke professional basketball's color barrier as the first non‑white player in NBA history, three years prior to African‑American integration in 1950.",
            "leagues": "<b>2. Institutional Architecture (NBA / WNBA / NCAA):</b><br>"
                       "The BAA/NBA was established between 1946 and 1949, expanding into the world's commercial and competitive basketball capital.<br><br>"
                       "In 1996, the WNBA was launched, establishing the gold standard for global professional women's sports. Meanwhile, NCAA March Madness grew into an iconic American cultural phenomenon.",
            "culture": "<b>3. Grassroots Heritage & Streetball Culture:</b><br>"
                       "American basketball culture spans high school state tournaments to iconic streetball sanctums like Rucker Park in Harlem, West 4th Street in NYC, and Venice Beach in Los Angeles.<br><br>"
                       "Streetball culture introduced playground flair, crossover dribbles, and rim‑rocking dunks into global basketball aesthetics."
                       + make_img_html("Streetball.png"),
            "figures": "<b>4. Key Pioneers & Global Legends:</b><br>"
                       "• <b>Wat Misaka:</b> First non‑white NBA player.<br>"
                       "• <b>Bill Russell & Wilt Chamberlain:</b> Defensive mastery (11 titles) and 100‑point single‑game record.<br>"
                       "• <b>Michael Jordan:</b> Global cultural icon and 6‑time Finals MVP.<br>"
                       "• <b>LeBron James & Steph Curry:</b> All‑time scoring leader and revolutionizer of 3‑point shooting.<br>"
                       "• <b>Cheryl Miller & Diana Taurasi:</b> Legends of the women's game."
                       + make_img_html("the_three.png"),
            "modern": "<b>5. Modern Era & World Dominance:</b><br>"
                      "The 1992 Barcelona Olympic 'Dream Team' popularized basketball globally. In 2024, Team USA captured its 17th Men's Olympic Gold Medal in Paris following an epic final against France."
                      + make_img_html(["dream_team.png", "team_USA.png"])
        }
    },
    {
        "id": 6, "country_code": "RUS", "name": "Russia (USSR)", "display_name": "Russia", "lat": 55.7558, "lon": 37.6173,
        "color": "#db2777", "start_year": 1958,
        "leader": "Sergei Belov / Alexander Gomelsky / Andrei Kirilenko",
        "photo": "russia.png",
        "sections": {
            "origin": "<b>1. Origin & Cold War Exchange (1906 / 1958):</b><br>"
                      "Basketball was first introduced to St. Petersburg in 1906 via the Mayak Society for Athletic Development (under YMCA influence).<br><br>"
                      "In 1958, a landmark US‑USSR Cultural Exchange Agreement initiated high‑profile basketball diplomacy tours during the Cold War, bringing Soviet and American teams together in exhibition series.",
            "leagues": "<b>2. 1972 Munich Gold Medal & Tactical System:</b><br>"
                       "In the dramatic final 3 seconds of the 1972 Munich Olympics Gold Medal match, the USSR defeated Team USA 51–50 in one of the most famous games in sports history.<br><br>"
                       "The Soviet state sports infrastructure relied on scientific athletic development, tactical discipline, and year‑round team synergy."
                       + make_img_html("Munich.png"),
            "culture": "<b>3. Institutionalization & Regional Leagues:</b><br>"
                       "The USSR Basketball Federation governed competitive play until 1991, transitioning into the Russian Basketball Federation (RBF).<br><br>"
                       "In 2008, the regional VTB United League was established, featuring top Eastern European professional clubs.",
            "figures": "<b>4. Key Pioneers & Global Figures:</b><br>"
                       "• <b>Sergei Belov:</b> Hero of the 1972 Olympic final and first non‑American international player inducted into the Naismith Hall of Fame (1992).<br>"
                       "• <b>Alexander Gomelsky:</b> Legendary coach ('Father of Soviet Basketball').<br>"
                       "• <b>Andrei Kirilenko ('AK‑47'):</b> NBA All‑Star and former RBF President."
                       + make_img_html("Andrei_Kirilenko.png"),
            "modern": "<b>5. Modern Era & EuroLeague Powerhouse:</b><br>"
                      "Russian professional clubs like CSKA Moscow dominated modern European basketball, winning 8 EuroLeague titles and maintaining a strong tactical coaching legacy."
        }
    },
    {
        "id": 8, "country_code": "RWA", "name": "Rwanda", "display_name": "Rwanda", "lat": -1.9403, "lon": 30.0619,
        "color": "#0891b2", "start_year": 2019,
        "leader": "Barack Obama / Masai Ujiri / FERWABA",
        "photo": "rwanda.png",
        "sections": {
            "origin": "<b>1. Origin & Modern African Strategy (2019–Present):</b><br>"
                      "In 2019, the NBA collaborated with FIBA to launch the Basketball Africa League (BAL). Kigali, Rwanda, was chosen as the premier strategic hub.<br><br>"
                      "This marked the NBA's first official professional league operating outside North America, signaling a revolutionary commitment to African sports infrastructure.",
            "leagues": "<b>2. State‑of‑the‑Art Infrastructure (BK Arena):</b><br>"
                       "The inauguration of the 10,000‑seat BK Arena (Kigali Arena) in 2019 transformed Rwanda into East Africa's sports hub.<br><br>"
                       "The arena regularly hosts BAL Finals, FIBA AfroBasket, and international athletic conferences, driving economic and sports diplomacy.",
            "culture": "<b>3. Grassroots Empowerment & Youth Academies:</b><br>"
                       "Operated in partnership with FERWABA (Fédération Rwandaise de Basketball) and NBA Africa, local programs prioritize youth academies, sports marketing education, and female youth participation across East Africa.",
            "figures": "<b>4. Key Pioneers & Strategic Visionaries:</b><br>"
                       "• <b>Barack Obama:</b> Former US President and NBA Africa strategic partner.<br>"
                       "• <b>Masai Ujiri:</b> Toronto Raptors Vice‑Chairman and Giants of Africa founder.<br>"
                       "• <b>Clare Akamanzi & FERWABA Leadership:</b> Key architects of Rwanda's sports hub strategy.",
            "modern": "<b>5. Modern Impact & Future Horizons:</b><br>"
                      "Rwanda's model has positioned Africa as a vibrant continent in the global basketball ecosystem, attracting international investment, talent scouts, and media networks."
        }
    }
]
# Quiz 题库
quiz_pool = [
    {"id": 1, "question": "In which year was basketball invented by Dr. James Naismith in Springfield, Massachusetts?", "options": ["1889", "1891", "1895", "1900"], "answer": "1891"},
    {"id": 2, "question": "What is the official standard height of a basketball hoop from the court floor worldwide?", "options": ["2.95 meters (9.5 ft)", "3.00 meters (9.8 ft)", "3.05 meters (10 ft)", "3.10 meters (10.2 ft)"], "answer": "3.05 meters (10 ft)"},
    {"id": 3, "question": "Who was the first non‑white and first Asian player drafted in NBA history (1947 by NY Knicks)?", "options": ["Yao Ming", "Wat Misaka", "Wang Zhizhi", "Rui Hachimura"], "answer": "Wat Misaka"},
    {"id": 4, "question": "In which country was 'Netball' developed in 1901 as an adaptation of basketball for female players?", "options": ["United Kingdom", "France", "Germany", "Brazil"], "answer": "United Kingdom"},
    {"id": 5, "question": "Which city serves as the primary strategic hosting hub for the Basketball Africa League (BAL) inaugurated in 2019?", "options": ["Nairobi, Kenya", "Dakar, Senegal", "Kigali, Rwanda", "Cairo, Egypt"], "answer": "Kigali, Rwanda"},
    {"id": 6, "question": "Where is the world's oldest continuously operating indoor basketball court located?", "options": ["Springfield, USA", "Rue de Trévise, Paris, France", "Tianjin, China", "London, UK"], "answer": "Rue de Trévise, Paris, France"},
    {"id": 7, "question": "In which city was basketball introduced as an official Olympic medal sport for the first time in 1936?", "options": ["Paris", "Berlin", "London", "Los Angeles"], "answer": "Berlin"},
    {"id": 8, "question": "Which South American country won back‑to‑back FIBA World Championships in 1959 and 1963?", "options": ["Argentina", "Brazil", "Uruguay", "Chile"], "answer": "Brazil"},
    {"id": 9, "question": "Who holds the record for the most total points scored in Olympic basketball history (1,093 points across 5 Olympics)?", "options": ["Oscar Schmidt", "Manu Ginóbili", "Pau Gasol", "Carmelo Anthony"], "answer": "Oscar Schmidt"},
    {"id": 10, "question": "In 1895, where was basketball first introduced and publicly demonstrated in China?", "options": ["Shanghai", "Beijing", "Tianjin", "Nanjing"], "answer": "Tianjin"},
    {"id": 11, "question": "What is the name of Asia's first professional basketball league, founded in 1975?", "options": ["CBA (China)", "PBA (Philippines)", "B.League (Japan)", "KBL (Korea)"], "answer": "PBA (Philippines)"},
    {"id": 12, "question": "Which national team won the 2023 FIBA World Cup undefeated in Manila?", "options": ["USA", "Serbia", "Germany", "Spain"], "answer": "Germany"},
    {"id": 13, "question": "In the dramatic final 3 seconds of the 1972 Munich Olympic Gold Medal game, which team defeated Team USA?", "options": ["Yugoslavia", "USSR (Soviet Union)", "France", "Italy"], "answer": "USSR (Soviet Union)"},
    {"id": 14, "question": "What famous 1992 US national team catalyzed the explosive global popularity of basketball at the Barcelona Olympics?", "options": ["Redeem Team", "Dream Team", "Select Team", "Global Squad"], "answer": "Dream Team"},
    {"id": 15, "question": "Which unique grassroots basketball event in Guizhou, China, went viral for drawing tens of thousands of rural fans?", "options": ["Streetball China", "Village BA (CunBA)", "Mountain Cup", "CUBAL Final"], "answer": "Village BA (CunBA)"}
]
df_dest = pd.DataFrame(history_data)
def get_great_circle_points(lat1, lon1, lat2, lon2, num_pts=40):
    phi1, lam1 = np.radians(lat1), np.radians(lon1)
    phi2, lam2 = np.radians(lat2), np.radians(lon2)
    v1 = np.array([np.cos(phi1) * np.cos(lam1), np.cos(phi1) * np.sin(lam1), np.sin(phi1)])
    v2 = np.array([np.cos(phi2) * np.cos(lam2), np.cos(phi2) * np.sin(lam2), np.sin(phi2)])
    cos_omega = np.dot(v1, v2)
    omega = np.arccos(np.clip(cos_omega, -1.0, 1.0))
    if omega < 1e-6:
        return [lon1] * num_pts, [lat1] * num_pts
    lons, lats = [], []
    for ti in np.linspace(0, 1, num_pts):
        v_interp = (np.sin((1 - ti) * omega) / np.sin(omega)) * v1 + (np.sin(ti * omega) / np.sin(omega)) * v2
        lats.append(np.degrees(np.arcsin(v_interp[2])))
        lons.append(np.degrees(np.arctan2(v_interp[1], v_interp[0])))
    return lons, lats
# ==================== 2. Dash 页面结构 ====================
app = dash.Dash(__name__, update_title=None, suppress_callback_exceptions=True)
server = app.server
court_background_css = {
    'backgroundColor': '#f8fafc',
    'backgroundImage': 'radial‑gradient(#e2e8f0 2px, transparent 2px), linear‑gradient(to right, #f1f5f9 2px, transparent 2px), linear‑gradient(to bottom, #f1f5f9 2px, transparent 2px)',
    'backgroundSize': '32px 32px, 64px 64px, 64px 64px',
    'color': '#1e293b',
    'fontFamily': '"Segoe UI", Arial, sans‑serif',
    'minHeight': '100vh',
    'padding': '30px 30px 10px 30px',
    'display': 'flex',
    'flexDirection': 'column'
}
app.layout = html.Div(style=court_background_css, children=[
    dcc.Store(id='quiz‑store‑data'),
    html.Div(style={'flex': '1'}, children=[
        html.H1("Mega Basketball Chronicles (1891 ‑ 2026)",
                style={'textAlign': 'center', 'color': '#0f172a', 'fontWeight': '800', 'marginBottom': '25px'}),
        dcc.Tabs(id="tabs‑menu", value='tab‑about', style={'fontWeight': 'bold'}, children=[
            dcc.Tab(label='About This Website', value='tab‑about', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='History Overview', value='tab‑overview', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='Interactive Globe', value='tab‑globe', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='Country Archives', value='tab‑countries', style={'backgroundColor': '#f1f5f9'}),
            dcc.Tab(label='Interactive Quiz', value='tab‑quiz', style={'backgroundColor': '#f1f5f9'}),
            # 【最后一个板块，最右侧标签】
            dcc.Tab(label='Philosophy of Global Sport', value='tab‑philosophy', style={'backgroundColor': '#f1f5f9'}),
        ]),
        html.Div(id='tabs‑content', style={
            'padding': '30px', 'backgroundColor': '#ffffff',
            'borderRadius': '0 0 12px 12px', 'boxShadow': '0 4px 20px rgba(0,0,0,0.05)',
            'border': '1px solid #e2e8f0', 'marginTop': '-1px'
        })
    ]),
    html.Footer(
        children=[
            html.P("© 2026 Xiyuan Wan. All rights reserved.",
                   style={'textAlign': 'center', 'color': '#64748b', 'fontSize': '14px', 'margin': '0',
                          'fontWeight': '500'})
        ],
        style={
            'padding': '20px 0 10px 0',
            'borderTop': '1px solid #e2e8f0',
            'marginTop': '40px'
        }
    )
])
# ==================== 3. 标签页主切换逻辑 ====================
@app.callback(
    Output('tabs‑content', 'children'),
    Input('tabs‑menu', 'value')
)
def render_tab_content(tab_name):
    if tab_name == 'tab‑about':
        return html.Div(style={'maxWidth': '850px', 'margin': '0 auto'}, children=[
            html.H2("The Changing Landscape of Basketball Globalization",
                    style={'color': '#1e3a8a', 'borderBottom': '2px solid #e2e8f0', 'paddingBottom': '10px'}),
            html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'marginBottom': '20px'},
                     children=[
                         html.Img(src=get_image_base64("nba_logo.png"),
                                  style={'maxHeight': '180px', 'objectFit': 'contain'}),
                         html.Img(src=get_image_base64("team_logos.png"),
                                  style={'maxHeight': '180px', 'objectFit': 'contain'})
                     ]),
            html.P(
                "As one of the four major professional sports leagues in North America, the NBA brings together the top basketball talents from around the world. Throughout the nearly 80‑year history of the NBA, homegrown American players have historically dominated this competition. From prehistoric giants like Wilt Chamberlain, who set the legendary single‑game 100‑point record, to Michael Jordan, revered worldwide as the 'Air Jordan', and the relentlessly fiercely competitive Kobe Bryant—followed by the meteoric rise of 2010s superstars like LeBron James, Kevin Durant, and Stephen Curry—the absolute dominance of the United States on the Olympic stage has been undeniable.",
                style={'fontSize': '16px', 'lineHeight': '1.8', 'textAlign': 'justify'}),
            html.Div(style={'textAlign': 'center', 'margin': '25px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("domestic.png"),
                         style={'maxWidth': '100%', 'maxHeight': '280px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),
            html.P(
                "However, in recent years, this narrative has shifted dramatically. The proportion of international players within the league has skyrocketed, with many not only proving their formidable skills but rapidly becoming the absolute franchise cornerstones within their first few seasons. The 'Greek Freak' Giannis Antetokounmpo, the otherworldly talent Victor Wembanyama, and the court maestro Nikola Jokić all hail from different corners of the globe and have captured numerous prestigious individual accolades. This global paradigm shift reached a boiling point during the 2024 Paris Olympics, where the Serbian national team led by Jokić and the French squad anchored by Wembanyama pushed Team USA to its absolute limits. Had it not been for the extraordinary, vintage heroics of James, Durant, and Curry, the coveted Olympic gold medal might have slipped from American hands.",
                style={'fontSize': '16px', 'lineHeight': '1.8', 'textAlign': 'justify'}),
            html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'margin': '25px 0 15px 0'},
                     children=[
                         html.Img(src=get_image_base64("foreign1.png"),
                                  style={'maxHeight': '200px', 'objectFit': 'contain', 'borderRadius': '6px'}),
                         html.Img(src=get_image_base64("foreign2.png"),
                                  style={'maxHeight': '200px', 'objectFit': 'contain', 'borderRadius': '6px'})
                     ]),
            html.P(
                "This visualization serves as a testament to that evolution. Basketball is no longer a sport tethered exclusively to its birthplace or heavily centralized in one superpower nation. The rise of international powerhouses demonstrates that the language of basketball has truly broken down cultural boundaries, distributing elite expertise across continents and reshaping global sports diplomacy in the 21st century.",
                style={'fontSize': '16px', 'lineHeight': '1.8', 'textAlign': 'justify', 'fontWeight': '500',
                       'color': '#0f172a'})
        ])
    elif tab_name == 'tab‑overview':
        return html.Div(style={'maxWidth': '900px', 'margin': '0 auto'}, children=[
            html.H2("Origin & Global Development of Basketball",
                    style={'color': '#1e3a8a', 'borderBottom': '2px solid #e2e8f0', 'paddingBottom': '10px'}),
            html.Div(style={'textAlign': 'center', 'margin': '20px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("oldest_hoop.png"),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),
            html.P(
                "Basketball was invented in December 1891 by Dr. James Naismith, a Canadian physical education instructor at the International YMCA Training School in Springfield, Massachusetts, USA. Tasked with creating a mild indoor winter sport for restless students, he drew inspiration from the folk game 'Duck‑on‑a‑Rock'. He used two peach baskets and a soccer ball, drafted the original 13 fundamental rules, and hosted the world’s first basketball match on December 21, 1891. Most of his original rules remain the core framework of modern basketball.",
                style={'fontSize': '16px', 'lineHeight': '1.7'}),
            html.Div(style={'textAlign': 'center', 'margin': '25px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("evolution.png"),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),
            html.P(
                "The standard height of the basketball hoop is exactly 3.05 meters (10 feet). When Dr. Naismith nailed the peach baskets to the gym balcony railing, the balcony was naturally 10 feet high. He never adjusted the height for balance and fairness, and this 10‑foot height has been preserved as the global official standard for all competitive basketball courts ever since.",
                style={'fontSize': '16px', 'lineHeight': '1.7'}),
            html.Div(style={'textAlign': 'center', 'margin': '25px 0 15px 0'}, children=[
                html.Img(src=get_image_base64("chamberlain.png"),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'borderRadius': '6px'})
            ]),
            html.P(
                "The sport spread rapidly via the global YMCA network after 1893. It first reached Western Europe (France, UK), then East Asia (China, Philippines), Latin America (Brazil), Oceania (Australia), and other continents. After World War I and World War II, basketball gained worldwide popularity. It became an official Olympic medal sport in 1936 Berlin. Later, the NBA was founded in 1947, growing into the world’s top professional league. FIBA standardized international competition rules, boosting transnational exchanges. In recent decades, basketball has evolved into a global mass sport with professional leagues, youth training systems and cultural diplomacy value across Africa, Europe, Asia, Australia, and the Americas.",
                style={'fontSize': '16px', 'lineHeight': '1.7'})
        ])
    elif tab_name == 'tab‑globe':
        standard_marks = {yr: f"{yr}" for yr in range(1890, 2031, 20)}
        return html.Div([
            html.Div(id='year‑display‑banner',
                     style={'textAlign': 'center', 'fontSize': '32px', 'fontWeight': 'bold', 'color': '#2563eb',
                            'marginBottom': '10px'}),
            html.Div([
                html.Label("Drag the slider to change timeline:",
                           style={'fontWeight': 'bold', 'color': '#475569', 'marginBottom': '8px', 'display': 'block'}),
                dcc.Slider(
                    id='timeline‑slider',
                    min=1891, max=2026,
                    step=1,
                    marks=standard_marks,
                    value=1891,
                    updatemode='drag'
                )
            ], style={'padding': '20px', 'background': '#f8fafc', 'borderRadius': '8px', 'border': '1px solid #e2e8f0',
                      'marginBottom': '15px'}),
            html.Div([
                dcc.Graph(
                    id='interactive‑globe‑graph',
                    style={'height': '600px', 'width': '100%'},
                    config={
                        'responsive': True,
                        'scrollZoom': True,
                        'displayModeBar': False
                    }
                )
            ], style={
                'width': '100%',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'backgroundColor': '#ffffff',
                'borderRadius': '8px'
            })
        ])
    elif tab_name == 'tab‑countries':
        df_sorted = df_dest.sort_values("name")
        dropdown_options = [{'label': row['name'], 'value': row['name']} for _, row in df_sorted.iterrows()]
        return html.Div([
            html.Div([
                html.Label("Select a Country Archive (Alphabetical Order A‑Z):",
                           style={'fontWeight': 'bold', 'color': '#1e293b', 'marginRight': '15px'}),
                dcc.Dropdown(
                    id='country‑dropdown',
                    options=dropdown_options,
                    value=df_sorted.iloc[0]['name'] if not df_sorted.empty else None,
                    style={'width': '320px', 'display': 'inline‑block', 'verticalAlign': 'middle'}
                )
            ], style={'marginBottom': '25px'}),
            html.Div(id='country‑archive‑display')
        ])
    elif tab_name == 'tab‑quiz':
        return html.Div(style={'maxWidth': '800px', 'margin': '0 auto'}, children=[
            html.H2("🏀 Basketball Globalization Knowledge Quiz",
                    style={'color': '#1e3a8a', 'borderBottom': '2px solid #e2e8f0', 'paddingBottom': '10px',
                           'textAlign': 'center'}),
            html.P("Test your knowledge! 5 random questions are sampled from our 15‑question bank each time.",
                   style={'textAlign': 'center', 'color': '#64748b', 'marginBottom': '20px'}),
            html.Div(style={'textAlign': 'center', 'marginBottom': '25px'}, children=[
                html.Button("🔄 Refresh / New Random 5 Questions", id="quiz‑refresh‑btn", n_clicks=0,
                            style={'backgroundColor': '#0f172a', 'color': 'white', 'border': 'none',
                                   'padding': '8px 20px', 'fontSize': '14px', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontWeight': '500'})
            ]),
            html.Div(id='quiz‑questions‑container'),
            html.Div(style={'textAlign': 'center', 'marginTop': '25px'}, children=[
                html.Button("Submit Answers", id="quiz‑submit‑btn", n_clicks=0,
                            style={'backgroundColor': '#2563eb', 'color': 'white', 'border': 'none',
                                   'padding': '12px 35px', 'fontSize': '16px', 'borderRadius': '6px',
                                   'cursor': 'pointer', 'fontWeight': 'bold'}),
                html.Div(id="quiz‑total‑score", style={'marginTop': '20px', 'fontSize': '20px', 'fontWeight': 'bold'})
            ])
        ])
    # ==========【最后一个板块，全部标签的末尾，文章写在这里】==========
    elif tab_name == 'tab‑philosophy':
        return html.Div(style={'maxWidth': '850px', 'margin': '0 auto'}, children=[
            html.H2("Philosophy of Global Sport: Basketball as a Shared Human Language",
                    style={'color': '#1e3a8a', 'borderBottom': '2px solid #e2e8f0', 'paddingBottom': '10px'}),
            # --------------------------
            #        在此粘贴你的体育哲学文章！！！
            #        多段就复制多个html.P()
            # --------------------------
            html.P(
                """
                Why and How Should People Engage in Sports: The Value of Sports to Individuals Revisited
                I. Introduction
                What exactly do sports bring to individuals? There is a wide range of perspectives on this issue. Some people might say that playing sports is to exercise and keep fit; some might say that playing sports can nourish one’s soul; others might say that playing sports is a profession with which to raise a family.
                But how exactly can sports help people? Before a detailed discussion, the definition of sports should first be made — we discuss sports, under Bernard Suits’ definition, as those in which the outcomes depend only “on the exercise of physical skills”.  Therefore, intellectual sports such as cards and board games are not included in the present discussion. 
                Now, we can dive into the details.
                We can first look at the arguments made by those people who hold that playing sports is a way to keep fit. Undoubtedly, aerobic exercise can improve cardiorespiratory function and help with weight loss and fat reduction, while anaerobic exercise helps build muscle and makes people stronger. Due to the poor physical condition of contemporary primary and secondary students, the Chinese government has written no less than 2 hours of daily physical activity for school students into its education policy.  Thus, it can be seen that sports play an important role in maintaining posture and promoting health. But in reality, it is not hard to find that many athletes, or even amateurs, suffer from major injuries. Therefore, although sports are good for our health, they can also harm our bodies; sports might be unable to achieve the goal of building up the body.
                What about the idea that “sports can promote the growth of the soul”? Granted, training for any sport is extremely boring; anyone who wants to be a successful athlete must endure its harshness. To keep going under extreme pain and discomfort — what we often call toughness — is generally viewed as the key factor in becoming a successful athlete. Therefore, if we can turn the passion for sports into the desire to win and the spirit of never giving up, it is a typical tempering of the soul, or what we may call “mental toughness.” But here come two subsequent questions: is it that sports cultivate mental toughness in people, or is mental toughness a precondition for participating in sports? Does strong mental toughness help one become a good athlete, or do we label someone as mentally tough simply because they are an outstanding athlete?  In particular, some of the world's top athletes are even seen as lacking mental toughness. For instance, NBA superstar Tracy McGrady, who scored 13 points in 35 seconds, was criticized as not being mentally tough enough because he chose not to play due to poor recovery from his knee injury. Therefore, the relationship between mental toughness and sports remains unanswered.
                In modern families, some parents send their children to practice sports because of their poor academic performance and their talent in sports, hoping to help them find a possible career in the future. However, although we can list many sports celebrities who have gained both wealth and fame and see many less excellent athletes who successfully went into coaching or physical education after retirement, the cruelty and selectivity of competitive sports force far more people who initially took this path to quit, leaving them unable to pursue a career in sports or find a relevant job; after all, only a small number of professional athletes achieve what is conventionally regarded as success. Moreover, there are many players who have had stellar athletic careers yet neither have accumulated enough material wealth for their retirement nor possess sufficient basic life skills. Many of them are riddled with injuries and can only live a poor life in stark contrast to their glorious careers, some even have to live on selling their medals or the handouts from others.
                From this, it appears that there exists a huge gap between what people expect sports can bring and what sports can truly bring to them. Then, what is the actual value of sports to individuals? How can we truly realize its value to individuals? Let’s first look at the answers from two distinguished philosophers, Plato and Aristotle.
                II. Sports, Music and Leisure: How Can Sports Bring Out Their Intrinsic Value to Individuals
                Plato mentioned in The Republic that the “physical exercise and effort” one undergoes aims mainly for “the passionate aspect of his nature”, not to strengthen his body. With proper training, he can become courageous; excessive training, however, can make him brutal.  In Plato’s view, when one devotes one’s entire life to sports without learning culture, the light of wisdom deep in the mind may gradually become dimmer, turning one into a reckless person who relies on force rather than persuasion.  However, if one receives only education in culture and does not engage in sports, the opposite extreme may emerge. Without physical exercise, the passionate aspect of one’s nature may become too weak and lack the courage and strength needed for action, he will become “a feeble fighter” or has “changed passion for peevishness and irritability”, and is “seething with discontent”.  Therefore, we should combine culture and physical exercise, in order that our passionate and our philosophical aspects “fit harmoniously together by being stretched and relaxed as much as is appropriate”; the two corresponding area of expertise answer the mind and the body “incidentally”. Here, Plato answered the follow-up question of why people should participate in sports by considering under what conditions sports can truly achieve their purposes. According to him, the core value of sports lies in combining physical exercise with culture, so as to forge a harmonious nature which is both temperate and courageous; physical fitness and nourishment of the passionate aspect of our nature are just the accompanying benefits. 
                In Aristotle’s view, “there are three sorts of constituent elements of the best life, i.e. external goods; goods of the body; and goods of the soul.”  A good citizen must have a habit of labor, but “the exertion must not be violent or specialized, as is the case with the athlete; it should rather be a general exertion, directed to all the activities of freeman,” because “the athlete’s habit of body neither produces a good condition for the general purposes of civic life, nor does it encourage ordinary health and the procreation of children.”  Moreover, gymnastics are commonly said to cultivate bravery, but courage cannot be fostered through sports alone; sports alone can only breed recklessness and cruelty. Those with courage should be temperate, possessing “lion-like temper” —“noble” rather than “ferocious”.  To achieve this goal, one must make good use of his leisure time to cultivate the mind ; and the value of music and some other branches of learning and education lies in “the cultivation of the mind in leisure”.  Aristotle prioritized the goods of the soul, arguing that anyone can earn a living and support his family through his own professional skills, but outward possession cannot be considered external goods unless “it is for the sake of the soul that these other things [property and health of the body] are desirable”.  Hence, once a sportsman is preoccupied with acquiring external goods, sports can also  “have a mechanical effect” and are therefore “menial and servile.” 
                III. Further Reflection on the Values of Sports to Individuals
                Plato’s and Aristotle’s ideas offer considerable insights for the development of modern professional sports. Many athletes begin their careers with excessive training at a very young age, seeking a competitive edge for their future career path. However, being over-trained is detrimental to health — leading to injuries, psychological disorders, or low self-esteem — and also deprives them of time to study academic subjects, leaving them with insufficient cultural cultivation.
                Although some of Aristotle’s ideas were radical and prejudiced, they did contain many reasonable elements. Modern physical education largely follows the guidance of Plato and Aristotle. By critically assimilating their views, we seek to achieve, as far as possible, a synthesis of sports with intellectual and aesthetic education. Tim Duncan, one of the greatest power forwards in NBA history, majored in psychology and earned a master’s degree. Qian Yang, who won the first gold medal in shooting at the 2020 Tokyo Olympics, is also a Tsinghua University graduate. As we can see, we can certainly choose to be professional athletes, however, we not only need jobs to support ourselves, but also need time for moral and spiritual life that elevate our souls and minds and help us become better versions of ourselves.
                Aristotle looked down on professional athletes, believing that such people, as well as those engaged in music performance, were menial and servile, but he held that those people have the right to support himself and his family with their professional skills and that a good way for citizens to recharge is by watching sporting events or music performances. 
                Therefore sports, however complex and dangerous, still benefit society, and thus the athletes who create this value can justifiably choose any sport as their profession, provided that —according to John Mill’s principle—it does no harm to others. Moreover, Modern psychology reveals that one can overcome the fear deep within his heart by exposing himself to fear-provoking stimuli, starting with the least frightening and ending with the most frightening. So, engaging in dangerous sports can not only give individuals a greater sense of control over their lives, but also cultivate the mental toughness to “turn fear into fuel” in real life. When coupled with necessary liberal arts education, i.e. ancient Greek’s music education, such athletes can grow into lions Aristotle anticipated. Furthermore, according to Suits, most sports involve “the voluntary attempt to overcome unnecessary obstacles”.   Obviously, these games can make sportsmen’s life more meaningful. This holds true in Suits’ utopian world and, to some extent, in the real world. Of course, those engaging in dangerous sports should clearly realize the extent of the risks involved, judge whether the risks are too high for him or her to be worth taking, and put safety measures in place if he or she decides to engage in such sports. The process of evaluating risk is itself a process of mental growth: risks help us know ourselves and understand what we truly treasure. 
                Therefore, contrary to what Aristotle held, professional athletes are not menial and servile—at least in today’s world. Gaining wealth by playing sports has its complete legitimacy, provided that professional athletes are not blinded by fame and wealth and thus do not violet the rules; once their souls are dominated by “external goods” they will not commit themselves to fairness and justice, and there leaves only one thing— to win by any means necessary, even if it comes at the cost of their body and soul. 
                IV. Conclusion
                In summary, the value of sports to individuals is not limited to physical fitness or a career; its core value lies in cultivating the soul and pushing individuals toward the ideal of becoming whole. However, sports alone cannot achieve this effect — it must be combined with liberal arts education.
                Although ancient Greek philosophers viewed professional athletes as menial and servile, in modern society, what we should look down upon are not athletes themselves, but those who abandon the integrity of the soul and cheat in pursuit of fame and wealth.
                Wealth and fame should never take priority over the virtue of the soul. Preserving the purity of our original love for sports is the most precious value that sports can offer individuals.



                Reference
                Aristotle (1999). The Politics of Aristotle (Translated with an Introduction Notes and Appendixes by Ernest Barker). Beijing: China Social Sciences Publishing House (Reprinted from the English Edition by Oxford University Press 1946).
                Devine, John W. & Frias, F. J. Lopez (Feb 4, 2020). “Philosophy of Sport”. https://plato.stanford.edu/entries/sport/
                Plato (1999). Republic (Translated into English by Robin Waterfield). Beijing: China Social Sciences Publishing House (Reprinted from the English Edition by Oxford University Press 1993).
                Ryall, Emily (2025). Philosophy of Sport: Key Questions (Translated into Chinese by Jiang Xiaojie). Xi’an: Northwest University Press.
                Suits, Bernard (1978). The Grasshopper: Games, Life, and Utopia. Toronto: University of Toronto Press. 
                Xinhua (2025). “The CPC Central Committee and the State Council Print and Issue the Master Plan on Building China into a Leading Country in Education (2024-2035) ”. https://www.xinhuanet.com/politics/20250119/f33c2caa323249ca8fd2038515ee9620/c.html

                """,
                style={'fontSize': '16px', 'lineHeight': '1.8', 'textAlign': 'justify'}
            ),
            # --------------------------
            #        文章粘贴结束
            # --------------------------
        ])
# ==================== 4. 3D 地球逻辑 ====================
@app.callback(
    [Output('interactive‑globe‑graph', 'figure'),
     Output('year‑display‑banner', 'children')],
    Input('timeline‑slider', 'value')
)
def update_globe(selected_year):
    fig = go.Figure()
    fig.add_trace(go.Choropleth(
        locations=["USA"], z=[0], colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],
        showscale=False, geo='geo', hoverinfo='none'
    ))
    fig.add_trace(go.Scattergeo(
        lon=[start_pt["lon"]], lat=[start_pt["lat"]], mode='markers+text',
        marker=dict(size=12, color='#ea580c', symbol='star'),
        text=["<b>Springfield (1891)</b>"], textposition="bottom center",
        textfont=dict(color="#ea580c", size=12),
        hoverinfo='none'
    ))
    active_countries = df_dest[df_dest["start_year"] <= selected_year]
    rot_lat, rot_lon = start_pt["lat"], start_pt["lon"]
    if not active_countries.empty:
        latest_country = active_countries.iloc[-1]
        rot_lat, rot_lon = latest_country["lat"], latest_country["lon"]
    for _, row in active_countries.iterrows():
        mlons, mlats = get_great_circle_points(start_pt["lat"], start_pt["lon"], row["lat"], row["lon"])
        fig.add_trace(go.Scattergeo(
            lon=mlons, lat=mlats, mode='lines',
            line=dict(width=2.5, color=row["color"]), opacity=0.85, hoverinfo='none'
        ))
        fig.add_trace(go.Scattergeo(
            lon=[row["lon"]], lat=[row["lat"]], mode='markers+text',
            text=[f"<b>{row['display_name']} ({row['start_year']})</b>"],
            textposition="top center", textfont=dict(size=11, color='#1e293b'),
            marker=dict(size=8, color=row["color"]), hoverinfo='none'
        ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        geo=dict(
            scope='world',
            projection=dict(
                type='orthographic',
                rotation=dict(lon=rot_lon, lat=rot_lat, roll=0)
            ),
            showland=True, landcolor='#f1f5f9',
            showocean=True, oceancolor='#e0f2fe',
            showcountries=True, countrycolor='#cbd5e1',
            showframe=False,
            bgcolor='rgba(0,0,0,0)',
            domain=dict(x=[0, 1], y=[0, 1])
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision='globe‑view'
    )
    return fig, f"🌍 Current Timeline Focus Year: {selected_year}"
# ==================== 5. 国家档案逻辑 ====================
@app.callback(
    Output('country‑archive‑display', 'children'),
    Input('country‑dropdown', 'value')
)
def update_country_archive(country_name):
    if not country_name:
        return html.Div("Please select a country from the dropdown menu.",
                        style={'padding': '20px', 'color': '#64748b'})
    filtered = df_dest[df_dest["name"] == country_name]
    if filtered.empty:
        return html.Div("Country data package not found.", style={'padding': '20px', 'color': '#ef4444'})
    row = filtered.iloc[0]
    country_fig = go.Figure()
    loc_list = [row["country_code"]]
    if row["country_code"] == "CHN":
        loc_list.append("TWN")
    country_fig.add_trace(go.Choropleth(
        locations=loc_list, z=[1] * len(loc_list),
        colorscale=[[0, row["color"]], [1, row["color"]]], showscale=False, hoverinfo='none'
    ))
    country_fig.add_trace(go.Scattergeo(
        lon=[row["lon"]], lat=[row["lat"]], mode='markers+text',
        text=[f"<b>{row['name']}</b>"], textposition="top center",
        marker=dict(size=10, color='#dc2626'), textfont=dict(size=14, color='#1e293b')
    ))
    country_fig.update_layout(
        template='plotly_white', showlegend=False,
        geo=dict(scope='world', showland=True, landcolor='#f8fafc', showcountries=True, countrycolor='#e2e8f0',
                 center=dict(lat=float(row["lat"]), lon=float(row["lon"])), projection_scale=2.8),
        height=280, margin=dict(l=0, r=0, t=10, b=10)
    )
    extra_top_img = []
    if row["name"] == "Australia":
        extra_top_img = [
            html.Div(style={'flex': '1', 'minWidth': '280px', 'textAlign': 'center'}, children=[
                html.Img(src=get_image_base64("Aus_Paris.png"),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'border': '1px solid #cbd5e1', 'borderRadius': '8px', 'background': '#f8fafc'})
            ])
        ]
    return html.Div([
        html.Div(style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', 'gap': '25px', 'marginBottom': '20px'}, children=[
            html.Div(style={'flex': '1', 'minWidth': '280px'}, children=[
                dcc.Graph(figure=country_fig, config={'displayModeBar': False})
            ]),
            html.Div(style={'flex': '1', 'minWidth': '280px', 'textAlign': 'center'}, children=[
                html.Img(src=get_image_base64(row["photo"]),
                         style={'maxWidth': '100%', 'maxHeight': '260px', 'objectFit': 'contain',
                                'border': '1px solid #cbd5e1', 'borderRadius': '8px', 'background': '#f8fafc'})
            ]),
            *extra_top_img,
            html.Div(style={'flex': '1.2', 'minWidth': '300px'}, children=[
                html.H2(f"{row['name']}", style={'color': '#1e3a8a', 'marginTop': '0', 'marginBottom': '10px'}),
                html.Div([
                    html.Strong("Introduction Year: ", style={'color': '#b45309', 'fontSize': '15px'}),
                    html.Span(str(row["start_year"]), style={'fontSize': '15px', 'fontWeight': 'bold'})
                ], style={'marginBottom': '10px'}),
                html.Div([
                    html.Strong("Key Influential Figures: ", style={'color': '#b45309', 'fontSize': '15px'}),
                    html.Span(row["leader"], style={'fontSize': '15px', 'fontWeight': '500'})
                ], style={'marginBottom': '15px'}),
                html.P("Select the sub‑tabs below to explore each historical section in full detail.",
                       style={'color': '#64748b', 'fontSize': '14px', 'fontStyle': 'italic'})
            ])
        ]),
        html.Hr(style={'borderColor': '#e2e8f0', 'margin': '20px 0'}),
        dcc.Tabs(id='country‑sub‑tabs', value='sub‑origin', children=[
            dcc.Tab(label='1. Origin & Early Intro', value='sub‑origin', style={'padding': '8px', 'fontSize': '13px'}),
            dcc.Tab(label='2. Leagues & Structure', value='sub‑leagues', style={'padding': '8px', 'fontSize': '13px'}),
            dcc.Tab(label='3. Culture & Grassroots', value='sub‑culture', style={'padding': '8px', 'fontSize': '13px'}),
            dcc.Tab(label='4. Key Figures & Pioneers', value='sub‑figures', style={'padding': '8px', 'fontSize': '13px'}),
            dcc.Tab(label='5. Modern Era & Triumphs', value='sub‑modern', style={'padding': '8px', 'fontSize': '13px'}),
        ]),
        html.Div(id='country‑sub‑content', style={
            'padding': '25px', 'backgroundColor': '#f8fafc',
            'borderRadius': '0 0 8px 8px', 'border': '1px solid #e2e8f0',
            'borderTop': 'none', 'minHeight': '180px'
        })
    ])
# ==================== 6. 国家档案子标签页切换 ====================
@app.callback(
    Output('country‑sub‑content', 'children'),
    [Input('country‑sub‑tabs', 'value'),
     Input('country‑dropdown', 'value')]
)
def render_sub_tab_content(sub_tab, country_name):
    if not country_name:
        return ""
    filtered = df_dest[df_dest["name"] == country_name]
    if filtered.empty:
        return ""
    sec = filtered.iloc[0]["sections"]
    content_map = {
        'sub‑origin': sec["origin"],
        'sub‑leagues': sec["leagues"],
        'sub‑culture': sec["culture"],
        'sub‑figures': sec["figures"],
        'sub‑modern': sec["modern"]
    }
    selected_text = content_map.get(sub_tab, "No section content available.")
    return dcc.Markdown(
        selected_text,
        dangerously_allow_html=True,
        style={'lineHeight': '1.8', 'fontSize': '15px', 'color': '#334155', 'textAlign': 'justify'}
    )
# ==================== 7. Quiz 测验逻辑 ====================
@app.callback(
    [Output('quiz‑store‑data', 'data'),
     Output('quiz‑questions‑container', 'children')],
    [Input('tabs‑menu', 'value'),
     Input('quiz‑refresh‑btn', 'n_clicks')]
)
def generate_random_quiz(tab_name, n_clicks):
    selected_5 = random.sample(quiz_pool, 5)
    rendered_questions = []
    for idx, q in enumerate(selected_5, start=1):
        question_title = f"{idx}. {q['question']}"
        q_element = html.Div(key=f"q‑container‑{q['id']}", style={
            'backgroundColor': '#f8fafc', 'padding': '20px', 'borderRadius': '8px',
            'marginBottom': '20px', 'border': '1px solid #e2e8f0'
        }, children=[
            html.H4(question_title, style={'color': '#0f172a', 'marginBottom': '12px'}),
            dcc.RadioItems(
                id={'type': 'quiz‑options', 'index': q['id']},
                options=[{'label': f" {opt}", 'value': opt} for opt in q['options']],
                style={'display': 'flex', 'flexDirection': 'column', 'gap': '8px', 'fontSize': '15px'}
            ),
            html.Div(id={'type': 'quiz‑feedback', 'index': q['id']}, style={'marginTop': '10px'})
        ])
        rendered_questions.append(q_element)
    return selected_5, rendered_questions
@app.callback(
    [Output({'type': 'quiz‑feedback', 'index': ALL}, 'children'),
     Output({'type': 'quiz‑feedback', 'index': ALL}, 'style'),
     Output('quiz‑total‑score', 'children')],
    Input('quiz‑submit‑btn', 'n_clicks'),
    [State({'type': 'quiz‑options', 'index': ALL}, 'value'),
     State('quiz‑store‑data', 'data')]
)
def evaluate_quiz(n_clicks, user_answers, current_quiz_data):
    if n_clicks == 0 or not user_answers or not current_quiz_data:
        empty_count = len(current_quiz_data) if current_quiz_data else 5
        return [""] * empty_count, [{}] * empty_count, ""
    feedbacks = []
    styles = []
    correct_count = 0
    for i, q in enumerate(current_quiz_data):
        selected = user_answers[i] if i < len(user_answers) else None
        correct = q["answer"]
        if selected == correct:
            correct_count += 1
            feedbacks.append("✓ Correct! Perfect answer.")
            styles.append({
                'color': '#15803d',
                'backgroundColor': '#dcfce7'
            })