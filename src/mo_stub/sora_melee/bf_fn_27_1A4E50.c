typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    int f : 5;
} S;

int fn_27_1A4E50(S* p) {
    return p->f;
}
