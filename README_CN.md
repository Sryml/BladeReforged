# BladeReforged

为**Blade of Darkness Reforged**制作了菜单交互 MOD，一切主旨在于更方便的使用它。

_此仓库不包含纹理文件_

## AutoBladePreset

Reshade 插件，基于[Reshade_5.4.2](https://github.com/crosire/reshade/tree/v5.4.2)，功能：

- 根据当前游戏地图自动切换预设
- 根据当前游戏状态（菜单中/游戏中）适当的关闭特效

与地图关联的预设文件在`ReShade.ini`中定义：

```ini
[AutoBladePreset]
Casa=..\..\bin\bin\Preset\Start character selection.ini
```

你需要使用带 Addon 的 Reshade 版本（5.0 或更高），建议使用：ReShade_Setup_5.4.2_Addon\
在[ReShade Repository](https://reshade.me/forum/general-discussion/294-reshade-repository-new-host)找到对应的版本

## 用法

1. 将 "BOD Reforged" 文件夹放到 "游戏根目录/BODLoader/Mods"
2. 从 "MODS->SETUP" 选项安装

## 工作方式

纹理的切换原理是移动文件而不是复制文件，因此这个过程是瞬间完成的。\
_出于安全考虑，纹理文件的移动不会有覆盖行为。_

BOD Reforged 文件夹里有两个文件夹（暂存区），它们的目录结构都与游戏目录相同。\
`BOD Reforged/Original`用于存放来自原始游戏的文件\
`BOD Reforged/Reforged`用于存放来自 Reforged 的文件

| 选项                          |                                                          描述                                                          |
| ----------------------------- | :--------------------------------------------------------------------------------------------------------------------: |
| Texture `2K`                  | 首先移动当前游戏文件到 Original 目录，然后移动 Reforged 里的文件到游戏目录<br>_按单个文件处理，如发生冲突则跳过此文件_ |
| Texture `Original`            | 首先移动当前游戏文件到 Reforged 目录，然后移动 Original 里的文件到游戏目录<br>_按单个文件处理，如发生冲突则跳过此文件_ |
| ReshadeFX `Enabled`           |                                      Reshade 文件是直接覆盖到`游戏根目录/bin/bin`                                      |
| HUD `Enabled`                 |                      先备份原始文件到 Original 目录，然后将 Reforged 文件覆盖到`游戏根目录/Data`                       |
| GamePlay<br>Enhancements `ON` |                       先备份原始文件到 Original 目录，然后将 Reforged 文件覆盖到`游戏根目录/Lib`                       |

## 构建

此项目使用 Visual Studio 2022 构建 AutoBladePreset。

1. 克隆此仓库\
   git clone https://github.com/Sryml/BladeReforged
2. 下载 [Reshade_5.4.2 仓库](https://github.com/crosire/reshade/archive/refs/tags/v5.4.2.zip)
3. 打开 Visual Studio 解决方案
4. 在项目属性的附加包含目录添加指向`reshade/include`的路径
5. 选择`64-bit`和`release`配置构建解决方案

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
