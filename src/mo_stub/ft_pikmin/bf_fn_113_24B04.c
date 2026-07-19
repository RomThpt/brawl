typedef struct {
    char pad[12];
    unsigned int f : 1;
} S;

unsigned int fn_113_24B04(S* p) {
    return p->f;
}
