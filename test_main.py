import pytest
from main import parse_markdown, read_file, generate_output

def test_read_file(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data='data'))
    try:
        assert read_file('filepath') == 'data'
    except Exception as e:
        pytest.fail(f"test_read_file failed with exception: {e}")

def test_generate_output_html(mocker):
    mocker.patch('main.parse_markdown', return_value='html')
    try:
        assert generate_output('markdown') == 'html'
    except Exception as e:
        pytest.fail(f"test_generate_output_html failed with exception: {e}")

def test_generate_output_ansi(mocker):
    mocker.patch('main.parse_markdown', return_value='html')
    try:
        assert generate_output('markdown', to_ansi=True) == 'html'
    except Exception as e:
        pytest.fail(f"test_generate_output_ansi failed with exception: {e}")

def test_parse_markdown_valid_bold():
    input_text = "**bold**"
    expected_output = '<p><b>bold</b></p>'
    try:
        assert parse_markdown(input_text) == expected_output
    except Exception as e:
        pytest.fail(f"test_parse_markdown_valid_bold failed with exception: {e}")

def test_parse_markdown_valid_italic():
    input_text = "_italic_"
    expected_output = '<p><i>italic</i></p>'
    try:
        assert parse_markdown(input_text) == expected_output
    except Exception as e:
        pytest.fail(f"test_parse_markdown_valid_italic failed with exception: {e}")

def test_parse_markdown_valid_monospaced():
    input_text = "`monospaced`"
    expected_output = '<p><tt>monospaced</tt></p>'
    try:
        assert parse_markdown(input_text) == expected_output
    except Exception as e:
        pytest.fail(f"test_parse_markdown_valid_monospaced failed with exception: {e}")

def test_parse_markdown_valid_headers():
    input_text = "# Header1\n## Header2"
    expected_output = '<p><h1>Header1</h1><h2>Header2</h2></p>'
    try:
        assert parse_markdown(input_text) == expected_output
    except Exception as e:
        pytest.fail(f"test_parse_markdown_valid_headers failed with exception: {e}")

def test_parse_markdown_valid_preformatted():
    input_text = "```\npreformatted text\n```"
    expected_output = '<p><pre>preformatted text\n</pre></p>'
    try:
        assert parse_markdown(input_text) == expected_output
    except Exception as e:
        pytest.fail(f"test_parse_markdown_preformatted failed with exception: {e}")

def test_parse_markdown_nested_formatting():
    input_text = "**bold and _italic_**"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: nested bold and italic', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: nested bold and italic", f"Expected error message 'Invalid markdown: nested bold and italic', but got '{str(e)}'"

def test_parse_markdown_nested_formatting_italic_bold():
    input_text = "_italic and **bold**_"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: nested italic and bold', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: nested italic and bold", f"Expected error message 'Invalid markdown: nested italic and bold', but got '{str(e)}'"

def test_parse_markdown_nested_formatting_bold_monospaced():
    input_text = "**bold and `monospaced`**"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: nested bold and monospaced', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: nested bold and monospaced", f"Expected error message 'Invalid markdown: nested bold and monospaced', but got '{str(e)}'"

def test_parse_markdown_nested_formatting_italic_monospaced():
    input_text = "_italic and `monospaced`_"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: nested italic and monospaced', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: nested italic and monospaced", f"Expected error message 'Invalid markdown: nested italic and monospaced', but got '{str(e)}'"