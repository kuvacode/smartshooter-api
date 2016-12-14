==========================
External API Documentation
==========================

:Version: v3.24

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

+--------------------+------------------------------------+
| msg_id             | Description                        |
+====================+====================================+
| CameraUpdatedMsg   | Information about camera status    |
+--------------------+------------------------------------+
| LiveviewUpdatedMsg | internal use                       |
+--------------------+------------------------------------+
| NodeUpdatedMsg     | Information about GRID node status |
+--------------------+------------------------------------+
| PhotoUpdatedMsg    | Information about photo status     |
+--------------------+------------------------------------+
| PropertyUpdatedMsg | Information about camera property  |
+--------------------+------------------------------------+


Request/Response Messages
~~~~~~~~~~~~~~~~~~~~~~~~~

The following table lists all the valid request/response messages.

+-------------------------+--------------------------------------------------------------------------+
| msg_id                  | Description                                                              |
+=========================+==========================================================================+
| AutofocusMsg            | Do auto focus with specified camera                                      |
+-------------------------+--------------------------------------------------------------------------+
| CheckClocksMsg          | Retrieve current date/time from all cameras                              |
+-------------------------+--------------------------------------------------------------------------+
| ConnectMsg              | Connect specified camera                                                 |
+-------------------------+--------------------------------------------------------------------------+
| DeleteMsg               | Delete specified photo from computer                                     |
+-------------------------+--------------------------------------------------------------------------+
| DetectCamerasMsg        | Request Smart Shooter to detect connected cameras                        |
+-------------------------+--------------------------------------------------------------------------+
| DisconnectMsg           | Disconnect specified camera                                              |
+-------------------------+--------------------------------------------------------------------------+
| DownloadMsg             | Download specified photo from camera to computer                         |
+-------------------------+--------------------------------------------------------------------------+
| EnableLiveviewDOFMsg    | Enable/disable liveview DOF (depth of field) preview on specified camera |
+-------------------------+--------------------------------------------------------------------------+
| EnableLiveviewMsg       | Enable/disable liveview on specified camera                              |
+-------------------------+--------------------------------------------------------------------------+
| EnableLiveviewRecordMsg | Enable/disable recording of liveview images on specified camera          |
+-------------------------+--------------------------------------------------------------------------+
| EnableLiveviewZoomMsg   | Enable/disable liveview zoom region on specified camera                  |
+-------------------------+--------------------------------------------------------------------------+
| EnableVideoMsg          | Start/stop video recording on specified camera                           |
+-------------------------+--------------------------------------------------------------------------+
| FormatAllMsg            | Format memory cards on all cameras                                       |
+-------------------------+--------------------------------------------------------------------------+
| IdentifyMsg             | Request specified camera identifies itself                               |
+-------------------------+--------------------------------------------------------------------------+
| LicenseMsg              | internal use                                                             |
+-------------------------+--------------------------------------------------------------------------+
| LiveviewFPSMsg          | Set desired liveview FPS for specified camera                            |
+-------------------------+--------------------------------------------------------------------------+
| LiveviewFocusMsg        | Drive liveview focus motor for specified camera                          |
+-------------------------+--------------------------------------------------------------------------+
| LiveviewPositionMsg     | Change liveview zoom region for specified camera                         |
+-------------------------+--------------------------------------------------------------------------+
| NetworkPingMsg          | internal use                                                             |
+-------------------------+--------------------------------------------------------------------------+
| NodeEndpointMsg         | internal use                                                             |
+-------------------------+--------------------------------------------------------------------------+
| RemoveNodeMsg           | internal use                                                             |
+-------------------------+--------------------------------------------------------------------------+
| RenameCameraMsg         | Set name for camera                                                      |
+-------------------------+--------------------------------------------------------------------------+
| RenameNodeMsg           | Set name for GRID node                                                   |
+-------------------------+--------------------------------------------------------------------------+
| RenamePhotoMsg          | Set filename for photo                                                   |
+-------------------------+--------------------------------------------------------------------------+
| ReshootMsg              | Reshoot photo using same filename on specified camera                    |
+-------------------------+--------------------------------------------------------------------------+
| SetBatchNumMsg          | Set the [B] batch number used when generating filenames                  |
+-------------------------+--------------------------------------------------------------------------+
| SetOptionsMsg           | Set Smart Shooter options                                                |
+-------------------------+--------------------------------------------------------------------------+
| SetPropertyMsg          | Set camera property on specified camera                                  |
+-------------------------+--------------------------------------------------------------------------+
| SetSequenceNumMsg       | Set the [S] sequence number used when generating filenames               |
+-------------------------+--------------------------------------------------------------------------+
| SetShutterButtonMsg     | Set shutter button state for specified camera                            |
+-------------------------+--------------------------------------------------------------------------+
| ShootMsg                | Take photo with specified camera                                         |
+-------------------------+--------------------------------------------------------------------------+
| SyncBatchNumMsg         | Force batch numbers back in sync for all cameras                         |
+-------------------------+--------------------------------------------------------------------------+
| SyncClocksMsg           | Synchronise clocks on all cameras                                        |
+-------------------------+--------------------------------------------------------------------------+
| SynchroniseMsg          | Request latest information about cameras/photos                          |
+-------------------------+--------------------------------------------------------------------------+
| TransferPhotoMsg        | internal use                                                             |
+-------------------------+--------------------------------------------------------------------------+


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

