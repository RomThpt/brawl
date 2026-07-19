typedef struct {
    char pad[8];
    int f : 4;
} S;

int fn_52_7618(S* p) {
    return p->f;
}
