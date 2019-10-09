[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# HomeAssistant - SamsungTV Custom Component

This is a custom component to allow control of SamsungTV devices in [HomeAssistant](https://home-assistant.io). Is a modified version of the built-in [samsungtv](https://www.home-assistant.io/integrations/samsungtv/) with some extra features:

# Additional Features:

* Ability to send keys using a native Home Assistant service
* Ability to customize source list at media player dropdown list

![N|Solid](https://i.imgur.com/8mCGZoO.png)
![N|Solid](https://i.imgur.com/t3e4bJB.png)

{% if not installed %}
# Installation (There are two methods, with HACS or manual)

### 1. Easy Mode

We support [HACS](https://hacs.netlify.com/). Open HACS panel, go to Settings > Add custom repository > https://github.com/roberodin/ha-samsungtv-custom > Select Integration category and Save. After adding a repository, go to "STORE", and search "Samsungtv Custom" and install.

### 2. Manual

Install it as you would do with any homeassistant custom component:

1. Download `custom_components` folder.
2. Copy the `samsungtv_custom` direcotry within the `custom_components` directory of your homeassistant installation. The `custom_components` directory resides within your homeassistant configuration directory.
**Note**: if the custom_components directory does not exist, you need to create it.
After a correct installation, your configuration directory should look like the following.
    ```
    └── ...
    └── configuration.yaml
    └── custom_components
        └── samsungtv_custom
            └── __init__.py
            └── media_player.py
            └── manifest.json
    ```
{% endif %}

# Configuration

1. Enable the component by editing the configuration.yaml file (within the config directory as well).
Edit it by adding the following lines:
    ```
    # Example configuration.yaml entry
    media_player:
      - platform: samsungtv_custom
        host: IP_ADDRESS
        sourcelist: '{"PlayStation": "KEY_HDMI1", "RaspberryPi": "KEY_HDMI2", "Chromecast": "KEY_HDMI3"}'
    ```
    **Note**: This is the same as the configuration for the built-in [Samsung Smart TV](https://www.home-assistant.io/integrations/samsungtv/) component.

    ### Custom configuration variables

    **sourcelist:**<br/>
    (json)(Optional)<br/>
    This contains the visible sources in the dropdown list in media player UI.<br/>
    Default value: '{"TV": "KEY_TV", "HDMI": "KEY_HDMI"}'<br/>

2. Reboot Home Assistant
3. Congrats! You're all set!

# Usage

### Send Keys
```
service: media_player.play_media
```

```json
{
  "entity_id": "media_player.samsungtv",
  "media_content_type": "send_key",
  "media_content_id": "KEY_CODE",
}
```
**Note**: Change "KEY_CODEKEY" by desired key_code.

Script example:
```
tv_channel_down:
  alias: Channel down
  sequence:
  - service: media_player.play_media
    data:
      entity_id: media_player.samsung_tv55
      media_content_id: KEY_CHDOWN
      media_content_type: "send_key"
```

***Key codes***
---------------
The list of accepted keys may vary depending on the TV model, but the following list has some common key codes and their descriptions.

*Power Keys*
____________
Key|Description
---|-----------
KEY_POWEROFF|PowerOFF
KEY_POWERON|PowerOn
KEY_POWER|PowerToggle

*Input Keys*
____________
Key|Description
---|-----------
KEY_SOURCE|Source
KEY_COMPONENT1|Component1
KEY_COMPONENT2|Component2
KEY_AV1|AV1
KEY_AV2|AV2
KEY_AV3|AV3
KEY_SVIDEO1|SVideo1
KEY_SVIDEO2|SVideo2
KEY_SVIDEO3|SVideo3
KEY_HDMI|HDMI
KEY_HDMI1|HDMI1
KEY_HDMI2|HDMI2
KEY_HDMI3|HDMI3
KEY_HDMI4|HDMI4
KEY_FM_RADIO|FMRadio
KEY_DVI|DVI
KEY_DVR|DVR
KEY_TV|TV
KEY_ANTENA|AnalogTV
KEY_DTV|DigitalTV

*Number Keys*
_____________
Key|Description
---|-----------
KEY_1|Key1
KEY_2|Key2
KEY_3|Key3
KEY_4|Key4
KEY_5|Key5
KEY_6|Key6
KEY_7|Key7
KEY_8|Key8
KEY_9|Key9
KEY_0|Key0

*Misc Keys*
___________
Key|Description
---|-----------
KEY_PANNEL_CHDOWN|3D
KEY_ANYNET|AnyNet+
KEY_ESAVING|EnergySaving
KEY_SLEEP|SleepTimer
KEY_DTV_SIGNAL|DTVSignal

*Channel Keys*
______________
Key|Description
---|-----------
KEY_CHUP|ChannelUp
KEY_CHDOWN|ChannelDown
KEY_PRECH|PreviousChannel
KEY_FAVCH|FavoriteChannels
KEY_CH_LIST|ChannelList
KEY_AUTO_PROGRAM|AutoProgram
KEY_MAGIC_CHANNEL|MagicChannel

*Volume Keys*
_____________
Key|Description
---|-----------
KEY_VOLUP|VolumeUp
KEY_VOLDOWN|VolumeDown
KEY_MUTE|Mute

*Direction Keys*
________________
Key|Description
---|-----------
KEY_UP|NavigationUp
KEY_DOWN|NavigationDown
KEY_LEFT|NavigationLeft
KEY_RIGHT|NavigationRight
KEY_RETURN|NavigationReturn/Back
KEY_ENTER|NavigationEnter

*Media Keys*
____________
Key|Description
---|-----------
KEY_REWIND|Rewind
KEY_STOP|Stop
KEY_PLAY|Play
KEY_FF|FastForward
KEY_REC|Record
KEY_PAUSE|Pause
KEY_LIVE|Live
KEY_QUICK_REPLAY|fnKEY_QUICK_REPLAY
KEY_STILL_PICTURE|fnKEY_STILL_PICTURE
KEY_INSTANT_REPLAY|fnKEY_INSTANT_REPLAY

*Picture in Picture*
____________________
Key|Description
---|-----------
KEY_PIP_ONOFF|PIPOn/Off
KEY_PIP_SWAP|PIPSwap
KEY_PIP_SIZE|PIPSize
KEY_PIP_CHUP|PIPChannelUp
KEY_PIP_CHDOWN|PIPChannelDown
KEY_AUTO_ARC_PIP_SMALL|PIPSmall
KEY_AUTO_ARC_PIP_WIDE|PIPWide
KEY_AUTO_ARC_PIP_RIGHT_BOTTOM|PIPBottomRight
KEY_AUTO_ARC_PIP_SOURCE_CHANGE|PIPSourceChange
KEY_PIP_SCAN|PIPScan

*Modes*
_______
Key|Description
---|-----------
KEY_VCR_MODE|VCRMode
KEY_CATV_MODE|CATVMode
KEY_DSS_MODE|DSSMode
KEY_TV_MODE|TVMode
KEY_DVD_MODE|DVDMode
KEY_STB_MODE|STBMode
KEY_PCMODE|PCMode

*Color Keys*
____________
Key|Description
---|-----------
KEY_GREEN|Green
KEY_YELLOW|Yellow
KEY_CYAN|Cyan
KEY_RED|Red

*Teletext*
__________
Key|Description
---|-----------
KEY_TTX_MIX|TeletextMix
KEY_TTX_SUBFACE|TeletextSubface

*AspectRatio*
______________
Key|Description
---|-----------
KEY_ASPECT|AspectRatio
KEY_PICTURE_SIZE|PictureSize
KEY_4_3|AspectRatio4:3
KEY_16_9|AspectRatio16:9
KEY_EXT14|AspectRatio3:4(Alt)
KEY_EXT15|AspectRatio16:9(Alt)

*Picture Mode*
______________
Key|Description
---|-----------
KEY_PMODE|PictureMode
KEY_PANORAMA|PictureModePanorama
KEY_DYNAMIC|PictureModeDynamic
KEY_STANDARD|PictureModeStandard
KEY_MOVIE1|PictureModeMovie
KEY_GAME|PictureModeGame
KEY_CUSTOM|PictureModeCustom
KEY_EXT9|PictureModeMovie(Alt)
KEY_EXT10|PictureModeStandard(Alt)

*Menus*
_______
Key|Description
---|-----------
KEY_MENU|Menu
KEY_TOPMENU|TopMenu
KEY_TOOLS|Tools
KEY_HOME|Home
KEY_CONTENTS|Contents
KEY_GUIDE|Guide
KEY_DISC_MENU|DiscMenu
KEY_DVR_MENU|DVRMenu
KEY_HELP|Help

*OSD*
_____
Key|Description
---|-----------
KEY_INFO|Info
KEY_CAPTION|Caption
KEY_CLOCK_DISPLAY|ClockDisplay
KEY_SETUP_CLOCK_TIMER|SetupClock
KEY_SUB_TITLE|Subtitle

*Zoom*
______
Key|Description
---|-----------
KEY_ZOOM_MOVE|ZoomMove
KEY_ZOOM_IN|ZoomIn
KEY_ZOOM_OUT|ZoomOut
KEY_ZOOM1|Zoom1
KEY_ZOOM2|Zoom2

*Other Keys*
____________
Key|Description
---|-----------
KEY_WHEEL_LEFT|WheelLeft
KEY_WHEEL_RIGHT|WheelRight
KEY_ADDDEL|Add/Del
KEY_PLUS100|Plus100
KEY_AD|AD
KEY_LINK|Link
KEY_TURBO|Turbo
KEY_CONVERGENCE|Convergence
KEY_DEVICE_CONNECT|DeviceConnect
KEY_11|Key11
KEY_12|Key12
KEY_FACTORY|KeyFactory
KEY_3SPEED|Key3SPEED
KEY_RSURF|KeyRSURF
KEY_FF_|FF_
KEY_REWIND_|REWIND_
KEY_ANGLE|Angle
KEY_RESERVED1|Reserved1
KEY_PROGRAM|Program
KEY_BOOKMARK|Bookmark
KEY_PRINT|Print
KEY_CLEAR|Clear
KEY_VCHIP|VChip
KEY_REPEAT|Repeat
KEY_DOOR|Door
KEY_OPEN|Open
KEY_DMA|DMA
KEY_MTS|MTS
KEY_DNIe|DNIe
KEY_SRS|SRS
KEY_CONVERT_AUDIO_MAINSUB|ConvertAudioMain/Sub
KEY_MDC|MDC
KEY_SEFFECT|SoundEffect
KEY_PERPECT_FOCUS|PERPECTFocus
KEY_CALLER_ID|CallerID
KEY_SCALE|Scale
KEY_MAGIC_BRIGHT|MagicBright
KEY_W_LINK|WLink
KEY_DTV_LINK|DTVLink
KEY_APP_LIST|ApplicationList
KEY_BACK_MHP|BackMHP
KEY_ALT_MHP|AlternateMHP
KEY_DNSe|DNSe
KEY_RSS|RSS
KEY_ENTERTAINMENT|Entertainment
KEY_ID_INPUT|IDInput
KEY_ID_SETUP|IDSetup
KEY_ANYVIEW|AnyView
KEY_MS|MS
KEY_MORE|
KEY_MIC|
KEY_NINE_SEPERATE|
KEY_AUTO_FORMAT|AutoFormat
KEY_DNET|DNET

*Auto Arc Keys*
_______________
Key|Description
---|-----------
KEY_AUTO_ARC_C_FORCE_AGING|
KEY_AUTO_ARC_CAPTION_ENG|
KEY_AUTO_ARC_USBJACK_INSPECT|
KEY_AUTO_ARC_RESET|
KEY_AUTO_ARC_LNA_ON|
KEY_AUTO_ARC_LNA_OFF|
KEY_AUTO_ARC_ANYNET_MODE_OK|
KEY_AUTO_ARC_ANYNET_AUTO_START|
KEY_AUTO_ARC_CAPTION_ON|
KEY_AUTO_ARC_CAPTION_OFF|
KEY_AUTO_ARC_PIP_DOUBLE|
KEY_AUTO_ARC_PIP_LARGE|
KEY_AUTO_ARC_PIP_LEFT_TOP|
KEY_AUTO_ARC_PIP_RIGHT_TOP|
KEY_AUTO_ARC_PIP_LEFT_BOTTOM|
KEY_AUTO_ARC_PIP_CH_CHANGE|
KEY_AUTO_ARC_AUTOCOLOR_SUCCESS|
KEY_AUTO_ARC_AUTOCOLOR_FAIL|
KEY_AUTO_ARC_JACK_IDENT|
KEY_AUTO_ARC_CAPTION_KOR|
KEY_AUTO_ARC_ANTENNA_AIR|
KEY_AUTO_ARC_ANTENNA_CABLE|
KEY_AUTO_ARC_ANTENNA_SATELLITE|

*Panel Keys*
____________
Key|Description
---|-----------
KEY_PANNEL_POWER|
KEY_PANNEL_CHUP|
KEY_PANNEL_VOLUP|
KEY_PANNEL_VOLDOW|
KEY_PANNEL_ENTER|
KEY_PANNEL_MENU|
KEY_PANNEL_SOURCE|
KEY_PANNEL_ENTER|

<br></br>
*Extended Keys*
_______________
Key|Description
---|-----------
KEY_EXT1|
KEY_EXT2|
KEY_EXT3|
KEY_EXT4|
KEY_EXT5|
KEY_EXT6|
KEY_EXT7|
KEY_EXT8|
KEY_EXT11|
KEY_EXT12|
KEY_EXT13|
KEY_EXT16|
KEY_EXT17|
KEY_EXT18|
KEY_EXT19|
KEY_EXT20|
KEY_EXT21|
KEY_EXT22|
KEY_EXT23|
KEY_EXT24|
KEY_EXT25|
KEY_EXT26|
KEY_EXT27|
KEY_EXT28|
KEY_EXT29|
KEY_EXT30|
KEY_EXT31|
KEY_EXT32|
KEY_EXT33|
KEY_EXT34|
KEY_EXT35|
KEY_EXT36|
KEY_EXT37|
KEY_EXT38|
KEY_EXT39|
KEY_EXT40|
KEY_EXT41|

Please note that some codes are different on the 2016+ TVs. For example, `KEY_POWEROFF` is `KEY_POWER` on the newer TVs.

***References***
----------------

The code list has been extracted from: https://github.com/kdschlosser/samsungctl