Mulitple
  Selects a set of specific cameras. The set of cameras is then identified by
  the ``CameraKeys`` field.

The same concept applies to photo selection, using the fields
``PhotoSelection``, ``PhotoKey``, and ``PhotoKeys``.

In the field definition list, these fields are referred to as
``[CAMERA SELECTION FIELDS]`` and ``[PHOTO SELECTION FIELDS]``, when definining
the list of sub-fields that can be contained in a JSON ``object``.


List of Fields
~~~~~~~~~~~~~~

+----------------------------------+--------------------------------------------------------------------+
| Name                             | Description                                                        |
+==================================+====================================================================+
| AutofocusMsg                     | Contains fields for the AutofocusMsg request                       |
+----------------------------------+--------------------------------------------------------------------+
| CameraAutofocusIsSupported       | Indicates if camera supports auto focus                            |
+----------------------------------+--------------------------------------------------------------------+
| CameraBatterylevel               | Indicates camera battery level in range 0 to 100                   |
+----------------------------------+--------------------------------------------------------------------+
| CameraBulbIsEnabled              | Indicates whether buld shooting mode is enabled                    |
+----------------------------------+--------------------------------------------------------------------+
| CameraBulbIsSupported            | Indicates whether buld shooting mode is supported                  |
+----------------------------------+--------------------------------------------------------------------+
| CameraDateTimeOffset             | Contains offset from local time for when syncing date/time         |
+----------------------------------+--------------------------------------------------------------------+
| CameraIsFocused                  | Indicates of camera auto focus action was successful               |
+----------------------------------+--------------------------------------------------------------------+
| CameraKey                        | Unique identfier for a camera                                      |
+----------------------------------+--------------------------------------------------------------------+
| CameraKeys                       | Array of unique camera identifiers                                 |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewDOFIsEnabled       | Indicates whether camera liveview DOF preview is enabled           |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewDOFIsSupported     | Indicates if camera liveview supports DOF (depth of field) preview |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewFPS                | Desired FPS of camera liveview stream                              |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewFocus              | Specifies camera liveview focus motor movement                     |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewIsEnabled          | Indicates whether camera liveview is enabled                       |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewIsSupported        | Indicates if camera supports liveview                              |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewSensorHeight       | Height of camera's sensor in pixels                                |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewSensorRegionBottom | Bottom pixel of camera's active liveview region                    |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewSensorRegionLeft   | Left pixel of camera's active liveview region                      |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewSensorRegionRight  | Right pixel of camera's active liveview region                     |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewSensorRegionTop    | Top pixel of camera's active liveview region                       |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewSensorWidth        | Width of camera's sensor in pixels                                 |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewVideoFPS           | Desired FPS of camera liveview stream during video recording       |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewZoomIsEnabled      | Indicates whether camera liveview zoom region is enabled           |
+----------------------------------+--------------------------------------------------------------------+
| CameraLiveviewZoomIsSupported    | Indicates if camera liveview supports a zoom region                |
+----------------------------------+--------------------------------------------------------------------+
| CameraMake                       | Make of camera                                                     |
+----------------------------------+--------------------------------------------------------------------+
| CameraMirrorLockupIsEnabled      | Indicates whether mirror lockup is enabled                         |
+----------------------------------+--------------------------------------------------------------------+
| CameraMirrorLockupIsSupported    | Indicates whether mirror lockup (MLU) is supported                 |
+----------------------------------+--------------------------------------------------------------------+
| CameraModel                      | Model of camera                                                    |
+----------------------------------+--------------------------------------------------------------------+
| CameraName                       | Name of camera                                                     |
+----------------------------------+--------------------------------------------------------------------+
| CameraNumAutofocus               | Number of camera auto focus attempts                               |
+----------------------------------+--------------------------------------------------------------------+
| CameraNumCards                   | Number of memory cards in camera                                   |
+----------------------------------+--------------------------------------------------------------------+
| CameraNumDownloadsComplete       | Number of photos downloaded from camera                            |
+----------------------------------+--------------------------------------------------------------------+
| CameraNumDownloadsFailed         | Number of failed photo download attempts                           |
+----------------------------------+--------------------------------------------------------------------+
| CameraNumPhotosFailed            | Number of failed photo attempts                                    |
+----------------------------------+--------------------------------------------------------------------+
| CameraNumPhotosTaken             | Number of photos taken by camera                                   |
+----------------------------------+--------------------------------------------------------------------+
| CameraPowersource                | Indicates camera power source                                      |
+----------------------------------+--------------------------------------------------------------------+
| CameraPropertyIsWriteable        | Indicates whether a camera property can be changed                 |
+----------------------------------+--------------------------------------------------------------------+
| CameraPropertyRange              | Array of valid values for a camera property                        |
+----------------------------------+--------------------------------------------------------------------+
| CameraPropertyType               | Specifies a camera property                                        |
+----------------------------------+--------------------------------------------------------------------+
| CameraPropertyValue              | Contains value for the camera property                             |
+----------------------------------+--------------------------------------------------------------------+
| CameraSelection                  | Determines the camera selection                                    |
+----------------------------------+--------------------------------------------------------------------+
| CameraSerialNumber               | Serial number of camera                                            |
+----------------------------------+--------------------------------------------------------------------+
| CameraShutterButton              | Virtual state of camera's shutter button                           |
+----------------------------------+--------------------------------------------------------------------+
| CameraStatus                     | Status of camera                                                   |
+----------------------------------+--------------------------------------------------------------------+
| CameraUpdatedMsg                 | Contains fields for the CameraUpdatedMsg event                     |
+----------------------------------+--------------------------------------------------------------------+
| CameraVideoIsEnabled             | Indicates whether video is being recorded                          |
+----------------------------------+--------------------------------------------------------------------+
| CameraVideoIsSupported           | Indicates whether video recording is supported                     |
+----------------------------------+--------------------------------------------------------------------+
| CheckClocksMsg                   | Contains fields for the CheckClocksMsg request                     |
+----------------------------------+--------------------------------------------------------------------+
| ConnectMsg                       | Contains fields for the ConnectMsg request                         |
+----------------------------------+--------------------------------------------------------------------+
| DeleteMsg                        | Contains fields for the DeleteMsg request                          |
+----------------------------------+--------------------------------------------------------------------+
| DetectCamerasMsg                 | Contains fields for the DetectCamerasMsg request                   |
+----------------------------------+--------------------------------------------------------------------+
| DisconnectMsg                    | Contains fields for the DisconnectMsg request                      |
+----------------------------------+--------------------------------------------------------------------+
| DownloadMsg                      | Contains fields for the DownloadMsg request                        |
+----------------------------------+--------------------------------------------------------------------+
| Enable                           | Generic indicator for enabling/disabling some state                |
+----------------------------------+--------------------------------------------------------------------+
| EnableLiveviewDOFMsg             | Contains fields for the EnableLiveviewDOFMsg request               |
+----------------------------------+--------------------------------------------------------------------+
| EnableLiveviewMsg                | Contains fields for the EnableLiveviewMsg request                  |
+----------------------------------+--------------------------------------------------------------------+
| EnableLiveviewRecordMsg          | Contains fields for the EnableLiveviewRecordMsg request            |
+----------------------------------+--------------------------------------------------------------------+
| EnableLiveviewZoomMsg            | Contains fields for the EnableLiveviewZoomMsg request              |
+----------------------------------+--------------------------------------------------------------------+
| EnableVideoMsg                   | Contains fields for the EnableVideoMsg request                     |
+----------------------------------+--------------------------------------------------------------------+
| FormatAllMsg                     | Contains fields for the FormatAllMsg request                       |
+----------------------------------+--------------------------------------------------------------------+
| GridAutoConnect                  | Contains the value for the 'Auto Connect' option                   |
+----------------------------------+--------------------------------------------------------------------+
| GridAutoSynchroniseTime          | Contains the value for the 'Auto Synchronise Time' option          |
+----------------------------------+--------------------------------------------------------------------+
| GridBarcode                      | Contains the [Z] barcode text                                      |
+----------------------------------+--------------------------------------------------------------------+
| GridBatchNum                     | Contains the [B] batch number                                      |
+----------------------------------+--------------------------------------------------------------------+
| GridDefaultFocusMode             | Contains the default camera focus mode                             |
+----------------------------------+--------------------------------------------------------------------+
| GridDefaultStorage               | Contains the default camera storage mode                           |
+----------------------------------+--------------------------------------------------------------------+
| GridFilenameExpression           | Contains the filename expression option                            |
+----------------------------------+--------------------------------------------------------------------+
| GridGenerateFilename             | Contains the value for the 'Generate Filename' option              |
+----------------------------------+--------------------------------------------------------------------+
| GridLiveviewDatalimit            | Contains the liveview recording data limit                         |
+----------------------------------+--------------------------------------------------------------------+
| GridScanBatchNum                 | Contains value for the 'Scan Batch Number' option                  |
+----------------------------------+--------------------------------------------------------------------+
| GridScanSequenceNum              | Contains the value for the 'Scan Sequence Number' option           |
+----------------------------------+--------------------------------------------------------------------+
| GridSequenceNum                  | Contains the [S] sequence number                                   |
+----------------------------------+--------------------------------------------------------------------+
| GridUniqueTag                    | Contains the [U] unique tag                                        |
+----------------------------------+--------------------------------------------------------------------+
| IdentifyMsg                      | Contains fields for the IdentifyMsg request                        |
+----------------------------------+--------------------------------------------------------------------+
| LiveviewFPSMsg                   | Contains fields for the LiveviewFPSMsg request                     |
+----------------------------------+--------------------------------------------------------------------+
| LiveviewFocusMsg                 | Contains fields for the LiveviewFocusMsg request                   |
+----------------------------------+--------------------------------------------------------------------+
| LiveviewPositionMsg              | Contains fields for the LiveviewPositionMsg request                |
+----------------------------------+--------------------------------------------------------------------+
| PhotoBarcode                     | Contains barcode text scanned from photo                           |
+----------------------------------+--------------------------------------------------------------------+
| PhotoComputedName                | Photo name generated by Smart Shooter                              |
+----------------------------------+--------------------------------------------------------------------+
| PhotoDateCaptured                | Data/time that photo was captured by camera                        |
+----------------------------------+--------------------------------------------------------------------+
| PhotoFilesize                    | Size of photo file                                                 |
+----------------------------------+--------------------------------------------------------------------+
| PhotoFormat                      | Format of photo image file                                         |
+----------------------------------+--------------------------------------------------------------------+
| PhotoHeight                      | Height of photo                                                    |
+----------------------------------+--------------------------------------------------------------------+
| PhotoIsImage                     | Indicates whether photo is image or not (possible video file)      |
+----------------------------------+--------------------------------------------------------------------+
| PhotoIsScanned                   | Indicates if barcode has been scanned from photo                   |
+----------------------------------+--------------------------------------------------------------------+
| PhotoKey                         | Unique identifier for a photo                                      |
+----------------------------------+--------------------------------------------------------------------+
| PhotoKeys                        | Array of unique photo identifiers                                  |
+----------------------------------+--------------------------------------------------------------------+
| PhotoLocation                    | Location of photo file                                             |
+----------------------------------+--------------------------------------------------------------------+
| PhotoOriginalName                | Original name of photo on camera                                   |
+----------------------------------+--------------------------------------------------------------------+
| PhotoSHA1                        | SHA1 of photo data contents                                        |
+----------------------------------+--------------------------------------------------------------------+
| PhotoSelection                   | Determines the photo selection                                     |
+----------------------------------+--------------------------------------------------------------------+
| PhotoUUID                        | Internal UUID of photo                                             |
+----------------------------------+--------------------------------------------------------------------+
| PhotoUpdatedMsg                  | Contains fields for the PhotoUpdatedMsg event                      |
+----------------------------------+--------------------------------------------------------------------+
| PhotoWidth                       | Width of photo                                                     |
+----------------------------------+--------------------------------------------------------------------+
| PropertyInfoMsg                  | Contains fields for the PropertyInfoMsg object                     |
+----------------------------------+--------------------------------------------------------------------+
| PropertyUpdatedMsg               | Contains fields for the PropertyUpdatedMsg event                   |
+----------------------------------+--------------------------------------------------------------------+
| RenameCameraMsg                  | Contains fields for the RenameCameraMsg request                    |
+----------------------------------+--------------------------------------------------------------------+
| RenamePhotoMsg                   | Contains fields for the RenamePhotoMsg request                     |
+----------------------------------+--------------------------------------------------------------------+
| ReshootMsg                       | Contains fields for the ReshootMsg request                         |
+----------------------------------+--------------------------------------------------------------------+
| Result                           | Generic result field indicating success or failure                 |
+----------------------------------+--------------------------------------------------------------------+
| SetBatchNumMsg                   | Contains fields for the SetBatchNumMsg request                     |
+----------------------------------+--------------------------------------------------------------------+
| SetOptionsMsg                    | Contains fields for SetOptionsMsg request                          |
+----------------------------------+--------------------------------------------------------------------+
| SetPropertyMsg                   | Contains fields for the SetPropertyMsg request                     |
+----------------------------------+--------------------------------------------------------------------+
| SetSequenceNumMsg                | Contains fields for SetSequenceNumMsg request                      |
+----------------------------------+--------------------------------------------------------------------+
| SetShutterButtonMsg              | Contains fields for the SetShutterButtonMsg request                |
+----------------------------------+--------------------------------------------------------------------+
| ShootMsg                         | Contains fields for the ShootMsg request                           |
+----------------------------------+--------------------------------------------------------------------+
| SyncBatchNumMsg                  | Contains fields for the SyncBatchNumMsg request                    |
+----------------------------------+--------------------------------------------------------------------+
| SyncClocksMsg                    | Contains fields for the SyncClocksMsg request                      |
+----------------------------------+--------------------------------------------------------------------+
| SynchroniseMsg                   | Contains fields for the SynchroniseMsg request                     |
+----------------------------------+--------------------------------------------------------------------+
| msg_id                           | Indicates the message contents                                     |
+----------------------------------+--------------------------------------------------------------------+
| msg_ref_num                      | Message reference number                                           |
+----------------------------------+--------------------------------------------------------------------+
| msg_type                         | Indicates whether message is request/response or event             |
+----------------------------------+--------------------------------------------------------------------+


