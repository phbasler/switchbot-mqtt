# switchbot-mqtt - MQTT client controlling SwitchBot button & curtain automators,
# compatible with home-assistant.io's MQTT Switch & Cover platform
#
# Copyright (C) 2020 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import typing

import paho.mqtt.client
import pytest
import switchbot

import switchbot_mqtt._actors.base

# pylint: disable=protected-access


def test_abstract() -> None:
    with pytest.raises(TypeError, match=r"\babstract class\b"):
        # pylint: disable=abstract-class-instantiated
        switchbot_mqtt._actors.base._MQTTControlledActor(  # type: ignore
            mac_address="dummy", retry_count=21, password=None
        )


def test_execute_command_abstract() -> None:
    class _ActorMock(switchbot_mqtt._actors.base._MQTTControlledActor):
        # pylint: disable=duplicate-code
        def __init__(
            self, mac_address: str, retry_count: int, password: typing.Optional[str]
        ) -> None:
            super().__init__(
                mac_address=mac_address, retry_count=retry_count, password=password
            )

        def execute_command(
            self,
            *,
            mqtt_message_payload: bytes,
            mqtt_client: paho.mqtt.client.Client,
            update_device_info: bool,
            mqtt_topic_prefix: str,
        ) -> None:
            assert 21
            super().execute_command(
                mqtt_message_payload=mqtt_message_payload,
                mqtt_client=mqtt_client,
                update_device_info=update_device_info,
                mqtt_topic_prefix=mqtt_topic_prefix,
            )

        def _get_device(self) -> switchbot.SwitchbotDevice:
            assert 42
            return super()._get_device()

    actor = _ActorMock(mac_address="aa:bb:cc:dd:ee:ff", retry_count=42, password=None)
    with pytest.raises(NotImplementedError):
        actor.execute_command(
            mqtt_message_payload=b"dummy",
            mqtt_client="dummy",
            update_device_info=True,
            mqtt_topic_prefix="whatever",
        )
    with pytest.raises(NotImplementedError):
        actor._get_device()
