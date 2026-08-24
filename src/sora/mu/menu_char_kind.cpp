#include <mu/menu.h>

struct MuCharKindEntry {
    u8 _0;
    u8 _1;
    u8 _2;
};

extern const MuCharKindEntry g_muCharKindTable[];

int muMenu::exchangeMuCharKindToGmCharacterKind(int id, int, int) {
    return g_muCharKindTable[id]._0;
}