Field Definitions
~~~~~~~~~~~~~~~~~

The following sections defines all the valid fields, along with associated data
type. The fields that are JSON objects, it lists the valid sub-fields that may
be contained within that object.

AutofocusMsg
  :Type:
    object
  :Description:
    Contains fields for the AutofocusMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]

CameraAutofocusIsSupported
  :Type:
    boolean
  :Description:
    Indicates if camera supports auto focus

CameraBatterylevel
  :Type:
    int32
  :Description:
    Indicates camera battery level in range 0 to 100

CameraBulbIsEnabled
  :Type:
    boolean
  :Description:
    Indicates whether buld shooting mode is enabled

CameraBulbIsSupported
  :Type:
    boolean
  :Description:
    Indicates whether buld shooting mode is supported

CameraDateTimeOffset
  :Type:
    int64
  :Description:
    Contains offset from local time for when syncing date/time

CameraIsFocused
  :Type:
    boolean
  :Description:
    Indicates of camera auto focus action was successful

CameraKey
  :Type:
    string
  :Description:
    Unique identfier for a camera

CameraKeys
  :Type:
    string[]
  :Description:
    Array of unique camera identifiers

CameraLiveviewDOFIsEnabled
  :Type:
    boolean
  :Description:
    Indicates whether camera liveview DOF preview is enabled

