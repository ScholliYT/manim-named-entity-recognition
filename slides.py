from manim import *
from manim_editor import PresentationSectionType
from flair.data import Sentence
from flair.models import SequenceTagger


tagger = None


def get_ner_tagged_sentence(text):
    global tagger

    if tagger is None:
        # load the NER tagger
        tagger = SequenceTagger.load("de-ner")
        print("SequenceTagger loaded")

    sentence = Sentence(text)
    # run NER over sentence
    tagger.predict(sentence)

    print(sentence)
    print("The following NER tags are found:")

    print(sentence.get_spans())

    return sentence


class NamedEntityRecognition1_1(Scene):
    def add_title(self):
        title_text = "Named Entity Recognition"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        intro_words1 = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.5).to_edge(UP)
        self.add(intro_words1)

    def construct(self):
        self.add_title()

        self.next_section("Funktionsweise", PresentationSectionType.NORMAL)
        working_principle = Text("Funktionsweise").shift(UP)
        self.play(Write(working_principle))

        self.next_section("State-of-the-art", PresentationSectionType.NORMAL)
        state_of_the_art = Text("State-of-the-art").next_to(working_principle, DOWN).shift(DOWN)
        self.play(Write(state_of_the_art))

        self.next_section("Frameworks", PresentationSectionType.NORMAL)
        frameworks = Text("Frameworks").next_to(state_of_the_art, DOWN).shift(DOWN)
        self.play(Write(frameworks))


class Problem1_2(Scene):
    def add_title(self):
        title_text = "Problem"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        title = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.5).to_edge(UP)
        self.add(title)

    def construct(self):
        self.add_title()

        example_text = "George Washington ging nach Washington"
        sentence = get_ner_tagged_sentence(example_text)

        self.next_section("Beispiel", PresentationSectionType.NORMAL)
        text = Text(example_text).scale(0.8)
        self.play(Write(text))

        for entity in sentence.to_dict("ner")["entities"]:
            start_offset = example_text[0 : entity["start_pos"]].count(" ")
            end_offset = example_text[0 : entity["end_pos"]].count(" ")
            fixed_start_pos = entity["start_pos"] - start_offset
            fixed_end_pos = entity["end_pos"] - end_offset
            print(
                entity,
                fixed_start_pos,
                fixed_end_pos,
                example_text.replace(" ", "")[fixed_start_pos:fixed_end_pos],
            )

            self.next_section(entity["text"], PresentationSectionType.NORMAL)
            tag_type = entity["labels"][0].value
            if tag_type == "PER":
                person_framebox = BackgroundRectangle(text[fixed_start_pos:fixed_end_pos], buff=0.05, color=GREEN)
                person_label = Text("Person", color=GREEN).scale(0.8).next_to(person_framebox, DOWN)
                self.play(Create(person_framebox), Write(person_label))
            elif tag_type == "LOC":
                location_framebox = BackgroundRectangle(text[fixed_start_pos:fixed_end_pos], buff=0.05, color=RED)
                location_label = Text("Location", color=RED).scale(0.8).next_to(location_framebox, DOWN)
                self.play(Create(location_framebox), Write(location_label))
            elif tag_type == "ORG":
                org_framebox = BackgroundRectangle(text[fixed_start_pos:fixed_end_pos], buff=0.05, color=BLUE)
                org_label = Text("Organization", color=BLUE).scale(0.8).next_to(org_framebox, DOWN)
                self.play(Create(org_framebox), Write(org_label))


