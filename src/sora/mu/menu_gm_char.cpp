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

int muMenu::exchangeGmCharacterKind2Something(int id) {
    return g_selchkindTable[id]._0;
}
