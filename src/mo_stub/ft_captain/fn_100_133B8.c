void fn_100_133B8(void) {
}

int fn_100_133BC(void* p) {
    return *(int*)((char*)p + 8);
}

void fn_100_133C4(void* p, int q) {
    *(int*)((char*)p + 8) = q;
}

int fn_100_133CC(void* p) {
    return *(int*)((char*)p + 8);
}
