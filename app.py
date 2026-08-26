import streamlit as st
import json
import os
import random
import math

# Page setup for mobile responsiveness
st.set_page_config(
    page_title="Adaptive Exam Simulator",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Progress file persistence path
PROGRESS_FILE = "progreso_estudiante.json"

# Clean CSS styling optimized for thumb-friendly mobile interaction
st.markdown("""
<style>
    /* Compact padding for mobile viewports */
    .reportview-container .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
    
    /* Prominent modern buttons with pleasant gradients */
    div.stButton > button:first-child {
        width: 100%;
        height: 3.4rem;
        font-size: 1.15rem !important;
        font-weight: bold;
        border-radius: 14px;
        border: none;
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.15);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #4338CA 0%, #2563EB 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 12px rgba(79, 70, 229, 0.25);
    }
    
    /* Stylized action boxes for navigation */
    div.secondary-btn > div.stButton > button:first-child {
        background: #F3F4F6 !important;
        color: #374151 !important;
        border: 1px solid #D1D5DB !important;
        box-shadow: none !important;
    }
    div.secondary-btn > div.stButton > button:first-child:hover {
        background: #E5E7EB !important;
        transform: none !important;
    }
    
    /* Spacious Radio Options containers */
    div.row-widget.stRadio > div {
        background-color: #F9FAFB;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        margin-bottom: 12px;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.01);
    }
    
    /* Text reading block layout (Verbal) */
    .passage-box {
        background-color: #F0FDF4;
        border-left: 5px solid #16A34A;
        padding: 15px;
        border-radius: 8px;
        font-size: 1.02rem;
        line-height: 1.6;
        color: #1F2937;
        margin-bottom: 20px;
        max-height: 300px;
        overflow-y: auto;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    
    /* Dashboard statistics card */
    .progress-card {
        background-color: white;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 3px 6px rgba(0,0,0,0.04);
        margin-bottom: 12px;
        text-align: center;
    }
    
    /* Style tables cleanly */
    .stTable table {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. VERBAL REASONING BANK (GROUNDED ENGLISH PASSAGES)
# ==========================================

VERBAL_BANK = [
    {
        "id": "v_newcomb_paradox",
        "type": "verbal",
        "theme": "Philosophy & Logic",
        "difficulty": "Hard",
        "passage": "Newcomb's paradox confronts two rational decision principles that usually align. A predictor almost infalibly puts 1 million euros in an opaque box if it predicts the agent will choose only that box, and 1,000 euros in a transparent box. The expected utility principle advises taking only the opaque box given the high probability of predictor success. The dominance principle, on the other hand, observes that, regardless of the already-determined contents of the opaque box, adding the transparent box never worsens the outcome, and therefore advises taking both. The discrepancy does not reveal that one of the principles is erroneous, but rather that both presuppose incompatible theses regarding whether the decision can be treated as causally independent of an already-determined state of the world.",
        "question": "According to the passage, what does the discrepancy in Newcomb's paradox reveal?",
        "options": [
            "A) The dominance principle demonstrates that choosing only the opaque box is always irrational.",
            "B) The divergence does not prove that one of the principles is incorrect, but rather that both assume incompatible theses regarding whether the decision can be treated as causally independent of an already determined state of the world.",
            "C) The expected utility principle has been proven mathematically superior in emerging markets.",
            "D) Both decision mechanisms are fundamentally flawed because they ignore transaction costs."
        ],
        "correct": "B",
        "explanation": "The text specifies that the divergence does not prove that one of the principles is incorrect, but rather that both 'assume incompatible theses regarding whether the decision can be treated as causally independent of an already determined state of the world' [Passage 62]."
    },
    {
        "id": "v_arrow_theorem",
        "type": "verbal",
        "theme": "Economy & Society",
        "difficulty": "Medium",
        "passage": "Arrow’s impossibility theorem states that no method of aggregating individual preferences into a social preference can simultaneously satisfy a set of seemingly reasonable conditions—unrestricted domain, absence of a dictator, Pareto efficiency, and independence from irrelevant alternatives—when there are at least three options. The result does not assert that every voting rule is useless, but rather that any rule adopted will have to sacrifice at least one of those conditions. Admitting intensities of preferences allows one to circumvent the impossibility, at the cost of requiring interpersonal comparisons that Arrow had ruled out.",
        "question": "According to Arrow's impossibility theorem, what is the consequence of having at least three options?",
        "options": [
            "A) Admitting preference intensities allows circumventing the impossibility, though it requires interpersonal comparisons that Arrow ruled out.",
            "B) The theorem demonstrates that voting rules are all useless in practice.",
            "C) Independence from irrelevant alternatives is the only condition that no method can satisfy.",
            "D) Arrow’s theorem proves that any voting system with three or more options is necessarily dictatorial."
        ],
        "correct": "A",
        "explanation": "The text indicates that admitting intensities of preferences 'allows one to circumvent the impossibility, at the cost of requiring interpersonal comparisons that Arrow had ruled out' [Passage 122]."
    },
    {
        "id": "v_bell_theorem",
        "type": "verbal",
        "theme": "Science & Technology",
        "difficulty": "Hard",
        "passage": "In quantum mechanics, Bell’s theorem shows that no local hidden-variable theory can reproduce all the statistical predictions of quantum mechanics. Bell’s inequalities set a bound that any local-realist model must respect; experiments repeatedly confirm their violation. What is excluded is their conjunction, not each one separately, and the choice of which to abandon goes beyond the experiment.",
        "question": "What does the experimental violation of Bell's inequalities rule out?",
        "options": [
            "A) It proves that any theory of hidden variables, whether local or not, is refuted.",
            "B) Experiments on Bell’s inequalities conclusively demonstrate that realism is false.",
            "C) What Bell’s theorem rules out is the combination of locality and realism, not each one separately, and the choice of which to abandon goes beyond the experiment.",
            "D) It proves that locality is true and realism must be abandoned."
        ],
        "correct": "C",
        "explanation": "The text specifies that 'what is excluded is their conjunction' (locality and realism) rather than each one separately, and the choice of which to abandon goes beyond the experiment itself [Passage 123]."
    },
    {
        "id": "v_wittgenstein_private",
        "type": "verbal",
        "theme": "Philosophy & Logic",
        "difficulty": "Hard",
        "passage": "Wittgenstein’s argument regarding private language holds that there cannot be a language whose terms refer to sensations accessible only to a single subject and that are, by principle, incomprehensible to others. The reason is not empirical, but conceptual: the correct use of a term requires a criterion that distinguishes between actually following a rule and merely believing that one is following it. In a hypothetical private language, there would be no difference between correctly applying the term and appearing to apply it correctly, since there would be no standard independent of the speaker’s present impression. Without that distinction, the very notion of correctness—and, with it, that of meaning—dissolves.",
        "question": "Why is a private language conceptually impossible according to Wittgenstein?",
        "options": [
            "A) The correctness of a term’s use depends solely on the speaker’s current impression.",
            "B) The argument holds that it is empirically difficult, though possible, to construct a private language.",
            "C) Wittgenstein asserts that private sensations do not exist.",
            "D) A private language is impossible because in it the distinction between correctly applying a term and believing that one is applying it correctly would vanish."
        ],
        "correct": "D",
        "explanation": "The text identifies the impossibility of a private language in that there would be no standard independent of the speaker's present impression, collapsing the distinction between actually applying something correctly and merely believing one is doing so [Passage 124]."
    },
    {
        "id": "v_gettier_problem",
        "type": "verbal",
        "theme": "Philosophy & Logic",
        "difficulty": "Medium",
        "passage": "In epistemology, Gettier’s problem shows that the classical definition of knowledge as a true and justified belief is insufficient: one can imagine cases in which a subject holds a true and justified belief that nevertheless does not constitute knowledge, because its truth is due to a stroke of luck unrelated to the justification. Internists add a fourth condition that excludes false premises or auxiliary assumptions.",
        "question": "What is the core implication of Gettier's problem in epistemology?",
        "options": [
            "A) The Gettier problem proves that knowledge is an unattainable concept.",
            "B) For a belief to be considered knowledge, it is sufficient for it to be true and for the believer to have a reason for it.",
            "C) Gettier's counterexamples suggest that a belief's truth being coincidental can undermine its status as knowledge.",
            "D) Any belief that happens to be true due to luck cannot be considered a justified belief."
        ],
        "correct": "C",
        "explanation": "Gettier's counterexamples show that having a justified true belief does not guarantee knowledge if the truth of that belief is ultimately a matter of coincidence or luck [Passage 68]."
    },
    {
        "id": "v_duhem_quine",
        "type": "verbal",
        "theme": "Science & Technology",
        "difficulty": "Hard",
        "passage": "According to the underdetermination thesis, scientific hypotheses are tested in bundles rather than in isolation, involving auxiliary assumptions; in the face of a failed prediction, logic does not determine which of the implicated statements must be revised. Quine radicalized this thesis by arguing that, in principle, any statement can be preserved from refutation if sufficient adjustments are made elsewhere in the system. This does not amount to a relativism that denies any rational basis for revision: criteria such as minimal disruption to the system (minimal mutilation) and the preservation of simplicity guide the choice, though they do not dictate it algorithmically.",
        "question": "In the face of a failed prediction, how is the revision of beliefs guided under the Duhem-Quine framework?",
        "options": [
            "A) Quine maintains that logic unambiguously determines which statement to revise in the face of a refutation.",
            "B) Any statement can be saved from refutation with appropriate adjustments, but criteria such as minimal mutilation and simplicity guide—without algorithmically dictating—what to revise.",
            "C) Holism implies that no rational criterion guides the revision of a belief system.",
            "D) According to Duhem-Quine, each scientific hypothesis is tested in a manner completely isolated from the rest."
        ],
        "correct": "B",
        "explanation": "The text explains that any statement can be saved from refutation if sufficient adjustments are made, and that pragmatic criteria like simplicity and 'minimal mutilation' guide our choice without providing an algorithmic formula [Passage 70]."
    },
    {
        "id": "v_austin_speech",
        "type": "verbal",
        "theme": "Philosophy & Logic",
        "difficulty": "Medium",
        "passage": "Austin’s theory of speech acts distinguishes three dimensions of an utterance: the locutionary act (saying something with meaning and reference), the illocutionary act (what is done by saying it: promising, warning, commanding), and the perlocutionary act (the effects produced in the listener: convincing, frightening). Illocutionary force is not reducible to literal meaning or isolated psychological intention: it depends on conventions that confer upon certain utterances, under appropriate circumstances, the status of an act. Hence, an utterance may fail not because it is false, but because it is 'ill-chosen': uttered without the authority or context required by convention.",
        "question": "Why might a speech act fail according to Austin?",
        "options": [
            "A) An utterance may fail because it is 'ill-chosen'—uttered without the authority or context required by convention—and not because it is false.",
            "B) The perlocutionary act consists of what is done by saying something, such as making a promise or giving an order.",
            "C) Austin argues that every failed utterance fails because it is false.",
            "D) The illocutionary force is reduced entirely to the literal meaning of the utterance."
        ],
        "correct": "A",
        "explanation": "The text states that an utterance may fail not because it is false, but because it is 'ill-chosen': uttered without the authority or context required by convention [Passage 74, 125]."
    },
    {
        "id": "v_vienna_convention",
        "type": "verbal",
        "theme": "Economy & Society",
        "difficulty": "Medium",
        "passage": "In the interpretation of international treaties, the Vienna Convention establishes a general rule that combines the ordinary meaning of the terms, their context, and the object and purpose of the treaty, and reserves for the preparatory works a supplementary role: they may be consulted only to confirm the resulting meaning or when the general interpretation leaves the meaning ambiguous or leads to a manifestly absurd result. This hierarchy subordinates the historical intent of the parties—reconstructed from the negotiations—to the text actually agreed upon, except in the limited cases in which that intent may legitimately be reintroduced.",
        "question": "What role do the preparatory works play in treaty interpretation under the Vienna Convention?",
        "options": [
            "A) The preparatory works play a supplementary role and are invoked only to confirm the meaning or when the meaning is ambiguous or absurd.",
            "B) The preparatory works take precedence over the ordinary meaning of the treaty’s terms.",
            "C) The historical intent of the parties takes precedence in all cases over the agreed-upon text.",
            "D) Interpretation must focus exclusively on the object and purpose of the treaty, setting aside the text."
        ],
        "correct": "A",
        "explanation": "The Vienna Convention designates preparatory works a supplementary role, to be consulted only to confirm meaning or when the text is ambiguous or leads to an absurd result [Passage 76, 126]."
    },
    {
        "id": "v_kuhn_incommensurability",
        "type": "verbal",
        "theme": "Science & Technology",
        "difficulty": "Hard",
        "passage": "Kuhn’s concept of incommensurability does not assert that rival paradigms are completely unintelligible to one another. Rather, it consists in the lack of a neutral language and shared criteria for a point-by-point comparison, while values such as accuracy, consistency, simplicity, scope, and fruitfulness guide—without dictating—the choice. The transition to a crisis requires an accumulation of anomalies and, above all, an alternative paradigm capable of accommodating them; thus, the mere existence of counterexamples rarely suffices to overturn a theory.",
        "question": "What is the nature of incommensurability between paradigms according to Kuhn?",
        "options": [
            "A) Incommensurability implies that rival paradigms are completely unintelligible to one another.",
            "B) Central terms retain the same reference when switching paradigms.",
            "C) Incommensurability consists in the lack of a neutral language and shared criteria for a point-by-point comparison, while values such as accuracy or fruitfulness guide—without dictating—the choice.",
            "D) Kuhn argues that the choice between paradigms is entirely irrational and random."
        ],
        "correct": "C",
        "explanation": "The text states that incommensurability represents the absence of a neutral language and shared criteria for comparison, while values like accuracy and fruitfulness guide the choice [Passage 78, 126]."
    },
    {
        "id": "v_lucas_critique",
        "type": "verbal",
        "theme": "Economy & Society",
        "difficulty": "Hard",
        "passage": "The Lucas critique, formulated in 1976, revolutionized macroeconomic policy evaluation by arguing that it is naive to predict the effects of a policy change based entirely on historical statistical relationships. Because economic agents adapt their expectations and behaviors when policy rules change, the parameters of estimated equations do not remain invariant across regimes. The critique requires modeling deep and stable parameters, such as preferences and technology, from which the response to each regime is derived endogenously.",
        "question": "What is the core argument of the Lucas critique regarding policy modeling?",
        "options": [
            "A) The critique requires modeling deep and stable parameters, such as preferences and technology, from which the response to each regime is derived endogenously.",
            "B) According to the critique, economic agents do not modify their behavior in anticipation of policy changes.",
            "C) Historically estimated parameters are invariant to regime changes, according to Lucas.",
            "D) Lucas’s critique concludes that it is impossible to evaluate the effect of any economic policy."
        ],
        "correct": "A",
        "explanation": "The critique states that because parameters of historical relationships vary under different policy rules, we must model stable, deep parameters like preferences and technology endogenously [Passage 80, 127]."
    },
    {
        "id": "v_searle_chinese",
        "type": "verbal",
        "theme": "Philosophy & Logic",
        "difficulty": "Hard",
        "passage": "Searle’s Chinese Room argument aims to show that the execution of a program, however sophisticated it may be, is not sufficient to constitute semantic understanding. An operator who manipulates Chinese symbols according to formal rules, without understanding the language, produces responses indistinguishable from those of a native speaker; according to Searle, syntax alone does not generate semantics. An influential rebuttal—the 'systems reply'—concedes that the operator does not understand, but maintains that understanding must be attributed to the complete system (operator, rules, data), not to one of its components. Searle objects that internalizing the entire system within the operator would not add any understanding.",
        "question": "What is the primary conclusion of Searle's Chinese Room argument and the response of the systems reply?",
        "options": [
            "A) Searle argues that the execution of a program is sufficient to constitute semantic understanding.",
            "B) The argument concludes that syntax alone does not generate semantics, and the system’s rebuttal shifts the dispute to the level of description to which understanding should be attributed.",
            "C) Searle accepts that internalizing the system within the operator produces genuine understanding.",
            "D) The system’s response affirms that the operator, in isolation, understands Chinese."
        ],
        "correct": "B",
        "explanation": "Searle argues syntax cannot produce semantics. The systems reply counters that the complete system has understanding, which Searle disputes, shifting the debate to the correct level of description [Passage 81, 128]."
    },
    {
        "id": "v_banach_tarski",
        "type": "verbal",
        "theme": "Science & Technology",
        "difficulty": "Hard",
        "passage": "In measure theory, the Banach–Tarski paradox states that a solid sphere in three-dimensional space can be decomposed into a finite number of pieces that, when reassembled by rigid motions, form two spheres identical to the original. The result does not contradict the conservation of physical volume: the pieces involved are non-measurable sets, lacking a well-defined volume, whose existence depends on the axiom of choice. The paradox, therefore, illuminates not so much a property of space as a tension between geometric intuition and the set-theoretic commitments we accept when admitting that axiom for non-constructive collections.",
        "question": "What does the Banach-Tarski paradox primarily illustrate?",
        "options": [
            "A) The result is independent of the axiom of choice.",
            "B) The Banach–Tarski paradox demonstrates that physical volume is not conserved when manipulating material objects.",
            "C) The paradox reveals a tension between geometric intuition and the set-theoretic commitments we make when accepting the axiom of choice for non-constructive sets.",
            "D) It shows that spatial coordinates are mathematically inconsistent under rigid motion."
        ],
        "correct": "C",
        "explanation": "The paradox does not violate physics because it operates on non-measurable mathematical sets; it highlights a tension between geometric intuition and accepting the axiom of choice [Passage 83, 129]."
    },
    {
        "id": "v_frege_sense",
        "type": "verbal",
        "theme": "Philosophy & Logic",
        "difficulty": "Medium",
        "passage": "The Fregean distinction between sense and reference resolves a difficulty concerning informative identity statements. 'The morning star is the evening star' is not trivial even though both terms refer to the same planet, Venus. Frege explains that every expression possesses, in addition to its reference, a sense: a mode of presenting the object. The equality of reference coupled with diversity of sense ensures that the statement conveys knowledge. The theory also sheds light on opaque contexts: in indirect speech, Frege argues, expressions do not refer to their usual reference but to their sense, which explains why the substitution of co-referents can alter the truth value.",
        "question": "How does Frege explain that 'The morning star is the evening star' is informative?",
        "options": [
            "A) The identity statement is informative because both terms have distinct references.",
            "B) The diversity of sense with identity of reference explains the informative nature of the statement, and in opaque contexts, expressions refer to their sense, which alters the substitution of coreferents.",
            "C) For Frege, sense and reference are one and the same thing.",
            "D) It is informative because it refers to two completely different planets."
        ],
        "correct": "B",
        "explanation": "Because morning star and evening star share a reference (Venus) but present it via different senses, the identity statement is informative. In opaque contexts, terms refer to their senses, affecting substitution [Passage 85, 130]."
    },
    {
        "id": "v_efficiency_wage",
        "type": "verbal",
        "theme": "Economy & Society",
        "difficulty": "Medium",
        "passage": "The efficiency wage hypothesis explains why, in certain labor markets, the equilibrium wage may be higher than the level that would equalize supply and demand, leading to persistent involuntary unemployment. Paying above the necessary minimum reduces turnover, attracts higher-productivity workers, and discourages negligence, since the cost of losing a well-paid job deters poor performance. The consequence is that unemployment is not interpreted here as mere temporary friction or as the result of externally imposed rigidities, but rather as a phenomenon that can arise from the optimization behavior of the firms themselves.",
        "question": "What does the efficiency wage hypothesis suggest about involuntary unemployment?",
        "options": [
            "A) Paying wages above the necessary minimum may be optimal for firms and generate involuntary unemployment that arises from their own optimization behavior.",
            "B) The unemployment described results exclusively from external rigidities imposed on the market.",
            "C) Paying higher wages does not affect productivity or worker turnover.",
            "D) The efficiency wage is always below the wage that equilibrates supply and demand."
        ],
        "correct": "A",
        "explanation": "Firms optimize by paying higher wages to boost productivity and retention, which sustains an above-market clearing rate and persistent unemployment as an outcome of firm optimization [Passage 88, 130]."
    },
    {
        "id": "v_liar_paradox",
        "type": "verbal",
        "theme": "Philosophy & Logic",
        "difficulty": "Hard",
        "passage": "The liar’s paradox arises from a self-referential sentence that asserts its own falsehood, creating a contradiction: if it is true, then it is false; if it is false, then it is true. Formal responses fall into different strategies. The hierarchical approaches, inspired by Tarski, prohibit a language from containing its own truth predicate, distributing 'true' across levels so that the paradoxical sentence is rendered ill-formed. Revisionist strategies admit additional truth values or gaps. Each approach comes at a cost: the hierarchical approach sacrifices the expressiveness of a semantically closed language; revisionist strategies sacrifice classical logical principles such as the excluded middle. There is no solution without a theoretical cost.",
        "question": "Which of the following describes the trade-offs of the formal solutions to the liar's paradox?",
        "options": [
            "A) Revisionist strategies preserve all the principles of classical logic intact.",
            "B) The liar’s paradox lacks any formal solution.",
            "C) Both the hierarchical and revisionist approaches resolve the paradox at the cost of a theoretical price: expressiveness or classical logical principles, respectively.",
            "D) The hierarchical strategy resolves the paradox without sacrificing semantic closedness."
        ],
        "correct": "C",
        "explanation": "The text concludes that both strategies have a theoretical cost: hierarchical approaches sacrifice the expressiveness of a semantically closed language, while revisionist approaches sacrifice classical principles [Passage 91, 132]."
    },
    {
        "id": "v_path_dependence",
        "type": "verbal",
        "theme": "Economy & Society",
        "difficulty": "Medium",
        "passage": "Path dependence describes a process in which historical accidents and network effects lock a system into a suboptimal configuration that is difficult to reverse. The classic example is the persistence of technological standards that prevailed due to historical accidents and network effects, not because of intrinsic superiority. The thesis does not claim that every persistent institution is inefficient—that would be a fallacy—but rather that the efficiency of the existing system cannot be inferred from its mere survival, since competitive selection does not guarantee, in the presence of increasing returns, the elimination of inferior solutions.",
        "question": "What does the path dependence thesis assert about existing systems?",
        "options": [
            "A) Dominant technological standards always prevail because of their intrinsic superiority.",
            "B) The efficiency of existing systems cannot be inferred from their mere survival, because, with increasing returns, competitive selection does not guarantee the elimination of inferior solutions.",
            "C) The outcome of these processes is determined solely by initial conditions and preferences.",
            "D) Path dependence implies that any institution that persists is necessarily inefficient."
        ],
        "correct": "B",
        "explanation": "Survival does not prove efficiency, as increasing returns and historical locking can preserve inferior solutions over superior ones [Passage 96, 137]."
    },
    {
        "id": "v_expected_utility",
        "type": "verbal",
        "theme": "Economy & Society",
        "difficulty": "Medium",
        "passage": "The von Neumann–Morgenstern expected utility theory derives the existence of a utility function that represents the preferences of a rational agent under risk, based on axioms such as completeness, transitivity, continuity, and independence. The Allais and Ellsberg paradoxes present systematic choice patterns that violate, respectively, the independence axiom and indifference to ambiguity. What is relevant is not that some individuals make mistakes, but that the violations are robust, persistent, and widespread, suggesting that the model does not adequately describe actual behavior, even though it may retain its value as a standard of rationality. Distinguishing between the descriptive and the normative is crucial here.",
        "question": "What do the Allais and Ellsberg paradoxes reveal about expected utility theory?",
        "options": [
            "A) Expected utility theory is not based on any axiom regarding preferences.",
            "B) The normative value of the model is refuted by the Allais and Ellsberg paradoxes.",
            "C) The Allais and Ellsberg paradoxes show that some individuals make isolated miscalculations.",
            "D) Violations of the model are robust and widespread, which calls into question its descriptive adequacy even though it may retain its normative value; it is important to distinguish between these two levels."
        ],
        "correct": "D",
        "explanation": "The paradoxes show systematic, robust violations, indicating the theory is descriptively inadequate for real behavior, though it remains a valid normative benchmark of rationality [Passage 99, 137]."
    },
    {
        "id": "v_sapir_whorf",
        "type": "verbal",
        "theme": "Science & Technology",
        "difficulty": "Sencillo",
        "passage": "The Sapir-Whorf hypothesis, also referred to as the principle of linguistic relativity, posits a correlation between linguistic structure and cognitive patterning. In its strong or deterministic version, it holds that the language spoken determines the limits of thought, such that distinctions that cannot be expressed in a language would be inconceivable to its speakers. This version lacks empirical support today and is largely abandoned. The weaker, more tenable interpretation asserts only that attention to language is an indispensable tool for detecting pseudo-problems, or that linguistic structures can modulate, without imposing insurmountable limits, the salience of perceptual categories within a given cognitive framework.",
        "question": "What is the current scientific standing of the strong versus weak versions of the Sapir-Whorf hypothesis?",
        "options": [
            "A) The strong version of the hypothesis now has solid empirical support.",
            "B) The weak version maintains that language imposes an insurmountable limit on what its speakers can think.",
            "C) Speakers cannot conceive of distinctions that their language does not encode lexically.",
            "D) The strong deterministic version lacks empirical support today, while the weaker version holds that linguistic variation modulates the salience of perceptual categories without imposing absolute limits."
        ],
        "correct": "D",
        "explanation": "The strong version has been rejected due to lack of evidence, while the weak version is accepted as showing language can influence cognitive prominence and attention without blocking thoughts [Passage 103]."
    },
    {
        "id": "v_peter_principle",
        "type": "verbal",
        "theme": "Science & Technology",
        "difficulty": "Sencillo",
        "passage": "The Peter Principle states that a person who is competent in their job will be promoted to a higher position that requires different skills. If the person lacks the skills required for the new role, they will be incompetent at their new level and will not receive further promotions. However, if they are competent in their new role, they will be promoted again and will continue to rise until they reach a level at which they are incompetent. Being incompetent, they will not meet the requirements for further promotion and will remain at that final level for the rest of their career. This outcome is inevitable, given sufficient time and assuming that there are enough positions in the company hierarchy to promote competent employees. The Peter Principle is expressed as follows: 'In a hierarchical structure, every employee tends to rise to their level of incompetence.'",
        "question": "What does the Peter Principle imply about hierarchical positions?",
        "options": [
            "A) According to this principle, the highest positions in the hierarchy will ultimately be occupied by someone who is incompetent.",
            "B) According to the Peter Principle, incompetence is seen as a positive trait that is rewarded.",
            "C) The Peter Principle states that employees voluntarily stop being promoted when they feel incompetent.",
            "D) The Peter Principle can be avoided by hiring external resources."
        ],
        "correct": "A",
        "explanation": "Because competent people are promoted until they reach a level at which they are incompetent, with the exception of the lowest entry-level positions, all posts will eventually be occupied by incompetent people [Passage 161]."
    },
    {
        "id": "v_bionics",
        "type": "verbal",
        "theme": "Science & Technology",
        "difficulty": "Sencillo",
        "passage": "Although stripped of flesh and bone, or severely damaged in these, the nerves and the parts of the brain that once controlled them remain alive. In many patients they are there, waiting to communicate, like telephone wires hanging loose, severed from their devices. With microscopic electrodes and almost magical surgery, doctors have begun connecting these parts of patients to devices such as cameras, microphones or motors. The result: the blind can see, the deaf can hear, and those who had lost an arm can fold their shirts. These are the people of the future, a group of individuals who will see the parts of their bodies they had lost replaced by devices implanted into their nervous systems that respond to commands from their brains. The machines used are commonly known as neural prostheses or, by the term preferred by scientists, coined from science fiction, bionics.",
        "question": "Which of the following statements is correct regarding bionics according to the text?",
        "options": [
            "A) Bionics is being developed in order to help restore natural capacities, and one day it will serve to improve and enhance them.",
            "B) Neural prostheses use electrodes, motors, microphones and cameras to restore sight, hearing and limbs.",
            "C) The term bionic comes from science fiction and is widely accepted by patients who use neural prostheses.",
            "D) The nerves that were once responsible for controlling a severed finger will gradually deteriorate until they are completely exhausted."
        ],
        "correct": "B",
        "explanation": "The text explicitly mentions microscopic electrodes, cameras, microphones, and motors as devices used to connect with the nervous system to restore biological functions [Passage 162]."
    }
]


# ==========================================
# 2. NUMERICAL REASONING PROCEDURAL GENERATORS (ENGLISH)
# ==========================================

def generate_numerical_patents():
    pop_germany = random.randint(81000, 83000)
    pop_switzerland = random.randint(7200, 7600)
    
    rate_germany_04 = round(random.uniform(265.0, 278.0), 1)
    rate_germany_05 = round(random.uniform(279.0, 288.0), 1)
    
    rate_switzerland_04 = round(random.uniform(395.0, 410.0), 1)
    rate_switzerland_05 = round(random.uniform(411.0, 425.0), 1)
    
    diff_rate = round(rate_switzerland_05 - rate_germany_05, 1)
    correct_val = round((pop_germany / 1000.0) * diff_rate)
    
    table = f"""
| Country | Population 2005 (thousands) | Patents per million (2004) | Patents per million (2005) |
| :--- | :---: | :---: | :---: |
| **Germany** | {pop_germany:,} | {rate_germany_04} | {rate_germany_05} |
| **Switzerland** | {pop_switzerland:,} | {rate_switzerland_04} | {rate_switzerland_05} |
"""
    question = "Based on the table, how many additional patents would **Germany** have needed to file in 2005 to match **Switzerland's** per capita applications in 2005?"
    
    correct_opt = f"{correct_val:,} patents"
    options_vals = [
        correct_val,
        round(correct_val * 1.1),
        round(correct_val * 0.9),
        round((pop_germany) * diff_rate),
        round(pop_switzerland * diff_rate)
    ]
    options_vals = list(set(options_vals))
    while len(options_vals) < 5:
        options_vals.append(correct_val + random.randint(-500, 500))
    options_vals.sort()
    
    letters = ["A", "B", "C", "D", "E"]
    options = []
    correct_letter = "A"
    for i, val in enumerate(options_vals):
        letter = letters[i]
        opt_str = f"{letter}) {val:,} patents"
        options.append(opt_str)
        if val == correct_val:
            correct_letter = letter
            
    explanation = f"""
**Step-by-Step Solution:**
1. **Find the difference in per capita rates in 2005:**
   $$\\text{{Difference}} = {rate_switzerland_05} - {rate_germany_05} = {diff_rate} \\text{{ patents per million inhabitants}}$$
2. **Apply this difference to Germany's population:**
   Germany's population is ${pop_germany:,}$ thousands (or ${pop_germany/1000.0:.3f}$ million).
   $$\\text{{Additional Patents}} = \\frac{{{pop_germany:,}}}{{1,000}} \\times {diff_rate} = {pop_germany/1000.0:.3f} \\times {diff_rate} \\approx {correct_val:,} \\text{{ patents}}$$
   
The correct option is **{correct_letter}**.
"""
    return {
        "id": f"num_pat_{random.randint(1000, 9999)}",
        "type": "numerical",
        "difficulty": "Medium",
        "table": table,
        "question": question,
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }

def generate_numerical_palace():
    year1_v = random.randint(1100, 1300)
    year3_v = random.randint(1400, 1600)
    
    spend1 = round(random.uniform(8.5, 9.5), 2)
    spend3 = round(random.uniform(11.0, 12.5), 2)
    
    bill1 = round(year1_v * spend1, 1)
    bill3 = round(year3_v * spend3, 1)
    
    pct_increase = round(((spend3 - spend1) / spend1) * 100, 1)
    
    table = f"""
| Year | Visitors (thousands) | Total Ticket Revenue (thousand EUR) |
| :---: | :---: | :---: |
| **Year 1** | {year1_v:,} | {bill1:,} |
| **Year 2** | {round((year1_v+year3_v)/2):,} | {round((bill1+bill3)/2):,} |
| **Year 3** | {year3_v:,} | {bill3:,} |
"""
    question = "Based on the table, what is the percentage increase in the **average spending per visitor** from Year 1 to Year 3?"
    
    correct_opt_val = pct_increase
    options_vals = [
        correct_opt_val,
        round(correct_opt_val * 0.8, 1),
        round(correct_opt_val * 1.2, 1),
        round(((bill3 - bill1) / bill1) * 100, 1),
        round(((year3_v - year1_v) / year1_v) * 100, 1)
    ]
    options_vals = list(set(options_vals))
    while len(options_vals) < 5:
        options_vals.append(round(correct_opt_val + random.uniform(-5.0, 5.0), 1))
    options_vals.sort()
    
    letters = ["A", "B", "C", "D", "E"]
    options = []
    correct_letter = "A"
    for i, val in enumerate(options_vals):
        letter = letters[i]
        opt_str = f"{letter}) {val:.1f}%"
        options.append(opt_str)
        if val == correct_opt_val:
            correct_letter = letter
            
    explanation = f"""
**Step-by-Step Solution:**
1. **Calculate average spend per visitor in Year 1:**
   $$\\text{{Average Spend Year 1}} = \\frac{{\\text{{Revenue}}}}{{\\text{{Visitors}}}} = \\frac{{{bill1:,} \\text{{ thousand EUR}}}}{{{year1_v:,} \\text{{ thousand visitors}}}} = {spend1:.2f} \\text{{ EUR per visitor}}$$
2. **Calculate average spend per visitor in Year 3:**
   $$\\text{{Average Spend Year 3}} = \\frac{{\\text{{Revenue}}}}{{\\text{{Visitors}}}} = \\frac{{{bill3:,} \\text{{ thousand EUR}}}}{{{year3_v:,} \\text{{ thousand visitors}}}} = {spend3:.2f} \\text{{ EUR per visitor}}$$
3. **Calculate percentage increase:**
   $$\\text{{Percentage Increase}} = \\frac{{{spend3:.2f} - {spend1:.2f}}}{{{spend1:.2f}}} \\times 100 = \\frac{{{spend3 - spend1:.2f}}}{{{spend1:.2f}}} \\times 100 = {pct_increase:.1f}\\%$$
   
The correct option is **{correct_letter}**.
"""
    return {
        "id": f"num_pal_{random.randint(1000, 9999)}",
        "type": "numerical",
        "difficulty": "Hard",
        "table": table,
        "question": question,
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }

def generate_numerical_energy():
    pop_swe = round(random.uniform(9.8, 10.4), 1)
    gwh_swe = random.randint(125000, 135000)
    co2_swe = random.randint(35000, 42000)
    
    pop_pol = round(random.uniform(37.5, 38.5), 1)
    gwh_pol = random.randint(145000, 155000)
    co2_pol = random.randint(290000, 310000)
    
    rate_swe = round(co2_swe / gwh_swe, 3)
    rate_pol = round(co2_pol / gwh_pol, 3)
    
    ratio = round(rate_pol / rate_swe, 2)
    
    table = f"""
| Country | Population (millions) | Energy Consumed (GWh) | CO2 Emissions (kilotonnes) |
| :--- | :---: | :---: | :---: |
| **Sweden** | {pop_swe} | {gwh_swe:,} | {co2_swe:,} |
| **Poland** | {pop_pol} | {gwh_pol:,} | {co2_pol:,} |
"""
    question = "Based on the table, the **CO2 emissions per GWh of energy consumed** in **Poland** is how many times that of **Sweden**?"
    
    correct_opt_val = ratio
    options_vals = [
        correct_opt_val,
        round(correct_opt_val * 0.7, 2),
        round(correct_opt_val * 1.3, 2),
        round((co2_pol / co2_swe), 2),
        round((gwh_pol / gwh_swe), 2)
    ]
    options_vals = list(set(options_vals))
    while len(options_vals) < 5:
        options_vals.append(round(correct_opt_val + random.uniform(-2.0, 2.0), 2))
    options_vals.sort()
    
    letters = ["A", "B", "C", "D", "E"]
    options = []
    correct_letter = "A"
    for i, val in enumerate(options_vals):
        letter = letters[i]
        opt_str = f"{letter}) {val:.2f} times"
        options.append(opt_str)
        if val == correct_opt_val:
            correct_letter = letter
            
    explanation = f"""
**Step-by-Step Solution:**
1. **Calculate Sweden's emission rate per GWh:**
   $$\\text{{Rate Sweden}} = \\frac{{{co2_swe:,} \\text{{ kilotonnes}}}}{{{gwh_swe:,} \\text{{ GWh}}}} \\approx {rate_swe:.3f} \\text{{ kilotonnes per GWh}}$$
2. **Calculate Poland's emission rate per GWh:**
   $$\\text{{Rate Poland}} = \\frac{{{co2_pol:,} \\text{{ kilotonnes}}}}{{{gwh_pol:,} \\text{{ GWh}}}} \\approx {rate_pol:.3f} \\text{{ kilotonnes per GWh}}$$
3. **Calculate the ratio:**
   $$\\text{{Ratio}} = \\frac{{{rate_pol:.3f}}}{{{rate_swe:.3f}}} \\approx {ratio:.2f} \\text{{ times}}$$
   
The correct option is **{correct_letter}**.
"""
    return {
        "id": f"num_nrg_{random.randint(1000, 9999)}",
        "type": "numerical",
        "difficulty": "Easy",
        "table": table,
        "question": question,
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }


# ==========================================
# 3. ABSTRACT REASONING PROCEDURAL GENERATORS (ENGLISH SVG)
# ==========================================

def generate_abstract_rotation():
    def get_box_svg(arrow_ang, dot_ang, size=80):
        return f"""
        <svg width="{size}" height="{size}" style="border: 2px solid #D1D5DB; border-radius: 8px; margin: 4px; background: white;">
            <!-- Circular track -->
            <circle cx="40" cy="40" r="30" stroke="#F3F4F6" stroke-width="2" fill="none" />
            <!-- Arrow group -->
            <g transform="rotate({arrow_ang}, 40, 40)">
                <line x1="40" y1="65" x2="40" y2="18" stroke="#3B82F6" stroke-width="4" stroke-linecap="round" />
                <polygon points="40,12 34,22 46,22" fill="#3B82F6" />
            </g>
            <!-- Dot group -->
            <g transform="rotate({dot_ang}, 40, 40)">
                <circle cx="40" cy="10" r="6" fill="#EF4444" />
            </g>
        </svg>
        """
    
    seq_svg = f"""
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; padding: 10px; background: #F9FAFB; border-radius: 12px; margin-bottom: 15px;">
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 1</p>{get_box_svg(0, 0)}</div>
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 2</p>{get_box_svg(90, 90)}</div>
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 3</p>{get_box_svg(180, 180)}</div>
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 4</p>{get_box_svg(270, 270)}</div>
    </div>
    """
    
    options_config = [
        ("A", 180, 0),
        ("B", 0, 0), # Correct
        ("C", 0, 180),
        ("D", 270, 90),
        ("E", 90, 270)
    ]
    random.shuffle(options_config)
    
    options_list = []
    correct_letter = "B"
    letters = ["A", "B", "C", "D", "E"]
    
    for i, (orig_id, arr, dot) in enumerate(options_config):
        letter = letters[i]
        opt_svg = get_box_svg(arr, dot, size=60)
        options_list.append(f"{letter}) {opt_svg}")
        if orig_id == "B":
            correct_letter = letter
            
    explanation = f"""
**Step-by-Step Solution:**
1. **Analyze the movement of the Blue Arrow:**
   - Step 1: Up ($0^\\circ$)
   - Step 2: Right ($90^\\circ$) - rotates $+90^\\circ$ (Clockwise).
   - Step 3: Down ($180^\\circ$) - rotates $+90^\\circ$.
   - Step 4: Left ($270^\\circ$) - rotates $+90^\\circ$.
   - **Step 5 should be:** Up ($0^\\circ$) - rotates $+90^\\circ$.
2. **Analyze the movement of the Red Dot:**
   - Step 1: Top ($0^\\circ$)
   - Step 2: Right ($90^\\circ$) - rotates $+90^\\circ$ (Clockwise).
   - Step 3: Bottom ($180^\\circ$) - rotates $+90^\\circ$.
   - Step 4: Left ($270^\\circ$) - rotates $+90^\\circ$.
   - **Step 5 should be:** Top ($0^\\circ$) - rotates $+90^\\circ$.
   
Therefore, the correct 5th figure in the sequence must have the Blue Arrow pointing **Up** and the Red Dot at the **Top**.
This corresponds to option **{correct_letter}**.
"""
    return {
        "id": f"abs_rot_{random.randint(1000, 9999)}",
        "type": "abstract",
        "difficulty": "Medium",
        "svg": seq_svg,
        "question": "What is the next figure in the logical sequence?",
        "options": options_list,
        "correct": correct_letter,
        "explanation": explanation
    }

def generate_abstract_shapes():
    def get_poly_svg(sides, num_lines, size=80):
        cx, cy, r = 40, 40, 25
        pts = []
        for s in range(sides):
            angle = s * (2 * math.pi / sides) - math.pi / 2
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            pts.append(f"{x},{y}")
        pts_str = " ".join(pts)
        
        lines_svg = ""
        for i in range(num_lines):
            x_line = cx - r + (2 * r / (num_lines + 1)) * (i + 1)
            y_diff = math.sqrt(max(0, r**2 - (x_line - cx)**2))
            lines_svg += f'<line x1="{x_line}" y1="{cy - y_diff}" x2="{x_line}" y2="{cy + y_diff}" stroke="#10B981" stroke-width="2" />'
            
        return f"""
        <svg width="{size}" height="{size}" style="border: 2px solid #D1D5DB; border-radius: 8px; margin: 4px; background: white;">
            <polygon points="{pts_str}" fill="none" stroke="#4F46E5" stroke-width="3" />
            {lines_svg}
        </svg>
        """
        
    seq_svg = f"""
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; padding: 10px; background: #F9FAFB; border-radius: 12px; margin-bottom: 15px;">
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 1</p>{get_poly_svg(3, 1)}</div>
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 2</p>{get_poly_svg(4, 2)}</div>
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 3</p>{get_poly_svg(5, 3)}</div>
        <div style="text-align: center;"><p style="margin: 0; font-size: 11px; color: #6B7280;">Step 4</p>{get_poly_svg(6, 4)}</div>
    </div>
    """
    
    options_config = [
        ("A", 7, 3),
        ("B", 6, 5),
        ("C", 7, 5), # Correct
        ("D", 8, 5),
        ("E", 7, 6)
    ]
    random.shuffle(options_config)
    
    options_list = []
    correct_letter = "C"
    letters = ["A", "B", "C", "D", "E"]
    
    for i, (orig_id, sides, lines) in enumerate(options_config):
        letter = letters[i]
        opt_svg = get_poly_svg(sides, lines, size=60)
        options_list.append(f"{letter}) {opt_svg}")
        if orig_id == "C":
            correct_letter = letter
            
    explanation = f"""
**Step-by-Step Solution:**
1. **Analyze the Shape's Geometry:**
   - Step 1: Triangle (3 sides)
   - Step 2: Square (4 sides) - increase of $+1$ side.
   - Step 3: Pentagon (5 sides) - increase of $+1$ side.
   - Step 4: Hexagon (6 sides) - increase of $+1$ side.
   - **Step 5 should be:** Heptagon (7 sides).
2. **Analyze the Green Internal Lines:**
   - Step 1: 1 vertical line
   - Step 2: 2 vertical lines - increase of $+1$ line.
   - Step 3: 3 vertical lines - increase of $+1$ line.
   - Step 4: 4 vertical lines - increase of $+1$ line.
   - **Step 5 should be:** 5 vertical lines.
   
Therefore, the correct 5th figure in the sequence must be a Heptagon (7-sided polygon) with exactly 5 internal vertical lines.
This corresponds to option **{correct_letter}**.
"""
    return {
        "id": f"abs_shp_{random.randint(1000, 9999)}",
        "type": "abstract",
        "difficulty": "Hard",
        "svg": seq_svg,
        "question": "What is the next figure in the logical sequence?",
        "options": options_list,
        "correct": correct_letter,
        "explanation": explanation
    }


# ==========================================
# 4. STATE AND SESSION MANAGEMENT
# ==========================================

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "verbal": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
        "numerical": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
        "abstract": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
        "failed_questions": []
    }

def save_progress(profile):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4, ensure_ascii=False)

if "profile" not in st.session_state:
    st.session_state.profile = load_progress()

if "current_test" not in st.session_state:
    st.session_state.current_test = None
    st.session_state.test_questions = []
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.review_mode = False
    st.session_state.selected_option = None
    st.session_state.show_explanation = False

# Configuration defaults
if "cfg_difficulty_mode" not in st.session_state:
    st.session_state.cfg_difficulty_mode = "Adaptive"
if "cfg_manual_diff" not in st.session_state:
    st.session_state.cfg_manual_diff = "Mixed"
if "cfg_length" not in st.session_state:
    st.session_state.cfg_length = "Standard"
if "cfg_verbal_filter" not in st.session_state:
    st.session_state.cfg_verbal_filter = "All"


# ==========================================
# 5. TEST GENERATOR LOGIC
# ==========================================

def start_new_test(category):
    st.session_state.current_test = category
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.show_explanation = False
    st.session_state.selected_option = None
    
    # Calculate lengths
    if st.session_state.cfg_length == "Quick":
        test_length = 10 if category == "verbal" else 5
    elif st.session_state.cfg_length == "Extended":
        test_length = 30 if category == "verbal" else 15
    else: # Standard
        test_length = 20 if category == "verbal" else 10
        
    profile = st.session_state.profile
    
    # Check difficulty
    if st.session_state.cfg_difficulty_mode == "Adaptive":
        user_diff = profile[category]["difficulty"]
        if user_diff == "Sencillo":
            user_diff = "Sencillo" # align terminology or convert
    else:
        user_diff = st.session_state.cfg_manual_diff
        
    # Spaced repetition: load failed pool
    failed_pool = [q for q in profile["failed_questions"] if q["type"] == category]
    
    test_questions = []
    
    # Inject some failed questions to review
    num_review = min(len(failed_pool), math.ceil(test_length * 0.3))
    if num_review > 0:
        sampled_failed = random.sample(failed_pool, num_review)
        for q in sampled_failed:
            q_copy = q.copy()
            q_copy["is_review"] = True
            test_questions.append(q_copy)
            
    needed = test_length - len(test_questions)
    
    if category == "verbal":
        # Apply theme filters
        bank_pool = VERBAL_BANK
        if st.session_state.cfg_verbal_filter != "All":
            bank_pool = [q for q in bank_pool if q["theme"] == st.session_state.cfg_verbal_filter]
            
        # Apply difficulty filters if not Mixed
        if user_diff != "Mixed":
            # Translate Spanish status internally if needed
            mapped_diff = "Sencillo" if user_diff in ["Sencillo", "Easy"] else ("Hard" if user_diff in ["Avanzado", "Hard"] else "Medium")
            diff_pool = [q for q in bank_pool if q["difficulty"] == mapped_diff]
            if len(diff_pool) >= needed:
                bank_pool = diff_pool
                
        existing_ids = {q["id"] for q in test_questions}
        available_pool = [q for q in bank_pool if q["id"] not in existing_ids]
        
        if len(available_pool) < needed:
            available_pool = bank_pool
            
        selected_verbal = random.sample(available_pool, min(len(available_pool), needed))
        test_questions.extend(selected_verbal)
        
    elif category == "numerical":
        for _ in range(needed):
            generator = random.choice([generate_numerical_patents, generate_numerical_palace, generate_numerical_energy])
            test_questions.append(generator())
            
    elif category == "abstract":
        for _ in range(needed):
            generator = random.choice([generate_abstract_rotation, generate_abstract_shapes])
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
        is_correct = (user_ans == q["correct"])
        if is_correct:
            correct_count += 1
            # Remove from failure pool
            profile["failed_questions"] = [fq for fq in profile["failed_questions"] if fq["id"] != q["id"]]
        else:
            # Store in failure pool
            if not any(fq["id"] == q["id"] for fq in profile["failed_questions"]):
                profile["failed_questions"].append({
                    "id": q["id"],
                    "type": q["type"],
                    "difficulty": q["difficulty"],
                    "passage": q.get("passage", ""),
                    "table": q.get("table", ""),
                    "svg": q.get("svg", ""),
                    "question": q["question"],
                    "options": q["options"],
                    "correct": q["correct"],
                    "explanation": q["explanation"]
                })
                
    # Update Stats
    profile[category]["completed"] += 1
    profile[category]["correct_total"] += correct_count
    total_completed = profile[category]["completed"] * len(questions)
    profile[category]["accuracy"] = round((profile[category]["correct_total"] / total_completed) * 100, 1)
    
    # Adaptive Step
    if st.session_state.cfg_difficulty_mode == "Adaptive":
        pct = (correct_count / len(questions)) * 100
        curr = profile[category]["difficulty"]
        if pct >= 80:
            if curr == "Sencillo":
                profile[category]["difficulty"] = "Medio"
            elif curr == "Medio":
                profile[category]["difficulty"] = "Avanzado"
        elif pct < 50:
            if curr == "Avanzado":
                profile[category]["difficulty"] = "Medio"
            elif curr == "Medio":
                profile[category]["difficulty"] = "Sencillo"
                
    st.session_state.profile = profile
    save_progress(profile)
    st.session_state.review_mode = True


# ==========================================
# 6. UI PRESENTATION VIEWS
# ==========================================

st.title("🧠 Adaptive Prep App")
st.caption("Custom Practice & Adaptive Logic Engine")

# MAIN HOME DASHBOARD
if st.session_state.current_test is None:
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📖 Study Cards", "⚙️ Settings"])
    
    with tab1:
        st.subheader("Your Progress")
        profile = st.session_state.profile
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="progress-card">
                <h4 style="margin:0;color:#4F46E5;">Verbal</h4>
                <p style="font-size:20px;font-weight:bold;margin:5px 0;">{profile['verbal']['accuracy']}%</p>
                <span style="font-size:11px;background:#EEF2F6;padding:3px 8px;border-radius:15px;color:#4F46E5;font-weight:bold;">Diff: {profile['verbal']['difficulty']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="progress-card">
                <h4 style="margin:0;color:#059669;">Numerical</h4>
                <p style="font-size:20px;font-weight:bold;margin:5px 0;">{profile['numerical']['accuracy']}%</p>
                <span style="font-size:11px;background:#ECFDF5;padding:3px 8px;border-radius:15px;color:#059669;font-weight:bold;">Diff: {profile['numerical']['difficulty']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="progress-card">
                <h4 style="margin:0;color:#D97706;">Abstract</h4>
                <p style="font-size:20px;font-weight:bold;margin:5px 0;">{profile['abstract']['accuracy']}%</p>
                <span style="font-size:11px;background:#FEF3C7;padding:3px 8px;border-radius:15px;color:#D97706;font-weight:bold;">Diff: {profile['abstract']['difficulty']}</span>
            </div>
            """, unsafe_allow_html=True)
            
        failed_count = len(profile["failed_questions"])
        if failed_count > 0:
            st.warning(f"🔄 **Spaced Repetition Alert:** You have **{failed_count} questions** in your review queue. These will appear in your upcoming tests to reinforce those concepts.")
        else:
            st.success("🎉 **Well Done!** Your error queue is completely empty.")
            
        st.markdown("---")
        st.subheader("Select Quiz to Start")
        
        # Action Buttons
        if st.button("💬 Start Verbal Reasoning Test"):
            start_new_test("verbal")
            st.rerun()
            
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
        if st.button("📊 Start Numerical Reasoning Test"):
            start_new_test("numerical")
            st.rerun()
            
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
        if st.button("🧩 Start Abstract Reasoning Test"):
            start_new_test("abstract")
            st.rerun()
            
    with tab2:
        st.subheader("Quick Method Cards")
        st.markdown("""
        **1. Verbal Reasoning Strategies**
        * Look for direct support in the text. Avoid choices that extend a narrow claim to a general truth.
        * Watch out for logical markers: *only*, *may*, *always*, *never*.
        * Correct options usually paraphrase direct sentences from the source texts.
        
        **2. Numerical Reasoning Strategies**
        * Ensure you match the correct columns and headers.
        * Watch the scale (e.g. population in thousands vs per-capita rate per million).
        * Read carefully whether a question asks for a raw count or a percentage shift.
        
        **3. Abstract Reasoning Logic**
        * **Rotation Rule:** Note the angular change per step (usually $45^\\circ$ or $90^\\circ$) and whether it is Clockwise (CW) or Counter-Clockwise (CCW).
        * **Geometric Steps:** Polygons often increase or decrease their side counts sequentially (e.g., $3 \\rightarrow 4 \\rightarrow 5 \\rightarrow 6$).
        """)
        
    with tab3:
        st.subheader("Configure Simulator Settings")
        
        st.session_state.cfg_difficulty_mode = st.radio(
            "Difficulty Steering Mode:",
            options=["Adaptive", "Manual"],
            index=["Adaptive", "Manual"].index(st.session_state.cfg_difficulty_mode)
        )
        
        if st.session_state.cfg_difficulty_mode == "Manual":
            st.session_state.cfg_manual_diff = st.selectbox(
                "Manual Level:",
                options=["Easy", "Medium", "Hard", "Mixed"],
                index=["Easy", "Medium", "Hard", "Mixed"].index(st.session_state.cfg_manual_diff)
            )
            
        st.session_state.cfg_length = st.selectbox(
            "Test Question Quantity:",
            options=["Quick", "Standard", "Extended"],
            index=["Quick", "Standard", "Extended"].index(st.session_state.cfg_length)
        )
        
        st.session_state.cfg_verbal_filter = st.selectbox(
            "Verbal Question Theme Filter:",
            options=["All", "Philosophy & Logic", "Science & Technology", "Economy & Society"],
            index=["All", "Philosophy & Logic", "Science & Technology", "Economy & Society"].index(st.session_state.cfg_verbal_filter)
        )
        
        st.markdown("---")
        if st.button("🗑️ Reset All Progress Metrics"):
            st.session_state.profile = {
                "verbal": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
                "numerical": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
                "abstract": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
                "failed_questions": []
            }
            save_progress(st.session_state.profile)
            st.success("Successfully reset progress data.")
            st.rerun()

# TEST REVIEW VIEW
elif st.session_state.review_mode:
    category = st.session_state.current_test
    questions = st.session_state.test_questions
    answers = st.session_state.answers
    
    correct_count = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["correct"])
    pct = int((correct_count / len(questions)) * 100)
    
    st.subheader("Test Completed")
    st.balloons() if pct >= 80 else None
    
    score_color = "#16A34A" if pct >= 70 else "#DC2626"
    st.markdown(f"""
    <div style="background-color: #F9FAFB; padding: 20px; border-radius: 16px; border: 2px solid #E5E7EB; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 14px; color: #6B7280; font-weight: bold; text-transform: uppercase;">Final Score</span>
        <h1 style="color: {score_color}; font-size: 45px; margin: 5px 0;">{correct_count} / {len(questions)}</h1>
        <p style="font-size: 18px; font-weight: bold; margin: 0;">Accuracy: {pct}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if pct >= 80:
        st.success(f"🌟 **Spectacular Performance!** You mastered this test. Your adaptive level is now: **{st.session_state.profile[category]['difficulty']}**.")
    elif pct >= 50:
        st.info("👍 **Solid Job.** You are making great progress. Keep it up to advance further.")
    else:
        st.warning(f"⚠️ **Focus Required.** Some topics were challenging. We've adjusted your adaptive difficulty to **{st.session_state.profile[category]['difficulty']}** to consolidate fundamentals.")
        
    st.markdown("---")
    st.subheader("Review Explanations")
    
    for i, q in enumerate(questions):
        user_ans = answers.get(i)
        is_correct = (user_ans == q["correct"])
        icon = "✅ Correct" if is_correct else f"❌ Failed (You chose {user_ans if user_ans else 'Blank'})"
        
        with st.expander(f"Question {i+1}: {icon}"):
            if "passage" in q and q["passage"]:
                st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
            if "table" in q and q["table"]:
                st.markdown(q["table"])
            if "svg" in q and q["svg"]:
                st.markdown(q["svg"], unsafe_allow_html=True)
                
            st.markdown(f"**Question:** {q['question']}")
            
            for opt in q["options"]:
                letter = opt[0]
                if letter == q["correct"]:
                    st.markdown(f"🟢 **{opt} (Correct)**")
                elif letter == user_ans:
                    st.markdown(f"🔴 **{opt} (Your Selection)**")
                else:
                    st.markdown(f"⚪ {opt}")
                    
            st.markdown("---")
            st.markdown(q["explanation"])
            
    st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
    if st.button("⬅️ Return to Main Dashboard"):
        st.session_state.current_test = None
        st.session_state.review_mode = False
        st.rerun()

# ACTIVE TEST SCREEN
else:
    category = st.session_state.current_test
    questions = st.session_state.test_questions
    idx = st.session_state.current_index
    q = questions[idx]
    
    # Header stats
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <span style="font-weight: bold; color: #4F46E5;">{category.upper()} - {q['difficulty']}</span>
        <span style="font-weight: bold; color: #6B7280;">Question {idx+1} of {len(questions)}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(idx / len(questions))
    
    if q.get("is_review"):
        st.warning("🔄 **Review Reinforcement:** You previously missed this question. Let's solve it successfully!")
        
    if "passage" in q and q["passage"]:
        st.markdown("**Read the Passage Carefully:**")
        st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
        
    if "table" in q and q["table"]:
        st.markdown("**Analyze the Data:**")
        st.markdown(q["table"])
        
    if "svg" in q and q["svg"]:
        st.markdown("**Analyze the Visual Sequence:**")
        st.markdown(q["svg"], unsafe_allow_html=True)
        
    st.markdown(f"<h3 style='font-size:1.15rem;margin-bottom:15px;'>{q['question']}</h3>", unsafe_allow_html=True)
    
    options_list = q["options"]
    
    selected_val = st.radio(
        "Choose your answer:",
        options=options_list,
        index=None if st.session_state.selected_option is None else options_list.index(st.session_state.selected_option),
        key=f"radio_active_q_{idx}"
    )
    
    if selected_val:
        st.session_state.selected_option = selected_val
        st.session_state.answers[idx] = selected_val[0]
        
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    
    if not st.session_state.show_explanation:
        if st.button("Confirm Answer"):
            if st.session_state.selected_option is None:
                st.warning("⚠️ Please select an option before proceeding.")
            else:
                st.session_state.show_explanation = True
                st.rerun()
    else:
        user_ans = st.session_state.answers.get(idx)
        if user_ans == q["correct"]:
            st.success("🎉 **Correct Answer!** Well reasoned.")
        else:
            st.error(f"❌ **Incorrect.** The correct answer was **{q['correct']}**.")
            
        with st.container():
            st.markdown("#### Solution:")
            st.markdown(q["explanation"])
            
        st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
        
        if idx + 1 < len(questions):
            if st.button("Next Question ➡️"):
                st.session_state.current_index += 1
                st.session_state.selected_option = None
                st.session_state.show_explanation = False
                st.rerun()
        else:
            if st.button("📊 View Test Results"):
                finish_active_test()
                st.rerun()
                
    st.markdown("<div style='margin-top:20px;' class='secondary-btn'></div>", unsafe_allow_html=True)
    col_back, _ = st.columns([1, 2])
    with col_back:
        if st.button("🚪 Exit Quiz"):
            st.session_state.current_test = None
            st.session_state.review_mode = False
            st.rerun()
