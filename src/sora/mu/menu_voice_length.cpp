#include <mu/menu.h>

struct MuSelchkindEntry {
    u8 _0;
    u8 _1[2];
    u8 _3;
    s32 _4;
    s32 _8;
    u8 _c[4];
};

extern MuSelchkindEntry g_selchkindTable[];

int muMenu::exchangeSelCharVoice2SelCharVoiceLengthE(int id) {
    return g_selchkindTable[id]._c[0];
}

int muMenu::exchangeSelCharVoice2SelCharVoiceLengthJ(int id) {
    return g_selchkindTable[id]._c[1];
}
