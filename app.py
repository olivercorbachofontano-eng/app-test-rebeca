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

# Mobile-Friendly Custom Styles
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
        font-size: 1.05rem;
        line-height: 1.65;
        color: #1F2937;
        margin-bottom: 20px;
        max-height: 300px;
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
        font-size: 1.2rem;
        padding: 8px 16px;
        border-radius: 20px;
        border: 1px solid #F59E0B;
        display: inline-block;
    }
    
    .tao-box {
        background-color: #F3F4F6;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #D1D5DB;
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
        "question": f"Which option (A, B, C, D, or E) logically completes the 5th frame in the sequence?",
        "options": [f"Option {l}" for l in labels],
        "correct": labels[correct_opt_idx],
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
        "question": f"Which option (A, B, C, D, or E) logically completes the 5th frame in the sequence?",
        "options": [f"Option {l}" for l in labels],
        "correct": labels[correct_opt_idx],
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
        "question": f"Which option (A, B, C, D, or E) logically completes the 5th frame in the sequence?",
        "options": [f"Option {l}" for l in labels],
        "correct": labels[correct_opt_idx],
        "img_bytes": buf.getvalue(),
        "explanation": expl
    }

VERBAL_BANK = [
    {
        "id": "v_searle_chinese",
        "type": "verbal",
        "difficulty": "Medium",
        "passage": "John Searle's Chinese Room argument challenges Strong Artificial Intelligence by maintaining that syntactic symbol manipulation does not constitute semantic understanding [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. Imagine a non-Chinese speaker in a sealed room manipulating Chinese characters according to an English rulebook [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. The person produces responses indistinguishable from a native speaker, yet understands no Chinese [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. The 'Systems Reply' concedes the operator lacks understanding but asserts that understanding belongs to the entire system (operator, rules, data) [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. Searle rebuts that if the operator internalizes the whole system, understanding remains absent [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "Which statement correctly synthesizes the Systems Reply and Searle's counter-argument?",
        "options": [
            "A) The Systems Reply claims understanding emerges at the system level; Searle rebuts that internalizing the system yields no true semantics.",
            "B) The Systems Reply claims the operator understands in isolation; Searle agrees the total system achieves consciousness.",
            "C) The Systems Reply denies translation is possible; Searle proves syntax eventually generates semantics.",
            "D) Both parties agree that simulating neural processes is identical to abstract symbol manipulation."
        ],
        "correct": "A",
        "explanation": "The Systems Reply posits that comprehension is a property of the total system rather than the human operator [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. Searle counters that even if the human memorizes and internalizes every rule and dataset of the system, the person is still executing pure syntactic manipulation without grasping semantic meaning [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_godel_incompleteness",
        "type": "verbal",
        "difficulty": "Hard",
        "passage": "Kurt Gödel's incompleteness theorems (1931) fundamentally reshaped mathematical logic [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. The First Theorem proves that any consistent formal system capable of expressing basic arithmetic contains propositions that are true but unprovable within the system [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. The Second Theorem demonstrates that such a system cannot prove its own consistency [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. These conclusions dismantled Hilbert's formalist program, which sought to establish mathematics on a complete and provably consistent axiomatic foundation [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "According to the passage, what direct implication do Gödel's theorems have for mathematical axiomatization?",
        "options": [
            "A) They prove that mathematics is inherently self-contradictory across all axiomatic domains.",
            "B) They demonstrate that in sufficiently rich formal systems, true statements exist that cannot be derived logically.",
            "C) They strengthen Hilbert's program by showing self-reference prevents contradiction.",
            "D) They show that first-order logic can verify its own consistency if prime numbers are excluded."
        ],
        "correct": "B",
        "explanation": "Gödel's First Theorem establishes that in any consistent formal system expressing basic arithmetic, there are true mathematical statements that evade derivation through the system's formal rules [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_wittgenstein_private",
        "type": "verbal",
        "difficulty": "Medium",
        "passage": "Wittgenstein's Private Language Argument holds that a language whose terms refer to inner sensations accessible solely to the speaker is logically impossible [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. In a private language, correctness would depend solely on the speaker's subjective impression, dissolving the distinction between following a rule correctly and merely believing one is following it [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. Consequently, mental concepts require publicly observable criteria to possess meaning [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "Why is a private language logically untenable according to Wittgenstein's analysis?",
        "options": [
            "A) Because human beings cannot share identical physical sensations.",
            "B) Because without an independent external standard, the concept of rule-following correctness dissolves.",
            "C) Because subjective sensations of pain or pleasure do not exist in objective reality.",
            "D) Because natural grammar is acquired exclusively through behavioral mimicry."
        ],
        "correct": "B",
        "explanation": "Without public, independent criteria of correctness, a speaker has no objective way to distinguish between correctly applying a word and merely thinking they are doing so, destroying linguistic normativity [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_banach_tarski",
        "type": "verbal",
        "difficulty": "Hard",
        "passage": "The Banach-Tarski paradox states that a solid 3D ball can be decomposed into a finite number of non-overlapping pieces, which can then be reassembled via rigid motions to form two identical copies of the original ball [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. This does not violate physical conservation laws because the pieces involved are non-measurable sets lacking a defined volume, whose existence depends on the Axiom of Choice [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. The result highlights the counter-intuitive consequences of admitting non-constructive sets in measure theory [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "What mathematical factor resolves the apparent contradiction of the Banach-Tarski paradox?",
        "options": [
            "A) Direct violation of physical mass conservation in solid matter.",
            "B) Division of the sphere into infinitesimally small atomic particles.",
            "C) The employment of non-measurable sets that lack a well-defined volume under the Axiom of Choice.",
            "D) The false assumption that the sphere's pieces are rigid solids."
        ],
        "correct": "C",
        "explanation": "The paradox operates purely in theoretical set theory using non-measurable sets that do not possess a standard geometric volume, enabled by the Axiom of Choice [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_popper_tolerance",
        "type": "verbal",
        "difficulty": "Easy",
        "passage": "Karl Popper's Paradox of Tolerance posits that if a society practices unlimited tolerance, its ability to remain tolerant will eventually be destroyed by the intolerant [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. Popper did not advocate suppressing intolerant ideas immediately (preferring rational debate and public opinion), but maintained that society must claim the right to suppress intolerance when the intolerant refuse rational discourse and resort to force [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "According to the passage, when is society justified in withholding tolerance from the intolerant?",
        "options": [
            "A) As soon as intolerant opinions cause offense to minority communities.",
            "B) Only when the intolerant abandon rational debate and engage in force or violence.",
            "C) Whenever intolerant views influence democratic election outcomes.",
            "D) Popper asserts intolerance is never justified under any circumstances."
        ],
        "correct": "B",
        "explanation": "Popper sets a specific threshold: tolerance should be extended to debate, but society reserves the right to suppress intolerance when intolerant actors reject reason and rely on violence or force [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_coase_theorem",
        "type": "verbal",
        "difficulty": "Medium",
        "passage": "The Coase Theorem states that if property rights are well-defined and transaction costs are zero, private bargaining will lead to an efficient allocation of resources regardless of initial property distribution [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. However, in real-world markets, transaction costs that hinder private bargaining are pervasive [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. Thus, Coase's work is not an argument for naive laissez-faire, but a framework to analyze how institutional costs shape market outcomes [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "What real-world factor restricts the direct application of the Coase Theorem's efficiency prediction?",
        "options": [
            "A) Constant intervention by judicial courts.",
            "B) The widespread existence of transaction costs that impede private negotiations.",
            "C) The mathematical impossibility of defining intellectual property rights.",
            "D) A lack of profit-maximizing behavior among economic agents."
        ],
        "correct": "B",
        "explanation": "In reality, transaction costs are substantial, meaning market transactions cannot automatically resolve externalities without institutional framework considerations [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_frame_problem",
        "type": "verbal",
        "difficulty": "Hard",
        "passage": "The Frame Problem in artificial intelligence exposes deep challenges in representing how an intelligent system updates knowledge about a changing world [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. When an action occurs, the system must determine which facts remain unchanged; explicitly listing all unchanged facts is computationally intractable [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. This indicates that intelligence requires default heuristic assumptions regarding relevance rather than pure deductive logic [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "What does the Frame Problem reveal about deductive logic in AI reasoning?",
        "options": [
            "A) That formal logic effortlessly represents all real-world environmental changes.",
            "B) That pure formal deduction without relevance heuristics is computationally intractable for updating real-world states.",
            "C) That qualification problems ensure action success if environmental variables are ignored.",
            "D) That human rationality relies exclusively on first-order predicate calculus."
        ],
        "correct": "B",
        "explanation": "Explicitly deducting all unchanged background facts after an action causes computational explosion, demonstrating that intelligence requires heuristic relevance rules rather than exhaustive deduction [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_newcomb_paradox",
        "type": "verbal",
        "difficulty": "Hard",
        "passage": "Newcomb's Paradox pit two standard decision theory principles against each other [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. A highly accurate predictor places 1 million euros in an opaque box if it predicted the agent will take only that box, and 1,000 euros in an open box that the agent can also take [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. The expected utility principle advises taking only the opaque box, while the dominance principle advises taking both boxes [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]. The conflict shows that the principles assume incompatible premises regarding whether choices are causally independent of predetermined states [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf].",
        "question": "What core assumption is in conflict in Newcomb's Paradox according to the text?",
        "options": [
            "A) Pure mathematics versus relativistic physics.",
            "B) Whether a rational decision can be treated as causally independent of a predetermined world state.",
            "C) Human intuition versus probability axioms.",
            "D) Wealth accumulation ethics versus distributive justice."
        ],
        "correct": "B",
        "explanation": "The paradox arises because decision principles conflict on whether the player's choice is causally independent of the predictor's prior state determination [6d3714c8-7fd8-4ebc-b514-7454a608d54f.pdf]."
    },
    {
        "id": "v_peter_principle",
        "type": "verbal",
        "difficulty": "Easy",
        "passage": "In organizational sociology, the Peter Principle states that in a hierarchy, every employee tends to rise to their level of incompetence [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. Promotions are awarded based on success in current roles rather than competence for the new role [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. Consequently, higher positions become filled with individuals who perform poorly, while organizational work is carried out by employees who have not yet reached their limit [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf].",
        "question": "What is the central thesis of the Peter Principle?",
        "options": [
            "A) Excellent performance guarantees success across all corporate management levels.",
            "B) Employees are promoted iteratively until they reach a role where they lack competence.",
            "C) Technical training programs are ineffective in modern firms.",
            "D) Executive promotions should be decided through democratic voting."
        ],
        "correct": "B",
        "explanation": "The principle highlights that promotion mechanics rely on past success, leading individuals to eventually settle in positions beyond their competence [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]."
    },
    {
        "id": "v_bionics_concept",
        "type": "verbal",
        "difficulty": "Easy",
        "passage": "Bionics is the interdisciplinary science of mimicking natural biological mechanisms to design advanced technological and medical devices [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. Neuroscientists note that bionics bridges biological abstraction and engineering solutions, such as neural prosthetics connected directly to the central nervous system [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. By synthesizing biological structures with material science, bionics produces innovative health and industrial designs [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf].",
        "question": "Which statement accurately describes the objective of bionics according to the passage?",
        "options": [
            "A) Replacing all human organs with purely mechanical devices.",
            "B) Designing artificial technologies and health solutions by imitating biological structures and mechanisms.",
            "C) Restricting medical research to archaeological fossil analysis.",
            "D) Rejecting aesthetic creativity in modern engineering."
        ],
        "correct": "B",
        "explanation": "Bionics explicitly applies biological principles and natural mechanisms to engineering and technological innovations [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]."
    }
]

