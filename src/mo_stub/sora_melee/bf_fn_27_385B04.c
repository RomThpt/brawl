typedef struct {
    char pad[8];
    unsigned int p0 : 10;
    int f : 10;
} S;

int fn_27_385B04(S* p) {
    return p->f;
}