CameraLiveviewDOFIsSupported
  :Type:
    boolean
  :Description:
    Indicates if camera liveview supports DOF (depth of field) preview

CameraLiveviewFPS
  :Type:
    int32
  :Description:
    Desired FPS of camera liveview stream

CameraLiveviewFocus
  :Type:
    string
  :Description:
    Specifies camera liveview focus motor movement
  :Valid range:
      - "Near1"
      - "Near2"
      - "Near3"
      - "Far1"
      - "Far2"
      - "Far3"

CameraLiveviewImage
  :Type:
    data
  :Description:
    internal use

CameraLiveviewIsEnabled
  :Type:
    boolean
  :Description:
    Indicates whether camera liveview is enabled

CameraLiveviewIsSupported
  :Type:
    boolean
  :Description:
    Indicates if camera supports liveview

CameraLiveviewSensorHeight
  :Type:
    int32
  :Description:
    Height of camera's sensor in pixels

CameraLiveviewSensorRegionBottom
  :Type:
    float
  :Description:
    Bottom pixel of camera's active liveview region

CameraLiveviewSensorRegionLeft
  :Type:
    float
  :Description:
    Left pixel of camera's active liveview region

CameraLiveviewSensorRegionRight
  :Type:
    float
  :Description:
    Right pixel of camera's active liveview region

