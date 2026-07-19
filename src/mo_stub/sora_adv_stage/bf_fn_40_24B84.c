typedef struct {
    char pad[8];
    unsigned int p0 : 6;
    unsigned int f : 1;
} S;

void fn_40_24B84(S* p) {
    p->f = 1;
}
