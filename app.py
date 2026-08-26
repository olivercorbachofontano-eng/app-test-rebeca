import streamlit as st
import json
import os
import random
import math

# Configuración de página responsive y amigable para móviles
st.set_page_config(
    page_title="Simulador de Examen - Práctica Adaptativa",
    page_icon="🧠",
    layout="centered", # Centrado es perfecto para móviles
    initial_sidebar_state="collapsed"
)

# Ruta del archivo de progreso local
PROGRESS_FILE = "progreso_estudiante.json"

# Estilos CSS personalizados para móviles (botones grandes, espaciados táctiles cómodos, responsive)
st.markdown("""
<style>
    /* Ajustes generales para pantallas estrechas */
    .reportview-container .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
    
    /* Botones táctiles grandes aptos para pulgares */
    div.stButton > button:first-child {
        width: 100%;
        height: 3.4rem;
        font-size: 1.15rem !important;
        font-weight: bold;
        border-radius: 14px;
        border: none;
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #4338CA 0%, #2563EB 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* Botones secundarios de navegación */
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
    
    /* Cajas de opciones de respuestas (grandes e interactivas) */
    div.row-widget.stRadio > div {
        background-color: #F9FAFB;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        margin-bottom: 15px;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
    }
    
    /* Bloques de textos de comprensión lectora (Verbal) */
    .passage-box {
        background-color: #F0FDF4;
        border-left: 5px solid #16A34A;
        padding: 16px;
        border-radius: 10px;
        font-size: 1.05rem;
        line-height: 1.65;
        color: #1F2937;
        margin-bottom: 22px;
        max-height: 280px;
        overflow-y: auto;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Tarjetas del Dashboard de Progreso */
    .progress-card {
        background-color: white;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        text-align: center;
    }
    
    /* Tarjetas de Reglas de Estudio */
    .rule-card {
        background-color: #FEE2E2;
        border-left: 5px solid #EF4444;
        padding: 14px;
        border-radius: 8px;
        font-size: 0.95rem;
        margin-bottom: 10px;
        color: #7F1D1D;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. BANCO DE PREGUNTAS EXTENDIDO DE EXAMEN (VERBAL) - 30 ITEMS
# ==========================================

VERBAL_BANK = [
    {
        "id": "v_searle_chinese",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Medio",
        "passage": "El argumento de la habitación china, propuesto por John Searle, desafía a la inteligencia artificial fuerte sosteniendo que la manipulación sintáctica de símbolos no constituye comprensión semántica [6]. Imagina a una persona en una habitación que manipula caracteres chinos siguiendo un libro de reglas. Produce respuestas perfectas indistinguibles de un hablante nativo, pero sigue sin comprender nada de chino [32]. La 'réplica de los sistemas' concede que el operador no entiende, pero afirma que la comprensión debe atribuirse al sistema completo (operador, reglas y datos) [32]. Searle objeta que si el operador internalizara todo el sistema, seguiría sin comprender chino [33].",
        "question": "¿Cuál de las siguientes afirmaciones sintetiza correctamente la réplica de los sistemas y la objeción de Searle?",
        "options": [
            "A) La réplica afirma que la comprensión emerge a nivel de todo el sistema; Searle objeta que internalizar el sistema no añade comprensión real.",
            "B) La réplica sostiene que el operador comprende de manera aislada; Searle acepta que el sistema completo genera conciencia.",
            "C) La réplica niega que pueda existir traducción perfecta; Searle demuestra que la sintaxis eventualmente produce semántica.",
            "D) Ambas partes coinciden en que la simulación de procesos neuronales es idéntica a la manipulación abstracta."
        ],
        "correct": "A",
        "explanation": "La réplica de los sistemas argumenta que la comprensión se atribuye al conjunto y no al operador individual [32]. Searle rebate esto señalando que incluso si el operador memoriza ('internaliza') todas las reglas y datos del sistema, seguirá realizando solo manipulación de símbolos sin comprender su significado semántico [33]."
    },
    {
        "id": "v_godel_incompleteness",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Avanzado",
        "passage": "Los teoremas de incompletez de Kurt Gödel (1931) transformaron nuestra comprensión de la lógica matemática [3]. El primer teorema demuestra que cualquier sistema formal consistente capaz de expresar aritmética básica contiene proposiciones que son verdaderas pero indemostrables dentro del sistema [3]. El segundo teorema prueba que tal sistema no puede demostrar su propia consistencia [3]. Estos resultados destrozaron el programa formalista de Hilbert, que buscaba fundamentar la matemática sobre bases axiomáticas completas y consistentes [3].",
        "question": "De acuerdo con el texto, ¿qué implicación directa tienen los teoremas de Gödel sobre la axiomatización de las matemáticas?",
        "options": [
            "A) Demuestran que la matemática es inherentemente inconsistente y contradictoria en todos sus niveles.",
            "B) Implican que en sistemas formales suficientemente ricos existen proposiciones verdaderas que eluden ser derivadas lógicamente.",
            "C) Fortalecen el programa formalista al demostrar que la autorreferencia previene contradicciones.",
            "D) Sugieren que la lógica de primer orden puede probar su propia consistencia si se eliminan los números primos."
        ],
        "correct": "B",
        "explanation": "El primer teorema demuestra de forma directa que en sistemas formales consistentes lo suficientemente ricos (capaces de expresar aritmética básica), existen proposiciones que son verdaderas pero que no se pueden demostrar (derivar formalmente) utilizando las reglas del propio sistema [3]."
    },
    {
        "id": "v_wittgenstein_private",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Medio",
        "passage": "El argumento de Wittgenstein contra el lenguaje privado sostiene que no puede existir un lenguaje cuyos términos se refieran a sensaciones accesibles exclusivamente para el hablante [28]. En un lenguaje privado, la corrección de un término dependería de la impresión subjetiva actual del hablante, lo cual disuelve la distinción entre seguir una regla correctamente y simplemente creer que se está siguiendo [29, 47]. Por tanto, los conceptos mentales deben estar respaldados por criterios públicamente observables [17].",
        "question": "¿Por qué es lógicamente imposible un lenguaje privado según el análisis de Wittgenstein?",
        "options": [
            "A) Porque es empíricamente imposible que dos seres humanos tengan las mismas sensaciones internas.",
            "B) Porque sin un patrón de corrección independiente a la impresión del hablante, el concepto de corrección y significado se disuelve.",
            "C) Porque las sensaciones privadas de dolor o placer no existen en el mundo real.",
            "D) Porque las reglas gramaticales del lenguaje natural se aprenden exclusivamente mediante la imitación conductual."
        ],
        "correct": "B",
        "explanation": "En ausencia de criterios externos o públicos, el hablante no tendría forma de distinguir entre estar aplicando una palabra correctamente o simplemente creer que lo hace, lo que destruye la normatividad necesaria para que exista el significado [29, 47]."
    },
    {
        "id": "v_banach_tarski",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Avanzado",
        "passage": "En teoría de la medida, la paradoja de Banach-Tarski establece que una esfera sólida tridimensional puede descomponerse en un número finito de piezas que, al reensamblarse mediante movimientos rígidos, forman dos esferas idénticas a la original [34]. Esto no contradice la física materialista, pues las piezas involucradas son conjuntos no medibles que carecen de volumen definido, cuya existencia depende del Axioma de Elección [34]. La paradoja ilumina una tensión entre nuestra intuición geométrica y los compromisos de la teoría de conjuntos al admitir colecciones no constructivas [35].",
        "question": "¿Cuál es la causa matemática detrás de la aparente contradicción de la paradoja de Banach-Tarski según el texto?",
        "options": [
            "A) La violación directa de la conservación de la masa física en objetos tridimensionales reales.",
            "B) La división de la esfera en piezas con volúmenes decimales extremadamente pequeños.",
            "C) El empleo de conjuntos no medibles que carecen de un volumen bien definido bajo el axioma de elección.",
            "D) La asunción errónea de que las piezas son rígidas cuando en realidad son flexibles."
        ],
        "correct": "C",
        "explanation": "La paradoja no rompe leyes físicas porque ocurre en el plano matemático utilizando conjuntos no medibles que no tienen un volumen definido. Esto es posible debido a los presupuestos teóricos del axioma de elección para conjuntos no constructivos [34, 35]."
    },
    {
        "id": "v_sorites_vagueness",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Sencillo",
        "passage": "La paradoja de sorites (o del montón) es un problema que surge de predicados vagos en el lenguaje natural [1]. Un montón de arena sigue siendo un montón si quitamos un solo grano; aplicando esta lógica repetidamente, llegaríamos a la conclusión absurda de que un solo grano constituye un montón [1]. La paradoja explota la vaguedad y no la ambigüedad: quitar un grano no cambia el estado, pero la repetición sí [41]. Las soluciones propuestas incluyen la lógica difusa (grados de verdad) y el supervaluacionismo (declaraciones imprecisas que retienen valores de verdad bajo ciertas condiciones) [1].",
        "question": "¿Qué distingue la vaguedad de la ambigüedad en el contexto de la paradoja de Sorites?",
        "options": [
            "A) La vaguedad implica que un término tiene múltiples significados discretos que el contexto puede aclarar.",
            "B) La vaguedad se caracteriza por la falta de límites precisos y transiciones graduales, mientras que la ambigüedad ofrece múltiples significados definidos.",
            "C) La vaguedad es una falla del pensamiento lógico que el supervaluacionismo elimina por completo de la sintaxis.",
            "D) No existe diferencia alguna; ambos conceptos describen exactamente el mismo fenómeno lingüístico."
        ],
        "correct": "B",
        "explanation": "El texto explica que el Sorites explota la vaguedad, es decir, términos cuyos límites son imprecisos y graduales (como 'montón') [41]. La ambigüedad, en cambio, se da cuando una palabra tiene varios significados discretos que el contexto resuelve [41]."
    },
    {
        "id": "v_popper_tolerance",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Sencillo",
        "passage": "La paradoja de la tolerancia de Karl Popper establece que si una sociedad es tolerante sin límites, su capacidad de ser tolerante será eventualmente destruida por los intolerantes [40]. La conclusión no es reprimir de inmediato las ideas intolerantes (Popper prefería contrarrestarlas con argumentos y opinión pública), sino reclamar el derecho a no tolerar a los intolerantes únicamente cuando estos rechazan el debate racional y recurren a la fuerza [40].",
        "question": "Según el fragmento, ¿cuándo está justificado, en última instancia, el derecho a no tolerar a los intolerantes?",
        "options": [
            "A) Tan pronto como expresen opiniones que resulten ofensivas para el resto de la comunidad.",
            "B) Únicamente cuando los intolerantes abandonan el debate racional y responden con el uso de la fuerza.",
            "C) Cuando sus opiniones empiezan a influir en los resultados electorales de la democracia.",
            "D) Popper sostiene que nunca está justificada la intolerancia bajo ninguna circunstancia práctica."
        ],
        "correct": "B",
        "explanation": "Popper establece un umbral muy claro: prefiere tolerar y debatir, pero se reserva el derecho a no tolerar a los intolerantes cuando se niegan a debatir racionalmente y eligen responder con la fuerza o la violencia [40]."
    },
    {
        "id": "v_sapir_whorf",
        "type": "verbal",
        "topic": "Ciencia y Tecnología",
        "difficulty": "Sencillo",
        "passage": "La hipótesis de Sapir-Whorf, en su versión determinista fuerte, sostiene que la estructura de la lengua que hablamos determina de forma absoluta los límites de nuestro pensamiento, de modo que lo que no se puede expresar en un idioma sería impensable para sus hablantes [38]. Esta versión carece de respaldo empírico hoy en día [38]. En cambio, la versión débil o de influencia cognitiva sugiere que el lenguaje influye en la memoria y la atención, facilitando ciertos pensamientos sin imponer barreras infranqueables.",
        "question": "¿Cuál es la situación actual de la versión fuerte de la hipótesis de Sapir-Whorf de acuerdo con las investigaciones?",
        "options": [
            "A) Cuenta con un sólido apoyo empírico gracias a estudios de neurociencia cognitiva.",
            "B) Es aceptada unánimemente en la lingüística moderna como la explicación estándar.",
            "C) Carece de sustento empírico contemporáneo, prefiriéndose en su lugar la versión de influencia débil.",
            "D) Se ha fusionado con las teorías conductistas para explicar el bilingüismo."
        ],
        "correct": "C",
        "explanation": "El texto es explícito al señalar que la versión fuerte de la hipótesis (determinismo lingüístico absoluto) 'carece de soporte empírico hoy en día', favoreciendo en cambio visiones de influencia débil sobre la cognición [38]."
    },
    {
        "id": "v_coase_theorem",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Medio",
        "passage": "El teorema de Coase establece que si los derechos de propiedad están bien definidos y los costos de transacción son nulos, la negociación privada llevará a una asignación de recursos eficiente, independientemente de la distribución inicial de dichos derechos [38]. Sin embargo, en el mundo real, los costos de transacción que impiden o dificultan las negociaciones privadas son la regla y no la excepción [38]. Por ende, el teorema no es una apología ciega del laissez-faire, sino una herramienta para analizar cómo los costos institucionales moldean el mercado.",
        "question": "¿Qué factor del mundo real limita la aplicación directa de la eficiencia predicha por el teorema de Coase?",
        "options": [
            "A) La intervención constante y benévola de los tribunales de arbitraje.",
            "B) La existencia generalizada de costos de transacción que dificultan o impiden la negociación privada.",
            "C) La impossibility matemática de definir derechos de propiedad intelectual.",
            "D) La falta de interés de los agentes económicos en maximizar sus ganancias."
        ],
        "correct": "B",
        "explanation": "El texto aclara que en la realidad, a diferencia de la asunción teórica del teorema, los costos de transacción que entorpecen la negociación son la regla general, lo que restringe que se logre una solución eficiente de manera espontánea [38]."
    },
    {
        "id": "v_frame_problem",
        "type": "verbal",
        "topic": "Ciencia y Tecnología",
        "difficulty": "Avanzado",
        "passage": "El problema del marco (frame problem) en inteligencia artificial revela dificultades profundas sobre cómo los sistemas inteligentes representan y actualizan su conocimiento sobre un mundo en constante cambio [67]. Al realizar una acción, el sistema debe determinar qué hechos siguen siendo ciertos y cuáles cambian; sin embargo, representar explícitamente todos los hechos inalterados resulta computacionalmente inabordable [67]. El problema de la cualificación agrava esto al requerir especificar todas las condiciones bajo las cuales una acción tendrá el efecto deseado [67]. Estos problemas sugieren que la inteligencia requiere no solo razonamiento deductivo, sino la capacidad de formular suposiciones heurísticas sobre relevancia y cambio [11, 13, 67].",
        "question": "De acuerdo con el texto, ¿qué revela el problema del marco sobre la naturaleza del razonamiento inteligente?",
        "options": [
            "A) Que la inteligencia se puede lograr exclusivamente a través de la representación lógica de todos los estados del entorno.",
            "B) Que el razonamiento lógico formal deductivo, sin heurísticas de relevancia, resulta computacionalmente intratable para actualizar la información.",
            "C) Que el problema de la cualificación asegura que cualquier acción tendrá éxito si se omiten las variables ambientales.",
            "D) Que Dennett demostró que el problema del marco carece de implicaciones para entender el pensamiento racional humano."
        ],
        "correct": "B",
        "explanation": "El texto destaca que actualizar lógicamente todos los hechos inalterados tras una acción es computacionalmente intratable, lo que implica que la inteligencia requiere de heurísticas de relevancia y suposiciones por defecto de cambio, superando la pura deducción formal explicta [13, 67]."
    },
    {
        "id": "v_newcomb_paradox",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Avanzado",
        "passage": "La paradoja de Newcomb enfrenta dos principios de decisión racionales que usualmente se alinean [26]. Un predictor casi infalible pone 1 millón de euros en una caja opaca si predice que el agente elegirá solo esa caja, y 1,000 euros en una caja transparente que siempre está ahí [26]. El principio de utilidad esperada aconseja elegir solo la caja opaca, dada la alta probabilidad de acierto del predictor [26]. El principio de dominancia aconseja elegir ambas cajas, pues haga lo que haga el predictor, añadir la caja transparente siempre añade 1,000 euros al resultado [27]. La discrepancia muestra que ambos principios presuponen tesis incompatibles sobre si la decisión es causalmente independiente de un estado predeterminado del mundo [27].",
        "question": "¿Qué tesis subyacente entra en conflicto directo en la paradoja de Newcomb según el pasaje?",
        "options": [
            "A) La validez intrínseca de las matemáticas puras frente a las leyes de la física relativista clásica.",
            "B) El supuesto de si una decisión racional puede tratarse como causalmente independiente de un estado predeterminado del mundo.",
            "C) La infalibilidad absoluta de la intuición humana frente al cálculo de probabilidades axiomático tradicional.",
            "D) El conflicto moral entre la acumulación egoísta de riquezas y el principio de la justicia distributiva."
        ],
        "correct": "B",
        "explanation": "El texto señala explícitamente que la paradoja surge porque los dos principios presuponen tesis incompatibles sobre la independencia causal de la decisión frente a un estado predeterminado [27]."
    },
    {
        "id": "v_logocentrism",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Avanzado",
        "passage": "La deconstrucción de Derrida revela cómo la filosofía occidental ha privilegiado sistemáticamente la presencia sobre la ausencia, el habla sobre la escritura y la identidad sobre la diferencia [8]. Este logocentrismo asume que el habla es una transmisión directa del pensamiento o logos, mientras que la escritura es una copia secundaria propensa al error [8]. Derrida introduce la noción de 'archi-escritura' para demostrar que el habla misma depende de la estructura diferencial que caracteriza a la escritura, impidiendo un significado puro y autosuficiente [8].",
        "question": "¿Por qué argumenta Derrida que el logocentrismo es insostenible según el pasaje?",
        "options": [
            "A) Porque la escritura es históricamente anterior al habla en todas las culturas conocidas.",
            "B) Porque el habla misma depende de la estructura diferencial y diferida (archi-escritura) que convencionalmente se atribuye a la escritura.",
            "C) Porque los filósofos griegos ya habían desechado el concepto de logos en el periodo clásico.",
            "D) Porque la deconstrucción demuestra que las palabras carecen de cualquier uso práctico o semántico."
        ],
        "correct": "B",
        "explanation": "Derrida sostiene que el logocentrismo es inviable porque el habla, lejos de ser una transmisión directa y pura de la razón, está condicionada por la misma estructura de diferencias y mediaciones que caracteriza a la escritura [8]."
    },
    {
        "id": "v_other_minds",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Medio",
        "passage": "El problema de las otras mentes plantea una brecha epistémica entre la primera y la tercera persona: ¿cómo sabemos que los demás poseen conciencia y estados mentales similares a los nuestros si solo observamos su conducta física? [12]. El conductismo intentó resolverlo reduciendo los estados mentales a disposiciones de comportamiento, sacrificando la cualidad subjetiva de la experiencia [12]. El argumento por analogía sugiere que, como mi conducta se asocia a mis estados mentales, conductas similares en otros indican mentes similares, pero este razonamiento es débil al basarse en un único caso observado (el propio) [12].",
        "question": "¿Cuál es el principal punto débil del argumento por analogía para conocer otras mentes?",
        "options": [
            "A) Que reduce de forma errónea los dolores y alegrías subjetivas a simples impulsos eléctricos cerebrales.",
            "B) Que se basa en una inducción extremadamente débil, al generalizar la existencia de mentes ajenas a partir de un único caso observado: uno mismo.",
            "C) Que niega que la conducta física de las personas guarde cualquier correlación con sus intenciones.",
            "D) Que exige un examen neurocientífico destructivo para poder ser verificado experimentalmente en laboratorios."
        ],
        "correct": "B",
        "explanation": "El pasaje indica que el argumento por analogía padece de debilidad epistémica porque intenta inferir una regla general para toda la humanidad basándose en la autoobservación de un único individuo [12]."
    },
    {
        "id": "v_hard_problem",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Medio",
        "passage": "El filósofo David Chalmers distingue entre los problemas fáciles y el problema difícil de la conciencia [9]. Los problemas fáciles explican funciones cognitivas y de procesamiento de información (atención, integración sensorial, etc.), mientras que el problema difícil se pregunta por qué existe la experiencia subjetiva (el 'qualia') en primer lugar: ¿por qué los procesos cerebrales se sienten de determinada manera desde adentro en lugar de ocurrir en la oscuridad cognitiva? [9]. Las teorías panpsiquistas sugieren que la conciencia es fundamental en el universo, pero enfrentan el 'problema de la combinación' al intentar explicar cómo microexperiencias se agrupan en una mente compleja [9].",
        "question": "¿A qué se refiere específicamente el 'problema difícil' de la conciencia según el fragmento?",
        "options": [
            "A) A la complejidad computacional para programar una red neuronal que reconozca rostros en tiempo real.",
            "B) A la cuestión de por qué existe una dimensión subjetiva de la experiencia asociada al procesamiento de información del cerebro.",
            "C) A la dificultad de combinar microexperiencias atómicas para dar origen a una mente humana única.",
            "D) Al tratamiento psiquiátrico de los trastornos de la atención y la memoria operativa cerebral."
        ],
        "correct": "B",
        "explanation": "El problema difícil radica en responder por qué los procesos de información del cerebro vienen acompañados de una experiencia subjetiva consciente en lugar de ser meras operaciones biológicas inconscientes [9]."
    },
    {
        "id": "v_lucas_critique",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Avanzado",
        "passage": "La crítica de Lucas, formulada en 1976, revolucionó la teoría de la política económica al argumentar que es ingenuo predecir los efectos de un cambio de política basándose puramente en relaciones observadas en datos históricos [31]. Lucas sostiene que los agentes económicos adaptan sus expectativas y comportamientos en respuesta a los cambios en las reglas de política [31, 48]. Por tanto, los parámetros de las ecuaciones estimadas bajo un régimen anterior no permanecerán invariables ante un nuevo régimen, requiriéndose modelar parámetros estables como las preferencias y la tecnología de forma endógena [31, 48].",
        "question": "¿Cuál es el argumento central de la crítica de Lucas sobre los modelos macroeconómicos de la época?",
        "options": [
            "A) Que es absolutamente imposible evaluar el impacto de cualquier decisión económica futura bajo ninguna metodología.",
            "B) Que los agentes económicos son pasivos y nunca modifican su comportamiento ante cambios regulatorios.",
            "C) Que los parámetros históricos estimados no son invariables, ya que los agentes modifican racionalmente su conducta en previsión de las nuevas políticas.",
            "D) Que el uso de herramientas estadísticas sofisticadas es innecesario si se conocen los deseos de los políticos estatales."
        ],
        "correct": "C",
        "explanation": "La crítica reside en que los parámetros empíricos estimados históricamente varían cuando cambia la política, dado que los ciudadanos adaptan activamente sus expectativas a las nuevas condiciones, inutilizando las predicciones estáticas [31, 48]."
    },
    {
        "id": "v_arrow_theorem",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Medio",
        "passage": "El teorema de imposibilidad de Arrow demuestra que ningún sistema de votación o regla de decisión colectiva puede convertir de manera consistente las preferencias individuales en una preferencia social que satisfaga simultáneamente un conjunto mínimo de condiciones lógicas y democráticas (universalidad, no dictadura, transitividad, independencia de alternativas irrelevantes), a menos que el sistema admita una dictadura [46]. Esto plantea dudas sobre la racionalidad colectiva en los procesos democráticos [46].",
        "question": "¿Cuál es la conclusión de Arrow sobre las reglas de decisión colectiva?",
        "options": [
            "A) Que las democracias siempre derivan en regímenes dictatoriales de partido único.",
            "B) Que es lógicamente imposible diseñar un sistema de votación colectiva que cumpla a la vez con todas las condiciones democráticas y de consistencia lógica sin ser dictatorial.",
            "C) Que las elecciones colectivas son irracionales porque los votantes nunca tienen información completa.",
            "D) Que los costos de transacción impiden que la sociedad civil llegue a acuerdos eficientes."
        ],
        "correct": "B",
        "explanation": "El teorema establece matemáticamente la imposibilidad de satisfacer a la vez condiciones democráticas y lógicas razonables al unificar preferencias individuales en una sola voluntad social sin incurrir en dictadura [46]."
    },
    {
        "id": "v_paraconsistent",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Avanzado",
        "passage": "El principio de no contradicción sostiene que una proposición no puede ser verdadera y falsa al mismo tiempo. Sin embargo, las lógicas paraconsistentes desafían esto al admitir ciertas contradicciones verdaderas (dialeteismo) sin colapsar en la trivialidad [42]. En la lógica clásica, el principio de explosión dictamina que de una contradicción se sigue cualquier proposición absurda (trivialidad) [42]. Bloqueando este principio de explosión, las lógicas paraconsistentes permiten razonar sistemáticamente en sistemas que toleran contradicciones localizadas sin volverlos inservibles [42, 43].",
        "question": "¿Cómo evitan las lógicas paraconsistentes colapsar en la trivialidad matemática según el texto?",
        "options": [
            "A) Eliminando por completo las contradicciones de su marco algebraico formal.",
            "B) Bloqueando el principio de explosión para evitar que una contradicción puntual permita derivar cualquier proposición.",
            "C) Aceptando que todas las proposiciones posibles en un sistema son simultáneamente verdaderas.",
            "D) Aplicando reglas de lógica difusa que imponen valores estrictamente binarios."
        ],
        "correct": "B",
        "explanation": "Al impedir que opere el principio clásico de explosión (*ex contradictione quodlibet*), una contradicción puntual no contamina todo el sistema deductivo, evitando la trivialidad [42, 43]."
    },
    {
        "id": "v_selfish_gene",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Sencillo",
        "passage": "Desde una perspectiva evolutiva centrada en el gen, Richard Dawkins argumenta que los organismos son esencialmente vehículos construidos por los genes para facilitar su propia replicación [42]. El término 'egoísta' es una metáfora metodológica para describir cómo la selección natural actúa a nivel del gen [42]. Lejos de fomentar un egoísmo despiadado a nivel del organismo, la teoría explica que comportamientos altruistas y cooperativos en animales evolucionan precisamente porque aumentan la probabilidad de supervivencia de los genes compartidos en familiares [42].",
        "question": "Según el texto, ¿cómo concilia la perspectiva del gen egoísta la existencia del comportamiento altruista en la naturaleza?",
        "options": [
            "A) Sostiene que el altruismo es una anomalía evolutiva que la selección natural acabará eliminando de todas las especies.",
            "B) Explica que cooperar a nivel de organismo favorece la supervivencia y replicación de los genes compartidos a nivel subyacente.",
            "C) Niega rotundamente que existan acciones de cooperación o empatía genuinas entre animales salvajes.",
            "D) Afirma que los genes son seres conscientes capaces de planificar su propia benevolencia comunitaria."
        ],
        "correct": "B",
        "explanation": "La teoría muestra que el altruismo del organismo es perfectamente coherente con el 'egoísmo' génico, ya que cooperar ayuda a perpetuar copias de los mismos genes presentes en los familiares [42]."
    },
    {
        "id": "v_anthropic_principle",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Sencillo",
        "passage": "El principio antrópico, en su versión débil, establece que nuestras observaciones del universo están necesariamente condicionadas por la existencia de observadores: solo podemos medir condiciones físicas y eras cosmológicas compatibles con el desarrollo de la vida orgánica y la inteligencia [44]. Esta formulación, que roza la tautología, es útil como corrección metodológica contra sesgos de selección en astrofísica al evaluar la probabilidad de diversos parámetros naturales [44].",
        "question": "¿Cuál es el valor metodológico del principio antrópico débil según el pasaje?",
        "options": [
            "A) Permite predecir con absoluta certeza que existe vida extraterrestre inteligente en galaxias vecinas.",
            "B) Sirve para corregir sesgos de selección, recordando que las leyes físicas que medimos deben ser compatibles con nuestra existencia.",
            "C) Demuestra que el universo fue diseñado específicamente con el propósito de albergar a la especie humana.",
            "D) Justifica el abandono de experimentos físicos basados en la recopilación empírica de datos espectrales."
        ],
        "correct": "B",
        "explanation": "El principio actúa como recordatorio metodológico de que la observación científica está sesgada: el mero hecho de que estemos aquí para medir las constantes físicas implica que estas deben ser compatibles con la vida [44]."
    },
    {
        "id": "v_prisoners_dilemma",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Sencillo",
        "passage": "En teoría de juegos, el dilema del prisionero describe una situación en la que dos agentes racionales eligen traicionarse mutuamente a pesar de que cooperar les daría un beneficio conjunto mucho mayor. La estrategia racional egoísta individual (el equilibrio de Nash) conduce a un resultado subóptio o ineficiente para ambos, ilustrando una tensión trágica entre el interés propio racional y la cooperación social.",
        "question": "¿Qué tensión central ilustra el dilema del prisionero?",
        "options": [
            "A) Que la cooperación colectiva surge de forma espontánea y automática siempre que los seres humanos actúan de forma libre.",
            "B) Que el interés propio racional de los individuos puede conducir a un resultado colectivo ineficiente y perjudicial para ambos.",
            "C) Que la traición mutua es éticamente superior a cualquier pacto social estructurado por la ley estatal.",
            "D) Que los sistemas judiciales de encarcelamiento preventivo violan las libertades civiles básicas de los sospechosos."
        ],
        "correct": "B",
        "explanation": "El dilema reside en que, persiguiendo su mejor opción egoísta individual, ambos agentes terminan en un equilibrio peor que el que habrían alcanzado mediante la cooperación coordinada."
    },
    {
        "id": "v_rawls_justice",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Medio",
        "passage": "En filosofía política, John Rawls propone que los principios de una sociedad justa deben acordarse tras un 'velo de ignorancia' [13]. En esta posición original, nadie conoce su estatus socioeconómico, capacidades intelectuales, género o concepción del bien [13]. Rawls argumenta que este velo garantiza la imparcialidad, pues al no saber si serán ricos o pobres, los agentes acordarán maximizar la posición de los más desfavorecidos (el principio minimax o de diferencia) para protegerse de la miseria extrema.",
        "question": "¿Cuál es la función del 'velo de ignorancia' en el modelo de justicia de Rawls según el texto?",
        "options": [
            "A) Ocultar información sobre corrupción gubernamental al electorado general para evitar protestas sociales.",
            "B) Forzar a los legisladores a ignorar las leyes físicas de la escasez de recursos al diseñar presupuestos económicos.",
            "C) Garantizar la imparcialidad en la elección de principios al ocultar la posición particular de cada agente en la futura sociedad.",
            "D) Promover la sumisión ciega de los ciudadanos ante las directivas del Estado soberano e institucional."
        ],
        "correct": "C",
        "explanation": "El velo de ignorancia anula los intereses egoístas obligando a los agentes a decidir basándose en consideraciones de equidad social, ya que podrían acabar en el escalafón más vulnerable del sistema [13]."
    },
    {
        "id": "v_robot_reply",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Sencillo",
        "passage": "Frente al argumento de Searle sobre la habitación china, la 'réplica del robot' sugiere que la falta de comprensión reside en que el sistema de la habitación está aislado sensorialmente del mundo externo [6, 15]. Si colocamos el programa dentro de un robot móvil que interactúe físicamente con su entorno, el sistema podrá asociar los caracteres con objetos reales a través de sensores y actuadores, posibilitando que emerja la verdadera semántica [6, 16].",
        "question": "¿En qué consiste la 'réplica del robot' descrita en el pasaje?",
        "options": [
            "A) En defender que las máquinas cibernéticas terminarán dominando a la humanidad debido a su superioridad física.",
            "B) En sostener que la interacción física con el entorno mediante sensores y actuadores es necesaria para dotar de semántica a los símbolos.",
            "C) En simular los impulsos nerviosos del cerebro biológico mediante redes neuronales analógicas de silicio.",
            "D) En argumentar que los robots carecen de cualquier posibilidad de realizar tareas complejas de manipulación sintáctica."
        ],
        "correct": "B",
        "explanation": "La réplica del robot argumenta que la semántica requiere corporeidad (*embodiment*): el robot conecta el símbolo lingüístico con el objeto del mundo físico a través de su experiencia sensorio-motora directo [6, 16]."
    },
    {
        "id": "v_peter_principle",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Sencillo",
        "passage": "En el estudio de la sociología organizacional, el Principio de Peter sostiene que en una jerarquía, todo empleado tiende a ascender hasta alcanzar su nivel de incompetencia. Esto implica que los puestos de mayor responsabilidad se llenan de forma inevitable con personas ineptas que antes realizaban bien tareas más sencillas, provocando ineficiencias sistémicas que son compensadas por empleados que todavía no han alcanzado su límite jerárquico.",
        "question": "¿Cuál es la tesis central que defiende el Principio de Peter?",
        "options": [
            "A) Que los buenos empleados siempre mantendrán su nivel de excelencia sin importar el puesto de la jerarquía empresarial.",
            "B) Que los trabajadores tienden a ser promocionados de manera sucesiva hasta un nivel donde su rendimiento se vuelve incompetente.",
            "C) Que la capacitación y educación laboral es inútil en las empresas privadas modernas.",
            "D) Que la promoción de puestos debe decidirse exclusivamente de manera democrática y asamblearia por los empleados."
        ],
        "correct": "B",
        "explanation": "El principio indica que las promociones se basan en el éxito en el puesto anterior y no en las capacidades para el nuevo cargo, lo que estanca a las personas una vez que fracasan en su nivel máximo."
    },
    {
        "id": "v_bionics_concept",
        "type": "verbal",
        "topic": "Ciencia y Tecnología",
        "difficulty": "Sencillo",
        "passage": "La biónica es la disciplina científica que busca imitar los sistemas y mecanismos de la naturaleza en el diseño tecnológico y médico [146]. Los neurocientíficos destacan que la creación artística y la biónica comparten procesos cognitivos comunes, donde se analiza la respuesta biológica o emocional evocada para evocarla o replicarla artificialmente en el diseño industrial o la salud [79, 146]. Al combinar la abstracción formal de un modelo biológico con soluciones ingenieriles, la biónica sintetiza ciencia y diseño estético de manera fluida [146].",
        "question": "¿Cuál de las siguientes afirmaciones describe el propósito de la biónica según el texto?",
        "options": [
            "A) Reemplazar la totalidad de los órganos humanos con componentes robóticos puramente mecánicos e inservibles.",
            "B) Diseñar tecnologías y soluciones artificiales imitando mecanismos y sistemas de la naturaleza.",
            "C) Limitar la investigación médica al estudio exclusivamente teórico de restos fósiles arqueológicos.",
            "D) Negar la utilidad de la creatividad estética en la ingeniería aplicada moderna."
        ],
        "correct": "B",
        "explanation": "El texto define la biónica como la aplicación de principios biológicos y mecanismos naturales al desarrollo de nuevas tecnologías [146]."
    },
    {
        "id": "v_trace_derrida",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Medio",
        "passage": "Derrida expone que cada signo lingüístico posee una estructura de 'huella' (*trace*), lo que significa que un signo nunca es autosuficiente ni tiene un significado puro por sí mismo [8]. La identidad y sentido de una palabra dependen de las huellas o marcas dejadas por otros signos ausentes de los cuales se diferencia [8]. Esta interconexión interminable desmiente la noción de una presencia pura de la verdad en la mente, revelando que el lenguaje funciona como una trama abierta de remisiones mutuas [8].",
        "question": "¿Qué consecuencia teórica se deriva de la estructura de la 'huella' en el lenguaje según Derrida?",
        "options": [
            "A) Que es imposible que los seres de una comunidad logren comunicarse de manera pragmática.",
            "B) Que los signos adquieren un significado inmediato y absoluto al aislarse de su contexto discursivo general.",
            "C) Que el sentido de un signo está interconectado con otros signos ausentes, imposibilitando la presencia pura del significado.",
            "D) Que los diccionarios tradicionales son las únicas fuentes de verdad científica inalterable."
        ],
        "correct": "C",
        "explanation": "La estructura de huella de Derrida significa que cada elemento lingüístico lleva consigo las marcas de otros términos de la cadena de significado, por lo que el sentido nunca está enteramente presente de forma pura o aislada [8]."
    },
    {
        "id": "v_moore_defense",
        "type": "verbal",
        "topic": "Filosofía y Lógica",
        "difficulty": "Avanzado",
        "passage": "Ante el escepticismo radical que argumenta la imposibilidad de conocer el mundo externo, el filósofo G.E. Moore propuso una famosa defensa del sentido común alzando su mano derecha y declarando 'aquí hay una mano' [45]. Moore sostiene que la certeza intuitiva que poseemos de verdades cotidianas es muy superior a la certeza de cualquier premisa escéptica compleja diseñada para desmentirlas [45]. Esta postura no intenta probar lógicamente que las premisas del escéptico sean falsas, sino que invierte la carga de la prueba en beneficio del realismo empírico [45].",
        "question": "¿Cuál es la estrategia metodológica empleada por G.E. Moore contra el escepticismo radical según el texto?",
        "options": [
            "A) Demostrar lógicamente a partir de axiomas puramente matemáticos la existencia física de la materia.",
            "B) Revertir la carga de la prueba, sosteniendo que la certidumbre de percepciones cotidianas supera la verosimilitud de las premisas escépticas.",
            "C) Aceptar la conclusión del escéptico de que es imposible saber si tenemos un cuerpo biológico real.",
            "D) Reducir la realidad externa a un conjunto de proyecciones subjetivas de la imaginación individual."
        ],
        "correct": "B",
        "explanation": "Moore argumenta que su certeza de poseer una mano es más racional de sostener que cualquier sofisticada premisa filosófica escéptica abstracta que concluya lo contrario, invirtiendo así la carga de la prueba [45, 46]."
    },
    # ---- 5 PREGUNTAS COMPLEMENTARIAS PARA COMPLETAR EL BANCO DE 30 ----
    {
        "id": "v_nudge_theory",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Medio",
        "passage": "La teoría del empujón (Nudge Theory), popularizada por Richard Thaler y Cass Sunstein, propone que intervenciones sutiles y no coactivas en la arquitectura de decisión pueden redirigir el comportamiento de las personas en direcciones deseables, sin prohibir ninguna opción ni alterar significativamente sus incentivos económicos [447fb7ab-0a38-4ba1-b5ee-304840837027.pdf]. Un empujón no es un mandato; colocar fruta a la altura de los ojos en una cafetería es un empujón, pero prohibir la comida chatarra no lo es.",
        "question": "De acuerdo con los autores de la teoría, ¿qué elemento caracteriza fundamentalmente a un 'empujón' lícito?",
        "options": [
            "A) La imposición de multas de bajo costo para desincentivar hábitos nocivos en la sociedad civil.",
            "B) La alteración del entorno de elección que respeta la libertad individual sin prohibir opciones ni usar coacción.",
            "C) El uso exclusivo de propaganda gubernamental explícita mediante los medios de comunicación.",
            "D) La reestructuración macroeconómica de los subsidios estatales para modificar precios de mercado."
        ],
        "correct": "B",
        "explanation": "El fragmento aclara de forma directa que un 'empujón' es un cambio sutil en la arquitectura de la elección que preserva la libertad de opción, lo cual excluye la coacción, prohibiciones o distorsiones de precios sustanciales [447fb7ab-0a38-4ba1-b5ee-304840837027.pdf]."
    },
    {
        "id": "v_mirror_neurons",
        "type": "verbal",
        "topic": "Ciencia y Tecnología",
        "difficulty": "Medio",
        "passage": "El descubrimiento de las neuronas espejo en la corteza premotora de primates revolucionó la neurociencia cognitiva al demostrar que las mismas células se activan tanto cuando un individuo realiza una acción motora dirigida a un objetivo como cuando observa a otro realizar esa misma acción [447fb7ab-0a38-4ba1-b5ee-304840837027.pdf]. Esto sugiere que el cerebro posee un sistema de simulación interna que permite mapear de manera directa las intenciones motoras y estados corporales ajenos sobre la propia representación neuronal, sentando las bases neurales de la empatía.",
        "question": "¿Cuál es la implicación principal de las neuronas espejo para la comprensión del comportamiento social según el texto?",
        "options": [
            "A) Demuestran que la empatía humana es un proceso puramente cultural que se aprende mediante condicionamiento clásico.",
            "B) Revelan la existencia de un mecanismo neural que simula internamente las acciones y estados de los demás para facilitar la comprensión social.",
            "C) Prueban que el cerebro humano es el único en la naturaleza capaz de planificar movimientos complejos y de precisión.",
            "D) Sugieren que la imitación ciega anula la capacidad crítica y creativa de los sistemas de inteligencia artificial."
        ],
        "correct": "B",
        "explanation": "La activación especular de estas neuronas en el espectador indica que el cerebro utiliza circuitos premotores idénticos para comprender las acciones del prójimo a nivel visceral y neural, facilitando la empatía de forma directa [447fb7ab-0a38-4ba1-b5ee-304840837027.pdf]."
    },
    {
        "id": "v_industrial_revolution",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Medio",
        "passage": "El debate historiográfico sobre la Revolución Industrial se centra en el nivel de vida de la clase trabajadora británica entre 1780 y 1840 [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. Los historiadores optimistas argumentan que el aumento del PIB per cápita y el descenso de los precios de bienes de consumo masivo demuestran un progreso material inequívoco [d28dd0c2-c8e1-4ad1-8204-6c014209f880.pdf]. En contraste, los pesimistas sostienen que métricas cualitativas y biológicas —como la reducción de la estatura promedio por desnutrición, la insalubridad urbana y las extenuantes jornadas infantiles— evidencian un alarmante deterioro en el bienestar humano general.",
        "question": "¿En qué difieren esencialmente las posturas optimistas y pesimistas respecto a la Revolución Industrial según el pasaje?",
        "options": [
            "A) En si los avances tecnológicos ocurrieron verdaderamente en Gran Bretaña o en la Europa continental.",
            "B) En el tipo de indicadores utilizados, priorizando unas el crecimiento económico agregado y otras el bienestar físico y cualitativo de la población.",
            "C) En el análisis de las causas de la mecanización textil, culpando unas al carbón y otras a las patentes.",
            "D) En decidir si la Revolución Industrial culminó antes o después del estallido de la Primera Guerra Mundial."
        ],
        "correct": "B",
        "explanation": "El texto explica que los optimistas se basan en el PIB y el consumo agregado (indicadores cuantitativos/económicos), mientras que los pesimistas se enfocan en la estatura, salubridad y trabajo infantil (indicadores cualitativos e higiénico-sociales) [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf, d28dd0c2-c8e1-4ad1-8204-6c014209f880.pdf]."
    },
    {
        "id": "v_metric_system",
        "type": "verbal",
        "topic": "Ciencia y Tecnología",
        "difficulty": "Sencillo",
        "passage": "La adopción del sistema métrico decimal por la Academia de Ciencias de Francia en 1795 no solo respondió a necesidades comerciales de estandarización, sino a un profundo ideal de la Ilustración: crear un sistema de pesos y medidas libre de arbitrariedades feudales y basado en la propia naturaleza [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. El metro se definió originalmente como la diezmillonésima parte de la distancia del ecuador al polo norte a lo largo del meridiano de París, garantizando que el patrón físico fuera 'para todos los pueblos, para todos los tiempos'.",
        "question": "De acuerdo con el fragmento, ¿cuál fue uno de los ideales fundamentales detrás del desarrollo del sistema métrico decimal?",
        "options": [
            "A) Facilitar la recaudación de impuestos de manera feudal en beneficio exclusivo de la corona francesa.",
            "B) Diseñar un patrón de medida de origen natural y universal que eliminara las disparidades e imposiciones arbitrarias feudales.",
            "C) Demostrar la superioridad absoluta de los científicos parisinos sobre los astrofísicos británicos.",
            "D) Impedir que las colonias francesas realizaran transacciones comerciales con monedas de metales pesados."
        ],
        "correct": "B",
        "explanation": "El texto expone que la Academia de Ciencias buscaba un sistema libre de las arbitrariedades del antiguo régimen feudal, fundamentando las unidades de medida en dimensiones físicas de la Tierra para dotarlas de validez universal [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]."
    },
    {
        "id": "v_warrington_bombings",
        "type": "verbal",
        "topic": "Economía y Sociedad",
        "difficulty": "Medio",
        "passage": "Los trágicos bombardeos del IRA en Warrington en 1993, que costaron la vida a dos niños pequeños, desataron un clamor popular masivo que catalizó el nacimiento de movimientos de paz fundamentales en el Reino Unido e Irlanda [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]. La conmoción social impulsó la creación de fundaciones dedicadas a la reconciliación y el entendimiento intercultural entre comunidades católicas y protestantes, demostrando que el dolor comunitario puede convertirse en un motor constructivo para la diplomacia ciudadana y la paz duradera.",
        "question": "Según el pasaje, ¿qué impacto social constructivo surgió directamente tras los sucesos de Warrington en 1993?",
        "options": [
            "A) La aprobación de medidas penales restrictivas severas en todos los aeropuertos internacionales.",
            "B) El nacimiento de movimientos de paz populares y fundaciones dedicadas a la reconciliación comunitaria y el entendimiento intercultural.",
            "C) La disolución pacífica e instantánea de todas las células militantes de Europa del Norte.",
            "D) Una reforma constitucional radical en el Parlamento de Londres que eliminó la división de condados."
        ],
        "correct": "B",
        "explanation": "El texto describe que la tragedia motivó una respuesta constructiva de la sociedad civil, la cual creó fundaciones para la paz y el acercamiento social entre comunidades tradicionalmente enfrentadas [dc178c12-a0ec-4973-a0eb-5e21ab074340.pdf]."
    }
]


# ==========================================
# 2. GENERADORES PROCEDURALES DE RAZONAMIENTO NUMÉRICO (GROUNDED)
# ==========================================

def generate_numerical_patents():
    countries_data = [
        {"name": "Finlandia", "pop": 5244, "rates": [264.0, 247.1, 248.6, 250.8]},
        {"name": "Alemania", "pop": 82409, "rates": [276.2, 283.7, 283.6, 290.7]},
        {"name": "Suecia", "pop": 9066, "rates": [246.2, 260.1, 280.0, 298.4]},
        {"name": "Suiza", "pop": 7441, "rates": [408.4, 417.5, 415.5, 429.3]},
        {"name": "Polonia", "pop": 37972, "rates": [120.0, 131.0, 138.5, 145.2]},
        {"name": "Bélgica", "pop": 10400, "rates": [140.2, 145.5, 150.3, 158.0]},
    ]
    
    c1, c2 = random.sample(countries_data, 2)
    if c1["rates"][1] > c2["rates"][1]:
        c1, c2 = c2, c1
        
    pop_c1 = c1["pop"]
    rate_c1 = c1["rates"][1]
    rate_c2 = c2["rates"][1]
    
    diff_rate = rate_c2 - rate_c1
    extra_needed = round((pop_c1 / 1000.0) * diff_rate)
    
    table = f"""
| País | Población 2005 (miles) | Patentes / Millón (2004) | Patentes / Millón (2005) |
| :--- | :---: | :---: | :---: |
| **{c1['name']}** | {c1['pop']:,} | {c1['rates'][0]:.1f} | {c1['rates'][1]:.1f} |
| **{c2['name']}** | {c2['pop']:,} | {c2['rates'][0]:.1f} | {c2['rates'][1]:.1f} |
"""

    question = f"Con base en la tabla de patentes de tus boletines [8c7f2974-c0d2-432b-a7f0-db4223a0dcef.pdf], ¿cuántas patentes más tendría que haber presentado **{c1['name']}** en 2005 para igualar a **{c2['name']}** en solicitudes per cápita?"
    
    correct_val = extra_needed
    options_vals = [correct_val]
    
    # Distractors
    dist1 = round((c2["pop"] / 1000.0) * diff_rate)
    if dist1 == correct_val:
        dist1 = correct_val + random.choice([15, -15, 25])
    dist2 = round((pop_c1 / 1000.0) * (c2["rates"][0] - c1["rates"][0]))
    if dist2 == correct_val or dist2 <= 0:
        dist2 = correct_val + random.choice([40, -40, 50])
    dist3 = round(pop_c1 * (diff_rate / 100.0))
    if dist3 == correct_val or dist3 <= 0:
        dist3 = correct_val + random.choice([70, -70, 85])
    dist4 = correct_val + random.choice([12, -12, 18, -18])
    if dist4 <= 0:
        dist4 = correct_val + 30
        
    for val in [dist1, dist2, dist3, dist4]:
        if val not in options_vals and len(options_vals) < 5:
            options_vals.append(val)
            
    while len(options_vals) < 5:
        alt = correct_val + random.randint(-50, 50)
        if alt not in options_vals and alt > 0:
            options_vals.append(alt)
            
    random.shuffle(options_vals)
    
    letters = ["A", "B", "C", "D", "E"]
    correct_letter = letters[options_vals.index(correct_val)]
    options = [f"{letters[i]}) {options_vals[i]} patentes" for i in range(5)]
    
    explanation = f"""
**Solución paso a paso:**
1. **Calcular la diferencia en tasas per cápita:** Restamos la tasa de solicitudes per cápita de {c2['name']} menos la de {c1['name']} en 2005:
   $$\\text{{Diferencia}} = {rate_c2:.1f} - {rate_c1:.1f} = {diff_rate:.1f} \\text{{ patentes por millón de habitantes}}$$
2. **Aplicar la diferencia a la población:** Dado que la población de {c1['name']} es de {pop_c1:,} miles (es decir, {pop_c1/1000:.3f} millones de habitantes), multiplicamos este valor por la diferencia de tasas:
   $$\\text{{Patentes adicionales}} = \\frac{{{pop_c1}}}{{1000}} \\times {diff_rate:.1f} = {pop_c1/1000:.3f} \\times {diff_rate:.1f} \\approx {extra_needed:,} \\text{{ patentes}}$$
   
La respuesta correcta es la opción **{correct_letter}** [8c7f2974-c0d2-432b-a7f0-db4223a0dcef.pdf].
"""
    return {
        "id": f"num_pat_{random.randint(1000, 9999)}",
        "type": "numerical",
        "difficulty": "Medio",
        "table": table,
        "question": question,
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }

def generate_numerical_palace():
    rev_monday = random.randint(4, 8) * 1000000 # 4M to 8M
    vis_monday = random.choice([40000, 50000, 60000])
    vis_friday = random.choice([25000, 30000, 45000])
    k = random.choice([2, 3, 4]) # Monday revenue is k times Friday's
    
    rev_friday = rev_monday / k
    price_monday = rev_monday / vis_monday
    price_friday = rev_friday / vis_friday
    ratio = price_monday / price_friday
    
    table = f"""
**Reporte de taquilla del Palacio Real de Madrid:**
- **Ingresos Totales del Lunes:** {rev_monday:,} €
- **Visitantes el Lunes:** {vis_monday:,} personas (mismo volumen registrado el sábado)
- **Visitantes el Viernes:** {vis_friday:,} personas
- **Relación de Ingresos:** Los ingresos del lunes fueron exactamente {k} veces superiores a los del viernes.
"""

    question = f"Utilizando las plantillas de ingresos institucionales de tus boletines [8c7f2974-c0d2-432b-a7f0-db4223a0dcef.pdf], ¿cuál es la relación (ratio) entre el precio medio de la entrada cobrada el lunes y el precio medio de la entrada del viernes?"
    
    correct_val = round(ratio, 2)
    options_vals = [correct_val]
    
    # Generate realistic distractors
    dist1 = round(k * (vis_monday / vis_friday), 2) # Inverse visitors ratio
    dist2 = round(vis_monday / vis_friday, 2) # Pure visitors ratio
    dist3 = round(float(k), 2) # Pure revenue ratio
    dist4 = round(ratio * 0.8, 2)
    
    for val in [dist1, dist2, dist3, dist4]:
        if val not in options_vals and len(options_vals) < 5:
            options_vals.append(val)
            
    while len(options_vals) < 5:
        alt = round(correct_val + random.choice([0.5, -0.5, 1.2, -0.8]), 2)
        if alt not in options_vals and alt > 0:
            options_vals.append(alt)
            
    random.shuffle(options_vals)
    
    letters = ["A", "B", "C", "D", "E"]
    correct_letter = letters[options_vals.index(correct_val)]
    options = [f"{letters[i]}) Ratio {options_vals[i]:.2f}" for i in range(5)]
    
    explanation = f"""
**Solución paso a paso:**
1. **Calcular el precio medio de la entrada el lunes:**
   $$\\text{{Precio Lunes}} = \\frac{{\\text{{Ingresos Lunes}}}}{{\\text{{Visitantes Lunes}}}} = \\frac{{{rev_monday:,} \\text{{ €}}}}{{{vis_monday:,}}} = {price_monday:.2f} \\text{{ € por entrada}}$$
2. **Calcular los ingresos totales del viernes:** Como los ingresos del lunes fueron {k} veces superiores:
   $$\\text{{Ingresos Viernes}} = \\frac{{{rev_monday:,}}}{{{k}}} = {rev_friday:,} \\text{{ €}}$$
3. **Calcular el precio medio de la entrada el viernes:**
   $$\\text{{Precio Viernes}} = \\frac{{{rev_friday:,} \\text{{ €}}}}{{{vis_friday:,}}} = {price_friday:.2f} \\text{{ € por entrada}}$$
4. **Calcular el ratio entre ambos precios (Lunes / Viernes):**
   $$\\text{{Ratio}} = \\frac{{{price_monday:.2f}}}{{{price_friday:.2f}}} = {ratio:.2f}$$
   
La respuesta correcta es la opción **{correct_letter}** [8c7f2974-c0d2-432b-a7f0-db4223a0dcef.pdf].
"""
    return {
        "id": f"num_pal_{random.randint(1000, 9999)}",
        "type": "numerical",
        "difficulty": "Avanzado",
        "table": table,
        "question": question,
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }

def generate_numerical_rd():
    countries = [
        {"name": "Alemania", "gdp": 4100, "rd_pct": 3.15, "pop": 84.0, "researchers": 530},
        {"name": "Francia", "gdp": 2850, "rd_pct": 2.25, "pop": 66.0, "researchers": 320},
        {"name": "Suecia", "gdp": 650, "rd_pct": 3.40, "pop": 10.5, "researchers": 105},
        {"name": "Irlanda", "gdp": 500, "rd_pct": 1.30, "pop": 5.2, "researchers": 35},
        {"name": "Polonia", "gdp": 700, "rd_pct": 0.80, "pop": 37.5, "researchers": 110}
    ]
    
    c = random.choice(countries)
    gdp = c["gdp"]
    rd_pct = c["rd_pct"]
    pop = c["pop"]
    res = c["researchers"]
    
    q_type = random.choice(["spend", "res_ratio"])
    
    table = f"""
| País | PIB (mil millones €) | Gasto I+D (% del PIB) | Población (millones) | Investigadores (miles) |
| :--- | :---: | :---: | :---: | :---: |
| **Alemania** | 4,100 | 3.15% | 84.0 | 530 |
| **Francia** | 2,850 | 2.25% | 66.0 | 320 |
| **Suecia** | 650 | 3.40% | 10.5 | 105 |
| **Irlanda** | 500 | 1.30% | 5.2 | 35 |
| **Polonia** | 700 | 0.80% | 37.5 | 110 |
"""

    if q_type == "spend":
        # Calculate total spending in millions
        total_spend = gdp * (rd_pct / 100.0) * 1000.0 # to millions
        correct_val = round(total_spend, 1)
        
        question = f"Utilizando la tabla de inversión en I+D [e876cdeb-2597-4b3d-91c0-ac325b548f54.pdf], ¿cuál fue el gasto total de **{c['name']}** en investigación y desarrollo (I+D) expresado en **millones de euros**?"
        
        options_vals = [correct_val]
        dist1 = round(gdp * rd_pct, 1) # simple multiplication
        dist2 = round(total_spend * 1.15, 1)
        dist3 = round(total_spend * 0.85, 1)
        dist4 = round(total_spend + 150, 1)
        
        for val in [dist1, dist2, dist3, dist4]:
            if val not in options_vals and len(options_vals) < 5:
                options_vals.append(val)
                
        while len(options_vals) < 5:
            alt = round(correct_val + random.randint(-200, 200), 1)
            if alt not in options_vals and alt > 0:
                options_vals.append(alt)
                
        random.shuffle(options_vals)
        letters = ["A", "B", "C", "D", "E"]
        correct_letter = letters[options_vals.index(correct_val)]
        options = [f"{letters[i]}) {options_vals[i]:,} millones €" for i in range(5)]
        
        explanation = f"""
**Solución paso a paso:**
1. **Identificar las variables del país {c['name']}:** El PIB es de {gdp:,} mil millones de euros y el gasto en I+D representa el {rd_pct:.2f}% de dicho PIB.
2. **Aplicar el porcentaje:** Multiplicamos el PIB por el porcentaje de gasto en I+D para obtener el total en miles de millones de euros:
   $$\\text{{Gasto en miles de millones}} = {gdp:,} \\times \\frac{{{rd_pct:.2f}}}{{100}} = {gdp * (rd_pct/100.0):.4f} \\text{{ mil millones de €}}$$
3. **Convertir a millones de euros:** Multiplicamos el resultado por 1,000 para pasar de mil millones a millones:
   $$\\text{{Gasto en millones}} = {gdp * (rd_pct/100.0):.4f} \\times 1000 = {correct_val:,} \\text{{ millones de €}}$$

La respuesta correcta es la opción **{correct_letter}** [e876cdeb-2597-4b3d-91c0-ac325b548f54.pdf].
"""
    else:
        # Calculate researchers per million inhabitants
        ratio_res = (res / pop) * 1000.0 # thousands res / millions pop = count per inhabitant * 1000 = per million
        # Wait, res is in thousands, pop is in millions.
        # res * 1000 is total researchers. pop * 1,000,000 is total population.
        # (res * 1000) / (pop * 1,000,000) = res / (pop * 1000) researchers per inhabitant.
        # Per million: (res / (pop * 1000)) * 1,000,000 = res * 1000 / pop.
        # E.g. Germany: 530,000 researchers / 84 million pop = 6309.5 per million inhabitants.
        # Let's verify this. Yes!
        correct_val = round(res * 1000.0 / pop, 1)
        
        question = f"Con base en la tabla de investigadores de tus boletines [e876cdeb-2597-4b3d-91c0-ac325b548f54.pdf], ¿cuántos **investigadores por millón de habitantes** tenía **{c['name']}** en 2024?"
        
        options_vals = [correct_val]
        dist1 = round(res / pop, 1) # forgot scale
        dist2 = round((res * 1000.0 / pop) * 1.12, 1) # 12% higher (confusing with another question)
        dist3 = round((res * 1000.0 / pop) * 0.9, 1)
        dist4 = round(correct_val + 500, 1)
        
        for val in [dist1, dist2, dist3, dist4]:
            if val not in options_vals and len(options_vals) < 5:
                options_vals.append(val)
                
        while len(options_vals) < 5:
            alt = round(correct_val + random.randint(-1000, 1000), 1)
            if alt not in options_vals and alt > 0:
                options_vals.append(alt)
                
        random.shuffle(options_vals)
        letters = ["A", "B", "C", "D", "E"]
        correct_letter = letters[options_vals.index(correct_val)]
        options = [f"{letters[i]}) {options_vals[i]:,} investigadores/millón" for i in range(5)]
        
        explanation = f"""
**Solución paso a paso:**
1. **Identificar las variables de {c['name']}:** El número total de investigadores es de {res:,} miles (es decir, {res*1000:,} personas) y la población total es de {pop:.1f} millones de personas.
2. **Dividir investigadores totales entre población (en millones):**
   $$\\text{{Ratio por millón de habitantes}} = \\frac{{\\text{{Investigadores (en miles)}} \\times 1000}}{{\\text{{Población (en millones)}}}} = \\frac{{{res:,} \\times 1000}}{{{pop:.1f}}} \\approx {correct_val:,} \\text{{ investigadores}}$$

La respuesta correcta es la opción **{correct_letter}** [e876cdeb-2597-4b3d-91c0-ac325b548f54.pdf].
"""

    return {
        "id": f"num_rd_{random.randint(1000, 9999)}",
        "type": "numerical",
        "difficulty": "Sencillo",
        "table": table,
        "question": question,
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }


# ==========================================
# 3. GENERADORES PROCEDURALES DE RAZONAMIENTO ABSTRACTO (SVG RESPONSIVE)
# ==========================================

def generate_abstract_rotation():
    shape_type = random.choice(["triangle", "L-shape", "arrow"])
    shape_step = random.choice([90, -90, 180])
    dot_step = random.choice([45, -45, 90, -90])
    
    shape_start_angle = random.choice([0, 90, 180, 270])
    dot_start_angle = random.choice([0, 45, 90, 135, 180, 225, 270, 315])
    
    states = []
    for i in range(5):
        shape_angle = (shape_start_angle + i * shape_step) % 360
        dot_angle = (dot_start_angle + i * dot_step) % 360
        states.append((shape_angle, dot_angle))
        
    def get_shape_path(stype):
        if stype == "triangle":
            return '<polygon points="0,-22 22,18 -22,18" fill="#F3F4F6" stroke="#1F2937" stroke-width="2.5"/>'
        elif stype == "L-shape":
            return '<path d="M -12,-20 L 12,-20 L 12,-8 L -3,-8 L -3,20 L -12,20 Z" fill="#F3F4F6" stroke="#1F2937" stroke-width="2.5"/>'
        else:
            return '<path d="M -8,-20 L 8,-20 L 8,-4 L 16,-4 L 0,16 L -16,-4 L -8,-4 Z" fill="#F3F4F6" stroke="#1F2937" stroke-width="2.5"/>'
            
    # Generate sequence of 4 frames side-by-side (fits mobile perfectly at 450px)
    seq_svg = f"""
    <svg width="100%" height="110" viewBox="0 0 450 110" style="background:#F9FAFB; border-radius:12px; border:1px solid #E5E7EB; display:block; margin:auto;">
    """
    for i in range(4):
        x_offset = i * 110 + 10
        shape_a, dot_a = states[i]
        seq_svg += f"""
        <g transform="translate({x_offset}, 5)">
            <rect x="0" y="0" width="90" height="90" rx="10" fill="white" stroke="#D1D5DB" stroke-width="1.5"/>
            <g transform="translate(45, 45)">
                <g transform="rotate({shape_a})">
                    {get_shape_path(shape_type)}
                </g>
                """
        rad = math.radians(dot_a)
        r = 28
        dot_x = r * math.cos(rad)
        dot_y = r * math.sin(rad)
        seq_svg += f"""
                <circle cx="{dot_x:.1f}" cy="{dot_y:.1f}" r="6.5" fill="#EF4444" stroke="#1F2937" stroke-width="1.5"/>
            </g>
            <text x="45" y="85" text-anchor="middle" font-size="9" font-weight="bold" fill="#9CA3AF">Paso {i+1}</text>
        </g>
        """
        if i < 3:
            arrow_x = x_offset + 95
            seq_svg += f"""
            <path d="M {arrow_x} 50 L {arrow_x+10} 50 M {arrow_x+6} 45 L {arrow_x+10} 50 L {arrow_x+6} 55" stroke="#9CA3AF" stroke-width="2" fill="none"/>
            """
    seq_svg += "</svg>"
    
    correct_shape_a, correct_dot_a = states[4]
    letters = ["A", "B", "C", "D", "E"]
    correct_letter = random.choice(letters)
    
    options = []
    options_svgs = {}
    
    used_combinations = [(correct_shape_a, correct_dot_a)]
    
    for letter in letters:
        if letter == correct_letter:
            opt_shape_a, opt_dot_a = correct_shape_a, correct_dot_a
        else:
            while True:
                opt_shape_a = (correct_shape_a + random.choice([0, 90, 180, 270])) % 360
                opt_dot_a = (correct_dot_a + random.choice([0, 45, 90, 135, 180, 225, 270, 315])) % 360
                if (opt_shape_a, opt_dot_a) not in used_combinations:
                    used_combinations.append((opt_shape_a, opt_dot_a))
                    break
            
        opt_svg = f"""
        <svg width="100%" height="80" viewBox="0 0 100 100" style="background:white; border-radius:10px; border:1.5px solid #D1D5DB; display:block; margin:auto;">
            <g transform="translate(50, 50)">
                <g transform="rotate({opt_shape_a})">
                    {get_shape_path(shape_type)}
                </g>
                """
        rad = math.radians(opt_dot_a)
        r = 28
        dot_x = r * math.cos(rad)
        dot_y = r * math.sin(rad)
        opt_svg += f"""
                <circle cx="{dot_x:.1f}" cy="{dot_y:.1f}" r="6.5" fill="#EF4444" stroke="#1F2937" stroke-width="1.5"/>
            </g>
        </svg>
        """
        options_svgs[letter] = opt_svg
        options.append(f"{letter}) Ver opción visual {letter}")
        
    shape_dir = "sentido horario" if shape_step > 0 else "sentido antihorario"
    if abs(shape_step) == 180:
        shape_dir = "rotación media (180º)"
    dot_dir = "sentido horario" if dot_step > 0 else "sentido antihorario"
    
    explanation = f"""
**Explicación geométrica:**
1. **Regla de Rotación del Objeto Central:** El *{shape_type}* del centro gira progresivamente **{abs(shape_step)}º en {shape_dir}** de un cuadro al siguiente [91944973-3db5-4bad-ba1c-7257356376e9.pdf].
2. **Regla del Punto Rojo:** El círculo rojo de control gira circularmente **{abs(dot_step)}º en {dot_dir}** en cada paso de la serie [8111d114-a22e-478d-95ca-842d3286d732.pdf].

Calculando la transición del Paso 4 al **Paso 5**:
- Rotación del objeto: `({states[3][0]}º + {shape_step}º) % 360 = {correct_shape_a}º`.
- Posición del punto rojo: `({states[3][1]}º + {dot_step}º) % 360 = {correct_dot_a}º`.

La única opción geométrica idéntica a este estado calculado es la **{correct_letter}** [91944973-3db5-4bad-ba1c-7257356376e9.pdf].
"""
    return {
        "id": f"abs_rot_{random.randint(1000, 9999)}",
        "type": "abstract",
        "difficulty": "Medio",
        "svg": seq_svg,
        "options_svgs": options_svgs,
        "question": "¿Qué figura geométrica sigue la secuencia lógica para ocupar la posición 5 (Paso 5)? Analiza las opciones visuales inferiores.",
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }

def generate_abstract_superposition():
    def get_rand_cell():
        while True:
            cell = [random.choice([0, 1]) for _ in range(4)]
            if 0 < sum(cell) < 4:
                return cell
                
    r1c1 = get_rand_cell()
    r1c2 = get_rand_cell()
    r1c3 = [r1c1[i] ^ r1c2[i] for i in range(4)]
    
    r2c1 = get_rand_cell()
    r2c2 = get_rand_cell()
    r2c3 = [r2c1[i] ^ r2c2[i] for i in range(4)]
    
    r3c1 = get_rand_cell()
    r3c2 = get_rand_cell()
    r3c3 = [r3c1[i] ^ r3c2[i] for i in range(4)]
    
    # Ensure answer is interesting
    if sum(r3c3) == 0 or sum(r3c3) == 4 or r3c3 == r3c1 or r3c3 == r3c2:
        return generate_abstract_superposition()
        
    def draw_cell_svg_g(cell, x_offset, y_offset, cell_size=50):
        g = f'<g transform="translate({x_offset}, {y_offset})">'
        g += f'<rect x="0" y="0" width="{cell_size}" height="{cell_size}" rx="6" fill="white" stroke="#9CA3AF" stroke-width="1.5"/>'
        sub_size = cell_size / 2 - 4
        positions = [
            (2, 2),
            (cell_size/2 + 2, 2),
            (2, cell_size/2 + 2),
            (cell_size/2 + 2, cell_size/2 + 2)
        ]
        for idx, (px, py) in enumerate(positions):
            if cell[idx] == 1:
                g += f'<rect x="{px}" y="{py}" width="{sub_size}" height="{sub_size}" rx="3" fill="#111827"/>'
        g += '</g>'
        return g

    matrix_svg = f"""
    <svg width="100%" height="200" viewBox="0 0 260 200" style="background:#F9FAFB; border-radius:12px; border:1px solid #E5E7EB; display:block; margin:auto;">
        <!-- Fila 1 -->
        {draw_cell_svg_g(r1c1, 10, 10)}
        <text x="70" y="40" text-anchor="middle" font-size="16" font-weight="bold" fill="#9CA3AF">+</text>
        {draw_cell_svg_g(r1c2, 80, 10)}
        <text x="140" y="40" text-anchor="middle" font-size="16" font-weight="bold" fill="#9CA3AF">=</text>
        {draw_cell_svg_g(r1c3, 150, 10)}
        
        <!-- Fila 2 -->
        {draw_cell_svg_g(r2c1, 10, 70)}
        <text x="70" y="100" text-anchor="middle" font-size="16" font-weight="bold" fill="#9CA3AF">+</text>
        {draw_cell_svg_g(r2c2, 80, 70)}
        <text x="140" y="100" text-anchor="middle" font-size="16" font-weight="bold" fill="#9CA3AF">=</text>
        {draw_cell_svg_g(r2c3, 150, 70)}
        
        <!-- Fila 3 -->
        {draw_cell_svg_g(r3c1, 10, 130)}
        <text x="70" y="160" text-anchor="middle" font-size="16" font-weight="bold" fill="#9CA3AF">+</text>
        {draw_cell_svg_g(r3c2, 80, 130)}
        <text x="140" y="160" text-anchor="middle" font-size="16" font-weight="bold" fill="#9CA3AF">=</text>
        
        <!-- Incógnita visual -->
        <g transform="translate(150, 130)">
            <rect x="0" y="0" width="50" height="50" rx="6" fill="#FEE2E2" stroke="#EF4444" stroke-width="2"/>
            <text x="25" y="32" text-anchor="middle" font-size="24" font-weight="bold" fill="#EF4444">?</text>
        </g>
    </svg>
    """
    
    letters = ["A", "B", "C", "D", "E"]
    correct_letter = random.choice(letters)
    
    options = []
    options_svgs = {}
    
    used_cells = [r3c3]
    for letter in letters:
        if letter == correct_letter:
            opt_cell = r3c3
        else:
            while True:
                dist = [random.choice([0, 1]) for _ in range(4)]
                if dist not in used_cells and 0 < sum(dist) < 4:
                    opt_cell = dist
                    used_cells.append(dist)
                    break
                    
        opt_svg = f"""
        <svg width="100%" height="80" viewBox="0 0 80 80" style="background:white; border-radius:10px; border:1.5px solid #D1D5DB; display:block; margin:auto;">
            {draw_cell_svg_g(opt_cell, 15, 15, cell_size=50)}
        </svg>
        """
        options_svgs[letter] = opt_svg
        options.append(f"{letter}) Ver opción visual {letter}")
        
    explanation = f"""
**Análisis Lógico de la Matriz de Superposición:**
Las figuras de cada fila siguen una regla matemática espacial estricta de superposición binaria [8111d114-a22e-478d-95ca-842d3286d732.pdf]:
- **Lógica de Fusión:** `Columna 1` y `Columna 2` se superponen para formar la `Columna 3`.
- **Regla de Cancelación (XOR):** Cuando un cuadrante negro coincide exactamente en la misma posición en ambas columnas iniciales, **se cancela de forma inmediata (se suprime)** en la tercera [8111d114-a22e-478d-95ca-842d3286d732.pdf, passage 71, 72]. Solo se mantienen los cuadrantes que están negros en un único lado de la suma.

Analizando detenidamente la tercera fila:
- Cuadrantes en Columna 1: {r3c1} (1 es relleno, 0 es vacío).
- Cuadrantes en Columna 2: {r3c2}.
- Aplicando XOR a cada cuadrante: `{r3c1} ^ {r3c2} = {r3c3}`.

La opción que reproduce con exactitud este patrón de cuadrantes es la **{correct_letter}** [8111d114-a22e-478d-95ca-842d3286d732.pdf].
"""
    return {
        "id": f"abs_sup_{random.randint(1000, 9999)}",
        "type": "abstract",
        "difficulty": "Avanzado",
        "svg": matrix_svg,
        "options_svgs": options_svgs,
        "question": "¿Qué figura completa la matriz lógica horizontal de la tercera fila de manera congruente?",
        "options": options,
        "correct": correct_letter,
        "explanation": explanation
    }


# ==========================================
# 4. GESTIÓN DEL ESTADO DE SESIÓN Y PERSISTENCIA (SOPORTE ADAPTATIVO)
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

# Inicializar sesión
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

# ==========================================
# 5. MOTOR ADAPTATIVO DE GENERACIÓN DE EXÁMENES
# ==========================================

def start_new_test(category):
    st.session_state.current_test = category
    st.session_state.current_index = 0
    st.session_state.answers = {}
    st.session_state.show_explanation = False
    st.session_state.selected_option = None
    
    # 1. Determinar longitud del test según la configuración actual
    length_setting = st.session_state.get("config_length", "Estándar")
    if category == "verbal":
        test_length = 10 if length_setting == "Rápido" else (30 if length_setting == "Extendido" else 20)
    else:
        test_length = 5 if length_setting == "Rápido" else (15 if length_setting == "Extendido" else 10)
        
    # 2. Cargar perfil y configuración de dificultad
    profile = st.session_state.profile
    mode_setting = st.session_state.get("config_mode", "Adaptativo")
    
    if mode_setting == "Adaptativo":
        user_diff = profile[category]["difficulty"]
    else:
        user_diff = st.session_state.get("config_diff", "Mezclado")
        
    # 3. Recuperar preguntas falladas de esta categoría para repetición espaciada (Spaced Repetition)
    failed_pool = [q for q in profile["failed_questions"] if q["type"] == category]
    
    test_questions = []
    
    # Insertar algunas preguntas que haya fallado antes
    num_review = min(len(failed_pool), max(1, test_length // 4))
    if num_review > 0:
        sampled_failed = random.sample(failed_pool, num_review)
        for q in sampled_failed:
            q_copy = q.copy()
            q_copy["is_review"] = True
            test_questions.append(q_copy)
            
    needed = test_length - len(test_questions)
    
    if category == "verbal":
        # Aplicar filtro de tema si existe
        topic_setting = st.session_state.get("config_topic", "Todos")
        if topic_setting == "Todos":
            topic_pool = VERBAL_BANK
        else:
            topic_pool = [q for q in VERBAL_BANK if q.get("topic") == topic_setting]
            if not topic_pool: # fallback
                topic_pool = VERBAL_BANK
                
        # Filtrar por dificultad
        if user_diff == "Mezclado":
            bank_pool = topic_pool
        else:
            bank_pool = [q for q in topic_pool if q["difficulty"] == user_diff]
            if len(bank_pool) < needed:
                other_diffs = [q for q in topic_pool if q["difficulty"] != user_diff]
                bank_pool += other_diffs
                
        # Evitar duplicar las que ya pusimos de repaso
        existing_ids = {q["id"] for q in test_questions}
        available_pool = [q for q in bank_pool if q["id"] not in existing_ids]
        
        if len(available_pool) < needed:
            available_pool = bank_pool
            
        selected_verbal = random.sample(available_pool, min(len(available_pool), needed))
        test_questions.extend(selected_verbal)
        
    elif category == "numerical":
        # Generar preguntas numéricas dinámicamente con plantillas
        for _ in range(needed):
            generator = random.choice([generate_numerical_patents, generate_numerical_palace, generate_numerical_rd])
            q = generator()
            if user_diff != "Mezclado":
                q["difficulty"] = user_diff
            test_questions.append(q)
            
    elif category == "abstract":
        # Generar secuencias de razonamiento abstracto dinámicas con SVG responsive
        for _ in range(needed):
            generator = random.choice([generate_abstract_rotation, generate_abstract_superposition])
            q = generator()
            if user_diff != "Mezclado":
                q["difficulty"] = user_diff
            test_questions.append(q)
            
    # Mezclar todo para equilibrar el repaso
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
            # Remover de la cola de falladas (Concepto superado)
            profile["failed_questions"] = [fq for fq in profile["failed_questions"] if fq["id"] != q["id"]]
        else:
            if not any(fq["id"] == q["id"] for fq in profile["failed_questions"]):
                profile["failed_questions"].append({
                    "id": q["id"],
                    "type": q["type"],
                    "difficulty": q["difficulty"],
                    "passage": q.get("passage", ""),
                    "table": q.get("table", ""),
                    "svg": q.get("svg", ""),
                    "options_svgs": q.get("options_svgs", {}),
                    "question": q["question"],
                    "options": q["options"],
                    "correct": q["correct"],
                    "explanation": q["explanation"]
                })
                
    profile[category]["completed"] += 1
    profile[category]["correct_total"] += correct_count
    
    # Calcular porcentaje histórico real
    test_len = len(questions)
    total_completed_questions = profile[category]["completed"] * test_len
    profile[category]["accuracy"] = round((profile[category]["correct_total"] / total_completed_questions) * 100, 1)
    
    # Ajuste Adaptativo de Dificultad (solo opera si el modo es Adaptativo)
    mode_setting = st.session_state.get("config_mode", "Adaptativo")
    if mode_setting == "Adaptativo":
        pct_correct = (correct_count / test_len) * 100
        current_diff = profile[category]["difficulty"]
        
        if pct_correct >= 80:
            if current_diff == "Sencillo":
                profile[category]["difficulty"] = "Medio"
            elif current_diff == "Medio":
                profile[category]["difficulty"] = "Avanzado"
        elif pct_correct < 50:
            if current_diff == "Avanzado":
                profile[category]["difficulty"] = "Medio"
            elif current_diff == "Medio":
                profile[category]["difficulty"] = "Sencillo"
                
    st.session_state.profile = profile
    save_progress(profile)
    st.session_state.review_mode = True


# ==========================================
# 6. VISTAS DE LA INTERFAZ DE USUARIO (TABS)
# ==========================================

# CABECERA PRINCIPAL DE LA APP
st.title("🧠 Simulador de Examen Adaptativo")
st.caption("Estructurado con Razonamiento Verbal (4 opciones), Numérico y Abstracto (5 opciones)")

# Pestañas en el menú principal para ampliar opciones
tab_main, tab_stats, tab_rules = st.tabs(["🚀 Practicar Examen", "📈 Ver Rendimiento", "📘 Tarjetas de Reglas"])

with tab_stats:
    st.subheader("Análisis Detallado de tu Progreso")
    profile = st.session_state.profile
    
    col_v, col_n, col_a = st.columns(3)
    with col_v:
        st.metric("Acierto Verbal", f"{profile['verbal']['accuracy']}%", help="Porcentaje de respuestas correctas en Verbal")
        st.caption(f"Nivel Adaptativo: **{profile['verbal']['difficulty']}**")
    with col_n:
        st.metric("Acierto Numérico", f"{profile['numerical']['accuracy']}%", help="Porcentaje de respuestas correctas en Numérico")
        st.caption(f"Nivel Adaptativo: **{profile['numerical']['difficulty']}**")
    with col_a:
        st.metric("Acierto Abstracto", f"{profile['abstract']['accuracy']}%", help="Porcentaje de respuestas correctas en Abstracto")
        st.caption(f"Nivel Adaptativo: **{profile['abstract']['difficulty']}**")
        
    st.markdown("---")
    st.markdown("### Cola de Repaso (Spaced Repetition)")
    failed_count = len(profile["failed_questions"])
    if failed_count > 0:
        st.warning(f"Tienes **{failed_count} ejercicios fallados** que el simulador priorizará en tus siguientes sesiones.")
        with st.expander("Ver tipos de preguntas acumuladas en la cola de repaso"):
            v_fails = sum(1 for f in profile["failed_questions"] if f["type"] == "verbal")
            n_fails = sum(1 for f in profile["failed_questions"] if f["type"] == "numerical")
            a_fails = sum(1 for f in profile["failed_questions"] if f["type"] == "abstract")
            st.write(f"- 💬 **Comprensión Verbal:** {v_fails} preguntas")
            st.write(f"- 📊 **Razonamiento Numérico:** {n_fails} preguntas")
            st.write(f"- 🧩 **Secuencias Abstractas:** {a_fails} preguntas")
    else:
        st.success("🎉 ¡Excelente! No tienes conceptos pendientes de reforzar.")
        
    if st.button("🧹 Resetear Todo el Progreso (Limpiar Historial)"):
        st.session_state.profile = {
            "verbal": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
            "numerical": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
            "abstract": {"accuracy": 0.0, "difficulty": "Sencillo", "streak": 0, "completed": 0, "correct_total": 0},
            "failed_questions": []
        }
        save_progress(st.session_state.profile)
        st.success("Historial completamente reseteado.")
        st.rerun()

with tab_rules:
    st.subheader("📘 Guía de Conceptos Clave para el Examen")
    st.markdown("Repasa estas lógicas y reglas de resolución extraídas directamente de tus boletines oficiales de examen:")
    
    st.markdown('<div class="rule-card"><strong>💬 Razonamiento Verbal:</strong> Lee atentamente buscando enunciados sustentados estrictamente por el texto. No asumas ni generalices premisas que no figuren textualmente [073fc2cb-1d2d-4809-bf9e-1845f15c00b9.pdf].</div>', unsafe_allow_html=True)
    st.markdown('<div class="rule-card"><strong>📊 Razonamiento Numérico:</strong> Identifica rápidamente las variables en las tablas. Presta atención al cálculo per cápita (siempre divide el valor de la población entre 1,000, ya que suele venir expresada en miles) [8c7f2974-c0d2-432b-a7f0-db4223a0dcef.pdf].</div>', unsafe_allow_html=True)
    st.markdown('<div class="rule-card"><strong>🧩 Razonamiento Abstracto:</strong> Las secuencias visuales combinan rotación progresiva de figuras (por ejemplo, giros de 90º o 45º) con el desplazamiento regular de puntos de control. Asimismo, en las matrices lógicas de superposición, si dos figuras coinciden en la misma posición, estas se cancelan [8111d114-a22e-478d-95ca-842d3286d732.pdf].</div>', unsafe_allow_html=True)


with tab_main:
    # --- PANTALLA DE INICIO (DASHBOARD) ---
    if st.session_state.current_test is None:
        st.subheader("Ajustes Avanzados del Examen")
        
        # Panel expandible para no saturar móviles
        with st.expander("⚙️ Configurar modo, longitud y temas", expanded=False):
            # 1. Modo de examen (Adaptativo o Manual)
            st.session_state.config_mode = st.radio(
                "Modo de Dificultad:",
                options=["Adaptativo", "Manual"],
                index=0,
                horizontal=True,
                help="El modo adaptativo ajusta tu dificultad de forma automática conforme aciertas o fallas."
            )
            
            # 2. Dificultad manual (solo si es manual)
            if st.session_state.config_mode == "Manual":
                st.session_state.config_diff = st.selectbox(
                    "Selecciona el Nivel del Examen:",
                    options=["Sencillo", "Medio", "Avanzado", "Mezclado"],
                    index=3
                )
            else:
                st.info(f"Dificultad adaptativa actual de tu perfil: **Verbal ({st.session_state.profile['verbal']['difficulty']})** · **Numérico ({st.session_state.profile['numerical']['difficulty']})** · **Abstracto ({st.session_state.profile['abstract']['difficulty']})**")
                
            # 3. Longitud del Examen
            st.session_state.config_length = st.radio(
                "Cantidad de Preguntas por Test:",
                options=["Rápido", "Estándar", "Extendido"],
                index=1,
                horizontal=True,
                help="Estándar (20 Verbal, 10 otros) · Rápido (10 Verbal, 5 otros) · Extendido (30 Verbal, 15 otros)"
            )
            
            # 4. Filtro por temas (específico de Verbal)
            st.session_state.config_topic = st.selectbox(
                "Filtro Temático (Sólo Razonamiento Verbal):",
                options=["Todos", "Filosofía y Lógica", "Ciencia y Tecnología", "Economía y Sociedad"]
            )
            
        st.markdown("---")
        st.subheader("Comenzar una Evaluación")
        
        # Mostrar alerta si hay repaso pendiente
        failed_count = len(st.session_state.profile["failed_questions"])
        if failed_count > 0:
            st.info(f"🔄 Se incluirán automáticamente preguntas de tu cola de repaso para reforzar conceptos.")
            
        # Botones de inicio táctiles, amplios e intuitivos
        st.write("Selecciona una sección para empezar:")
        
        v_btn_text = "💬 Iniciar Razonamiento Verbal"
        if st.session_state.config_length == "Rápido":
            v_btn_text += " (10 Preguntas)"
        elif st.session_state.config_length == "Extendido":
            v_btn_text += " (30 Preguntas)"
        else:
            v_btn_text += " (20 Preguntas)"
            
        if st.button(v_btn_text):
            start_new_test("verbal")
            st.rerun()
            
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
        
        n_btn_text = "📊 Iniciar Razonamiento Numérico"
        if st.session_state.config_length == "Rápido":
            n_btn_text += " (5 Preguntas)"
        elif st.session_state.config_length == "Extendido":
            n_btn_text += " (15 Preguntas)"
        else:
            n_btn_text += " (10 Preguntas)"
            
        if st.button(n_btn_text):
            start_new_test("numerical")
            st.rerun()
            
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
        
        a_btn_text = "🧩 Iniciar Razonamiento Abstracto"
        if st.session_state.config_length == "Rápido":
            a_btn_text += " (5 Preguntas)"
        elif st.session_state.config_length == "Extendido":
            a_btn_text += " (15 Preguntas)"
        else:
            a_btn_text += " (10 Preguntas)"
            
        if st.button(a_btn_text):
            start_new_test("abstract")
            st.rerun()

    # --- PANTALLA DE RESULTADOS / REVISIÓN DEL TEST ---
    elif st.session_state.review_mode:
        category = st.session_state.current_test
        questions = st.session_state.test_questions
        answers = st.session_state.answers
        
        # Calcular estadísticas finales
        correct_count = sum(1 for i, q in enumerate(questions) if answers.get(i) == q["correct"])
        pct = int((correct_count / len(questions)) * 100)
        
        st.markdown("### Examen Finalizado")
        st.balloons() if pct >= 75 else None
        
        # Tarjeta móvil de puntuación final
        color_score = "#16A34A" if pct >= 70 else "#DC2626"
        st.markdown(f"""
        <div style="background-color: #F9FAFB; padding: 22px; border-radius: 16px; border: 2px solid #E5E7EB; text-align: center; margin-bottom: 22px;">
            <span style="font-size: 14px; color: #6B7280; font-weight: bold; text-transform: uppercase;">Puntuación de la Ronda</span>
            <h1 style="color: {color_score}; font-size: 45px; margin: 5px 0;">{correct_count} / {len(questions)}</h1>
            <p style="font-size: 18px; font-weight: bold; margin: 0;">Porcentaje de Aciertos: {pct}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        if pct >= 80:
            st.success(f"🌟 **¡Rendimiento Excelente!** Has dominado esta ronda. El motor adaptativo ha establecido tu nivel en **'{st.session_state.profile[category]['difficulty']}'**.")
        elif pct >= 50:
            st.info("👍 **Buen trabajo.** Vas por excelente camino. Continúa practicando para dominar las preguntas más complejas.")
        else:
            st.warning(f"⚠️ **Atención y Refuerzo:** Esta ronda ha sido difícil. Hemos ajustado tu nivel recomendado a **'{st.session_state.profile[category]['difficulty']}'** para asentar tus bases.")
            
        st.markdown("---")
        st.markdown("### Desglose y Solución Detallada")
        
        for i, q in enumerate(questions):
            user_ans = answers.get(i)
            is_correct = (user_ans == q["correct"])
            icon = "✅ Correcta" if is_correct else f"❌ Fallada (Marcaste {user_ans if user_ans else 'Blanco'})"
            
            with st.expander(f"Pregunta {i+1}: {icon} — {q['question'][:50]}..."):
                if "passage" in q and q["passage"]:
                    st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
                    
                if "table" in q and q["table"]:
                    st.markdown(q["table"])
                    
                if "svg" in q and q["svg"]:
                    st.markdown(q["svg"], unsafe_allow_html=True)
                    
                # Si tiene opciones con SVGs (como abstracto), mostrarlas
                if "options_svgs" in q and q["options_svgs"]:
                    st.markdown("**Opciones visuales de respuestas:**")
                    cols = st.columns(5)
                    keys = ["A", "B", "C", "D", "E"]
                    for idx_c, key in enumerate(keys):
                        with cols[idx_c]:
                            st.markdown(q["options_svgs"][key], unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align:center;font-weight:bold;margin:0;'>{key}</p>", unsafe_allow_html=True)
                
                st.markdown(f"**Pregunta:** {q['question']}")
                
                # Mostrar opciones con colores (verde=correcta, rojo=seleccionada errónea)
                for opt in q["options"]:
                    opt_letter = opt[0]
                    if opt_letter == q["correct"]:
                        st.write(f"🟢 **{opt} (Respuesta Correcta)**")
                    elif opt_letter == user_ans:
                        st.write(f"🔴 **{opt} (Tu Selección)**")
                    else:
                        st.write(f"⚪ {opt}")
                        
                st.markdown("---")
                st.markdown(q["explanation"])
                
        st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)
        if st.button("⬅️ Volver al Panel de Práctica"):
            st.session_state.current_test = None
            st.session_state.review_mode = False
            st.rerun()

    # --- PANTALLA DE PREGUNTA ACTIVA ---
    else:
        category = st.session_state.current_test
        questions = st.session_state.test_questions
        idx = st.session_state.current_index
        q = questions[idx]
        
        # Cabecera de progreso táctil para móvil
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: bold; color: #4F46E5;">{category.upper()} - {q['difficulty']}</span>
            <span style="font-weight: bold; color: #6B7280;">{idx+1} de {len(questions)}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress((idx) / len(questions))
        
        if q.get("is_review"):
            st.warning("🔄 **Pregunta de Refuerzo:** Este ejercicio lo fallaste anteriormente. ¡Demuestra que ya lo dominas!")
            
        # Renderizar pasajes o tablas según existan
        if "passage" in q and q["passage"]:
            st.markdown("**Texto de Comprensión Lectora:**")
            st.markdown(f"<div class='passage-box'>{q['passage']}</div>", unsafe_allow_html=True)
            
        if "table" in q and q["table"]:
            st.markdown("**Tabla de datos a analizar:**")
            st.markdown(q["table"])
            
        if "svg" in q and q["svg"]:
            st.markdown("**Analiza la secuencia geométrica:**")
            st.markdown(q["svg"], unsafe_allow_html=True)
            
        # Si tiene opciones con SVGs (Razonamiento Abstracto)
        if "options_svgs" in q and q["options_svgs"]:
            st.markdown("<div style='margin-top:15px; margin-bottom:10px;'><strong>Opciones visuales de respuestas (A - E):</strong></div>", unsafe_allow_html=True)
            cols = st.columns(5)
            keys = ["A", "B", "C", "D", "E"]
            for idx_c, key in enumerate(keys):
                with cols[idx_c]:
                    st.markdown(q["options_svgs"][key], unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:center;font-weight:bold;margin:0;'>{key}</p>", unsafe_allow_html=True)
            
        st.markdown(f"<h3 style='font-size:1.15rem;margin-top:15px;margin-bottom:15px;'>{q['question']}</h3>", unsafe_allow_html=True)
        
        # Selección de opciones táctiles Streamlit
        options_list = q["options"]
        selected_val = st.radio(
            "Selecciona tu respuesta:",
            options=options_list,
            index=None if st.session_state.selected_option is None else options_list.index(st.session_state.selected_option),
            key=f"radio_q_{idx}"
        )
        
        if selected_val:
            st.session_state.selected_option = selected_val
            st.session_state.answers[idx] = selected_val[0]
            
        st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
        
        # Confirmación interactiva
        if not st.session_state.show_explanation:
            if st.button("Confirmar Respuesta"):
                if st.session_state.selected_option is None:
                    st.warning("⚠️ Por favor, selecciona una opción antes de confirmar.")
                else:
                    st.session_state.show_explanation = True
                    st.rerun()
        else:
            user_ans_letter = st.session_state.answers.get(idx)
            is_correct = (user_ans_letter == q["correct"])
            
            if is_correct:
                st.success("🎉 **¡Respuesta Correcta!** Muy bien razonado.")
            else:
                st.error(f"❌ **Respuesta Incorrecta.** La opción correcta era la **{q['correct']}**.")
                
            with st.container():
                st.markdown("#### Explicación Detallada:")
                st.markdown(q["explanation"])
                
            st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
            
            # Navegación del examen
            if idx + 1 < len(questions):
                if st.button("Siguiente Pregunta ➡️"):
                    st.session_state.current_index += 1
                    st.session_state.selected_option = None
                    st.session_state.show_explanation = False
                    st.rerun()
            else:
                if st.button("📊 Ver Resultados de la Prueba"):
                    finish_active_test()
                    st.rerun()
                    
        # Opción para salir del examen
        st.markdown("<div style='margin-top:20px;' class='secondary-btn'></div>", unsafe_allow_html=True)
        col_back, _ = st.columns([1, 2])
        with col_back:
            if st.button("🚪 Abandonar Test"):
                st.session_state.current_test = None
                st.session_state.review_mode = False
                st.rerun()
