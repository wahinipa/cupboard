#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.context import Context


def test_context_set_item():
    context = Context()
    context['foo'] = 'bar'
    assert 'bar' == context['foo']


def test_context_get():
    context = Context()
    context['foo'] = 'bar'
    assert 'bar' == context.get('foo')
    assert 'bar' == context.get('foo', 'abc')
    assert 'abc' == context.get('nada', 'abc')


def test_context_setdefault():
    context = Context()
    assert 'abc' == context.get('foo', 'abc')
    context.setdefault('foo', 'bar')
    assert 'bar' == context.get('foo')
    context.setdefault('foo', 'xyz')
    assert 'bar' == context.get('foo', 'qed')


def test_context_items():
    context = Context()
    context['foo'] = 'bar'
    context['a'] = 'apple'
    context_items = context.items()
    assert len(context_items) == 2
    assert ('foo', 'bar') in context_items
    assert ('a', 'apple') in context_items


def test_context_as_dictionary():
    inner_context = Context()
    inner_context['a'] = 'apple'
    outer_context = Context()
    outer_context['z'] = 'zebra'
    outer_context['I'] = 321
    outer_context['child'] = inner_context
    inner_context['i'] = 123
    alpha_context = Context()
    alpha_context['aaa'] = 'AAA'
    beta_context = Context()
    beta_context['bbb'] = [1, 2, 3]
    outer_context['lll'] = [alpha_context, beta_context]

    expected = {
        'child': {
            'i': 123,
            'a': 'apple',
        },
        'I': 321,
        'z': 'zebra',
        'lll': [
            {'aaa': 'AAA'},
            {'bbb': [1, 2, 3]},
        ]
    }
    assert expected == outer_context.as_dictionary


def test_context_merging():
    alpha_context = Context()
    alpha_context['aaa'] = 'AAA'
    beta_context = Context()
    beta_context['bbb'] = [1, 2, 3]
    alpha_context |= beta_context
    assert alpha_context['bbb'] == [1, 2, 3]


def test_context_append_to_list():
    context = Context()
    context.append_to_list('bbb', 1)
    context.append_to_list('bbb', 2)
    context.append_to_list('bbb', 3)
    assert context['bbb'] == [1, 2, 3]