class Motivation1_3(Scene):
    def add_title(self):
        title_text = "Motivation"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        title = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.5).to_edge(UP)
        self.add(title)

    def construct(self):
        self.add_title()

        self.next_section("Processing Pipeline", PresentationSectionType.NORMAL)
        processing_pipeline_text = Text("Erster Teil einer Processing Pipeline")
        self.play(Write(processing_pipeline_text))

        self.next_section("Processing Pipeline.1", PresentationSectionType.SUB_NORMAL)
        processing_pipeline_text.generate_target()
        processing_pipeline_text.target.shift(2 * UP)
        processing_pipeline_text.target.set_color(GRAY)
        processing_pipeline_text.target.scale(0.5)
        self.play(MoveToTarget(processing_pipeline_text))

        self.next_section("Beispiel", PresentationSectionType.NORMAL)
        example_text = "Max, Moritz, Anna und Nele fahren nach Köln"
        sentence = get_ner_tagged_sentence(example_text)
        text = Text(example_text).scale(0.8)
        self.play(Write(text))

        self.next_section("Frage", PresentationSectionType.NORMAL)
        question_text = Text("Wie viele Personen fahren nach Köln?").scale(0.7).shift(DOWN)
        self.play(Write(question_text))

        self.next_section("Frage", PresentationSectionType.SUB_NORMAL)
        question_text.generate_target()
        question_text.target.shift(2 * DOWN + 2 * LEFT)
        self.play(MoveToTarget(question_text))

        # add tagging
        person_labels = []
        for entity in sentence.to_dict("ner")["entities"]:
            start_offset = example_text[0 : entity["start_pos"]].count(" ")
            end_offset = example_text[0 : entity["end_pos"]].count(" ")
            fixed_start_pos = entity["start_pos"] - start_offset
            fixed_end_pos = entity["end_pos"] - end_offset
            print(
                entity,
                fixed_start_pos,
                fixed_end_pos,
                example_text.replace(" ", "")[fixed_start_pos:fixed_end_pos],
            )

            self.next_section(entity["text"], PresentationSectionType.NORMAL)
            tag_type = entity["labels"][0].value
            if tag_type == "PER":
                person_framebox = BackgroundRectangle(text[fixed_start_pos:fixed_end_pos], buff=0.05, color=GREEN)
                person_label = Text("PER", color=GREEN).next_to(person_framebox, DOWN)
                self.play(Create(person_framebox), Write(person_label))
                person_labels.append(person_label)
            elif tag_type == "LOC":
                location_framebox = BackgroundRectangle(text[fixed_start_pos:fixed_end_pos], buff=0.05, color=RED)
                location_label = Text("LOC", color=RED).next_to(location_framebox, DOWN)
                self.play(Create(location_framebox), Write(location_label))

        self.next_section("Count", PresentationSectionType.NORMAL)
        person_count_text = Text(str(len(person_labels)), color=GREEN).next_to(question_text, RIGHT)
        self.play(Transform(VGroup(*person_labels), person_count_text))


class OldWorkingPrinciple2_1(Scene):
    def add_title(self):
        title_text = "Funktionsweise"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        title = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.5).to_edge(UP)
        self.add(title)

    def construct(self):
        self.add_title()

        # Dictionary
        self.next_section("Dictionary", PresentationSectionType.NORMAL)
        dictionary = Text("Dictionary / Lexikon").shift(1.5 * UP)
        self.play(Write(dictionary))

        self.next_section("Dictionary Beispiel", PresentationSectionType.NORMAL)
        dictionary_example_persons = (
            Text('PER = {"Max", "Moritz", "Anna", "Nele"}', color=GRAY).scale(0.8).next_to(dictionary, DOWN)
        )
        dictionary_example_locations = (
            Text('LOC = {"Dortmund", "Köln", "Berlin"}', color=GRAY)
            .scale(0.8)
            .next_to(dictionary_example_persons, DOWN)
        )
        self.play(Write(dictionary_example_persons))
        self.play(Write(dictionary_example_locations))

        dictionary_group = Group(dictionary, dictionary_example_persons, dictionary_example_locations)

        self.next_section("Dictionary Example.1", PresentationSectionType.SUB_NORMAL)
        dictionary_group.generate_target()
        dictionary_group.target.shift(4 * LEFT + UP)
        dictionary_group.target.scale(0.5)
        self.play(MoveToTarget(dictionary_group))

        # Handcraft features
        self.next_section("Handgefertigte Merkmale", PresentationSectionType.NORMAL)
        handcraft_features = Text("Handgefertigte Merkmale")
        self.play(Write(handcraft_features))

        self.next_section("Handgefertigte Merkmale Beispiele", PresentationSectionType.SUB_NORMAL)
        handcraft_features_capitalizaiton = (
            Text("Großschreibung", color=GRAY).scale(0.8).next_to(handcraft_features, DOWN)
        )
        handcraft_features_length = (
            Text("Wortlänge", color=GRAY).scale(0.8).next_to(handcraft_features_capitalizaiton, DOWN)
        )
        handcraft_features_alphabet = (
            Text("Zeichensatz (Buchstaben, Zahlen...)", color=GRAY).scale(0.8).next_to(handcraft_features_length, DOWN)
        )
        self.play(Write(handcraft_features_capitalizaiton))
        self.play(Write(handcraft_features_length))
        self.play(Write(handcraft_features_alphabet))


