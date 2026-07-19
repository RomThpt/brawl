typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    int f : 5;
} S;

int fn_76_3E28(S* p) {
    return p->f;
}