def generate_numerical_patents():
    pop = random.randint(7000, 85000)
    rate04 = round(random.uniform(250.0, 420.0), 1)
    rate05 = round(rate04 + random.uniform(5.0, 25.0), 1)
    target_rate = round(rate05 + random.uniform(80.0, 150.0), 1)
    
    diff_rate = round(target_rate - rate05, 1)
    diff_patents = int(round((pop / 1000.0) * diff_rate))
    
    table_md = f"""
| Country | Population 2005 (thousands) | Patent Apps per M hab. (2004) | Patent Apps per M hab. (2005) |
| :--- | :---: | :---: | :---: |
| **Germany / Benchmark** | {pop:,} | {rate04} | {rate05} |
| **Switzerland / Target** | 7,441 | 408.4 | {target_rate} |
"""
    options = [
        f"A) {diff_patents - 1500:,} patents",
        f"B) {diff_patents + 2400:,} patents",
        f"C) {diff_patents - 450:,} patents",
        f"D) {diff_patents + 850:,} patents",
        f"E) {diff_patents:,} patents"
    ]
    
    return {
        "id": f"num_pat_{random.randint(1000,9999)}",
        "type": "numerical",
        "difficulty": "Medium",
        "table": table_md,
        "question": f"Based on the table, how many additional patent applications would Germany need to file in 2005 to match Switzerland's per capita rate of {target_rate} per million inhabitants?",
        "options": options,
        "correct": "E",
        "explanation": f"**Step-by-Step Calculation:**\n1. **Per Capita Rate Gap:** {target_rate} - {rate05} = **{diff_rate} patent applications per million inhabitants**.\n2. **Population Application:** Germany's population is {pop:,} thousand (or {pop/1000:.3f} million).\n3. **Additional Patents Needed:** ({pop}/1000) × {diff_rate} = **{diff_patents:,} additional patent applications** (Option E)."
    }

