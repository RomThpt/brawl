#include <mu/menu.h>

struct MuSelchkindEntry {
    u8 _0;
    u8 _1[2];
    u8 _3;
    s32 _4;
    s32 _8;
    u8 _c[4];
};

extern MuSelchkindEntry g_muSelchkindTable[];
extern MuSelchkindEntry g_selchkindTable[];

int muMenu::exchangeMuSelchkind2GmCharacterKind(int id, int, int) {
    u32 kind = g_muSelchkindTable[id]._0;
    if (kind == 255) {
        kind = 62;
    }
    return kind;
}

int muMenu::exchangeMuSelchkind2MuStockchkind(int id) {
    return g_muSelchkindTable[id]._3;
}

int muMenu::exchangeMuSelchkind2MuStockchkind(int id, int, int) {
    return g_muSelchkindTable[id]._4;
}

int muMenu::exchangeSelchkind2SelCharVoice(int id) {
    return g_selchkindTable[id]._8;
}
