#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.display_context import DisplayContext


def test_display_context_initial_context():
    context = DisplayContext({'foo': 'bar'})
    assert context['foo'] == 'bar'


def test_display_context_init_params():
    context = DisplayContext(title='The Title', project_name="Project", page_template="stuff.j2")
    assert context['title'] == 'The Title'
    assert context['page_template'] == 'stuff.j2'
    assert context['project_name'] == 'Project'


def test_context_notation():
    context = DisplayContext()
    context.add_notation(label="LLL", tag="TTT", url="URL", value="VVV", lines="SSS")
    notations = context['notations']
    assert len(notations) == 1
    assert notations[0]['label'] == "LLL"
    assert notations[0]['tag'] == "TTT"
    assert notations[0]['url'] == "URL"
    assert notations[0]['value'] == "VVV"
    assert notations[0]['lines'] == "SSS"


def test_context_multi_line_notation():
    context = DisplayContext()
    context.add_multiline_notation(label="LLL", tag="TTT", url="URL", multiline=None)
    assert context.get('notations') is None

    context.add_multiline_notation(label="LLL", tag="TTT", url="URL", multiline='one line')
    notations = context['notations']
    assert len(notations) == 1
    assert notations[0]['label'] == "LLL"
    assert notations[0]['tag'] == "TTT"
    assert notations[0]['url'] == "URL"
    assert notations[0]['value'] == "one line"
    assert notations[0].get('lines') is None

    context.add_multiline_notation(label="LLL", tag="TTT", url="URL", multiline='two\nlines')
    notations = context['notations']
    assert len(notations) == 2
    assert notations[1]['label'] == "LLL"
    assert notations[1]['tag'] == "TTT"
    assert notations[1]['url'] == "URL"
    assert notations[1]['lines'] == ['two', 'lines']
    assert notations[1].get('value') is None

def test_context_has_tasks():
    outer_context = DisplayContext()
    assert not outer_context.get('has_tasks')
    inner_context = DisplayContext()
    assert not inner_context.get('has_tasks')
    inner_context.add_task('URL', 'LABEL', 'TASK')
    assert inner_context.get('has_tasks')
    assert not outer_context.get('has_tasks')
    outer_context.add_child_context(inner_context)
    assert outer_context.get('has_tasks')

