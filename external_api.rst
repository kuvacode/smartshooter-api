==========================
External API Documentation
==========================

:Version: v4.11

Copyright 2016-2019, Kuvacode Oy. All rights reserved.


Smart Shooter can be integrated with an external system by using the External
API feature. This provides two key channels of communication:

- Publisher of event information
- Server for handling command requests


Transport
---------

The External API uses the ZeroMQ library for managing the communication
transport layer. Visit http://zeromq.org for more information on how to use
ZeroMQ from your system. This also defines the programming model for using the
event publisher and request/reply server, as these are implementated as ZeroMQ
socket endpoints.


Encoding
--------

All messages passed over the External API are encoded in JSON format. Visit
http://json.org for more information on how to handle this type of message
format.


Listening to Events
-------------------

The event publisher will broadcast messages about important events that happen
inside Smart Shooter. This includes:

- When a new photo is taken
- When a photo changes state (downloaded/deleted/renamed etc)
- When a new camera is detected
- When a camera changes state
- When a camera property changes state


Sending Requests
----------------

The request/reply server inside Smart Shooter can handle requests to do various
actions such as:

- Connect/Disconnect camera
- Take photo
- Download/rename/delete photo
- Change camera property
- Auto focus camera
- Change sequence/batch number


Messages
--------

All messages include the following 3 fields:

msg_type
  Indicates whether this is a request/response or event message. Valid values
  are "Request", "Response", or "Event".

msg_id
  Indicates the contents of the message.

msg_ref_num
  Number associated with the message. For event messages, this is a unique and
  incremented number. For requests, the sender should set it to a unique number,
  and the same number will be sent back in the response message.

Subsequent fields in the message will depend on the current ``msg_id``.


Event Messages
~~~~~~~~~~~~~~

The following table lists all the valid event messages.

+-----------------+------------------------------------------------+
| msg_id          | Description                                    |
+=================+================================================+
| CameraUpdated   | Information about camera status                |
+-----------------+------------------------------------------------+
| LiveviewUpdated | internal use                                   |
+-----------------+------------------------------------------------+
| NodeUpdated     | Information about GRID node status             |
+-----------------+------------------------------------------------+
| OptionsUpdated  | Information about app options                  |
+-----------------+------------------------------------------------+
| PhotoUpdated    | Information about photo status                 |
+-----------------+------------------------------------------------+
| RelayCustomText | Send custom text to all External API listeners |
+-----------------+------------------------------------------------+


Request/Response Messages
~~~~~~~~~~~~~~~~~~~~~~~~~

The following table lists all the valid request/response messages.

+----------------------+---------------------------------------------------------------------------+
| msg_id               | Description                                                               |
+======================+===========================================================================+
| Autofocus            | Do auto focus with specified camera                                       |
+----------------------+---------------------------------------------------------------------------+
| CheckClocks          | Retrieve current date/time from all cameras                               |
+----------------------+---------------------------------------------------------------------------+
| Connect              | Connect specified camera                                                  |
+----------------------+---------------------------------------------------------------------------+
| Delete               | Delete specified photo from computer                                      |
+----------------------+---------------------------------------------------------------------------+
| DetectCameras        | Request Smart Shooter to detect connected cameras                         |
+----------------------+---------------------------------------------------------------------------+
| Disconnect           | Disconnect specified camera                                               |
+----------------------+---------------------------------------------------------------------------+
| Download             | Download specified photo from camera to computer                          |
+----------------------+---------------------------------------------------------------------------+
| EnableLiveview       | Enable/disable live view on specified camera                              |
+----------------------+---------------------------------------------------------------------------+
| EnableLiveviewDOF    | Enable/disable live view DOF (depth of field) preview on specified camera |
+----------------------+---------------------------------------------------------------------------+
| EnableLiveviewRecord | Enable/disable recording of live view images on specified camera          |
+----------------------+---------------------------------------------------------------------------+
| EnableLiveviewZoom   | Enable/disable live view zoom region on specified camera                  |
+----------------------+---------------------------------------------------------------------------+
| EnableVideo          | Start/stop video recording on specified camera                            |
+----------------------+---------------------------------------------------------------------------+
| FormatAll            | Format memory cards on all cameras                                        |
+----------------------+---------------------------------------------------------------------------+
| Identify             | Request specified camera identifies itself                                |
+----------------------+---------------------------------------------------------------------------+
| IncrementProperty    | Increment/decrement camera property on specified camera                   |
+----------------------+---------------------------------------------------------------------------+
| License              | internal use                                                              |
+----------------------+---------------------------------------------------------------------------+
| LiveviewFPS          | Set desired live view FPS for specified camera                            |
+----------------------+---------------------------------------------------------------------------+
| LiveviewFocus        | Drive live view focus motor for specified camera                          |
+----------------------+---------------------------------------------------------------------------+
| LiveviewPosition     | Change live view zoom region for specified camera                         |
+----------------------+---------------------------------------------------------------------------+
| NetworkPing          | internal use                                                              |
+----------------------+---------------------------------------------------------------------------+
| NodeEndpoint         | internal use                                                              |
+----------------------+---------------------------------------------------------------------------+
| RemoveNode           | internal use                                                              |
+----------------------+---------------------------------------------------------------------------+
| RenameCamera         | Set name for camera                                                       |
+----------------------+---------------------------------------------------------------------------+
| RenameNode           | Set name for GRID node                                                    |
+----------------------+---------------------------------------------------------------------------+
| RenamePhoto          | Set filename for photo                                                    |
+----------------------+---------------------------------------------------------------------------+
| Reshoot              | Reshoot photo using same filename on specified camera                     |
+----------------------+---------------------------------------------------------------------------+
| SetBatchNum          | Set the [B] batch number used when generating filenames                   |
+----------------------+---------------------------------------------------------------------------+
| SetCameraGroup       | Set group for camera                                                      |
+----------------------+---------------------------------------------------------------------------+
| SetOptions           | Set Smart Shooter options                                                 |
+----------------------+---------------------------------------------------------------------------+
| SetProperty          | Set camera property on specified camera                                   |
+----------------------+---------------------------------------------------------------------------+
| SetSequenceNum       | Set the [S] sequence number used when generating filenames                |
+----------------------+---------------------------------------------------------------------------+
| SetShutterButton     | Set shutter button state for specified camera                             |
+----------------------+---------------------------------------------------------------------------+
| Shoot                | Take photo with specified camera                                          |
+----------------------+---------------------------------------------------------------------------+
| SyncBatchNum         | Force batch numbers back in sync for all cameras                          |
+----------------------+---------------------------------------------------------------------------+
| SyncClocks           | Synchronise clocks on all cameras                                         |
+----------------------+---------------------------------------------------------------------------+
| Synchronise          | Request latest information about cameras/photos                           |
+----------------------+---------------------------------------------------------------------------+
| TransferPhoto        | internal use                                                              |
+----------------------+---------------------------------------------------------------------------+