def generate_numerical_palace():
    visitors = random.randint(120, 280) * 1000
    fee = round(random.uniform(12.50, 18.50), 2)
    discount_pct = random.choice([15, 20, 25])
    discounted_visitors_pct = random.choice([30, 40, 50])
    
    disc_fee = round(fee * (1 - discount_pct/100.0), 2)
    full_visitors = int(visitors * (1 - discounted_visitors_pct/100.0))
    disc_visitors = int(visitors * (discounted_visitors_pct/100.0))
    
    total_rev = round(full_visitors * fee + disc_visitors * disc_fee, 2)
    
    table_md = f"""
| Category | Metric Value |
| :--- | :--- |
| **Total Annual Visitors** | {visitors:,} visitors |
| **Standard Entry Fee** | €{fee:.2f} per person |
| **Discounted Ticket Share** | {discounted_visitors_pct}% of total visitors |
| **Discount Rate** | {discount_pct}% off standard entry fee |
"""
    options = [
        f"A) €{total_rev * 1.15:,.2f}",
        f"B) €{total_rev:,.2f}",
        f"C) €{total_rev * 0.85:,.2f}",
        f"D) €{total_rev * 1.08:,.2f}",
        f"E) €{total_rev * 0.92:,.2f}"
    ]
    
    return {
        "id": f"num_pal_{random.randint(1000,9999)}",
        "type": "numerical",
        "difficulty": "Easy",
        "table": table_md,
        "question": "What is the total annual ticket revenue generated by the monument?",
        "options": options,
        "correct": "B",
        "explanation": f"**Step-by-Step Calculation:**\n1. **Full-Price Visitors:** {100-discounted_visitors_pct}% of {visitors:,} = {full_visitors:,} visitors × €{fee:.2f} = **€{full_visitors*fee:,.2f}**.\n2. **Discounted Visitors:** {discounted_visitors_pct}% of {visitors:,} = {disc_visitors:,} visitors × €{disc_fee:.2f} = **€{disc_visitors*disc_fee:,.2f}**.\n3. **Total Revenue:** €{full_visitors*fee:,.2f} + €{disc_visitors*disc_fee:,.2f} = **€{total_rev:,.2f}** (Option B)."
    }

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "verbal": {"accuracy": 0.0, "difficulty": "Easy", "completed": 0, "correct_total": 0},
        "numerical": {"accuracy": 0.0, "difficulty": "Easy", "completed": 0, "correct_total": 0},
        "abstract": {"accuracy": 0.0, "difficulty": "Easy", "completed": 0, "correct_total": 0},
        "failed_questions": []
    }

