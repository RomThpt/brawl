void fn_8038918C(void* p, int q) {
    *(int*)((char*)p + 16) = q;
}

void fn_80389194(void* p, int q) {
    *(unsigned char*)((char*)p + 20) = q;
}

int fn_8038919C(void* p) {
    return *(unsigned char*)((char*)p + 20);
}