class NewWorkingPrinciple2_2(Scene):
    def add_title(self):
        title_text = "Funktionsweise"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        title = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.5).to_edge(UP)
        self.add(title)

    def construct(self):
        self.add_title()

        # NN
        self.next_section("NN", PresentationSectionType.NORMAL)
        text_nn = Text("Neural Networks")
        self.play(Write(text_nn))

        # RNN
        self.next_section("RNN", PresentationSectionType.NORMAL)
        text_rnn = Text("Recurrent").next_to(text_nn, LEFT)
        self.play(Write(text_rnn))

        self.next_section("RNN - Shift", PresentationSectionType.NORMAL)
        text_rrn = VGroup(text_nn, text_rnn)
        self.play(text_rrn.animate.shift(2 * UP))


        # TODO Mini tutorial on RNNs
        # TODO Mini tutorial on LSTMs
        # TODO Mini tutorial on Transformer?


class AscendingIndexWordEmbedding2_3(Scene):
    def add_title(self):
        title_text = "Naive Word Embedding"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        title = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.5).to_edge(UP)
        self.add(title)

    def construct(self):
        self.add_title()

        self.next_section("Naiv", PresentationSectionType.NORMAL)
        text = Text("Wörter aufsteigend nummerieren").shift(2 * UP)
        self.play(Write(text))

        self.next_section("Beispiel", PresentationSectionType.NORMAL)
        words = Text('{"Max", "Moritz", "Anna", "Nele"}').scale(0.8)
        self.play(Write(words))

        self.next_section("Sortiert", PresentationSectionType.NORMAL)
        words_sorted = Text('["Anna", "Max", "Moritz", "Nele"]').scale(0.8)
        self.play(TransformMatchingShapes(words, words_sorted, run_time=3, path_arc=PI / 2))

        self.next_section("Backup", PresentationSectionType.NORMAL)
        words_sorted_backup = words_sorted.copy()
        words_sorted_backup.generate_target()
        words_sorted_backup.target.set_color(GRAY)
        words_sorted_backup.target.shift(UP)
        self.play(MoveToTarget(words_sorted_backup))

        self.next_section("Index", PresentationSectionType.NORMAL)
        words_sorted_with_idx = Text("[0,1,2,3]").scale(0.8)
        self.play(ReplacementTransform(words_sorted, words_sorted_with_idx))

        self.next_section("Dictionary", PresentationSectionType.NORMAL)
        embedding_elements = VGroup(words_sorted_backup, words_sorted_with_idx)
        embedding = Paragraph('embedding = {\n  "Anna": 0, "Max": 1, \n  "Moritz": 2, "Nele": 3\n}').scale(0.8)
        self.play(ReplacementTransform(embedding_elements, embedding))

        # show problem with ascending numbering
        problem_text1 = Text('dist("Anna", "Max") = 1').shift(2 * DOWN).scale(0.8)
        problem_text2 = Text('dist("Anna", "Nele") = 3').next_to(problem_text1, DOWN).scale(0.8)

        self.next_section("Problem - 1", PresentationSectionType.NORMAL)
        self.play(Write(problem_text1))

        self.next_section("Problem - 2", PresentationSectionType.NORMAL)
        self.play(Write(problem_text2))