CameraLiveviewSensorRegionTop
  :Type:
    float
  :Description:
    Top pixel of camera's active liveview region

CameraLiveviewSensorWidth
  :Type:
    int32
  :Description:
    Width of camera's sensor in pixels

CameraLiveviewVideoFPS
  :Type:
    int32
  :Description:
    Desired FPS of camera liveview stream during video recording

CameraLiveviewZoomIsEnabled
  :Type:
    boolean
  :Description:
    Indicates whether camera liveview zoom region is enabled

CameraLiveviewZoomIsSupported
  :Type:
    boolean
  :Description:
    Indicates if camera liveview supports a zoom region

CameraMake
  :Type:
    string
  :Description:
    Make of camera

CameraMirrorLockupIsEnabled
  :Type:
    boolean
  :Description:
    Indicates whether mirror lockup is enabled

CameraMirrorLockupIsSupported
  :Type:
    boolean
  :Description:
    Indicates whether mirror lockup (MLU) is supported

CameraModel
  :Type:
    string
  :Description:
    Model of camera

CameraName
  :Type:
    string
  :Description:
    Name of camera

CameraNumAutofocus
  :Type:
    int32
  :Description:
    Number of camera auto focus attempts

CameraNumCards
  :Type:
    int32
  :Description:
    Number of memory cards in camera

CameraNumDownloadsComplete
  :Type:
    int32
  :Description:
    Number of photos downloaded from camera

CameraNumDownloadsFailed
  :Type:
    int32
  :Description:
    Number of failed photo download attempts

CameraNumPhotosFailed
  :Type:
    int32
  :Description:
    Number of failed photo attempts

CameraNumPhotosTaken
  :Type:
    int32
  :Description:
    Number of photos taken by camera