def save_progress(profile):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4, ensure_ascii=False)

if "profile" not in st.session_state:
    st.session_state.profile = load_progress()

if "current_test" not in st.session_state:
    st.session_state.current_test = None
    st.session_state.test_mode = "practice_adaptive"
    st.session_state.test_questions = []
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.flagged = set()
    st.session_state.eliminated = {}
    st.session_state.review_mode = False
    st.session_state.summary_grid_mode = False
    st.session_state.selected_option = None
    st.session_state.show_explanation = False
    st.session_state.start_time = None
    st.session_state.time_limit = 0
    st.session_state.scratchpad = ""

def start_new_test(category, mode="practice_adaptive", custom_length=None):
    st.session_state.current_test = category
    st.session_state.test_mode = mode
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.flagged = set()
    st.session_state.eliminated = {}
    st.session_state.show_explanation = False
    st.session_state.review_mode = False
    st.session_state.summary_grid_mode = False
    st.session_state.selected_option = None
    st.session_state.start_time = time.time()
    
    if mode == "epso_ad5":
        if category == "verbal":
            test_length = 20
            st.session_state.time_limit = 35 * 60
        elif category == "numerical":
            test_length = 10
            st.session_state.time_limit = 20 * 60
        else:
            test_length = 10
            st.session_state.time_limit = 10 * 60
    else:
        test_length = custom_length if custom_length else (20 if category == "verbal" else 10)
        st.session_state.time_limit = 0
        
    profile = st.session_state.profile
    user_diff = profile[category]["difficulty"]
    
    failed_pool = [q for q in profile["failed_questions"] if q["type"] == category]
    test_questions = []
    
    num_review = min(len(failed_pool), 3)
    if num_review > 0:
        sampled_failed = random.sample(failed_pool, num_review)
        for q in sampled_failed:
            q_copy = q.copy()
            q_copy["is_review"] = True
            test_questions.append(q_copy)
            
    needed = test_length - len(test_questions)
    
    if category == "verbal":
        bank_pool = [q for q in VERBAL_BANK if q["difficulty"] == user_diff]
        if len(bank_pool) < needed:
            other_diffs = [q for q in VERBAL_BANK if q["difficulty"] != user_diff]
            bank_pool += other_diffs
        existing_ids = {q["id"] for q in test_questions}
        available_pool = [q for q in bank_pool if q["id"] not in existing_ids]
        if len(available_pool) < needed:
            available_pool = VERBAL_BANK
        selected_verbal = random.sample(available_pool, min(len(available_pool), needed))
        test_questions.extend(selected_verbal)
        
    elif category == "numerical":
        for _ in range(needed):
            generator = random.choice([generate_numerical_patents, generate_numerical_palace])
            test_questions.append(generator())
            
    elif category == "abstract":
        for _ in range(needed):
            generator = random.choice([generate_abstract_rotation_png, generate_abstract_side_progression_png, generate_abstract_grid_shift_png])
            test_questions.append(generator())
            
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
        if user_ans == q["correct"]:
            correct_count += 1
            profile["failed_questions"] = [fq for fq in profile["failed_questions"] if fq["id"] != q["id"]]
        else:
            if not any(fq["id"] == q["id"] for fq in profile["failed_questions"]):
                profile["failed_questions"].append({
                    "id": q["id"],
                    "type": q["type"],
                    "difficulty": q["difficulty"],
                    "question": q["question"],
                    "options": q["options"],
                    "correct": q["correct"],
                    "explanation": q["explanation"]
                })
                
    profile[category]["completed"] += 1
    profile[category]["correct_total"] += correct_count
    total_q = profile[category]["completed"] * len(questions)
    profile[category]["accuracy"] = round((profile[category]["correct_total"] / max(1, total_q)) * 100, 1)
    
    pct_correct = (correct_count / len(questions)) * 100
    curr_diff = profile[category]["difficulty"]
    if pct_correct >= 80:
        profile[category]["difficulty"] = "Medium" if curr_diff == "Easy" else "Hard"
    elif pct_correct < 50:
        profile[category]["difficulty"] = "Medium" if curr_diff == "Hard" else "Easy"
        
    st.session_state.profile = profile
    save_progress(profile)
    st.session_state.review_mode = True
    st.session_state.summary_grid_mode = False

