from app.lib import testMap
from app.lib import concepts


def generate_fixed_text(test_type):
    text = {}

    f = testMap.map[test_type]
    text['header'] = f.text.header_text
    text['js_folder'] = f.text.js_folder
    text['when_to_use'] = f.text.generate_when_to_use_text()
    text['assumptions'] = f.text.generate_assumptions_text()
    text['options'] = f.text.generate_options_text()

    # Concepts text
    concept_text = ""
    concept_list = concepts.concept_map[test_type]
    for concept in concept_list:
        concept_text += concepts.concepts_text[concept]
    text['concepts'] = concept_text

    return text