CameraPowersource
  :Type:
    string
  :Description:
    Indicates camera power source
  :Valid range:
      - "AC"
      - "Battery"
      - "Unknown"

CameraPropertyIsWriteable
  :Type:
    boolean
  :Description:
    Indicates whether a camera property can be changed

CameraPropertyRange
  :Type:
    string[]
  :Description:
    Array of valid values for a camera property

CameraPropertyType
  :Type:
    string
  :Description:
    Specifies a camera property
  :Valid range:
      - "Aperture"
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
  :Type:
    string
  :Description:
    Contains value for the camera property

CameraSelection
  :Type:
    string
  :Description:
    Determines the camera selection
  :Valid range:
      - "All"
      - "Single"
      - "Multiple"

CameraSerialNumber
  :Type:
    string
  :Description:
    Serial number of camera

CameraShutterButton
  :Type:
    string
  :Description:
    Virtual state of camera's shutter button
  :Valid range:
      - "Off"
      - "Half"
      - "Full"

CameraStatus
  :Type:
    string
  :Description:
    Status of camera
  :Valid range:
      - "Absent"
      - "Lost"
      - "Disconnected"
      - "Ready"
      - "Busy"
      - "Error"

CameraUpdatedMsg
  :Type:
    object
  :Description:
    Contains fields for the CameraUpdatedMsg event
  :Event fields:
      - [CAMERA SELECTION FIELDS]
      - CameraStatus
      - CameraName
      - CameraSerialNumber
      - CameraMake
      - CameraModel
      - CameraNumCards
      - GridBatchNum
      - CameraDateTimeOffset
      - CameraAutofocusIsSupported
      - CameraIsFocused
      - CameraLiveviewIsSupported
      - CameraLiveviewZoomIsSupported
      - CameraLiveviewDOFIsSupported
      - CameraLiveviewIsEnabled
      - CameraLiveviewZoomIsEnabled
      - CameraLiveviewDOFIsEnabled
      - CameraLiveviewSensorWidth
      - CameraLiveviewSensorHeight
      - CameraLiveviewSensorRegionLeft
      - CameraLiveviewSensorRegionBottom
      - CameraLiveviewSensorRegionRight
      - CameraLiveviewSensorRegionTop
      - CameraVideoIsSupported
      - CameraVideoIsEnabled
      - CameraBulbIsSupported
      - CameraBulbIsEnabled
      - CameraPowersource
      - CameraBatterylevel
      - CameraNumPhotosTaken
      - CameraNumPhotosFailed
      - CameraNumDownloadsComplete
      - CameraNumDownloadsFailed
      - CameraNumAutofocus
      - NodeKey

CameraVideoIsEnabled
  :Type:
    boolean
  :Description:
    Indicates whether video is being recorded

CameraVideoIsSupported
  :Type:
    boolean
  :Description:
    Indicates whether video recording is supported

CheckClocksMsg
  :Type:
    object
  :Description:
    Contains fields for the CheckClocksMsg request
  :Request fields:

ConnectMsg
  :Type:
    object
  :Description:
    Contains fields for the ConnectMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]

DeleteMsg
  :Type:
    object
  :Description:
    Contains fields for the DeleteMsg request
  :Request fields:
      - [PHOTO SELECTION FIELDS]

DetectCamerasMsg
  :Type:
    object
  :Description:
    Contains fields for the DetectCamerasMsg request
  :Request fields:

DisconnectMsg
  :Type:
    object
  :Description:
    Contains fields for the DisconnectMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]

DownloadMsg
  :Type:
    object
  :Description:
    Contains fields for the DownloadMsg request
  :Request fields:
      - [PHOTO SELECTION FIELDS]

Enable
  :Type:
    boolean
  :Description:
    Generic indicator for enabling/disabling some state

EnableLiveviewDOFMsg
  :Type:
    object
  :Description:
    Contains fields for the EnableLiveviewDOFMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - Enable

EnableLiveviewMsg
  :Type:
    object
  :Description:
    Contains fields for the EnableLiveviewMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - Enable

EnableLiveviewRecordMsg
  :Type:
    object
  :Description:
    Contains fields for the EnableLiveviewRecordMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - Enable

EnableLiveviewZoomMsg
  :Type:
    object
  :Description:
    Contains fields for the EnableLiveviewZoomMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - Enable

EnableVideoMsg
  :Type:
    object
  :Description:
    Contains fields for the EnableVideoMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - Enable

FormatAllMsg
  :Type:
    object
  :Description:
    Contains fields for the FormatAllMsg request
  :Request fields:

GridAutoConnect
  :Type:
    boolean
  :Description:
    Contains the value for the 'Auto Connect' option

GridAutoSynchroniseTime
  :Type:
    boolean
  :Description:
    Contains the value for the 'Auto Synchronise Time' option

GridBarcode
  :Type:
    string
  :Description:
    Contains the [Z] barcode text