Fields
------

Each field is expected to contain data is a certain format. The different
data types are listed below:

+----------+-----------------------------------+
| Type     | Description                       |
+==========+===================================+
| string   | UTF-8 encoded string              |
+----------+-----------------------------------+
| string[] | Array of strings                  |
+----------+-----------------------------------+
| boolean  | true or false                     |
+----------+-----------------------------------+
| float    | Floating point number             |
+----------+-----------------------------------+
| int32    | Integer in range of int32_t       |
+----------+-----------------------------------+
| int64    | Integer in range of uint32_t      |
+----------+-----------------------------------+
| uint32   | Integer in range of int64_t       |
+----------+-----------------------------------+
| uint64   | Integer in range of uint64_t      |
+----------+-----------------------------------+
| data     | Binary data (internal use only)   |
+----------+-----------------------------------+
| object   | JSON object containing sub-fields |
+----------+-----------------------------------+
| object[] | Array of objects                  |
+----------+-----------------------------------+


Camera and Photo Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~

Each camera and photo is given a 'key', which as a text string that uniquely
identifies that camera/photo.

When a particular camera or photo needs to be specified on a message, there are
some dedicated fields for this. They allow a single camera to be specifed, or a
specific set of cameras, or simply just all cameras.

The first field is ``CameraSelection``, this controls whether the selection is:

All
  Selects all cameras.

Single
  Selects a single specific camera. The camera is then identified by the
  ``CameraKey`` field.

Group
  Selects all the cameras from a specific group. The group is then identified
  by the ``CameraGroup`` field.

Multiple
  Selects a set of specific cameras. The set of cameras is then identified by
  the ``CameraKeys`` field.

The same concept applies to photo selection, using the fields
``PhotoSelection``, ``PhotoKey``, and ``PhotoKeys``.

In the field definition list, these fields are referred to as
``[CAMERA SELECTION FIELDS]`` and ``[PHOTO SELECTION FIELDS]``, when definining
the list of sub-fields that can be contained in a JSON ``object``.


List of Fields
~~~~~~~~~~~~~~

