# -*- coding: utf-8 -*-
#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the
# License.
#

import typing
from ask_sdk_model import Response
from ask_sdk_model.ui import SsmlOutputSpeech, Reprompt
from ask_sdk_model.interfaces.display import (
    TextContent, PlainText, RichText)

if typing.TYPE_CHECKING:
    from typing import Union
    from ask_sdk_model import Directive
    from ask_sdk_model.ui import Card


PLAIN_TEXT_TYPE = "PlainText"
"""str: Helper variable for plain text type."""

RICH_TEXT_TYPE = "RichText"
"""str: Helper variable for rich text type."""


class ResponseFactory(object):
    """ResponseFactory is class which provides helper functions to help
    building a response.
    """

    def __init__(self):
        # type: () -> None
        """The ResponseFactory has property Response with all
        parameters initialized to None.
        """
        self.response = Response(
            output_speech=None, card=None, reprompt=None,
            directives=None, should_end_session=None)

    def speak(self, speech):
        # type: (str) -> 'ResponseFactory'
        """Say the provided speech to the user.

        :param speech: the output speech sent back to the user.
        :type speech: str
        :return: response factory with partial response being built and
            access from self.response.
        :rtype: ResponseFactory
        """
        ssml = "<speak>{}</speak>".format(self.__trim_outputspeech(
            speech_output=speech))
        self.response.output_speech = SsmlOutputSpeech(ssml=ssml)
        return self

    def ask(self, reprompt):
        # type: (str) -> 'ResponseFactory'
        """Provide reprompt speech to the user, if no response for
        8 seconds.

        The should_end_session value will be set to false except when
        the video app launch directive is present in directives.

        :param reprompt: the output speech to reprompt.
        :type reprompt: str
        :return: response factory with partial response being built and
            access from self.response.
        :rtype: ResponseFactory
        """
        ssml = "<speak>{}</speak>".format(self.__trim_outputspeech(
            speech_output=reprompt))
        output_speech = SsmlOutputSpeech(ssml=ssml)
        self.response.reprompt = Reprompt(output_speech=output_speech)
        if not self.__is_video_app_launch_directive_present():
            self.response.should_end_session = False
        return self

    def set_card(self, card):
        # type: (Card) -> 'ResponseFactory'
        """Renders a card within the response.

        For more information about card object in response, click here:
        https://developer.amazon.com/docs/custom-skills/request-and-response-json-reference.html#card-object.

        :param card: card object in response sent back to user.
        :type card: :py:class:`ask_sdk_model.ui.card.Card`
        :return: response factory with partial response being built
            and access from self.response.
        :rtype: ResponseFactory
        """
        self.response.card = card
        return self

    def add_directive(self, directive):
        # type: (Directive) -> 'ResponseFactory'
        """Adds directive to response.

        :param directive: the directive sent back to Alexa device.
        :type directive: :py:class:`ask_sdk_model.Directive`
        :return: response factory with partial response being built and
            access from self.response.
        :rtype: ResponseFactory
        """
        if self.response.directives is None:
            self.response.directives = []

        if (directive is not None and
                directive.object_type == "VideoApp.Launch"):
            self.response.should_end_session = None
        self.response.directives.append(directive)
        return self

    def set_should_end_session(self, should_end_session):
        # type: (bool) -> 'ResponseFactory'
        """Sets shouldEndSession value to null/false/true.

        :param should_end_session: value to show if the session should
            be ended or not.
        :type should_end_session: bool
        :return: response factory with partial response being built and
            access from self.response.
        :rtype: ResponseFactory
        """
        if not self.__is_video_app_launch_directive_present():
            self.response.should_end_session = should_end_session
        return self

    def __trim_outputspeech(self, speech_output=None):
        # type: (Union[str, None]) -> str
        """Trims the output speech if it already has the
        <speak></speak> tag.

        :param speech_output: the output speech sent back to user.
        :type speech_output: str
        :return: the trimmed output speech.
        :rtype: Union[bool, None]
        """
        if speech_output is None:
            return ""
        speech = speech_output.strip()
        if speech.startswith("<speak>") and speech.endswith("</speak>"):
            return speech[7:-8].strip()
        return speech

    def __is_video_app_launch_directive_present(self):
        # type: () -> bool
        """Checks if the video app launch directive is present or not.

        :return: boolean to show if video app launch directive is
            present or not.
        :rtype: bool
        """
        if self.response.directives is None:
            return False

        for directive in self.response.directives:
            if (directive is not None and
                    directive.object_type == "VideoApp.Launch"):
                return True
        return False


