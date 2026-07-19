typedef struct {
    char pad[8];
    unsigned int f : 2;
} S;

void fn_67_4FF4(S* p, int v) {
    p->f = v;
}
