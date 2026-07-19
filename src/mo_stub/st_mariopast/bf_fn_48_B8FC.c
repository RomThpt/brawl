typedef struct {
    char pad[8];
    unsigned int p0 : 14;
    int f : 7;
} S;

int fn_48_B8FC(S* p) {
    return p->f;
}
