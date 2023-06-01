# BladeReforged

Made a menu interaction MOD for **Blade of Darkness Reforged**, everything is aimed at using it more conveniently.

_This repository does not contain texture files._

## AutoBladePreset

Reshade addon, Based on [Reshade_5.4.2](https://github.com/crosire/reshade/tree/v5.4.2), features:

- Automatically switch presets according to the current game map
- Properly turn off special effects according to the current game state (in the menu/in-game)

Preset files associated with maps are defined in `ReShade.ini`:

```ini
[AutoBladePreset]
Casa=..\..\bin\bin\Preset\Start character selection.ini
```

You need to use Reshade version (5.0 or higher) with Addon, it is recommended to use: ReShade_Setup_5.4.2_Addon\
Find the corresponding version in [ReShade Repository](https://reshade.me/forum/general-discussion/294-reshade-repository-new-host)

## Usage

1. Put the "BOD Reforged" folder into "GameRoot/BODLoader/Mods"
2. Install from "MODS->SETUP" option

## Way of working

The principle of switching textures is to move files instead of copy files, so the process is instantaneous.\
_For security reasons, moving texture files will not have overwriting behavior._

There are two folders (staging areas) in the `BOD Reforged` folder, both of which have the same directory structure as the game directory.\
`BOD Reforged/Original` is for files from the original game\
`BOD Reforged/Reforged` is for files from the Reforged

| Option                        |                                                                                     Description                                                                                      |
| ----------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Texture `2K`                  | First move the current game file to the `Original` directory, then move the files in `Reforged` to the game directory<br>_Single file processing, skip this file if conflict occurs_ |
| Texture `Original`            | First move the current game file to the `Reforged` directory, then move the files in `Original` to the game directory<br>_Single file processing, skip this file if conflict occurs_ |
| ReshadeFX `Enabled`           |                                                      The Reshade file is directly overwritten to `game root directory/bin/bin`                                                       |
| HUD `Enabled`                 |                            Back up the original files to the Original directory first<br>then overwrite the Reforged files to `game root directory/Data`                             |
| GamePlay<br>Enhancements `ON` |                             Back up the original files to the Original directory first<br>then overwrite the Reforged files to `game root directory/Lib`                             |

## Building

This project uses Visual Studio 2022 to build AutoBladePreset.

1. Clone this repository\
   git clone https://github.com/Sryml/BladeReforged
2. Download the [Reshade_5.4.2 repository](https://github.com/crosire/reshade/archive/refs/tags/v5.4.2.zip)
3. Open the Visual Studio solution
4. Add a path to `reshade/include` in the additional included directory of project properties
5. Select the `64-bit` and `release` configuration to build the solution

<hr>

## Blade of Darkness Reforged (by sfb)

Blade of Darkness Reforged is a total visual overhaul including minor gameplay enhancements.\
Reforged aims to update the visual fidelity of Blade of Darkness whilst not straying too far from the original look and feel.

Although many textures have changed from their original design, each and every texture is based on an upscaled version of the original allowing for greater visual authenticity and feel.

Overall, Reforged strikes a good balance between old and new by highlighting Blade of Darkness' atmospheric strengths via Reshade and providing more details and fidelity across all textures through much higher resolutions.

## Blade of Darkness Reforged features include -

Upscaled 2k handmade textures based on the original textures covering all maps\*, objects, weapons, characters and npcs.

Individual Reshade presets for each map. These individual Reshade configs have been carefully designed for each map and include Bloom, DOF, AO, SSR, HDR and tonemapping.

## Useful links

[Arokhslair.net](https://www.arokhslair.net/wp/)\
[Steamcommunity.com](https://steamcommunity.com/app/1710170/discussions/)
