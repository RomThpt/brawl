#include <mu/menu.h>

struct MuSelchkindEntry {
    u8 _0;
    u8 _1[2];
    u8 _3;
    s32 _4;
    s32 _8;
    u8 _c[4];
};

struct MuCharKindEntry {
    u8 _0;
    u8 _1;
    u8 _2;
};

extern MuSelchkindEntry g_muSelchkindTable[];
extern const MuCharKindEntry g_muCharKindTable[];

int muMenu::exchangeMuSelchkindToMuCharKind(int id, int, int) {
    return g_muSelchkindTable[id]._1[1];
}

int muMenu::exchangeMuCharKindToMuStockchkind(int id, int, int) {
    return g_muCharKindTable[id]._2;
}
