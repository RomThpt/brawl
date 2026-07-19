void* fn_27_D9368(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 36) idx -= 36;
    return (char*)p + idx * 48 + 12;
}
