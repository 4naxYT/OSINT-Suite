# OSINT (Open source intelligence) Repo
> This is a suite that helps people perform `OSINT` on people or similar

![License](https://img.shields.io/badge/License-Source%20Available-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![Language](https://img.shields.io/badge/Language-Batch%20%26%20Python-lightgrey?style=for-the-badge)
![Powered by](https://img.shields.io/badge/Powered%20by-ExifTool-important?style=for-the-badge)

This repo is ment to give you as many tools to help with gathering information  

## Ip Reverse search
> use someone's IP to get aproximate location
Run our python script via:
```bash
"Run IPcheck.bat"
```

## Metadata (Exif Stripping)
> This suite contains a working copy of `exiftools`,   
> to install the latest go to [ https://exiftool.org/ ]

### Put all your data to be `metadata searched `into :
```bash
cd "Exif tool\DATA"
```

### Verify
```bash
exiftool -ver
```
Should show a version number ex.[ `13.59` ]

### Run
> or use our `Get meta.bat` tool

```bash
exiftool "< Image > . < Extention >"
REM example : [ exiftool "Photo.jpg" ]
```
or the following to only get location
```bash
exiftool -n -GPSLatitude -GPSLongitude "< Image > . < Extention >"
REM or
exiftool -f -GPSPosition "< Image > . < Extention >"
```

### Location
Search:
```Stylus
maps.google.com
```
Click: [ `Ask Maps` ], 
Paste the position you get, and check out the location

## License

> 📌 Forking Policy: While this license restricts redistribution to third parties, forking the repository on GitHub for personal improvement, learning, and contributing back is welcome and encouraged.