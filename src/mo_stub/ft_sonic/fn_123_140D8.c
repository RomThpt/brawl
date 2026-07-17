int fn_123_140D8(void* p) {
    return *(unsigned short*)((char*)p + 20);
}

int fn_123_140E0(void* p) {
    return *(int*)((char*)p + 8);
}

int fn_123_140E8(void* p) {
    return *(unsigned short*)((char*)p + 22);
}

int fn_123_140F0(void* p) {
    return *(int*)((char*)p + 12);
}

void fn_123_140F8(void* p, int q) {
    *(unsigned short*)((char*)p + 22) = q;
}