+----------------------------------+------------------------------------------------------------------------+
| Name                             | Description                                                            |
+==================================+========================================================================+
| AutoConnect                      | Contains the value for the 'Auto Connect' option                       |
+----------------------------------+------------------------------------------------------------------------+
| AutoSynchroniseTime              | Contains the value for the 'Auto Synchronise Time' option              |
+----------------------------------+------------------------------------------------------------------------+
| Autofocus                        | Contains fields for the Autofocus request                              |
+----------------------------------+------------------------------------------------------------------------+
| Barcode                          | Contains the [Z] barcode text                                          |
+----------------------------------+------------------------------------------------------------------------+
| BulbTimer                        | Bulb timer interval for bulb mode capture                              |
+----------------------------------+------------------------------------------------------------------------+
| CameraAutofocusIsSupported       | Indicates if camera supports auto focus                                |
+----------------------------------+------------------------------------------------------------------------+
| CameraBatterylevel               | Indicates camera battery level in range 0 to 100                       |
+----------------------------------+------------------------------------------------------------------------+
| CameraBulbIsEnabled              | Indicates whether buld shooting mode is enabled                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraBulbIsSupported            | Indicates whether buld shooting mode is supported                      |
+----------------------------------+------------------------------------------------------------------------+
| CameraDateTimeOffset             | Contains offset from local time for when syncing date/time             |
+----------------------------------+------------------------------------------------------------------------+
| CameraDownloadRate               | Transfer rate for last photo download in mbytes/sec                    |
+----------------------------------+------------------------------------------------------------------------+
| CameraGroup                      | Group that camera belongs to                                           |
+----------------------------------+------------------------------------------------------------------------+
| CameraInfo                       | Contains fields for the CameraInfo object                              |
+----------------------------------+------------------------------------------------------------------------+
| CameraIsFocused                  | Indicates of camera auto focus action was successful                   |
+----------------------------------+------------------------------------------------------------------------+
| CameraKey                        | Unique identfier for a camera                                          |
+----------------------------------+------------------------------------------------------------------------+
| CameraKeys                       | Array of unique camera identifiers                                     |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewAFRegionBottom     | Bottom pixel of camera's active auto focus region                      |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewAFRegionLeft       | Left pixel of camera's active auto focus region                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewAFRegionRight      | Right pixel of camera's active auto focus region                       |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewAFRegionTop        | Top pixel of camera's active auto focus region                         |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewDOFIsEnabled       | Indicates whether camera live view DOF preview is enabled              |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewDOFIsSupported     | Indicates if camera live view supports DOF (depth of field) preview    |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewFPS                | Desired FPS of camera live view stream                                 |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewFocusIsSupported   | Indicates if camera live view supports moving focus                    |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewFocusStep          | Specifies camera live view focus motor movement                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewIsEnabled          | Indicates whether camera live view is enabled                          |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewIsSupported        | Indicates if camera supports live view                                 |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewNumFrames          | The number of liveview frames since liveview was enabled               |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewSensorHeight       | Height of camera's sensor in pixels                                    |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewSensorRegionBottom | Bottom pixel of camera's active live view region                       |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewSensorRegionLeft   | Left pixel of camera's active live view region                         |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewSensorRegionRight  | Right pixel of camera's active live view region                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewSensorRegionTop    | Top pixel of camera's active live view region                          |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewSensorWidth        | Width of camera's sensor in pixels                                     |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewVideoFPS           | Desired FPS of camera live view stream during video recording          |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewZoomIsEnabled      | Indicates whether camera live view zoom region is enabled              |
+----------------------------------+------------------------------------------------------------------------+
| CameraLiveviewZoomIsSupported    | Indicates if camera live view supports a zoom region                   |
+----------------------------------+------------------------------------------------------------------------+
| CameraMake                       | Make of camera                                                         |
+----------------------------------+------------------------------------------------------------------------+
| CameraMirrorLockupIsEnabled      | Indicates whether mirror lockup is enabled                             |
+----------------------------------+------------------------------------------------------------------------+
| CameraMirrorLockupIsSupported    | Indicates whether mirror lockup (MLU) is supported                     |
+----------------------------------+------------------------------------------------------------------------+
| CameraModel                      | Model of camera                                                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraName                       | Name of camera                                                         |
+----------------------------------+------------------------------------------------------------------------+
| CameraNumAutofocus               | Number of camera auto focus attempts                                   |
+----------------------------------+------------------------------------------------------------------------+
| CameraNumCards                   | Number of memory cards in camera                                       |
+----------------------------------+------------------------------------------------------------------------+
| CameraNumDownloadsComplete       | Number of photos downloaded from camera                                |
+----------------------------------+------------------------------------------------------------------------+
| CameraNumDownloadsFailed         | Number of failed photo download attempts                               |
+----------------------------------+------------------------------------------------------------------------+
| CameraNumPhotosFailed            | Number of failed photo attempts                                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraNumPhotosTaken             | Number of photos taken by camera                                       |
+----------------------------------+------------------------------------------------------------------------+
| CameraPowersource                | Indicates camera power source                                          |
+----------------------------------+------------------------------------------------------------------------+
| CameraPropertyInfo               | Contains fields for the CameraPropertyInfo object                      |
+----------------------------------+------------------------------------------------------------------------+
| CameraPropertyIsWriteable        | Indicates whether a camera property can be changed                     |
+----------------------------------+------------------------------------------------------------------------+
| CameraPropertyRange              | Array of valid values for a camera property                            |
+----------------------------------+------------------------------------------------------------------------+
| CameraPropertyStep               | Contains range step for IncrementProperty message                      |
+----------------------------------+------------------------------------------------------------------------+
| CameraPropertyType               | Specifies a camera property                                            |
+----------------------------------+------------------------------------------------------------------------+
| CameraPropertyValue              | Contains value for the camera property                                 |
+----------------------------------+------------------------------------------------------------------------+
| CameraSelection                  | Determines the camera selection                                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraSerialNumber               | Serial number of camera                                                |
+----------------------------------+------------------------------------------------------------------------+
| CameraShutterButton              | Virtual state of camera's shutter button                               |
+----------------------------------+------------------------------------------------------------------------+
| CameraStatus                     | Status of camera                                                       |
+----------------------------------+------------------------------------------------------------------------+
| CameraUpdated                    | Contains fields for the CameraUpdated event                            |
+----------------------------------+------------------------------------------------------------------------+
| CameraVideoElapsedTime           | Elapsed time of video recording in milliseconds                        |
+----------------------------------+------------------------------------------------------------------------+
| CameraVideoIsEnabled             | Indicates whether video is being recorded                              |
+----------------------------------+------------------------------------------------------------------------+
| CameraVideoIsSupported           | Indicates whether video recording is supported                         |
+----------------------------------+------------------------------------------------------------------------+
| CheckClocks                      | Contains fields for the CheckClocks request                            |
+----------------------------------+------------------------------------------------------------------------+
| Connect                          | Contains fields for the Connect request                                |
+----------------------------------+------------------------------------------------------------------------+
| CustomText                       | Field that can contain arbitrary text                                  |
+----------------------------------+------------------------------------------------------------------------+
| DefaultFocusMode                 | Contains the default camera focus mode                                 |
+----------------------------------+------------------------------------------------------------------------+
| DefaultStorage                   | Contains the default camera storage mode                               |
+----------------------------------+------------------------------------------------------------------------+
| Delete                           | Contains fields for the Delete request                                 |
+----------------------------------+------------------------------------------------------------------------+
| DetectCameras                    | Contains fields for the DetectCameras request                          |
+----------------------------------+------------------------------------------------------------------------+
| Disconnect                       | Contains fields for the Disconnect request                             |
+----------------------------------+------------------------------------------------------------------------+
| Download                         | Contains fields for the Download request                               |
+----------------------------------+------------------------------------------------------------------------+
| DownloadPath                     | Contains value for the 'Photo Download Directory' option               |
+----------------------------------+------------------------------------------------------------------------+
| Enable                           | Generic indicator for enabling/disabling some state                    |
+----------------------------------+------------------------------------------------------------------------+
| EnableLiveview                   | Contains fields for the EnableLiveview request                         |
+----------------------------------+------------------------------------------------------------------------+
| EnableLiveviewDOF                | Contains fields for the EnableLiveviewDOF request                      |
+----------------------------------+------------------------------------------------------------------------+
| EnableLiveviewRecord             | Contains fields for the EnableLiveviewRecord request                   |
+----------------------------------+------------------------------------------------------------------------+
| EnableLiveviewZoom               | Contains fields for the EnableLiveviewZoom request                     |
+----------------------------------+------------------------------------------------------------------------+
| EnableVideo                      | Contains fields for the EnableVideo request                            |
+----------------------------------+------------------------------------------------------------------------+
| FallbackPath                     | Contains value for the fallback photo download path                    |
+----------------------------------+------------------------------------------------------------------------+
| FilenameExpression               | Contains the filename expression option                                |
+----------------------------------+------------------------------------------------------------------------+
| FormatAll                        | Contains fields for the FormatAll request                              |
+----------------------------------+------------------------------------------------------------------------+
| Identify                         | Contains fields for the Identify request                               |
+----------------------------------+------------------------------------------------------------------------+
| IncrementProperty                | Contains fields for the IncrementProperty request                      |
+----------------------------------+------------------------------------------------------------------------+
| LiveviewFPS                      | Contains fields for the LiveviewFPS request                            |
+----------------------------------+------------------------------------------------------------------------+
| LiveviewFocus                    | Contains fields for the LiveviewFocus request                          |
+----------------------------------+------------------------------------------------------------------------+
| LiveviewPosition                 | Contains fields for the LiveviewPosition request                       |
+----------------------------------+------------------------------------------------------------------------+
| OptionsInfo                      | Contains fields for OptionsInfo object                                 |
+----------------------------------+------------------------------------------------------------------------+
| OptionsUpdated                   | Contains fields for the OptionsUpdated event                           |
+----------------------------------+------------------------------------------------------------------------+
| PhotoAperture                    | Lens aperture of photo                                                 |
+----------------------------------+------------------------------------------------------------------------+
| PhotoBarcode                     | Contains barcode text scanned from photo                               |
+----------------------------------+------------------------------------------------------------------------+
| PhotoBatchNum                    | Contains the [B] batch number                                          |
+----------------------------------+------------------------------------------------------------------------+
| PhotoComputedName                | Photo name generated by Smart Shooter, before filename collision check |
+----------------------------------+------------------------------------------------------------------------+
| PhotoDateCaptured                | Data/time that photo was captured by camera                            |
+----------------------------------+------------------------------------------------------------------------+
| PhotoFilesize                    | Size of photo file                                                     |
+----------------------------------+------------------------------------------------------------------------+
| PhotoFocalLength                 | Lens focal length of photo                                             |
+----------------------------------+------------------------------------------------------------------------+
| PhotoFormat                      | Format of photo image file                                             |
+----------------------------------+------------------------------------------------------------------------+
| PhotoHash                        | Hash of photo data contents                                            |
+----------------------------------+------------------------------------------------------------------------+
| PhotoHeight                      | Height of photo                                                        |
+----------------------------------+------------------------------------------------------------------------+
| PhotoISO                         | Camera ISO of photo                                                    |
+----------------------------------+------------------------------------------------------------------------+
| PhotoInfo                        | Contains fields for the PhotoInfo object                               |
+----------------------------------+------------------------------------------------------------------------+
| PhotoIsHidden                    | Indicates whether photo is hidden                                      |
+----------------------------------+------------------------------------------------------------------------+
| PhotoIsImage                     | Indicates whether photo is image or not (possible video file)          |
+----------------------------------+------------------------------------------------------------------------+
| PhotoIsScanned                   | Indicates if barcode has been scanned from photo                       |
+----------------------------------+------------------------------------------------------------------------+
| PhotoKey                         | Unique identifier for a photo                                          |
+----------------------------------+------------------------------------------------------------------------+
| PhotoKeys                        | Array of unique photo identifiers                                      |
+----------------------------------+------------------------------------------------------------------------+
| PhotoLocation                    | Location of photo file                                                 |
+----------------------------------+------------------------------------------------------------------------+
| PhotoName                        | Photo name once finally saved to disk                                  |
+----------------------------------+------------------------------------------------------------------------+
| PhotoOrientation                 | Orientation of photo                                                   |
+----------------------------------+------------------------------------------------------------------------+
| PhotoOrigin                      | Identifier for origin of photo                                         |
+----------------------------------+------------------------------------------------------------------------+
| PhotoOriginalName                | Original name of photo on camera                                       |
+----------------------------------+------------------------------------------------------------------------+
| PhotoSelection                   | Determines the photo selection                                         |
+----------------------------------+------------------------------------------------------------------------+
| PhotoSequenceNum                 | Contains the [S] sequence number                                       |
+----------------------------------+------------------------------------------------------------------------+
| PhotoSessionName                 | Contains the [N] session name                                          |
+----------------------------------+------------------------------------------------------------------------+
| PhotoSessionNum                  | Contains the [I] session number                                        |
+----------------------------------+------------------------------------------------------------------------+
| PhotoShutterSpeed                | Camera shutter speed of photo                                          |
+----------------------------------+------------------------------------------------------------------------+
| PhotoUUID                        | Internal UUID of photo                                                 |
+----------------------------------+------------------------------------------------------------------------+
| PhotoUpdated                     | Contains fields for the PhotoUpdated event                             |
+----------------------------------+------------------------------------------------------------------------+
| PhotoWidth                       | Width of photo                                                         |
+----------------------------------+------------------------------------------------------------------------+
| RelayCustomText                  | Contains fields for the RelayCustomText event                          |
+----------------------------------+------------------------------------------------------------------------+
| RenameCamera                     | Contains fields for the RenameCamera request                           |
+----------------------------------+------------------------------------------------------------------------+
| RenamePhoto                      | Contains fields for the RenamePhoto request                            |
+----------------------------------+------------------------------------------------------------------------+
| Reshoot                          | Contains fields for the Reshoot request                                |
+----------------------------------+------------------------------------------------------------------------+
| SetBatchNum                      | Contains fields for the SetBatchNum request                            |
+----------------------------------+------------------------------------------------------------------------+
| SetCameraGroup                   | Contains fields for the SetCameraGroup request                         |
+----------------------------------+------------------------------------------------------------------------+
| SetOptions                       | Contains fields for SetOptions request                                 |
+----------------------------------+------------------------------------------------------------------------+
| SetProperty                      | Contains fields for the SetProperty request                            |
+----------------------------------+------------------------------------------------------------------------+
| SetSequenceNum                   | Contains fields for SetSequenceNum request                             |
+----------------------------------+------------------------------------------------------------------------+
| SetShutterButton                 | Contains fields for the SetShutterButton request                       |
+----------------------------------+------------------------------------------------------------------------+
| Shoot                            | Contains fields for the Shoot request                                  |
+----------------------------------+------------------------------------------------------------------------+
| SyncBatchNum                     | Contains fields for the SyncBatchNum request                           |
+----------------------------------+------------------------------------------------------------------------+
| SyncClocks                       | Contains fields for the SyncClocks request                             |
+----------------------------------+------------------------------------------------------------------------+
| Synchronise                      | Contains fields for the Synchronise request                            |
+----------------------------------+------------------------------------------------------------------------+
| UniqueTag                        | Contains the [U] unique tag                                            |
+----------------------------------+------------------------------------------------------------------------+
| msg_id                           | Identifier string for message type                                     |
+----------------------------------+------------------------------------------------------------------------+
| msg_result                       | Generic result field indicating success or failure                     |
+----------------------------------+------------------------------------------------------------------------+
| msg_seq_num                      | Message sequence number                                                |
+----------------------------------+------------------------------------------------------------------------+
| msg_type                         | Indicates whether message is request/response or event                 |
+----------------------------------+------------------------------------------------------------------------+
| msg_user_id                      | Custom user ID number                                                  |
+----------------------------------+------------------------------------------------------------------------+


