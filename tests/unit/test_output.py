# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from unittest.mock import Mock
from unittest.mock import patch

from pytest import mark
from rich.text import Text

from jrnl.messages import Message
from jrnl.output import print_msg
from jrnl.output import wrap_with_ansi_colors


@patch("jrnl.output.print_msgs")
def test_print_msg_calls_print_msgs_as_list_with_style(print_msgs):
    test_msg = Mock(Message)
    print_msg(test_msg)
    print_msgs.assert_called_once_with([test_msg], style=test_msg.style)


@patch("jrnl.output.print_msgs")
def test_print_msg_calls_print_msgs_with_kwargs(print_msgs):
    test_msg = Mock(Message)
    kwargs = {
        "delimter": "test delimiter 🤡",
        "get_input": True,
        "hide_input": True,
        "some_rando_arg": "💩",
    }
    print_msg(test_msg, **kwargs)
    print_msgs.assert_called_once_with([test_msg], style=test_msg.style, **kwargs)


@mark.parametrize("legacy_windows", [False, True])
@mark.parametrize("lines", [None, "40"])
def test_wrap_preserves_width_and_ansi_with_terminal_height(
    monkeypatch, legacy_windows, lines
):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    if lines is None:
        monkeypatch.delenv("LINES", raising=False)
    else:
        monkeypatch.setenv("LINES", lines)

    # Fill the requested width exactly so losing a column forces an extra line.
    text = "word " * 15 + "end"
    with patch("rich.console.detect_legacy_windows", return_value=legacy_windows):
        result = wrap_with_ansi_colors(f"\x1b[31m{text}\x1b[0m", width=len(text))

    assert Text.from_ansi(result).plain == text
    assert "\x1b[31m" in result