GridBatchNum
  :Type:
    int32
  :Description:
    Contains the [B] batch number

GridDefaultFocusMode
  :Type:
    string
  :Description:
    Contains the default camera focus mode
  :Valid range:
      - "Not set"
      - "AF Single"
      - "AF Continuous"
      - "AF Auto"
      - "MF"

GridDefaultStorage
  :Type:
    string
  :Description:
    Contains the default camera storage mode
  :Valid range:
      - "Disk"
      - "Card"
      - "Both"
      - "JPEG"

GridFilenameExpression
  :Type:
    string
  :Description:
    Contains the filename expression option

GridFilenameValidation
  :Type:
    string
  :Description:
    internal use

GridGenerateFilename
  :Type:
    boolean
  :Description:
    Contains the value for the 'Generate Filename' option

GridLiveviewDatalimit
  :Type:
    int32
  :Description:
    Contains the liveview recording data limit

GridScanBatchNum
  :Type:
    boolean
  :Description:
    Contains value for the 'Scan Batch Number' option

GridScanSequenceNum
  :Type:
    boolean
  :Description:
    Contains the value for the 'Scan Sequence Number' option

GridSequenceNum
  :Type:
    int32
  :Description:
    Contains the [S] sequence number

GridUniqueTag
  :Type:
    string
  :Description:
    Contains the [U] unique tag

IdentifyMsg
  :Type:
    object
  :Description:
    Contains fields for the IdentifyMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]

License
  :Type:
    string
  :Description:
    internal use

LicenseMsg
  :Type:
    object
  :Description:
    internal use

LiveviewFPSMsg
  :Type:
    object
  :Description:
    Contains fields for the LiveviewFPSMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - CameraLiveviewFPS
      - CameraLiveviewVideoFPS

LiveviewFocusMsg
  :Type:
    object
  :Description:
    Contains fields for the LiveviewFocusMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - CameraLiveviewFocus

LiveviewPositionMsg
  :Type:
    object
  :Description:
    Contains fields for the LiveviewPositionMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - CameraLiveviewPositionX
      - CameraLiveviewPositionY

LiveviewUpdatedMsg
  :Type:
    object
  :Description:
    internal use

NetworkAddress
  :Type:
    string
  :Description:
    internal use

NetworkDiscoveryMsg
  :Type:
    object
  :Description:
    internal use

NetworkEndpoint
  :Type:
    string
  :Description:
    internal use

NetworkPingMsg
  :Type:
    object
  :Description:
    internal use

NetworkPort
  :Type:
    int32
  :Description:
    internal use

NetworkTimestamp
  :Type:
    uint64
  :Description:
    internal use

NetworkVersion
  :Type:
    string
  :Description:
    internal use

NodeEndpoint
  :Type:
    string
  :Description:
    internal use

NodeEndpointMsg
  :Type:
    object
  :Description:
    internal use

NodeIsLiveviewConsumer
  :Type:
    boolean
  :Description:
    internal use

NodeIsMaster
  :Type:
    boolean
  :Description:
    internal use

NodeKey
  :Type:
    string
  :Description:
    internal use

NodeName
  :Type:
    string
  :Description:
    internal use

NodeSyncLocal
  :Type:
    boolean
  :Description:
    internal use

NodeSyncVersion
  :Type:
    int32
  :Description:
    internal use

NodeTransferMode
  :Type:
    float
  :Description:
    internal use

NodeUpdatedMsg
  :Type:
    object
  :Description:
    internal use

NodeVersion
  :Type:
    string
  :Description:
    internal use

PhotoBarcode
  :Type:
    string
  :Description:
    Contains barcode text scanned from photo

PhotoComputedName
  :Type:
    string
  :Description:
    Photo name generated by Smart Shooter

PhotoDateCaptured
  :Type:
    string
  :Description:
    Data/time that photo was captured by camera

PhotoFilesize
  :Type:
    uint64
  :Description:
    Size of photo file

PhotoFormat
  :Type:
    string
  :Description:
    Format of photo image file
  :Valid range:
      - "JPEG"
      - "PNG"
      - "Raw"
      - "TGA"
      - "TIFF"
      - "Unknown"

PhotoHeight
  :Type:
    int32
  :Description:
    Height of photo

PhotoIsImage
  :Type:
    boolean
  :Description:
    Indicates whether photo is image or not (possible video file)

PhotoIsScanned
  :Type:
    boolean
  :Description:
    Indicates if barcode has been scanned from photo

PhotoKey
  :Type:
    string
  :Description:
    Unique identifier for a photo

PhotoKeys
  :Type:
    string[]
  :Description:
    Array of unique photo identifiers

PhotoLocation
  :Type:
    string
  :Description:
    Location of photo file
  :Valid range:
      - "Orphaned"
      - "Deleted"
      - "Hidden"
      - "Camera"
      - "Local Disk"