Field Definitions
~~~~~~~~~~~~~~~~~

The following sections defines all the valid fields, along with associated data
type. The fields that are JSON objects, it lists the valid sub-fields that may
be contained within that object.

AutoConnect
  :Type:            boolean
  :Description:     Contains the value for the 'Auto Connect' option

AutoSynchroniseTime
  :Type:            boolean
  :Description:     Contains the value for the 'Auto Synchronise Time' option

Autofocus
  :Type:            object
  :Description:     Contains fields for the Autofocus request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"

Barcode
  :Type:            string
  :Description:     Contains the [Z] barcode text

BulbTimer
  :Type:            int64
  :Description:     Bulb timer interval for bulb mode capture

CameraAutofocusIsSupported
  :Type:            boolean
  :Description:     Indicates if camera supports auto focus

CameraBatterylevel
  :Type:            int32
  :Description:     Indicates camera battery level in range 0 to 100

CameraBulbIsEnabled
  :Type:            boolean
  :Description:     Indicates whether buld shooting mode is enabled

CameraBulbIsSupported
  :Type:            boolean
  :Description:     Indicates whether buld shooting mode is supported

CameraDateTimeOffset
  :Type:            int64
  :Description:     Contains offset from local time for when syncing date/time

CameraDownloadRate
  :Type:            float
  :Description:     Transfer rate for last photo download in mbytes/sec

