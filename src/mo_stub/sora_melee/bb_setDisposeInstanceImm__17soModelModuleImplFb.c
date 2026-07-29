typedef struct {
    char pad[197];
    unsigned char p0 : 3;
    unsigned char f : 1;
} S;

void setDisposeInstanceImm__17soModelModuleImplFb(S* s, unsigned char v) {
    s->f = v;
}