PhotoOriginalName
  :Type:
    string
  :Description:
    Original name of photo on camera

PhotoSHA1
  :Type:
    string
  :Description:
    SHA1 of photo data contents

PhotoSelection
  :Type:
    string
  :Description:
    Determines the photo selection

PhotoUUID
  :Type:
    string
  :Description:
    Internal UUID of photo

PhotoUpdatedMsg
  :Type:
    object
  :Description:
    Contains fields for the PhotoUpdatedMsg event
  :Event fields:
      - [PHOTO SELECTION FIELDS]
      - PhotoLocation
      - PhotoUUID
      - PhotoOriginalName
      - PhotoComputedName
      - PhotoDateCaptured
      - PhotoFormat
      - PhotoWidth
      - PhotoHeight
      - PhotoFilesize
      - PhotoIsImage
      - PhotoIsScanned
      - PhotoSHA1
      - PhotoBarcode
      - GridSequenceNum
      - GridBatchNum
      - CameraKey
      - NodeKey

PhotoWidth
  :Type:
    int32
  :Description:
    Width of photo

PropertyInfoMsg
  :Type:
    object
  :Description:
    Contains fields for the PropertyInfoMsg object
  :Event fields:
      - CameraPropertyType
      - CameraPropertyValue
      - CameraPropertyIsWriteable
      - CameraPropertyRange

PropertyUpdatedMsg
  :Type:
    object
  :Description:
    Contains fields for the PropertyUpdatedMsg event
  :Event fields:
      - [CAMERA SELECTION FIELDS]
      - PropertyInfoMsg[]

RemoveNodeMsg
  :Type:
    object
  :Description:
    internal use

RenameCameraMsg
  :Type:
    object
  :Description:
    Contains fields for the RenameCameraMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - CameraName

RenameNodeMsg
  :Type:
    object
  :Description:
    internal use

RenamePhotoMsg
  :Type:
    object
  :Description:
    Contains fields for the RenamePhotoMsg request
  :Request fields:
      - [PHOTO SELECTION FIELDS]
      - PhotoComputedName

ReshootMsg
  :Type:
    object
  :Description:
    Contains fields for the ReshootMsg request
  :Request fields:
      - [PHOTO SELECTION FIELDS]

Result
  :Type:
    boolean
  :Description:
    Generic result field indicating success or failure

SetBatchNumMsg
  :Type:
    object
  :Description:
    Contains fields for the SetBatchNumMsg request
  :Request fields:
      - GridBatchNum

SetOptionsMsg
  :Type:
    object
  :Description:
    Contains fields for SetOptionsMsg request
  :Request fields:
      - GridFilenameExpression
      - GridFilenameValidation
      - GridUniqueTag
      - GridBarcode
      - GridDefaultStorage
      - GridDefaultFocusMode
      - GridGenerateFilename
      - GridAutoConnect
      - GridAutoSynchroniseTime
      - GridScanSequenceNum
      - GridScanBatchNum
      - GridLiveviewDatalimit

SetPropertyMsg
  :Type:
    object
  :Description:
    Contains fields for the SetPropertyMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - CameraPropertyType
      - CameraPropertyValue

SetSequenceNumMsg
  :Type:
    object
  :Description:
    Contains fields for SetSequenceNumMsg request
  :Request fields:
      - GridSequenceNum

SetShutterButtonMsg
  :Type:
    object
  :Description:
    Contains fields for the SetShutterButtonMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]
      - CameraShutterButton

ShootMsg
  :Type:
    object
  :Description:
    Contains fields for the ShootMsg request
  :Request fields:
      - [CAMERA SELECTION FIELDS]

SyncBatchNumMsg
  :Type:
    object
  :Description:
    Contains fields for the SyncBatchNumMsg request
  :Request fields:

SyncClocksMsg
  :Type:
    object
  :Description:
    Contains fields for the SyncClocksMsg request
  :Request fields:
      - CameraDateTimeOffset

SynchroniseMsg
  :Type:
    object
  :Description:
    Contains fields for the SynchroniseMsg request
  :Request fields:
  :Response fields:
      - NodeUpdatedEventMsg
      - SetOptionsMsg
      - LicenseMsg
      - CameraUpdatedMsg[]
      - PhotoUpdatedMsg[]
      - PropertyUpdatedMsg[]

TransferData
  :Type:
    data
  :Description:
    internal use

TransferOffset
  :Type:
    uint32
  :Description:
    internal use

TransferPhotoMsg
  :Type:
    object
  :Description:
    internal use

TransferSize
  :Type:
    uint32
  :Description:
    internal use

msg_id
  :Type:
    string
  :Description:
    Indicates the message contents

msg_ref_num
  :Type:
    int32
  :Description:
    Message reference number

msg_type
  :Type:
    string
  :Description:
    Indicates whether message is request/response or event
  :Valid range:
      - "Request"
      - "Response"
      - "Event"