CameraGroup
  :Type:            string
  :Description:     Group that camera belongs to

CameraInfo
  :Type:            object
  :Description:     Contains fields for the CameraInfo object
  :Fields:          - "[CAMERA SELECTION FIELDS]"
                    - "CameraStatus"
                    - "CameraName"
                    - "CameraGroup"
                    - "CameraSerialNumber"
                    - "CameraMake"
                    - "CameraModel"
                    - "CameraNumCards"
                    - "PhotoBatchNum"
                    - "CameraDateTimeOffset"
                    - "CameraAutofocusIsSupported"
                    - "CameraIsFocused"
                    - "CameraLiveviewIsSupported"
                    - "CameraLiveviewZoomIsSupported"
                    - "CameraLiveviewDOFIsSupported"
                    - "CameraLiveviewFocusIsSupported"
                    - "CameraLiveviewIsEnabled"
                    - "CameraLiveviewZoomIsEnabled"
                    - "CameraLiveviewDOFIsEnabled"
                    - "CameraLiveviewNumFrames"
                    - "CameraLiveviewSensorWidth"
                    - "CameraLiveviewSensorHeight"
                    - "CameraLiveviewSensorRegionLeft"
                    - "CameraLiveviewSensorRegionBottom"
                    - "CameraLiveviewSensorRegionRight"
                    - "CameraLiveviewSensorRegionTop"
                    - "CameraLiveviewAFRegionLeft"
                    - "CameraLiveviewAFRegionBottom"
                    - "CameraLiveviewAFRegionRight"
                    - "CameraLiveviewAFRegionTop"
                    - "CameraVideoIsSupported"
                    - "CameraVideoIsEnabled"
                    - "CameraVideoElapsedTime"
                    - "CameraBulbIsSupported"
                    - "CameraBulbIsEnabled"
                    - "CameraPowersource"
                    - "CameraBatterylevel"
                    - "CameraDownloadRate"
                    - "CameraNumPhotosTaken"
                    - "CameraNumPhotosFailed"
                    - "CameraNumDownloadsComplete"
                    - "CameraNumDownloadsFailed"
                    - "CameraNumAutofocus"
                    - "CameraPropertyInfo[]"
                    - "NodeKey"

CameraIsFocused
  :Type:            boolean
  :Description:     Indicates of camera auto focus action was successful

CameraKey
  :Type:            string
  :Description:     Unique identfier for a camera

CameraKeys
  :Type:            string[]
  :Description:     Array of unique camera identifiers

CameraLiveviewAFRegionBottom
  :Type:            float
  :Description:     Bottom pixel of camera's active auto focus region

CameraLiveviewAFRegionLeft
  :Type:            float
  :Description:     Left pixel of camera's active auto focus region

CameraLiveviewAFRegionRight
  :Type:            float
  :Description:     Right pixel of camera's active auto focus region

CameraLiveviewAFRegionTop
  :Type:            float
  :Description:     Top pixel of camera's active auto focus region

CameraLiveviewDOFIsEnabled
  :Type:            boolean
  :Description:     Indicates whether camera live view DOF preview is enabled

CameraLiveviewDOFIsSupported
  :Type:            boolean
  :Description:     Indicates if camera live view supports DOF (depth of field) preview

