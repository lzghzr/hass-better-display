"""Platform for Monitor Control integration."""
from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaPlayerDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity


from .const import DOMAIN
from .device import MonitorDevice

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Monitor volume control."""
    device = hass.data[DOMAIN][config_entry.entry_id]
    await device.coordinator.async_config_entry_first_refresh()
    async_add_entities([MonitorVolumeMedia(device)])

class MonitorVolumeMedia(CoordinatorEntity, MediaPlayerEntity):
    """Representation of Monitor volume control."""

    def __init__(self, device: MonitorDevice) -> None:
        super().__init__(device.coordinator)
        self._device = device
        self._attr_state = MediaPlayerState.ON
        self._attr_device_class = MediaPlayerDeviceClass.RECEIVER
        self._attr_unique_id = f"{device.name}_volume"
        self._attr_name = f"{device.name} Volume"
        self._attr_device_info = device.device_info
        self._attr_supported_features = MediaPlayerEntityFeature.VOLUME_SET | \
                                        MediaPlayerEntityFeature.VOLUME_MUTE
        self._attr_icon = "mdi:volume-high"

    @property
    def is_volume_muted(self) -> bool | None:
        """Boolean if volume is currently muted."""
        return self._device.mute_state == 'on'

    @property
    def volume_level(self) -> float | None:
        """Volume level of the media player (0..1)."""
        return self._device.volume

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        await self._device.async_set_volume(volume)

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        state = "on" if mute else "off"
        await self._device.async_mute_volume(state)
