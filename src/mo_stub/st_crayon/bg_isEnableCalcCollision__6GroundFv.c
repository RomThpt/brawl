typedef struct {
    char pad[108];
    unsigned char p0 : 4;
    unsigned char f : 1;
} S;

unsigned char isEnableCalcCollision__6GroundFv(S* s) {
    return s->f;
}
