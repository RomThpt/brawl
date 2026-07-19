typedef struct {
    char pad[8];
    int f : 4;
} S;

int fn_27_CD258(S* p) {
    return p->f;
}