CameraLiveviewFPS
  :Type:            int32
  :Description:     Desired FPS of camera live view stream

CameraLiveviewFocusIsSupported
  :Type:            boolean
  :Description:     Indicates if camera live view supports moving focus

CameraLiveviewFocusStep
  :Type:            string
  :Description:     Specifies camera live view focus motor movement
  :Valid range:     - "Near1"
                    - "Near2"
                    - "Near3"
                    - "Far1"
                    - "Far2"
                    - "Far3"

CameraLiveviewImage
  :Type:            data
  :Description:     internal use

CameraLiveviewIsEnabled
  :Type:            boolean
  :Description:     Indicates whether camera live view is enabled

CameraLiveviewIsSupported
  :Type:            boolean
  :Description:     Indicates if camera supports live view

CameraLiveviewNumFrames
  :Type:            uint32
  :Description:     The number of liveview frames since liveview was enabled

CameraLiveviewSensorHeight
  :Type:            int32
  :Description:     Height of camera's sensor in pixels

CameraLiveviewSensorRegionBottom
  :Type:            float
  :Description:     Bottom pixel of camera's active live view region

CameraLiveviewSensorRegionLeft
  :Type:            float
  :Description:     Left pixel of camera's active live view region

CameraLiveviewSensorRegionRight
  :Type:            float
  :Description:     Right pixel of camera's active live view region

CameraLiveviewSensorRegionTop
  :Type:            float
  :Description:     Top pixel of camera's active live view region

CameraLiveviewSensorWidth
  :Type:            int32
  :Description:     Width of camera's sensor in pixels

CameraLiveviewVideoFPS
  :Type:            int32
  :Description:     Desired FPS of camera live view stream during video recording

CameraLiveviewZoomIsEnabled
  :Type:            boolean
  :Description:     Indicates whether camera live view zoom region is enabled

CameraLiveviewZoomIsSupported
  :Type:            boolean
  :Description:     Indicates if camera live view supports a zoom region

CameraMake
  :Type:            string
  :Description:     Make of camera

CameraMirrorLockupIsEnabled
  :Type:            boolean
  :Description:     Indicates whether mirror lockup is enabled

CameraMirrorLockupIsSupported
  :Type:            boolean
  :Description:     Indicates whether mirror lockup (MLU) is supported

CameraModel
  :Type:            string
  :Description:     Model of camera

CameraName
  :Type:            string
  :Description:     Name of camera

CameraNumAutofocus
  :Type:            int32
  :Description:     Number of camera auto focus attempts

CameraNumCards
  :Type:            int32
  :Description:     Number of memory cards in camera

CameraNumDownloadsComplete
  :Type:            int32
  :Description:     Number of photos downloaded from camera

CameraNumDownloadsFailed
  :Type:            int32
  :Description:     Number of failed photo download attempts

CameraNumPhotosFailed
  :Type:            int32
  :Description:     Number of failed photo attempts

CameraNumPhotosTaken
  :Type:            int32
  :Description:     Number of photos taken by camera

CameraPowersource
  :Type:            string
  :Description:     Indicates camera power source
  :Valid range:     - "AC"
                    - "Battery"
                    - "Unknown"

CameraPropertyInfo
  :Type:            object
  :Description:     Contains fields for the CameraPropertyInfo object
  :Fields:          - "CameraPropertyType"
                    - "CameraPropertyValue"
                    - "CameraPropertyIsWriteable"
                    - "CameraPropertyRange"

CameraPropertyIsWriteable
  :Type:            boolean
  :Description:     Indicates whether a camera property can be changed

CameraPropertyRange
  :Type:            string[]
  :Description:     Array of valid values for a camera property

CameraPropertyStep
  :Type:            string
  :Description:     Contains range step for IncrementProperty message

CameraPropertyType
  :Type:            string
  :Description:     Specifies a camera property
  :Valid range:     - "Aperture"
                    - "ShutterSpeed"
                    - "ISO"
                    - "Exposure"
                    - "Quality"
                    - "ProgramMode"
                    - "MeteringMode"
                    - "FocusMode"
                    - "DriveMode"
                    - "WhiteBalance"
                    - "Storage"
                    - "MirrorLockup"

CameraPropertyValue
  :Type:            string
  :Description:     Contains value for the camera property

CameraSelection
  :Type:            string
  :Description:     Determines the camera selection
  :Valid range:     - "All"
                    - "Single"
                    - "Group"
                    - "Multiple"

CameraSerialNumber
  :Type:            string
  :Description:     Serial number of camera

CameraShutterButton
  :Type:            string
  :Description:     Virtual state of camera's shutter button
  :Valid range:     - "Off"
                    - "Half"
                    - "Full"

CameraStatus
  :Type:            string
  :Description:     Status of camera
  :Valid range:     - "Absent"
                    - "Lost"
                    - "Disconnected"
                    - "Ready"
                    - "Busy"
                    - "Error"

CameraUpdated
  :Type:            object
  :Description:     Contains fields for the CameraUpdated event
  :Event fields:    - "[CameraInfo FIELDS]"

CameraVideoElapsedTime
  :Type:            int64
  :Description:     Elapsed time of video recording in milliseconds

CameraVideoIsEnabled
  :Type:            boolean
  :Description:     Indicates whether video is being recorded

CameraVideoIsSupported
  :Type:            boolean
  :Description:     Indicates whether video recording is supported

CheckClocks
  :Type:            object
  :Description:     Contains fields for the CheckClocks request

Connect
  :Type:            object
  :Description:     Contains fields for the Connect request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"

CustomText
  :Type:            string
  :Description:     Field that can contain arbitrary text

DefaultFocusMode
  :Type:            string
  :Description:     Contains the default camera focus mode
  :Valid range:     - "Not set"
                    - "AF Single"
                    - "AF Continuous"
                    - "AF Auto"
                    - "MF"

DefaultStorage
  :Type:            string
  :Description:     Contains the default camera storage mode
  :Valid range:     - "Disk"
                    - "Card"
                    - "Both"

