typedef struct {
    char pad[8];
    int f : 3;
} S;

int fn_72_BE1C(S* p) {
    return p->f;
}
