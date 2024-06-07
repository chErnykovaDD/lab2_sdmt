import pytest
from main import parse_markdown, read_file, generate_output

def test_read_file(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data='data'))
    try:
        assert read_file('filepath') == 'data'
    except Exception as e:
        pytest.fail(f"test_read_file failed with exception: {e}")

def test_read_file_nonexistent(mocker):
    mocker.patch('builtins.open', side_effect=FileNotFoundError())
    try:
        read_file('nonexistent_file')
        pytest.fail("Expected FileNotFoundError, but no exception was raised")
    except FileNotFoundError as e:
        assert isinstance(e, FileNotFoundError), f"Expected FileNotFoundError, but got {type(e)}"

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

def test_parse_markdown_unclosed_bold():
    input_text = "**bold text"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: unclosed bold', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: unclosed bold", f"Expected error message 'Invalid markdown: unclosed bold', but got '{str(e)}'"

def test_parse_markdown_unclosed_italic():
    input_text = "_italic text"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: unclosed italic', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: unclosed italic", f"Expected error message 'Invalid markdown: unclosed italic', but got '{str(e)}'"

def test_parse_markdown_unclosed_monospaced():
    input_text = "`monospaced text"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: unclosed monospaced', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: unclosed monospaced", f"Expected error message 'Invalid markdown: unclosed monospaced', but got '{str(e)}'"

def test_parse_markdown_unclosed_preformatted():
    input_text = "```\npreformatted text"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: unclosed preformatted block', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: unclosed preformatted block", f"Expected error message 'Invalid markdown: unclosed preformatted block', but got '{str(e)}'"

def test_parse_markdown_invalid_bold_combination():
    input_text = "** bold text **"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: spaces are not allowed between bold markers and text', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: spaces are not allowed between bold markers and text", f"Expected error message 'Invalid markdown: spaces are not allowed between bold markers and text', but got '{str(e)}'"

def test_parse_markdown_invalid_italic_combination():
    input_text = "_ italic text _"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: spaces are not allowed between italic markers and text', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: spaces are not allowed between italic markers and text", f"Expected error message 'Invalid markdown: spaces are not allowed between italic markers and text', but got '{str(e)}'"

def test_parse_markdown_invalid_monospaced_combination():
    input_text = "` monospaced text `"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: spaces are not allowed between monospaced markers and text', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: spaces are not allowed between monospaced markers and text", f"Expected error message 'Invalid markdown: spaces are not allowed between monospaced markers and text', but got '{str(e)}'"

def test_parse_markdown_incomplete_preformatted():
    input_text = "```\npreformatted text\n``"
    try:
        parse_markdown(input_text)
        pytest.fail("Expected ValueError with message 'Invalid markdown: unclosed preformatted block', but no exception was raised")
    except ValueError as e:
        assert str(e) == "Invalid markdown: unclosed preformatted block", f"Expected error message 'Invalid markdown: unclosed preformatted block', but got '{str(e)}'"

def test_parse_markdown_multiple_headers():
    input_text = "# Header 1\n## Header 2"
    expected_output = "<p><h1>Header 1</h1><h2>Header 2</h2></p>"
    try:
        assert parse_markdown(input_text) == expected_output
    except Exception as e:
        pytest.fail(f"test_parse_markdown_multiple_headers failed with exception: {e}")

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