Delete
  :Type:            object
  :Description:     Contains fields for the Delete request
  :Request fields:  - "[PHOTO SELECTION FIELDS]"

DetectCameras
  :Type:            object
  :Description:     Contains fields for the DetectCameras request

Disconnect
  :Type:            object
  :Description:     Contains fields for the Disconnect request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"

Download
  :Type:            object
  :Description:     Contains fields for the Download request
  :Request fields:  - "[PHOTO SELECTION FIELDS]"

DownloadPath
  :Type:            string
  :Description:     Contains value for the 'Photo Download Directory' option

Enable
  :Type:            boolean
  :Description:     Generic indicator for enabling/disabling some state

EnableLiveview
  :Type:            object
  :Description:     Contains fields for the EnableLiveview request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "Enable"

EnableLiveviewDOF
  :Type:            object
  :Description:     Contains fields for the EnableLiveviewDOF request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "Enable"

EnableLiveviewRecord
  :Type:            object
  :Description:     Contains fields for the EnableLiveviewRecord request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "Enable"

EnableLiveviewZoom
  :Type:            object
  :Description:     Contains fields for the EnableLiveviewZoom request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "Enable"

EnableVideo
  :Type:            object
  :Description:     Contains fields for the EnableVideo request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "Enable"

FallbackPath
  :Type:            string
  :Description:     Contains value for the fallback photo download path

FilenameExpression
  :Type:            string
  :Description:     Contains the filename expression option

FormatAll
  :Type:            object
  :Description:     Contains fields for the FormatAll request

Identify
  :Type:            object
  :Description:     Contains fields for the Identify request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"

IncrementProperty
  :Type:            object
  :Description:     Contains fields for the IncrementProperty request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraPropertyType"
                    - "CameraPropertyStep"

License
  :Type:            object
  :Description:     internal use

License
  :Type:            string
  :Description:     internal use

LiveviewFPS
  :Type:            object
  :Description:     Contains fields for the LiveviewFPS request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraLiveviewFPS"
                    - "CameraLiveviewVideoFPS"

LiveviewFocus
  :Type:            object
  :Description:     Contains fields for the LiveviewFocus request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraLiveviewFocusStep"

LiveviewPosition
  :Type:            object
  :Description:     Contains fields for the LiveviewPosition request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraLiveviewPositionX"
                    - "CameraLiveviewPositionY"

LiveviewUpdated
  :Type:            object
  :Description:     internal use

NetworkAddress
  :Type:            string
  :Description:     internal use

NetworkDiscovery
  :Type:            object
  :Description:     internal use

NetworkEndpoint
  :Type:            string
  :Description:     internal use

NetworkPing
  :Type:            object
  :Description:     internal use

NetworkPort
  :Type:            int32
  :Description:     internal use

NetworkTimestamp
  :Type:            uint64
  :Description:     internal use

NetworkVersion
  :Type:            string
  :Description:     internal use

NodeEndpoint
  :Type:            string
  :Description:     internal use

NodeEndpoint
  :Type:            object
  :Description:     internal use

NodeInfo
  :Type:            object
  :Description:     internal use

NodeIsLiveviewConsumer
  :Type:            boolean
  :Description:     internal use

NodeIsMaster
  :Type:            boolean
  :Description:     internal use

NodeKey
  :Type:            string
  :Description:     internal use

NodeKeys
  :Type:            string[]
  :Description:     internal use

NodeName
  :Type:            string
  :Description:     internal use

NodePlatform
  :Type:            string
  :Description:     internal use

NodeSelection
  :Type:            string
  :Description:     internal use

NodeSyncLocal
  :Type:            boolean
  :Description:     internal use

NodeSyncVersion
  :Type:            uint32
  :Description:     internal use

NodeTransferMode
  :Type:            float
  :Description:     internal use

NodeUpdated
  :Type:            object
  :Description:     internal use

NodeVersion
  :Type:            string
  :Description:     internal use

OptionsInfo
  :Type:            object
  :Description:     Contains fields for OptionsInfo object
  :Fields:          - "FilenameExpression"
                    - "PhotoSessionName"
                    - "PhotoSessionNum"
                    - "UniqueTag"
                    - "Barcode"
                    - "DefaultStorage"
                    - "DefaultFocusMode"
                    - "AutoConnect"
                    - "AutoSynchroniseTime"
                    - "DownloadPath"
                    - "FallbackPath"

OptionsUpdated
  :Type:            object
  :Description:     Contains fields for the OptionsUpdated event
  :Event fields:    - "[OptionsInfo FIELDS]"

PhotoAperture
  :Type:            string
  :Description:     Lens aperture of photo

PhotoBarcode
  :Type:            string
  :Description:     Contains barcode text scanned from photo

PhotoBatchNum
  :Type:            int32
  :Description:     Contains the [B] batch number

PhotoComputedName
  :Type:            string
  :Description:     Photo name generated by Smart Shooter, before filename collision check

PhotoDateCaptured
  :Type:            string
  :Description:     Data/time that photo was captured by camera

PhotoFilesize
  :Type:            uint64
  :Description:     Size of photo file

PhotoFocalLength
  :Type:            string
  :Description:     Lens focal length of photo

PhotoFormat
  :Type:            string
  :Description:     Format of photo image file
  :Valid range:     - "JPEG"
                    - "PNG"
                    - "Raw"
                    - "TGA"
                    - "TIFF"
                    - "Unknown"

PhotoHash
  :Type:            string
  :Description:     Hash of photo data contents

PhotoHeight
  :Type:            int32
  :Description:     Height of photo

PhotoISO
  :Type:            string
  :Description:     Camera ISO of photo

