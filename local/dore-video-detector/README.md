# Doré Stream Detector v0.1

Local-only browser runtime detector for public or authorized media. Inspired by the network-detection architecture used by primedl stream-detector (MPL-2.0) and ManifestHawk (MIT), but implemented here as a small Doré-specific detector rather than copied source.

Detects HLS, DASH and MSS by URL and response Content-Type after JavaScript playback starts, then relays the detected manifest to the Doré loopback bridge at 127.0.0.1:43127. It does not download media, decrypt DRM, bypass authentication, or transmit captures to a remote server.

Load this directory as an unpacked Chromium extension for development. Firefox packaging can follow after the detector contract stabilizes.