class OneHotWordEmbedding2_4(Scene):
    def add_title(self):
        title_text = "One-hot Word Embedding"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        title = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.5).to_edge(UP)
        self.add(title)

    def construct(self):
        self.add_title()

        self.next_section("Beschreibung", PresentationSectionType.NORMAL)
        text = Tex("Basisvektoren im $\\mathbb{R}^n$").shift(2 * UP)
        self.play(Write(text))

        self.next_section("Moritz", PresentationSectionType.NORMAL)
        moritz = Tex("Moritz = $\\left(\\begin{array}{c} 1 \\\\ 0 \\\\ 0 \\end{array}\\right)$").shift(4 * LEFT)
        self.play(Write(moritz))

        self.next_section("Köln", PresentationSectionType.NORMAL)
        koeln = Tex('K\\"oln = $\\left(\\begin{array}{c} 0 \\\\ 1 \\\\ 0 \\end{array}\\right)$')
        self.play(Write(koeln))

        self.next_section("Dortmund", PresentationSectionType.NORMAL)
        dortmund = Tex("Dortmund = $\\left(\\begin{array}{c} 0 \\\\ 0 \\\\ 1 \\end{array}\\right)$").shift(4.5 * RIGHT)
        self.play(Write(dortmund))


class OneHotWordEmbeddingPlot2_5(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            z_range=[-1.5, 1.5, 1],
            x_length=9,
            y_length=9,
            z_length=6,
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        text3d = Text("One-hot Word Embedding", gradient=(BLUE, BLUE_D)).scale(0.8)
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        self.add(axes)

        vec1 = Vector([3, 0, 0])
        vec2 = Vector([0, 3, 0])
        vec3 = Vector([0, 0, 2])

        self.next_section("Moritz", PresentationSectionType.NORMAL)
        self.play(Create(vec1))
        moritz = Text("Moritz").scale(0.5).move_to(2.5 * LEFT)
        self.add_fixed_in_frame_mobjects(moritz)
        self.play(Create(moritz))

        self.next_section("Köln", PresentationSectionType.NORMAL)
        self.play(Create(vec2))
        koeln = Text("Köln").scale(0.5).move_to(2.5 * RIGHT)
        self.add_fixed_in_frame_mobjects(koeln)
        self.play(Write(koeln))

        self.next_section("Dortmund", PresentationSectionType.NORMAL)
        self.play(Create(vec3))
        dortmund = Text("Dortmund").scale(0.5).move_to(2 * UP + RIGHT)
        self.add_fixed_in_frame_mobjects(dortmund)
        self.play(Create(dortmund))

        # show problem with ascending numbering
        self.next_section("Problem", PresentationSectionType.NORMAL)
        problem_text1 = Text('dist("Dortmund", "Moritz") = dist("Dortmund", "Köln")').to_edge(DOWN).scale(0.8)
        self.add_fixed_in_frame_mobjects(problem_text1)
        self.play(Write(problem_text1))

        self.next_section("Dortmund - Moritz", PresentationSectionType.NORMAL)
        dm_line = Line(vec3.get_end(), vec1.get_end(), color=RED)
        self.play(Create(dm_line))


        self.next_section("Rotate line", PresentationSectionType.LOOP)
        self.play(Rotate(dm_line, angle=PI/2, axis=[0,0,1], about_point=ORIGIN))
        self.wait(0.5)
        self.play(Rotate(dm_line, angle=-PI/2, axis=[0,0,1], about_point=ORIGIN))
        self.wait(0.5)



class WordEmbedding2_6(Scene):
    def add_title(self):
        title = "Semantical Word Embedding"
        self.next_section(title, PresentationSectionType.NORMAL)
        title = Text(title, gradient=(BLUE, BLUE_D), should_center=True).scale(1.3).to_edge(UP)
        self.add(title)

    def construct(self):
        self.add_title()

        self.next_section("Axes", PresentationSectionType.NORMAL)
        numberplane = NumberPlane().shift(2 * DOWN)  # y_length=5
        self.play(Create(numberplane))

        self.next_section("Dortmund", PresentationSectionType.NORMAL)
        arrow = Arrow(2 * DOWN, [2, 1, 0], buff=0)
        tip_text = Text("Dortmund").next_to(arrow.get_end(), RIGHT)
        self.play(Create(arrow), Write(tip_text))

        self.next_section("Köln", PresentationSectionType.NORMAL)
        arrow = Arrow(2 * DOWN, [2, 0, 0], buff=0)
        tip_text = Text("Köln").next_to(arrow.get_end(), RIGHT)
        self.play(Create(arrow), Write(tip_text))

        self.next_section("Moritz", PresentationSectionType.NORMAL)
        arrow = Arrow(2 * DOWN, [-3, 0, 0], buff=0)
        tip_text = Text("Moritz").next_to(arrow.get_end(), LEFT)
        self.play(Create(arrow), Write(tip_text))

        self.next_section("Anna", PresentationSectionType.NORMAL)
        arrow = Arrow(2 * DOWN, [-4, -1, 0], buff=0)
        tip_text = Text("Anna").next_to(arrow.get_end(), LEFT)
        self.play(Create(arrow), Write(tip_text))

class Datsets3_1(Scene):
    def add_title(self):
        title_text = "Datensätze"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        intro_words1 = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.2).to_edge(UP)
        self.add(intro_words1)

    def construct(self):
        self.add_title()

        self.next_section("Conll2003", PresentationSectionType.NORMAL)
        conll2003 = Text("Conll2003").shift(1.5*UP).to_edge(LEFT).shift(0.5*RIGHT)
        self.play(Write(conll2003))
        
        self.next_section("Sprachen", PresentationSectionType.NORMAL)
        conll2003_languages = Text("Englisch + Deutsch").next_to(conll2003, RIGHT).scale(0.6).shift(0.1*DOWN+0.5*LEFT)
        self.play(Write(conll2003_languages))

        self.next_section("Entities", PresentationSectionType.NORMAL)
        conll2003_entity_categories = Text("4 Kategorien").next_to(conll2003_languages, RIGHT).scale(0.6).shift(0.25*LEFT)
        self.play(Write(conll2003_entity_categories))

        self.next_section("Entities", PresentationSectionType.SUB_NORMAL)
        conll2003_entities = Text("PER,LOC,ORG,MISC", t2c={"PER": GREEN, "LOC": RED, "ORG": BLUE, "MISC": PURPLE}).next_to(conll2003_languages, RIGHT).scale(0.6).shift(0.5*LEFT)
        self.play(ReplacementTransform(conll2003_entity_categories, conll2003_entities))

        self.next_section("Beispielsatz", PresentationSectionType.SUB_NORMAL)
        conll2003_example = "Germany's representative to the European Union's veterinary committee\nWerner Zwingmann said on Wednesday consumers should buy sheepmeat\nfrom countries other than Britain until the scientific advice was clearer."


        t2c_dict = {
            "[0:7]": RED,
            "[28:41]": BLUE,
            "[62:77]": GREEN,
            "[141:148]": RED
        }

        # t2c_dict = {}
        # sentence = get_ner_tagged_sentence(conll2003_example)
        # for entity in sentence.to_dict("ner")["entities"]:
        #     start_offset = conll2003_example[0 : entity["start_pos"]].count(" ")
        #     end_offset = conll2003_example[0 : entity["end_pos"]].count(" ")
        #     fixed_start_pos = entity["start_pos"] - start_offset
        #     fixed_end_pos = entity["end_pos"] - end_offset
        #     print(
        #         entity,
        #         fixed_start_pos,
        #         fixed_end_pos,
        #         conll2003_example.replace(" ", "")[fixed_start_pos:fixed_end_pos],
        #     )

        #     tag_type = entity["labels"][0].value
        #     if tag_type == "PER":
        #         color=GREEN
        #     elif tag_type == "LOC":
        #         color=RED
        #     elif tag_type == "ORG":
        #         color=BLUE
        #     t2c_dict[f"[{fixed_start_pos}:{fixed_end_pos}]"] = color


        conll2003_example_text = Paragraph(conll2003_example, color=GRAY, t2c=t2c_dict).scale(0.5).next_to(conll2003, DOWN).to_edge(LEFT).shift(0.8*RIGHT)
        self.play(Write(conll2003_example_text))

        self.next_section("Score", PresentationSectionType.NORMAL)
        conll2003_score =     Tex("Normaler F1-Score: $\\geq 93\\%$").scale(0.7).shift(DOWN)
        conll2003_top_score = Tex("Top F1-Score: $94.6\\%$").scale(0.7).next_to(conll2003_score, DOWN)
        self.play(Write(conll2003_score))
        self.play(Write(conll2003_top_score))



