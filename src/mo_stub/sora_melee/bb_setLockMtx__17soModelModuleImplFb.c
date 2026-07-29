typedef struct {
    char pad[197];
    unsigned char p0 : 1;
    unsigned char f : 1;
} S;

void setLockMtx__17soModelModuleImplFb(S* s, unsigned char v) {
    s->f = v;
}
