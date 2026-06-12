---
title: "louis-e/arnis: Generate any location from the real world in Minecraft with a high level of detail."
source: "https://github.com/louis-e/arnis"
author:
published:
created: 2026-06-12
description: "Generate any location from the real world in Minecraft with a high level of detail. - louis-e/arnis"
tags:
  - "clippings"
---
[![Banner](https://github.com/louis-e/arnis/raw/main/assets/git/banner.png)](https://github.com/louis-e/arnis/blob/main/assets/git/banner.png)

## Arnis

Arnis creates complex and accurate Minecraft Java Edition (1.17+) and Bedrock Edition worlds that reflect real-world geography, topography, and architecture.

This free and open source project is designed to handle large-scale geographic data from the real world and generate detailed Minecraft worlds. The algorithm processes geospatial data from OpenStreetMap as well as elevation data to create an accurate Minecraft representation of terrain and architecture. Generate your hometown, big cities, and natural landscapes with ease!

***Want mobile generation or larger map sizes?** [MapSmith](https://arnismc.com/mapsmith/) generates worlds in your browser, no install required.*

[![Minecraft Preview](https://github.com/louis-e/arnis/raw/main/assets/git/preview.jpg)](https://github.com/louis-e/arnis/blob/main/assets/git/preview.jpg) *This GitHub page and [arnismc.com](https://arnismc.com/) are the only official project websites. Do not download Arnis from any other website.*

## ⌨️ Usage

[![](https://github.com/louis-e/arnis/raw/main/assets/git/gui.png)](https://github.com/louis-e/arnis/blob/main/assets/git/gui.png)  
Download the [latest release](https://github.com/louis-e/arnis/releases/) or [compile](louis-earnis%20Generate%20any%20location%20from%20the%20real%20world%20in%20Minecraft%20with%20a%20high%20level%20of%20detail.md#trophy-open-source) the project on your own.

Choose your area on the map using the rectangle tool and select your Minecraft world - then simply click on *Start Generation*! Additionally, you can customize various generation settings, such as world scale, spawn point, or building interior generation.

## 📚 Documentation

[![Banner](https://github.com/louis-e/arnis/raw/main/assets/git/documentation.png)](https://github.com/louis-e/arnis/blob/main/assets/git/documentation.png)

Full documentation is available in the [GitHub Wiki](https://github.com/louis-e/arnis/wiki/), covering topics such as technical explanations, FAQs, contribution guidelines and roadmaps.

backgroundvid.webm<video src="https://private-user-images.githubusercontent.com/44675238/557072822-420acc19-a850-418e-8397-1a45b05582ab.webm?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODEyNDQ1NTAsIm5iZiI6MTc4MTI0NDI1MCwicGF0aCI6Ii80NDY3NTIzOC81NTcwNzI4MjItNDIwYWNjMTktYTg1MC00MThlLTgzOTctMWE0NWIwNTU4MmFiLndlYm0_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNjEyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDYxMlQwNjA0MTBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1kOTdkMTZlNGFmNWQ3MzYwZGYxNzA3Nzk1MmFjMWViODVlYzI0YmQ3MzUyYjhkN2I0MTE2MWYxN2E2MzI3MTU5JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9dmlkZW8lMkZ3ZWJtIn0.E6AVahUbC-I8t4xNk661vrLXeZ1LGZxq-VkbgQDtSwI" controls="controls"></video>

## 🏆 Open Source

#### Key objectives of this project

- **Modularity**: Ensure that all components (e.g., data fetching, processing, and world generation) are cleanly separated into distinct modules for better maintainability and scalability.
- **Performance Optimization**: We aim to maintain strong performance and fast world generation.
- **Comprehensive Documentation**: Detailed in-code documentation for a clear structure and logic.
- **User-Friendly Experience**: Focus on making the project easy to use for end users.
- **Cross-Platform Support**: We want this project to run smoothly on Windows, macOS, and Linux.

#### How to contribute

This project is open source and welcomes contributions from everyone! Whether you're interested in fixing bugs, improving performance, adding new features, or enhancing documentation, your input is valuable. Simply fork the repository, make your changes, and submit a pull request. Please respect the above-mentioned key objectives. Contributions of all levels are appreciated, and your efforts help improve this tool for everyone.

Command line Build: `cargo run --no-default-features -- --terrain --path="C:/YOUR_PATH/.minecraft/saves/worldname" --bbox="min_lat,min_lng,max_lat,max_lng"`  
GUI Build: `cargo run`

After your pull request is merged, I will take care of regularly creating update releases which will include your changes.

If you are using Nix, you can run the program directly with `nix run github:louis-e/arnis -- --terrain --path=YOUR_PATH/.minecraft/saves/worldname --bbox="min_lat,min_lng,max_lat,max_lng"`

## ⭐ Star History

[

![Star History Chart](https://camo.githubusercontent.com/f42835b2949b50de7ce5f278c7a9a91fa58ccce06090dc11c63ba63c1909769a/68747470733a2f2f6170692e737461722d686973746f72792e636f6d2f7376673f7265706f733d6c6f7569732d652f61726e6973264461746526747970653d44617465)

](https://star-history.com/#louis-e/arnis&Date)

## 📰 Academic & Press Recognition

[![Banner](https://github.com/louis-e/arnis/raw/main/assets/git/recognition.png)](https://github.com/louis-e/arnis/blob/main/assets/git/recognition.png)

Arnis has been recognized in various academic and press publications after gaining more attention in December 2024.

[Building realistic Minecraft worlds with Open Data on AWS: How Arnis uses elevation datasets at scale](https://aws.amazon.com/de/blogs/publicsector/building-realistic-minecraft-worlds-with-open-data-on-aws-how-arnis-uses-elevation-datasets-at-scale/)

[Floodcraft: Game-based Interactive Learning Environment using Minecraft for Flood Mitigation and Preparedness for K-12 Education](https://www.researchgate.net/publication/384644535_Floodcraft_Game-based_Interactive_Learning_Environment_using_Minecraft_for_Flood_Mitigation_and_Preparedness_for_K-12_Education)

[Hackaday: Bringing OpenStreetMap Data into Minecraft](https://hackaday.com/2024/12/30/bringing-openstreetmap-data-into-minecraft/)

[TomsHardware: Minecraft Tool Lets You Create Scale Replicas of Real-World Locations](https://www.tomshardware.com/video-games/pc-gaming/minecraft-tool-lets-you-create-scale-replicas-of-real-world-locations-arnis-uses-geospatial-data-from-openstreetmap-to-generate-minecraft-maps)

[XDA Developers: Hometown Minecraft Map: Arnis](https://www.xda-developers.com/hometown-minecraft-map-arnis/)

Free to use press assets, including screenshots and logos, can be found [here](https://drive.google.com/file/d/1T1IsZSyT8oa6qAO_40hVF5KR8eEVCJjo/view?usp=sharing).

## ©️ License Information

Copyright (c) 2022-2026 Louis Erbkamm (louis-e)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.[^1]

The Luanti block-name mapping in `src/luanti_block_map.rs` is derived from [MC2MT](https://github.com/rollerozxa/MC2MT) by rollerozxa and is licensed under the GNU Lesser General Public License v2.1 or later. The full attribution and license header are preserved in that file.

Download Arnis only from the official source [https://arnismc.com](https://arnismc.com/) or [https://github.com/louis-e/arnis/](https://github.com/louis-e/arnis/). Every other website providing a download and claiming to be affiliated with the project is unofficial and may be malicious.

The logo was made by @nxfx21.

NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.

[^1]: [https://github.com/louis-e/arnis/blob/main/LICENSE](https://github.com/louis-e/arnis/blob/main/LICENSE)