# APP HEADER
st.title("🎯 EPSO AD5 Exam Simulator")
st.caption("Official TAO Remote Testing Environment & Adaptive Practice Engine")

# DASHBOARD VIEW
if st.session_state.current_test is None:
    st.subheader("Your Study & Performance Overview")
    profile = st.session_state.profile
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="progress-card">
            <h4 style="margin:0;color:#4F46E5;">Verbal</h4>
            <p style="font-size:22px;font-weight:bold;margin:4px 0;">{profile['verbal']['accuracy']}%</p>
            <span style="font-size:11px;background:#EEF2F6;padding:3px 8px;border-radius:12px;color:#4F46E5;font-weight:bold;">{profile['verbal']['difficulty']}</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="progress-card">
            <h4 style="margin:0;color:#059669;">Numerical</h4>
            <p style="font-size:22px;font-weight:bold;margin:4px 0;">{profile['numerical']['accuracy']}%</p>
            <span style="font-size:11px;background:#ECFDF5;padding:3px 8px;border-radius:12px;color:#059669;font-weight:bold;">{profile['numerical']['difficulty']}</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="progress-card">
            <h4 style="margin:0;color:#D97706;">Abstract</h4>
            <p style="font-size:22px;font-weight:bold;margin:4px 0;">{profile['abstract']['accuracy']}%</p>
            <span style="font-size:11px;background:#FEF3C7;padding:3px 8px;border-radius:12px;color:#D97706;font-weight:bold;">{profile['abstract']['difficulty']}</span>
        </div>
        """, unsafe_allow_html=True)
        
    failed_count = len(profile["failed_questions"])
    if failed_count > 0:
        st.info(f"🔄 **Spaced Repetition Active:** You have **{failed_count} questions in your review queue**. They will automatically reappear in your upcoming tests to reinforce weak concepts.")
    else:
        st.success("🎉 **All Concepts Mastered!** No failed questions currently in your review queue.")
        
    st.markdown("---")
    
    st.subheader("Select Exam Mode")
    
    tab_epso, tab_practice = st.tabs(["🎯 Official EPSO AD5 Mock Exam", "🧠 Adaptive Practice Mode"])
    
    with tab_epso:
        st.markdown("""
        **Official EPSO AD5 Testing Parameters (TAO Platform):**
        - **Verbal Reasoning:** 20 Questions | **35 Minutes** (105s / q)
        - **Numerical Reasoning:** 10 Questions | **20 Minutes** (120s / q)
        - **Abstract Reasoning:** 10 Questions | **10 Minutes** (60s / q)
        
        *Includes official countdown timer, scratchpad notes, question flagging, and option eliminator.*
        """)
        
        if st.button("💬 Start EPSO Verbal Reasoning (35 Min)"):
            start_new_test("verbal", mode="epso_ad5")
            st.rerun()
            
        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        if st.button("📊 Start EPSO Numerical Reasoning (20 Min)"):
            start_new_test("numerical", mode="epso_ad5")
            st.rerun()
            
        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        if st.button("🧩 Start EPSO Abstract Reasoning (10 Min)"):
            start_new_test("abstract", mode="epso_ad5")
            st.rerun()
            
    with tab_practice:
        st.markdown("Practice at your own pace without timer constraints. The engine adapts difficulty based on your real-time performance.")
        
        c_len, c_diff = st.columns(2)
        with c_len:
            custom_q_len = st.selectbox("Test Length:", [10, 20, 30], index=0)
            
        if st.button("💬 Practice Verbal Reasoning"):
            start_new_test("verbal", mode="practice_adaptive", custom_length=custom_q_len)
            st.rerun()
            
        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        if st.button("📊 Practice Numerical Reasoning"):
            start_new_test("numerical", mode="practice_adaptive", custom_length=custom_q_len)
            st.rerun()
            
        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
        if st.button("🧩 Practice Abstract Reasoning"):
            start_new_test("abstract", mode="practice_adaptive", custom_length=custom_q_len)
            st.rerun()

# TAO SUMMARY GRID VIEW
elif st.session_state.summary_grid_mode:
    questions = st.session_state.test_questions
    answers = st.session_state.answers
    flagged = st.session_state.flagged
    
    st.subheader("📋 TAO Exam Review Summary")
    st.markdown("Review your question status before submitting your test:")
    
    cols = st.columns(5)
    for idx, q in enumerate(questions):
        c = cols[idx % 5]
        is_ans = idx in answers
        is_flag = idx in flagged
        
        status_str = "✅ Ans" if is_ans else "⚪ Unans"
        if is_flag:
            status_str += " 🚩"
            
        with c:
            if st.button(f"Q{idx+1}\n{status_str}", key=f"grid_btn_{idx}"):
                st.session_state.current_index = idx
                st.session_state.summary_grid_mode = False
                st.rerun()
                
    st.markdown("---")
    col_sub, col_ret = st.columns(2)
    with col_sub:
        if st.button("🚨 Final Submit Test"):
            finish_active_test()
            st.rerun()
    with col_ret:
        if st.button("⬅️ Return to Question"):
            st.session_state.summary_grid_mode = False
            st.rerun()

# REVIEW MODE
elif st.session_state.review_mode:
    category = st.session_state.current_test
    questions = st.session_state.test_questions
    answers = st.session_state.answers
    
    correct_count = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["correct"])
    pct = int((correct_count / len(questions)) * 100)
    
    st.markdown("### Test Completed!")
    
    color_score = "#16A34A" if pct >= 70 else "#DC2626"
    st.markdown(f"""
    <div style="background-color: #F9FAFB; padding: 20px; border-radius: 16px; border: 2px solid #E5E7EB; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 13px; color: #6B7280; font-weight: bold; text-transform: uppercase;">Official Test Score</span>
        <h1 style="color: {color_score}; font-size: 46px; margin: 4px 0;">{correct_count} / {len(questions)}</h1>
        <p style="font-size: 18px; font-weight: bold; margin: 0;">Accuracy: {pct}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if pct >= 70:
        st.success("🌟 **Pass Benchmark Reached!** Excellent logical deduction and time management.")
    else:
        st.warning("⚠️ **Pass Benchmark Not Met.** Review the detailed explanations below to strengthen weak concepts.")
        
    st.markdown("---")
    st.markdown("### Question Breakdown & Detailed Explanations")
    
    for i, q in enumerate(questions):
        user_ans = answers.get(i)
        is_correct = (user_ans == q["correct"])
        icon = "✅ Correct" if is_correct else f"❌ Incorrect (You chose {user_ans if user_ans else 'Blank'})"
        
        with st.expander(f"Question {i+1}: {icon}"):
            if "passage" in q and q["passage"]:
                st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
            if "table" in q and q["table"]:
                st.markdown(q["table"])
            if "img_bytes" in q and q["img_bytes"]:
                st.image(q["img_bytes"], use_container_width=True)
                
            st.markdown(f"**Question:** {q['question']}")
            for opt in q["options"]:
                letter = opt[0]
                if letter == q["correct"]:
                    st.write(f"🟢 **{opt} (Correct Answer)**")
                elif letter == user_ans:
                    st.write(f"🔴 **{opt} (Your Choice)**")
                else:
                    st.write(f"⚪ {opt}")
                    
            st.markdown(q["explanation"])
            
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    if st.button("⬅️ Return to Main Menu"):
        st.session_state.current_test = None
        st.session_state.review_mode = False
        st.rerun()

