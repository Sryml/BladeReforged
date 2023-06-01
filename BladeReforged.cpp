// #include <iostream>
#include <string>
#include <map>
#include <filesystem>
#include <fstream>

#include "reshade.hpp"

using namespace std;
namespace fs = std::filesystem;

//
static bool _no_debug_info = false;
static fs::path MESSAGE_FILE = "../../BODLoader/Mods/BOD Reforged/Scripts/.message";
static fs::file_time_type MESSAGE_MTIME = fs::last_write_time(MESSAGE_FILE);
static string _pre_map;
static reshade::api::effect_runtime *_runtime;

// static int _count = 0;

#if 0
static map<string, string> _map = {
    {"Casa", "Start character selection"},
    {"Barb_M1", "Kashgar (Barbarian 1st level)"},
    {"Ragnar_M2", "Tabriz (knight 1st level)"},
    {"Dwarf_M3", "Kazel Zalam (Dwarf 1st level)"},
    {"Ruins_M4", "Marakamda (Amazon 1st level)"},
    {"Mine_M5", "Mines of Kelbegen"},
    {"Labyrinth_M6", "Fortress of Tell Halaf"},
    {"Tomb_M7", "Tombs of Ephyra"},
    {"Island_M8", "Island of Karum"},
    {"Orc_M9", "Shalatuwar Fortress"},
    {"Ice_M11", "Fortress of Nemrut"},
    {"Btomb_M12", "Oasis of Nejeb"},
    {"Desert_M13", "Temple of Al Farum"},
    {"Volcano_M14", "Forge of Xshathra"},
    {"Palace_M15", "Temple of Ianna"},
    {"Tower_M16", "Tower of Dal Gurak"},
    {"Chaos_M17", "The Abyss"},
};

//

bool isFileExists_ifstream(string &name)
{
    ifstream f(name.c_str());
    return f.good();
}
#endif

void log_message(int level, const char *message)
{
    if (level == 4 && _no_debug_info)
    {
        return;
    }
    reshade::log_message(level, message);
    // !_no_debug_info ? reshade::log_message(level, message) : (void)0;
}

static void auto_config()
{
    log_message(4, "auto_config");
    reshade::api::effect_runtime *runtime;
    runtime = ::_runtime;

    fstream file;
    file.open(MESSAGE_FILE, ios::in); // only read
    string curr_mode;
    string curr_map;
    getline(file, curr_mode);
    getline(file, curr_map);
    file.close();

    if (curr_mode == "Disabled")
    {
        runtime->set_effects_state(false);
        runtime->set_current_preset_path("..\\..\\bin\\bin\\Preset\\.ini");
    }
    else if (curr_mode == "Menu")
    {
        runtime->set_effects_state(false);
    }
    else if (curr_mode == "Game")
    {
        runtime->set_effects_state(true);
    }

    if (curr_map != _pre_map)
    {
        ::_pre_map = curr_map;
        // string path = "..\\..\\bin\\bin\\Preset\\" + (_map.count(curr_map) ? _map[curr_map] : "") + ".ini";
        // runtime->set_current_preset_path(path.c_str());
        bool has_preset = true;
        char path[200] = "";
        size_t length = sizeof(path);
        has_preset = reshade::config_get_value(nullptr, "AutoBladePreset", curr_map.c_str(), path, &length);
        if (!has_preset)
        {
            strcpy_s(path, "..\\..\\bin\\bin\\Preset\\.ini");
        }
        else
        {
            const char fmt[] = "set preset: %s";
            char buf[sizeof(fmt) + sizeof(path)] = "";
            sprintf(buf, fmt, path);
            log_message(3, buf);
        }
        runtime->set_current_preset_path(path);
    }
}

#if 0
static void on_init_effect_runtime(reshade::api::effect_runtime *runtime)
{
    static int f_count = 0;
    // log_message(4, "on_init_effect_runtime");

    if (f_count < 1)
    {
        f_count++;
        // runtime->set_effects_state(false);
        // log_message(4, "set_effects_state(false)");
        // char s[50];
        // sprintf(s, "on_init_effect_runtime: %016p", runtime);
        // log_message(4, s);
    }
    // ::_runtime = runtime;
}

static void on_destroy_effect_runtime(reshade::api::effect_runtime *runtime)
{
    static int f_count = 0;
    if (f_count < 3)
    {
        f_count++;
        char s[50];
        sprintf(s, "on_destroy_effect_runtime: %016p", runtime);
        log_message(4, s);
        // _count = 0;
    }

    // log_message(4, "on_destroy_effect_runtime");
    // return;
    // ::_runtime = nullptr;
}
#endif

static void on_present(reshade::api::command_queue *queue, reshade::api::swapchain *swapchain, const reshade::api::rect *source_rect, const reshade::api::rect *dest_rect, uint32_t dirty_rect_count, const reshade::api::rect *dirty_rects)
{
    auto lstTime = fs::last_write_time(MESSAGE_FILE);
    if (lstTime != MESSAGE_MTIME)
    {
        if (!::_runtime)
        {
            return;
        }

        ::MESSAGE_MTIME = lstTime;
        auto_config();
    }
}

static void on_reshade_finish_effects(reshade::api::effect_runtime *runtime, reshade::api::command_list *, reshade::api::resource_view rtv, reshade::api::resource_view)
{
    static int f_count = 0;
    if (f_count < 1)
    {
        f_count++;
        runtime->set_effects_state(false);
        log_message(4, "set_effects_state(false)");
    }

    if (runtime != ::_runtime)
    {
        ::_runtime = runtime;
        log_message(4, "assign: _runtime");
        // char s[50];
        // sprintf(s, "on_reshade_finish_effects: %016p", runtime);
        // log_message(4, s);
    }
}

//
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID)
{
    static int f_count = 0;
    if (f_count < 1)
    {
        f_count++;
        reshade::config_set_value(nullptr, "GENERAL", "PresetPath", "..\\..\\bin\\bin\\Preset\\Start character selection.ini");

        reshade::config_get_value(nullptr, "AutoBladePreset", "NoDebugInfo", _no_debug_info);
    }

    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        if (!reshade::register_addon(hinstDLL))
            return FALSE;

        // reshade::register_event<reshade::addon_event::init_effect_runtime>(on_init_effect_runtime);
        // reshade::register_event<reshade::addon_event::destroy_effect_runtime>(on_destroy_effect_runtime);
        reshade::register_event<reshade::addon_event::present>(on_present);
        reshade::register_event<reshade::addon_event::reshade_finish_effects>(on_reshade_finish_effects);
        break;
    case DLL_PROCESS_DETACH:

        reshade::unregister_addon(hinstDLL);
        break;
    }
    return TRUE;
}
