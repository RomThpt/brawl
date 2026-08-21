#include <ef/ef_screen.h>
#include <so/so_world.h>
#include <st/st_melee.h>
#include <st/st_trigger_observe.h>

extern "C" const float lbl_27_rodata_3934;

stMelee::~stMelee() {
    g_soWorld->m_gravityUp = lbl_27_rodata_3934;
    g_soWorld->m_gravityDown = lbl_27_rodata_3934;
    *(s32*)((char*)g_efScreen + 476) = 0;
    if (m_wind2ndData) {
        delete m_wind2ndData;
    }
}
