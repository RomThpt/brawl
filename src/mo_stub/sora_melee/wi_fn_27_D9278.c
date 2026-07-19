void* fn_27_D9278(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 52) idx -= 52;
    return (char*)p + idx * 48 + 12;
}
