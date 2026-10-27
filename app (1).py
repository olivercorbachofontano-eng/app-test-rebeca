import streamlit as st
import json
import os
import random
import math
import time
import io
import base64
from PIL import Image, ImageDraw, ImageFont

# Page Configuration
st.set_page_config(
    page_title="EPSO AD5 Exam Simulator & Adaptive Practice",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

PROGRESS_FILE = "progreso_estudiante.json"

# Custom CSS for Mobile and Desktop
st.markdown("""
<style>
    .reportview-container .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
    
    div.stButton > button:first-child {
        width: 100%;
        height: 3.4rem;
        font-size: 1.1rem !important;
        font-weight: bold;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #4338CA 0%, #2563EB 100%);
        transform: translateY(-1px);
    }
    
    .passage-box {
        background-color: #F0FDF4;
        border-left: 5px solid #16A34A;
        padding: 16px;
        border-radius: 10px;
        font-size: 1.02rem;
        line-height: 1.6;
        color: #1F2937;
        margin-bottom: 20px;
        max-height: 280px;
        overflow-y: auto;
    }
    
    .progress-card {
        background-color: white;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        text-align: center;
    }
    
    .timer-badge {
        background-color: #FEF3C7;
        color: #B45309;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #F59E0B;
        display: inline-block;
    }
    
    div.row-widget.stRadio > div {
        background-color: #F9FAFB;
        padding: 14px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for PIL Abstract Reasoning Images
def draw_polygon(draw, cx, cy, num_sides, radius, rotation=0, fill=None, outline='black', width=2):
    points = []
    for i in range(num_sides):
        angle = rotation + i * 2 * math.pi / num_sides - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=fill, outline=outline, width=width)

def generate_abstract_rotation_png():
    img = Image.new('RGB', (900, 350), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, 900, 32], fill=(243, 244, 246))
    draw.text((15, 8), "ABSTRACT REASONING: ROTATION & VERTEX TRACKING", fill=(31, 41, 55))
    
    angle_step = random.choice([45, 90])
    sides = random.choice([3, 4, 5, 6])
    correct_opt_idx = random.randint(0, 4)
    labels = ['A', 'B', 'C', 'D', 'E']
    
    for i in range(5):
        x0 = 15 + i * 175
        y0 = 42
        x1 = x0 + 160
        y1 = 175
        draw.rectangle([x0, y0, x1, y1], outline=(79, 70, 229), width=3, fill=(249, 250, 251))
        draw.text((x0 + 8, y0 + 5), f"Frame {i+1}" if i < 4 else "Frame 5 (?)", fill=(107, 114, 128))
        cx, cy = (x0 + x1)//2, (y0 + y1)//2 + 5
        
        if i < 4:
            rot = i * (angle_step * math.pi / 180.0)
            draw_polygon(draw, cx, cy, sides, 38, rotation=rot, fill=(238, 242, 255), outline=(79, 70, 229), width=3)
            dot_angle = rot - math.pi / 2
            dot_x = cx + 38 * math.cos(dot_angle)
            dot_y = cy + 38 * math.sin(dot_angle)
            draw.ellipse([dot_x-7, dot_y-7, dot_x+7, dot_y+7], fill=(225, 29, 72))
        else:
            draw.rectangle([cx-22, cy-22, cx+22, cy+22], fill=(238, 242, 255), outline=(79, 70, 229), width=2)
            draw.text((cx-5, cy-10), "?", fill=(79, 70, 229))
            
    draw.rectangle([0, 185, 900, 215], fill=(243, 244, 246))
    draw.text((15, 192), "OPTIONS (Choose the correct 5th figure: A, B, C, D, or E)", fill=(31, 41, 55))
    
    target_rot = 4 * (angle_step * math.pi / 180.0)
    for idx, label in enumerate(labels):
        x0 = 15 + idx * 175
        y0 = 225
        x1 = x0 + 160
        y1 = 335
        draw.rectangle([x0, y0, x1, y1], outline=(209, 213, 219), width=2, fill=(255, 255, 255))
        draw.text((x0 + 8, y0 + 5), f"Option {label}", fill=(55, 65, 81))
        cx, cy = (x0 + x1)//2, (y0 + y1)//2 + 5
        
        if idx == correct_opt_idx:
            rot = target_rot
        else:
            rot = (idx + 1) * (60 * math.pi / 180.0)
            if abs(rot - target_rot) < 0.05:
                rot += 0.7
                
        draw_polygon(draw, cx, cy, sides, 35, rotation=rot, fill=(255, 255, 255), outline=(107, 114, 128), width=2)
        dot_angle = rot - math.pi / 2
        dot_x = cx + 35 * math.cos(dot_angle)
        dot_y = cy + 35 * math.sin(dot_angle)
        draw.ellipse([dot_x-6, dot_y-6, dot_x+6, dot_y+6], fill=(225, 29, 72))
        
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    expl = f"**Step-by-Step Logic:**\n1. **Rotation Rule:** The {sides}-sided polygon rotates clockwise by **{angle_step}°** in each step.\n2. **Indicator Tracking:** The red indicator dot stays attached to the top vertex as the polygon rotates.\n3. **5th Frame Target:** Starting from Frame 1 at 0°, Frame 5 completes 4 increments of {angle_step}°, resulting in a total rotation of {4*angle_step}°. Option **{labels[correct_opt_idx]}** shows this exact orientation."
    
    return {
        "id": f"abs_rot_{random.randint(1000,9999)}",
        "type": "abstract",
        "difficulty": "Medium",
        "question": f"Which option (Option A, B, C, D, or E) logically completes the 5th frame in the sequence?",
        "options": [f"Option {l}" for l in labels],
        "correct": f"Option {labels[correct_opt_idx]}",
        "img_bytes": buf.getvalue(),
        "explanation": expl
    }

def generate_abstract_side_progression_png():
    img = Image.new('RGB', (900, 350), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, 900, 32], fill=(243, 244, 246))
    draw.text((15, 8), "ABSTRACT REASONING: POLYGON SIDES & SHADING CYCLE", fill=(31, 41, 55))
    
    start_sides = random.choice([3, 4])
    correct_opt_idx = random.randint(0, 4)
    labels = ['A', 'B', 'C', 'D', 'E']
    
    for i in range(5):
        x0 = 15 + i * 175
        y0 = 42
        x1 = x0 + 160
        y1 = 175
        draw.rectangle([x0, y0, x1, y1], outline=(79, 70, 229), width=3, fill=(249, 250, 251))
        draw.text((x0 + 8, y0 + 5), f"Frame {i+1}" if i < 4 else "Frame 5 (?)", fill=(107, 114, 128))
        cx, cy = (x0 + x1)//2, (y0 + y1)//2 + 5
        
        if i < 4:
            curr_sides = start_sides + i
            is_filled = (i % 2 == 1)
            draw_polygon(draw, cx, cy, curr_sides, 38, rotation=0, fill=(79, 70, 229) if is_filled else (255, 255, 255), outline=(79, 70, 229), width=3)
        else:
            draw.rectangle([cx-22, cy-22, cx+22, cy+22], fill=(238, 242, 255), outline=(79, 70, 229), width=2)
            draw.text((cx-5, cy-10), "?", fill=(79, 70, 229))
            
    draw.rectangle([0, 185, 900, 215], fill=(243, 244, 246))
    draw.text((15, 192), "OPTIONS (Choose the correct 5th figure: A, B, C, D, or E)", fill=(31, 41, 55))
    
    target_sides = start_sides + 4
    target_filled = (4 % 2 == 1)
    
    for idx, label in enumerate(labels):
        x0 = 15 + idx * 175
        y0 = 225
        x1 = x0 + 160
        y1 = 335
        draw.rectangle([x0, y0, x1, y1], outline=(209, 213, 219), width=2, fill=(255, 255, 255))
        draw.text((x0 + 8, y0 + 5), f"Option {label}", fill=(55, 65, 81))
        cx, cy = (x0 + x1)//2, (y0 + y1)//2 + 5
        
        if idx == correct_opt_idx:
            opt_sides = target_sides
            opt_filled = target_filled
        else:
            opt_sides = (start_sides + idx + 1) if (start_sides + idx + 1) != target_sides else (target_sides + 2)
            opt_filled = (idx % 2 == 0)
            
        draw_polygon(draw, cx, cy, opt_sides, 35, rotation=0, fill=(79, 70, 229) if opt_filled else (255, 255, 255), outline=(107, 114, 128), width=2)
        
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    expl = f"**Step-by-Step Logic:**\n1. **Side Count Progression:** The shape adds +1 side per step (Frame 1: {start_sides}, Frame 2: {start_sides+1}, Frame 3: {start_sides+2}, Frame 4: {start_sides+3}). Frame 5 requires **{target_sides} sides**.\n2. **Shading Cycle:** Color alternates between White fill (odd frames: 1, 3, 5) and Solid Fill (even frames: 2, 4). Frame 5 requires a **White fill**.\n3. **Conclusion:** Option **{labels[correct_opt_idx]}** is the correct {target_sides}-sided polygon."
    
    return {
        "id": f"abs_sides_{random.randint(1000,9999)}",
        "type": "abstract",
        "difficulty": "Easy",
        "question": f"Which option (Option A, B, C, D, or E) logically completes the 5th frame in the sequence?",
        "options": [f"Option {l}" for l in labels],
        "correct": f"Option {labels[correct_opt_idx]}",
        "img_bytes": buf.getvalue(),
        "explanation": expl
    }

def generate_abstract_grid_shift_png():
    img = Image.new('RGB', (900, 350), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, 900, 32], fill=(243, 244, 246))
    draw.text((15, 8), "ABSTRACT REASONING: 3x3 MATRIX GRID SHIFT", fill=(31, 41, 55))
    
    correct_opt_idx = random.randint(0, 4)
    labels = ['A', 'B', 'C', 'D', 'E']
    
    pos_sequence = [(0,0), (0,1), (0,2), (1,2), (2,2)]
    
    for i in range(5):
        x0 = 15 + i * 175
        y0 = 42
        x1 = x0 + 160
        y1 = 175
        draw.rectangle([x0, y0, x1, y1], outline=(79, 70, 229), width=3, fill=(249, 250, 251))
        draw.text((x0 + 8, y0 + 5), f"Frame {i+1}" if i < 4 else "Frame 5 (?)", fill=(107, 114, 128))
        
        if i < 4:
            gx_start, gy_start = x0 + 35, y0 + 30
            cell_size = 28
            r_target, c_target = pos_sequence[i]
            for r in range(3):
                for c in range(3):
                    cx0 = gx_start + c * cell_size
                    cy0 = gy_start + r * cell_size
                    is_active = (r == r_target and c == c_target)
                    draw.rectangle([cx0, cy0, cx0+cell_size, cy0+cell_size], fill=(225, 29, 72) if is_active else (255, 255, 255), outline=(156, 163, 175), width=1)
        else:
            cx, cy = (x0 + x1)//2, (y0 + y1)//2 + 5
            draw.rectangle([cx-22, cy-22, cx+22, cy+22], fill=(238, 242, 255), outline=(79, 70, 229), width=2)
            draw.text((cx-5, cy-10), "?", fill=(79, 70, 229))
            
    draw.rectangle([0, 185, 900, 215], fill=(243, 244, 246))
    draw.text((15, 192), "OPTIONS (Choose the correct 5th figure: A, B, C, D, or E)", fill=(31, 41, 55))
    
    target_pos = pos_sequence[4]
    
    for idx, label in enumerate(labels):
        x0 = 15 + idx * 175
        y0 = 225
        x1 = x0 + 160
        y1 = 335
        draw.rectangle([x0, y0, x1, y1], outline=(209, 213, 219), width=2, fill=(255, 255, 255))
        draw.text((x0 + 8, y0 + 5), f"Option {label}", fill=(55, 65, 81))
        
        gx_start, gy_start = x0 + 35, y0 + 30
        cell_size = 28
        
        if idx == correct_opt_idx:
            r_opt, c_opt = target_pos
        else:
            r_opt = (idx * 2) % 3
            c_opt = (idx + 1) % 3
            if (r_opt, c_opt) == target_pos:
                r_opt, c_opt = 1, 0
                
        for r in range(3):
            for c in range(3):
                cx0 = gx_start + c * cell_size
                cy0 = gy_start + r * cell_size
                is_active = (r == r_opt and c == c_opt)
                draw.rectangle([cx0, cy0, cx0+cell_size, cy0+cell_size], fill=(225, 29, 72) if is_active else (255, 255, 255), outline=(156, 163, 175), width=1)
                
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    expl = f"**Step-by-Step Logic:**\n1. **Grid Border Shift:** The active red cell moves clockwise around the perimeter of the 3x3 matrix by 1 cell step per frame.\n2. **Path Analysis:** Top-Left (0,0) -> Top-Middle (0,1) -> Top-Right (0,2) -> Middle-Right (1,2) -> **Bottom-Right (2,2)**.\n3. **Conclusion:** Frame 5 requires the active square at row 3, column 3 (Bottom-Right), depicted in Option **{labels[correct_opt_idx]}**."
    
    return {
        "id": f"abs_grid_{random.randint(1000,9999)}",
        "type": "abstract",
        "difficulty": "Hard",
        "question": f"Which option (Option A, B, C, D, or E) logically completes the 5th frame in the sequence?",
        "options": [f"Option {l}" for l in labels],
        "correct": f"Option {labels[correct_opt_idx]}",
        "img_bytes": buf.getvalue(),
        "explanation": expl
    }

# Dynamic Numerical Generators
def generate_numerical_patents():
    pop_ger = random.randint(80000, 83000)
    pop_swi = random.randint(7200, 7800)
    rate_ger = round(random.uniform(270.0, 290.0), 1)
    rate_swi = round(random.uniform(410.0, 430.0), 1)
    
    diff_rate = round(rate_swi - rate_ger, 1)
    extra_needed = int(round((pop_ger / 1000.0) * diff_rate))
    
    correct_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
    options_dict = {}
    letters = ['A', 'B', 'C', 'D', 'E']
    
    for l in letters:
        if l == correct_letter:
            options_dict[l] = f"{extra_needed:,} patents"
        else:
            wrong_val = int(extra_needed * random.choice([0.1, 0.8, 1.25, 10.0]))
            options_dict[l] = f"{wrong_val:,} patents"
            
    table_md = f"""
| Country | Population (thousands) | Patent Apps per Million Hab. |
| :--- | :---: | :---: |
| **Germany** | {pop_ger:,} | {rate_ger} |
| **Switzerland** | {pop_swi:,} | {rate_swi} |
"""
    expl = f"""**Step-by-Step Calculation:**
1. **Per Capita Difference:** Calculate Switzerland rate minus Germany rate:
   $$\\text{{Diff}} = {rate_swi} - {rate_ger} = {diff_rate} \\text{{ applications per million habitant}}$$
2. **Total Additional Patents:** Apply difference to Germany population ({pop_ger:,} thousands = {pop_ger/1000:.3f} million):
   $$\\text{{Extra Patents}} = \\frac{{{pop_ger}}}{{1000}} \\times {diff_rate} = {extra_needed:,} \\text{{ patents}}$$
Option **{correct_letter}** is correct."""

    return {
        "id": f"num_pat_{random.randint(1000,9999)}",
        "type": "numerical",
        "difficulty": "Medium",
        "table": table_md,
        "question": f"Based on the table, how many additional patent applications would Germany need to match Switzerland's per capita rate?",
        "options": [f"{l}) {options_dict[l]}" for l in letters],
        "correct": f"{correct_letter}) {options_dict[correct_letter]}",
        "explanation": expl
    }

def generate_numerical_palace():
    annual_visitors = random.randint(1200000, 1600000)
    avg_ticket = round(random.uniform(12.5, 16.0), 2)
    total_rev = round(annual_visitors * avg_ticket, 2)
    
    letters = ['A', 'B', 'C', 'D', 'E']
    correct_letter = random.choice(letters)
    options_dict = {}
    
    for l in letters:
        if l == correct_letter:
            options_dict[l] = f"€{total_rev:,.2f}"
        else:
            wrong_val = round(total_rev * random.choice([0.7, 0.85, 1.15, 1.3]), 2)
            options_dict[l] = f"€{wrong_val:,.2f}"
            
    table_md = f"""
| Scenario Metric | Annual Volume | Average Ticket Price |
| :--- | :---: | :---: |
| **Royal Palace Monument Visitors** | {annual_visitors:,} visitors | €{avg_ticket:.2f} |
"""
    expl = f"""**Step-by-Step Calculation:**
1. **Total Revenue:** Multiply Annual Visitors by Average Ticket Price:
   $$\\text{{Total Revenue}} = {annual_visitors:,} \\times €{avg_ticket:.2f} = €{total_rev:,.2f}$$
Option **{correct_letter}** is correct."""

    return {
        "id": f"num_pal_{random.randint(1000,9999)}",
        "type": "numerical",
        "difficulty": "Easy",
        "table": table_md,
        "question": f"What is the total annual ticket revenue generated by the monument based on the table?",
        "options": [f"{l}) {options_dict[l]}" for l in letters],
        "correct": f"{correct_letter}) {options_dict[correct_letter]}",
        "explanation": expl
    }

# Expanded Verbal Question Bank in English
VERBAL_BANK = [
    {
        "id": "v_searle_chinese_en",
        "type": "verbal",
        "difficulty": "Medium",
        "passage": "John Searle's Chinese Room argument challenges strong artificial intelligence by holding that syntactic manipulation of symbols does not constitute semantic understanding. Imagine a non-Chinese speaker in a room who manipulates Chinese characters according to a rulebook. He produces answers indistinguishable from a native speaker, yet understands no Chinese. The 'systems reply' concedes the operator lacks understanding, but argues understanding belongs to the entire system (operator, rules, and data). Searle objects that if the operator internalizes the whole system, he still understands no Chinese.",
        "question": "Which statement accurately summarizes the systems reply and Searle's counter-argument?",
        "options": [
            "A) The systems reply claims understanding emerges at the system level; Searle counters that internalizing the system yields no real understanding.",
            "B) The systems reply holds the operator understands in isolation; Searle agrees the system produces consciousness.",
            "C) The systems reply denies perfect translation exists; Searle proves syntax eventually generates semantics.",
            "D) Both parties agree simulating neural processes is identical to abstract symbol manipulation."
        ],
        "correct": "A",
        "explanation": "The systems reply attributes understanding to the total system. Searle refutes this by noting that even if the operator memorizes all rules and data ('internalizes' the system), he performs pure symbol manipulation without grasping semantic meaning."
    },
    {
        "id": "v_godel_incompleteness_en",
        "type": "verbal",
        "difficulty": "Hard",
        "passage": "Kurt Gödel's incompleteness theorems (1931) reshaped mathematical logic. The first theorem proves that any consistent formal system capable of expressing basic arithmetic contains propositions that are true but unprovable within the system. The second theorem demonstrates that such a system cannot prove its own consistency. These findings dismantled Hilbert's formalist program, which sought to ground all mathematics on complete and consistent axiomatic foundations.",
        "question": "According to the passage, what is a direct implication of Gödel's theorems for mathematical axiomatization?",
        "options": [
            "A) They prove mathematics is inherently contradictory at all formal levels.",
            "B) They imply that in sufficiently rich formal systems, true statements exist that elude logical derivation.",
            "C) They strengthen Hilbert's formalist program by proving self-reference prevents errors.",
            "D) They show first-order logic can prove its own consistency if prime numbers are excluded."
        ],
        "correct": "B",
        "explanation": "The first incompleteness theorem directly establishes that in rich consistent formal systems, there are true statements that cannot be proven using the rules of the system itself."
    },
    {
        "id": "v_wittgenstein_private_en",
        "type": "verbal",
        "difficulty": "Medium",
        "passage": "Wittgenstein's private language argument contends that a language whose terms refer exclusively to the speaker's private sensations cannot exist. In a private language, the correctness of a term would depend solely on the speaker's subjective impression, dissolving the distinction between following a rule correctly and merely believing one is following it. Thus, mental concepts require publicly observable criteria.",
        "question": "Why is a private language logically impossible according to Wittgenstein's analysis?",
        "options": [
            "A) Because it is empirically impossible for two human beings to share identical internal sensations.",
            "B) Because without an independent, public standard of correctness, the concept of meaning dissolves.",
            "C) Because private sensations like pain or pleasure do not exist in the physical world.",
            "D) Because grammatical rules of natural language are learned exclusively through behavioral imitation."
        ],
        "correct": "B",
        "explanation": "Without external, public criteria, the speaker has no way to distinguish between actually applying a word correctly and merely thinking he is, which destroys normativity and meaning."
    },
    {
        "id": "v_banach_tarski_en",
        "type": "verbal",
        "difficulty": "Hard",
        "passage": "In measure theory, the Banach-Tarski paradox establishes that a solid 3D sphere can be decomposed into a finite number of non-overlapping pieces that, when reassembled via rigid motions, form two identical copies of the original sphere. This does not violate material physics because the pieces are non-measurable sets lacking defined volumes, whose existence depends on the Axiom of Choice.",
        "question": "What mathematical reason explains the Banach-Tarski paradox according to the text?",
        "options": [
            "A) The direct violation of physical mass conservation in real three-dimensional solids.",
            "B) The division of the sphere into pieces with extremely small decimal volume measurements.",
            "C) The use of non-measurable sets that lack well-defined volumes under the Axiom of Choice.",
            "D) The erroneous assumption that the pieces are rigid when they are actually flexible."
        ],
        "correct": "C",
        "explanation": "The paradox operates mathematically using non-measurable sets that do not have a defined volume under the Axiom of Choice, meaning physical conservation laws do not apply."
    },
    {
        "id": "v_sorites_vagueness_en",
        "type": "verbal",
        "difficulty": "Easy",
        "passage": "The Sorites paradox (or paradox of the heap) arises from vague predicates in natural language. A heap of sand remains a heap if one grain is removed; repeating this logic leads to the absurd conclusion that a single grain forms a heap. The paradox exploits vagueness rather than ambiguity: removing one grain does not alter the state, but repetition does.",
        "question": "What distinguishes vagueness from ambiguity in the context of the Sorites paradox?",
        "options": [
            "A) Vagueness means a term has multiple discrete meanings clarified by context.",
            "B) Vagueness is characterized by imprecise boundaries and gradual transitions, whereas ambiguity involves multiple distinct meanings.",
            "C) Vagueness is a logical flaw that supervaluationism completely removes from language.",
            "D) There is no difference; both terms describe the exact same linguistic phenomenon."
        ],
        "correct": "B",
        "explanation": "The passage explains that Sorites exploits vagueness—terms with imprecise, boundary-less transitions (like 'heap')—unlike ambiguity, which occurs when a word has several distinct meanings."
    },
    {
        "id": "v_popper_tolerance_en",
        "type": "verbal",
        "difficulty": "Easy",
        "passage": "Karl Popper's paradox of tolerance states that if a society is tolerant without limit, its ability to be tolerant will eventually be destroyed by the intolerant. Popper concluded that society should counter intolerant ideas with argument, but must claim the right to suppress them if the intolerant refuse rational debate and resort to force.",
        "question": "When is refusing to tolerate the intolerant justified according to Karl Popper?",
        "options": [
            "A) As soon as they express opinions that offend members of the community.",
            "B) Only when the intolerant refuse rational debate and resort to force.",
            "C) Whenever their views begin influencing democratic election results.",
            "D) Popper holds that intolerance is never justified under any circumstances."
        ],
        "correct": "B",
        "explanation": "Popper sets a clear threshold: society should debate intolerant ideas peacefully, but retains the right to suppress intolerance when the intolerant reject rational dialogue and use force."
    },
    {
        "id": "v_peter_principle_en",
        "type": "verbal",
        "difficulty": "Easy",
        "passage": "In organizational sociology, the Peter Principle states that in a hierarchy, every employee tends to rise to their level of incompetence. This implies that higher-level positions become filled with incompetent individuals who previously performed well in simpler roles, causing systemic inefficiencies.",
        "question": "What is the central claim of the Peter Principle?",
        "options": [
            "A) Good employees maintain excellence regardless of their position in the corporate hierarchy.",
            "B) Workers tend to be promoted successively until reaching a position where they are incompetent.",
            "C) Corporate training programs are useless in modern private enterprises.",
            "D) Job promotions should be decided democratically by company employees."
        ],
        "correct": "B",
        "explanation": "The principle holds that promotions are based on success in current roles rather than skills needed for the new position, stalling workers once they reach a job beyond their capability."
    },
    {
        "id": "v_rawls_justice_en",
        "type": "verbal",
        "difficulty": "Medium",
        "passage": "John Rawls proposed that principles of a just society should be agreed upon behind a 'veil of ignorance'. In this original position, no one knows their socioeconomic status, intelligence, gender, or talent. Rawls argues this guarantees impartiality, as agents will choose principles that protect the least advantaged.",
        "question": "What function does the 'veil of ignorance' serve in Rawls's theory of justice?",
        "options": [
            "A) To hide government corruption from voters to prevent civil unrest.",
            "B) To force lawmakers to ignore economic resource limits during budgeting.",
            "C) To guarantee impartiality by concealing each agent's personal position in the future society.",
            "D) To promote blind obedience to state directives."
        ],
        "correct": "C",
        "explanation": "The veil of ignorance prevents self-interested decision-making by forcing agents to choose fair rules, knowing they could end up in the most vulnerable social position."
    }
]

# Progress Persistence
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "verbal": {"accuracy": 0.0, "difficulty": "Medium", "completed": 0, "correct_total": 0},
        "numerical": {"accuracy": 0.0, "difficulty": "Medium", "completed": 0, "correct_total": 0},
        "abstract": {"accuracy": 0.0, "difficulty": "Medium", "completed": 0, "correct_total": 0},
        "failed_questions": []
    }

def save_progress(profile):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4, ensure_ascii=False)

if "profile" not in st.session_state:
    st.session_state.profile = load_progress()

if "current_test" not in st.session_state:
    st.session_state.current_test = None
    st.session_state.exam_mode = "AD5" # "AD5" or "Practice"
    st.session_state.test_questions = []
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.flags = {}
    st.session_state.eliminated = {}
    st.session_state.start_time = None
    st.session_state.time_limit_sec = 0
    st.session_state.review_mode = False
    st.session_state.selected_option = None

def start_new_test(category, mode="AD5"):
    st.session_state.current_test = category
    st.session_state.exam_mode = mode
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.flags = {}
    st.session_state.eliminated = {}
    st.session_state.selected_option = None
    st.session_state.review_mode = False
    st.session_state.start_time = time.time()
    
    # EPSO AD5 Official Limits:
    # Verbal: 20 questions in 35 min (2100 s)
    # Numerical: 10 questions in 20 min (1200 s)
    # Abstract: 10 questions in 10 min (600 s)
    if category == "verbal":
        test_length = 20
        st.session_state.time_limit_sec = 2100 if mode == "AD5" else 1800
    elif category == "numerical":
        test_length = 10
        st.session_state.time_limit_sec = 1200 if mode == "AD5" else 900
    else: # abstract
        test_length = 10
        st.session_state.time_limit_sec = 600 if mode == "AD5" else 600
        
    profile = st.session_state.profile
    test_questions = []
    
    # Recover failed questions for Spaced Repetition in practice mode
    failed_pool = [q for q in profile["failed_questions"] if q["type"] == category]
    num_review = min(len(failed_pool), 3)
    if num_review > 0 and mode == "Practice":
        for q in random.sample(failed_pool, num_review):
            q_copy = q.copy()
            q_copy["is_review"] = True
            test_questions.append(q_copy)
            
    needed = test_length - len(test_questions)
    
    if category == "verbal":
        pool = list(VERBAL_BANK)
        while len(pool) < needed:
            pool.extend(VERBAL_BANK)
        selected = random.sample(pool, needed)
        test_questions.extend(selected)
    elif category == "numerical":
        generators = [generate_numerical_patents, generate_numerical_palace]
        for _ in range(needed):
            gen = random.choice(generators)
            test_questions.append(gen())
    else: # abstract
        generators = [generate_abstract_rotation_png, generate_abstract_side_progression_png, generate_abstract_grid_shift_png]
        for _ in range(needed):
            gen = random.choice(generators)
            test_questions.append(gen())
            
    random.shuffle(test_questions)
    st.session_state.test_questions = test_questions[:test_length]

def finish_active_test():
    profile = st.session_state.profile
    category = st.session_state.current_test
    questions = st.session_state.test_questions
    answers = st.session_state.answers
    
    correct_count = 0
    for i, q in enumerate(questions):
        user_ans = answers.get(i)
        is_correct = (user_ans == q["correct"])
        if is_correct:
            correct_count += 1
            profile["failed_questions"] = [fq for fq in profile["failed_questions"] if fq["id"] != q["id"]]
        else:
            if not any(fq["id"] == q["id"] for fq in profile["failed_questions"]):
                profile["failed_questions"].append(q)
                
    profile[category]["completed"] += 1
    profile[category]["correct_total"] += correct_count
    total_q = profile[category]["completed"] * (20 if category == "verbal" else 10)
    profile[category]["accuracy"] = round((profile[category]["correct_total"] / max(1, total_q)) * 100, 1)
    
    st.session_state.profile = profile
    save_progress(profile)
    st.session_state.review_mode = True

# UI - App Title
st.title("🎯 EPSO AD5 Exam Simulator")
st.caption("Official TAO Platform Rules & Adaptive Practice Tool")

# DASHBOARD HOME
if st.session_state.current_test is None:
    st.subheader("Your Study Progress")
    profile = st.session_state.profile
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="progress-card">
            <h4 style="margin:0;color:#4F46E5;">Verbal</h4>
            <p style="font-size:22px;font-weight:bold;margin:4px 0;">{profile['verbal']['accuracy']}%</p>
            <span style="font-size:11px;color:#6B7280;">20 Qs / 35 Min</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="progress-card">
            <h4 style="margin:0;color:#059669;">Numerical</h4>
            <p style="font-size:22px;font-weight:bold;margin:4px 0;">{profile['numerical']['accuracy']}%</p>
            <span style="font-size:11px;color:#6B7280;">10 Qs / 20 Min</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="progress-card">
            <h4 style="margin:0;color:#D97706;">Abstract</h4>
            <p style="font-size:22px;font-weight:bold;margin:4px 0;">{profile['abstract']['accuracy']}%</p>
            <span style="font-size:11px;color:#6B7280;">10 Qs / 10 Min</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.subheader("Select Exam Mode")
    
    mode_choice = st.radio("Choose Mode:", ["Official EPSO AD5 Mode (Strict Timers & TAO Tools)", "Adaptive Practice Mode (Free Pace)"], index=0)
    selected_mode = "AD5" if "Official" in mode_choice else "Practice"
    
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    
    if st.button("💬 Start Verbal Reasoning (20 Questions - 35 Min)"):
        start_new_test("verbal", selected_mode)
        st.rerun()
        
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
    if st.button("📊 Start Numerical Reasoning (10 Questions - 20 Min)"):
        start_new_test("numerical", selected_mode)
        st.rerun()
        
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
    if st.button("🧩 Start Abstract Reasoning (10 Questions - 10 Min)"):
        start_new_test("abstract", selected_mode)
        st.rerun()

# TEST REVIEW / RESULTS SCREEN
elif st.session_state.review_mode:
    questions = st.session_state.test_questions
    answers = st.session_state.answers
    correct_count = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["correct"])
    pct = int((correct_count / len(questions)) * 100)
    
    st.subheader("Exam Results & Detailed Solutions")
    st.markdown(f"""
    <div style="background-color: #F9FAFB; padding: 20px; border-radius: 16px; border: 2px solid #E5E7EB; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 13px; color: #6B7280; font-weight: bold; text-transform: uppercase;">Final Score</span>
        <h1 style="color: {'#16A34A' if pct>=60 else '#DC2626'}; font-size: 42px; margin: 5px 0;">{correct_count} / {len(questions)}</h1>
        <p style="font-size: 16px; font-weight: bold; margin: 0;">Accuracy: {pct}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    for i, q in enumerate(questions):
        user_ans = answers.get(i)
        is_correct = (user_ans == q["correct"])
        status_str = "✅ Correct" if is_correct else f"❌ Incorrect (You chose {user_ans if user_ans else 'Blank'})"
        
        with st.expander(f"Question {i+1}: {status_str}"):
            if "passage" in q and q["passage"]:
                st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
            if "table" in q and q["table"]:
                st.markdown(q["table"])
            if "img_bytes" in q and q["img_bytes"]:
                st.image(q["img_bytes"], use_container_width=True)
                
            st.markdown(f"**Question:** {q['question']}")
            for opt in q["options"]:
                if opt == q["correct"]:
                    st.write(f"🟢 **{opt} (Correct Answer)**")
                elif opt == user_ans:
                    st.write(f"🔴 **{opt} (Your Selection)**")
                else:
                    st.write(f"⚪ {opt}")
            st.markdown(q["explanation"])
            
    if st.button("⬅️ Return to Main Menu"):
        st.session_state.current_test = None
        st.session_state.review_mode = False
        st.rerun()

# ACTIVE QUESTION SCREEN
else:
    category = st.session_state.current_test
    questions = st.session_state.test_questions
    idx = st.session_state.current_index
    q = questions[idx]
    
    # Calculate Timer
    elapsed = int(time.time() - st.session_state.start_time)
    rem_sec = max(0, st.session_state.time_limit_sec - elapsed)
    mins, secs = divmod(rem_sec, 60)
    
    # Top Header Bar
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.markdown(f"**{category.upper()} REASONING** — Question **{idx+1} of {len(questions)}**")
    with col_t2:
        st.markdown(f"<div class='timer-badge'>⏱️ {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
        
    st.progress((idx + 1) / len(questions))
    
    # Flag for review button
    is_flagged = st.session_state.flags.get(idx, False)
    if st.checkbox("🚩 Flag for Review", value=is_flagged, key=f"flag_{idx}"):
        st.session_state.flags[idx] = True
    else:
        st.session_state.flags[idx] = False
        
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
    
    # Display Content
    if "passage" in q and q["passage"]:
        st.markdown("**Reading Passage:**")
        st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
        
    if "table" in q and q["table"]:
        st.markdown("**Data Table:**")
        st.markdown(q["table"])
        
    if "img_bytes" in q and q["img_bytes"]:
        st.markdown("**Abstract Visual Sequence:**")
        st.image(q["img_bytes"], use_container_width=True)
        
    st.markdown(f"### {q['question']}")
    
    # Options Radio Selector
    options_list = q["options"]
    current_sel = st.session_state.answers.get(idx, None)
    selected_idx = options_list.index(current_sel) if current_sel in options_list else None
    
    choice = st.radio(
        "Select your answer:",
        options=options_list,
        index=selected_idx,
        key=f"radio_q_{idx}"
    )
    
    if choice:
        st.session_state.answers[idx] = choice
        
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    
    # Navigation Buttons
    c_prev, c_next, c_sub = st.columns([1, 1, 1])
    with c_prev:
        if idx > 0 and st.button("⬅️ Previous"):
            st.session_state.current_index -= 1
            st.rerun()
    with c_next:
        if idx + 1 < len(questions) and st.button("Next ➡️"):
            st.session_state.current_index += 1
            st.rerun()
    with c_sub:
        if st.button("🏁 Finish Exam"):
            finish_active_test()
            st.rerun()
            
    # E-Tools Scratchpad Expander
    with st.expander("🛠️ TAO E-Tools: Scratchpad / Notes"):
        st.text_area("Use this area for rough calculations or text notes:", height=100, key=f"scratch_{idx}")