# ACTIVE QUESTION VIEW
else:
    category = st.session_state.current_test
    questions = st.session_state.test_questions
    idx = st.session_state.current_index
    q = questions[idx]
    
    if st.session_state.test_mode == "epso_ad5":
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, int(st.session_state.time_limit - elapsed))
        mins, secs = divmod(remaining, 60)
        
        if remaining == 0:
            st.error("⏰ **Time's Up!** Auto-submitting your exam...")
            finish_active_test()
            st.rerun()
            
        t_col1, t_col2 = st.columns([2, 1])
        with t_col1:
            st.markdown(f"**EPSO AD5 {category.upper()} EXAM**")
        with t_col2:
            st.markdown(f"<div class='timer-badge'>⏱️ {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
            
    st.progress((idx + 1) / len(questions))
    
    col_f, col_e, col_s = st.columns(3)
    with col_f:
        is_flagged = idx in st.session_state.flagged
        flag_label = "🚩 Flagged" if is_flagged else "🏳️ Flag for Review"
        if st.button(flag_label, key=f"flag_btn_{idx}"):
            if is_flagged:
                st.session_state.flagged.remove(idx)
            else:
                st.session_state.flagged.add(idx)
            st.rerun()
            
    with col_e:
        elim_list = st.session_state.eliminated.get(idx, [])
        st.caption(f"✂️ Eliminated: {', '.join(elim_list) if elim_list else 'None'}")
        
    with col_s:
        with st.popover("🧮 E-Tools"):
            st.markdown("**TAO Scratchpad & Calculator Tool:**")
            st.text_area("Scratchpad Notes:", key=f"scratch_{idx}", value=st.session_state.scratchpad)
            
    st.markdown("---")
    
    if "passage" in q and q["passage"]:
        st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
    if "table" in q and q["table"]:
        st.markdown(q["table"])
    if "img_bytes" in q and q["img_bytes"]:
        st.image(q["img_bytes"], use_container_width=True)
        
    st.markdown(f"### Question {idx+1} of {len(questions)}")
    st.markdown(f"**{q['question']}**")
    
    options_list = q["options"]
    curr_elim = st.session_state.eliminated.get(idx, [])
    
    st.markdown("**Option Eliminator (Strike out distractors):**")
    e_cols = st.columns(len(options_list))
    for opt_idx, opt_str in enumerate(options_list):
        letter = opt_str[0]
        with e_cols[opt_idx]:
            is_elim = letter in curr_elim
            btn_txt = f"❌ {letter}" if is_elim else f"✂️ {letter}"
            if st.button(btn_txt, key=f"elim_{idx}_{letter}"):
                if is_elim:
                    curr_elim.remove(letter)
                else:
                    curr_elim.append(letter)
                st.session_state.eliminated[idx] = curr_elim
                st.rerun()
                
    st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
    
    user_choice = st.radio(
        "Select your answer:",
        options=options_list,
        index=None if idx not in st.session_state.answers else [o[0] for o in options_list].index(st.session_state.answers[idx]),
        key=f"radio_choice_{idx}"
    )
    
    if user_choice:
        st.session_state.answers[idx] = user_choice[0]
        
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        if idx > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_index -= 1
                st.rerun()
                
    with nav_col2:
        if st.button("📋 Review Summary"):
            st.session_state.summary_grid_mode = True
            st.rerun()
            
    with nav_col3:
        if idx + 1 < len(questions):
            if st.button("Next ➡️"):
                st.session_state.current_index += 1
                st.rerun()
        else:
            if st.button("🚨 Finish Test"):
                st.session_state.summary_grid_mode = True
                st.rerun()