PhotoInfo
  :Type:            object
  :Description:     Contains fields for the PhotoInfo object
  :Fields:          - "[PHOTO SELECTION FIELDS]"
                    - "PhotoLocation"
                    - "PhotoUUID"
                    - "PhotoName"
                    - "PhotoOriginalName"
                    - "PhotoComputedName"
                    - "PhotoDateCaptured"
                    - "PhotoOrigin"
                    - "PhotoFormat"
                    - "PhotoOrientation"
                    - "PhotoWidth"
                    - "PhotoHeight"
                    - "PhotoAperture"
                    - "PhotoShutterSpeed"
                    - "PhotoISO"
                    - "PhotoFocalLength"
                    - "PhotoFilesize"
                    - "PhotoIsImage"
                    - "PhotoIsHidden"
                    - "PhotoIsScanned"
                    - "PhotoHash"
                    - "PhotoBarcode"
                    - "PhotoSequenceNum"
                    - "PhotoBatchNum"
                    - "PhotoSessionNum"
                    - "PhotoSessionName"
                    - "CameraKey"
                    - "NodeKey"

PhotoIsHidden
  :Type:            boolean
  :Description:     Indicates whether photo is hidden

PhotoIsImage
  :Type:            boolean
  :Description:     Indicates whether photo is image or not (possible video file)

PhotoIsScanned
  :Type:            boolean
  :Description:     Indicates if barcode has been scanned from photo

PhotoKey
  :Type:            string
  :Description:     Unique identifier for a photo

PhotoKeys
  :Type:            string[]
  :Description:     Array of unique photo identifiers

PhotoLocation
  :Type:            string
  :Description:     Location of photo file
  :Valid range:     - "Orphaned"
                    - "Deleted"
                    - "Camera"
                    - "Local Disk"

PhotoName
  :Type:            string
  :Description:     Photo name once finally saved to disk

PhotoOrientation
  :Type:            string
  :Description:     Orientation of photo
  :Valid range:     - "None"
                    - "Rotate270"
                    - "Rotate180"
                    - "Rotate90"
                    - "FlipY"
                    - "InverseTranspose"
                    - "FlipX"
                    - "Transpose"
                    - "Unknown"

PhotoOrigin
  :Type:            string
  :Description:     Identifier for origin of photo

PhotoOriginalName
  :Type:            string
  :Description:     Original name of photo on camera

PhotoSelection
  :Type:            string
  :Description:     Determines the photo selection
  :Valid range:     - "All"
                    - "Single"
                    - "Multiple"

PhotoSequenceNum
  :Type:            int32
  :Description:     Contains the [S] sequence number

PhotoSessionName
  :Type:            string
  :Description:     Contains the [N] session name

PhotoSessionNum
  :Type:            int32
  :Description:     Contains the [I] session number

PhotoShutterSpeed
  :Type:            string
  :Description:     Camera shutter speed of photo

PhotoUUID
  :Type:            string
  :Description:     Internal UUID of photo

PhotoUpdated
  :Type:            object
  :Description:     Contains fields for the PhotoUpdated event
  :Event fields:    - "[PhotoInfo FIELDS]"

PhotoWidth
  :Type:            int32
  :Description:     Width of photo

RelayCustomText
  :Type:            object
  :Description:     Contains fields for the RelayCustomText event
  :Request fields:  - "CustomText"

RemoveNode
  :Type:            object
  :Description:     internal use

RenameCamera
  :Type:            object
  :Description:     Contains fields for the RenameCamera request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraName"

RenameNode
  :Type:            object
  :Description:     internal use

RenamePhoto
  :Type:            object
  :Description:     Contains fields for the RenamePhoto request
  :Request fields:  - "[PHOTO SELECTION FIELDS]"
                    - "PhotoComputedName"

Reshoot
  :Type:            object
  :Description:     Contains fields for the Reshoot request
  :Request fields:  - "[PHOTO SELECTION FIELDS]"

SetBatchNum
  :Type:            object
  :Description:     Contains fields for the SetBatchNum request
  :Request fields:  - "PhotoBatchNum"

SetCameraGroup
  :Type:            object
  :Description:     Contains fields for the SetCameraGroup request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraGroup"

SetOptions
  :Type:            object
  :Description:     Contains fields for SetOptions request
  :Request fields:  - "[OptionsInfo FIELDS]"

SetProperty
  :Type:            object
  :Description:     Contains fields for the SetProperty request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraPropertyType"
                    - "CameraPropertyValue"

SetSequenceNum
  :Type:            object
  :Description:     Contains fields for SetSequenceNum request
  :Request fields:  - "PhotoSequenceNum"

SetShutterButton
  :Type:            object
  :Description:     Contains fields for the SetShutterButton request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "CameraShutterButton"

Shoot
  :Type:            object
  :Description:     Contains fields for the Shoot request
  :Request fields:  - "[CAMERA SELECTION FIELDS]"
                    - "BulbTimer"
                    - "PhotoOrigin"

SyncBatchNum
  :Type:            object
  :Description:     Contains fields for the SyncBatchNum request

SyncClocks
  :Type:            object
  :Description:     Contains fields for the SyncClocks request
  :Request fields:  - "CameraDateTimeOffset"

Synchronise
  :Type:            object
  :Description:     Contains fields for the Synchronise request
  :Response fields: - "OptionsInfo"
                    - "NodeInfo[]"
                    - "CameraInfo[]"
                    - "PhotoInfo[]"

TransferData
  :Type:            data
  :Description:     internal use

TransferOffset
  :Type:            uint32
  :Description:     internal use

TransferPhoto
  :Type:            object
  :Description:     internal use

TransferSize
  :Type:            uint32
  :Description:     internal use

UniqueTag
  :Type:            string
  :Description:     Contains the [U] unique tag

msg_id
  :Type:            string
  :Description:     Identifier string for message type

msg_result
  :Type:            boolean
  :Description:     Generic result field indicating success or failure

msg_seq_num
  :Type:            uint32
  :Description:     Message sequence number

msg_type
  :Type:            string
  :Description:     Indicates whether message is request/response or event
  :Valid range:     - "Request"
                    - "Response"
                    - "Event"

msg_user_id
  :Type:            uint32
  :Description:     Custom user ID number