def get_plain_text_content(primary_text=None, secondary_text=None, tertiary_text=None):
    # type: (str, str, str) -> TextContent
    """Responsible for building plain text content object using
    ask-sdk-model in Alexa skills kit display interface.
    https://developer.amazon.com/docs/custom-skills/display-interface-reference.html#textcontent-object-specifications.

    :type primary_text: (optional) str
    :type secondary_text: (optional) str
    :type tertiary_text: (optional) str
    :return: Text Content instance with primary, secondary and tertiary
        text set as Plain Text objects.
    :rtype: :py:class:`ask_sdk_model.interfaces.display.TextContent`
    :raises: ValueError
    """
    return get_text_content(
        primary_text=primary_text, primary_text_type=PLAIN_TEXT_TYPE,
        secondary_text=secondary_text, secondary_text_type=PLAIN_TEXT_TYPE,
        tertiary_text=tertiary_text, tertiary_text_type=PLAIN_TEXT_TYPE)


def get_rich_text_content(primary_text=None, secondary_text=None, tertiary_text=None):
    # type: (str, str, str) -> TextContent
    """Responsible for building plain text content object using
    ask-sdk-model in Alexa skills kit display interface.
    https://developer.amazon.com/docs/custom-skills/display-interface-reference.html#textcontent-object-specifications.

    :type primary_text: (optional) str
    :type secondary_text: (optional) str
    :type tertiary_text: (optional) str
    :return: Text Content instance with primary, secondary and tertiary
        text set as Plain Text objects.
    :rtype: :py:class:`ask_sdk_model.interfaces.display.TextContent`
    :raises: ValueError
    """
    return get_text_content(
        primary_text=primary_text, primary_text_type=RICH_TEXT_TYPE,
        secondary_text=secondary_text, secondary_text_type=RICH_TEXT_TYPE,
        tertiary_text=tertiary_text, tertiary_text_type=RICH_TEXT_TYPE)


def get_text_content(
        primary_text=None, primary_text_type=PLAIN_TEXT_TYPE,
        secondary_text=None, secondary_text_type=PLAIN_TEXT_TYPE,
        tertiary_text=None, tertiary_text_type=PLAIN_TEXT_TYPE):
    # type: (str, str, str, str, str, str) -> TextContent
    """Responsible for building text content object using ask-sdk-model
    in Alexa skills kit display interface.
    https://developer.amazon.com/docs/custom-skills/display-interface-reference.html#textcontent-object-specifications.

    :type primary_text: (optional) str
    :param primary_text_type: Type of the primary text field. Allowed
        values are `PlainText` and `RichText`.
        Defaulted to `PlainText`.
    :type primary_text_type: (optional) str
    :type secondary_text: (optional) str
    :param secondary_text_type: Type of the secondary text field.
        Allowed values are `PlainText` and `RichText`.
        Defaulted to `PlainText`.
    :type tertiary_text: (optional) str
    :param tertiary_text_type: Type of the tertiary text field.
        Allowed values are `PlainText` and `RichText`.
        Defaulted to `PlainText`.
    :return: Text Content instance with primary, secondary and tertiary
        text set.
    :rtype: :py:class:`ask_sdk_model.interfaces.display.TextContent`
    :raises: ValueError
    """
    text_content = TextContent()
    if primary_text:
        text_content.primary_text = __set_text_field(
            primary_text, primary_text_type)
    if secondary_text:
        text_content.secondary_text = __set_text_field(
            secondary_text, secondary_text_type)
    if tertiary_text:
        text_content.tertiary_text = __set_text_field(
            tertiary_text, tertiary_text_type)
    return text_content


def __set_text_field(text, text_type):
    # type: (str, str) -> Union[None, PlainText, RichText]
    """Helper method to create text field according to text type.

    :type text: str
    :param text_type: Type of the primary text field. Allowed values
        are `PlainText` and `RichText`.
    :type text_type: str
    :return: Object of type
        :py:class:`ask_sdk_model.interfaces.display.PlainText` or
        :py:class:`ask_sdk_model.interfaces.display.RichText` depending
        on text_type
    :rtype: object
    :raises: ValueError
    """
    if text:
        if text_type not in [PLAIN_TEXT_TYPE, RICH_TEXT_TYPE]:
            raise ValueError("Invalid type provided: {}".format(text_type))

        if text_type == PLAIN_TEXT_TYPE:
            return PlainText(text=text)
        else:
            return RichText(text=text)
    else:
        return None