class ChallengesWithHistoricalData4_1(Scene):
    def add_title(self):
        title_text = "Herausforderung: Historische Daten"
        self.next_section(title_text, PresentationSectionType.NORMAL)
        intro_words1 = Text(title_text, gradient=(BLUE, BLUE_D), should_center=True).scale(1.2).to_edge(UP)
        self.add(intro_words1)

    def construct(self):
        self.add_title()

        self.next_section("Noisy Input", PresentationSectionType.NORMAL)
        noisy_input = Text("Noisy Input").shift(1.5*UP+4*LEFT)
        self.play(Write(noisy_input))
        self.next_section("Noisy Input", PresentationSectionType.SUB_NORMAL)
        noisy_input_example = Text("Zeichenweise Erkennungsfehler", color=GRAY).scale(0.5).next_to(noisy_input, DOWN)
        self.play(Write(noisy_input_example)) 

        self.next_section("Wenig Daten", PresentationSectionType.NORMAL)
        limited_data = Text("Wenig Daten").next_to(noisy_input, DOWN).shift(DOWN)
        self.play(Write(limited_data))
        self.next_section("Wenig Daten", PresentationSectionType.SUB_NORMAL)
        limited_data_example = Text("Kein Wikipedia", color=GRAY).scale(0.5).next_to(limited_data, DOWN)
        self.play(Write(limited_data_example)) 

        self.next_section("Domain Shift", PresentationSectionType.NORMAL)
        domain_shift = Text("Domain Shift").next_to(limited_data, DOWN).shift(DOWN)
        self.play(Write(domain_shift))
        self.next_section("Domain Shift", PresentationSectionType.SUB_NORMAL)
        domain_shift_example = Text("Zeitungstexte -> Briefe", color=GRAY).scale(0.5).next_to(domain_shift, DOWN)
        self.play(Write(domain_shift_example))


        
        
        self.next_section("Dynamische Sprache", PresentationSectionType.NORMAL)
        dynamic_language = Text("Dynamische Sprache").shift(1.5*UP+3*RIGHT)
        self.play(Write(dynamic_language))

        self.next_section("Schreibweisen", PresentationSectionType.SUB_NORMAL)
        dynamic_language_example = Text("Schreibweisen").scale(0.8).next_to(dynamic_language, DOWN)
        self.play(Write(dynamic_language_example)) 
        self.next_section("Litteratur", PresentationSectionType.SUB_NORMAL)
        dynamic_language_example = Text("Litteratur", color=GRAY, t2c={'[:3]': GRAY, '[3:4]': RED, '[4:]': GRAY}).scale(0.5).next_to(dynamic_language_example, DOWN)
        self.play(Write(dynamic_language_example)) 



        self.next_section("Konventionen", PresentationSectionType.SUB_NORMAL)
        dynamic_language_example = Text("Konventionen").scale(0.8).next_to(dynamic_language_example, DOWN).shift(0.5*DOWN)
        self.play(Write(dynamic_language_example)) 
        self.next_section("Anrede", PresentationSectionType.SUB_NORMAL)
        dynamic_language_example = Text("Anrede", color=GRAY).scale(0.5).next_to(dynamic_language_example, DOWN)
        self.play(Write(dynamic_language_example)) 

        self.next_section("Entity drift", PresentationSectionType.SUB_NORMAL)
        dynamic_language_example = Text("Entity drift").scale(0.8).next_to(dynamic_language_example, DOWN).shift(0.5*DOWN)
        self.play(Write(dynamic_language_example)) 

        # TODO Find better example of entity drift
        self.next_section("Preußen", PresentationSectionType.SUB_NORMAL)
        dynamic_language_example = Text("Preußen - Früher Region, heute Fußballverein", color=GRAY).scale(0.5).next_to(dynamic_language_example, DOWN)
        self.play(Write(dynamic_language_example)) 
